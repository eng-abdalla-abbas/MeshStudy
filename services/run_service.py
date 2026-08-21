import FreeCAD as App
import json
import os
import time
from strategies.registry import get_qoi_extractor, get_refinement_strategy
from core.exceptions import MeshStudyError

class MeshStudyRunService:
    """The main excutive file, and the absloute coordinator"""
    
    def __init__(self, study_obj):
        self.obj = study_obj
        self.doc = study_obj.Document

    def execute(self, progress_callback=None) -> list:
        
        doc = App.ActiveDocument
        obj = doc.getObject("MeshStudy")
        
        # Check the links
        if not self.obj.TheStudyTarget:
            raise MeshStudyError("No Analysis target selected in MeshStudy object.")
            
        mesh_obj = self.obj.MeshObject
        solver_obj = self.obj.SolverObject
        if not mesh_obj or not solver_obj:
            raise MeshStudyError("Mesh object or Solver object is missing from the analysis.")

        # get the Refinement method
        qoi_extractor = get_qoi_extractor(self.obj.QuantityOfInterest)
        refinement_strat = get_refinement_strategy()
        
        # Calculate the Sizes with the method
        sizes = refinement_strat.calculate_sizes(
            self.obj.InitialMeshSize, 
            self.obj.NumberOfRuns, 
            self.obj.RefinementFactor
        )

        results = []
        
        # Repeate along the runs
        for run_idx, (max_size, min_size) in enumerate(sizes, start=1):
            if progress_callback:
                progress_callback(run_idx, len(sizes), f"Meshing (Size: {min_size})...")

            # Meshing
            from fem.mesh_runner import MeshRunner
            MeshRunner.generate(self.obj, (max_size, min_size))

            # Check Elementes and nodes number
            nodes = len(mesh_obj.FemMesh.Nodes)
            elements = len(mesh_obj.FemMesh.Volumes)

            # Waiting intervals
            if progress_callback:
                progress_callback(run_idx, len(sizes), "Waiting interval (a chance to stop)...")
            time.sleep(2)

            # Check if stop
            from services import send_signal
            if send_signal.get_signal("STOP"):
                print("received stop")
                send_signal.reset_signal()
                break
                
            # Running CalculiX
            if progress_callback:
                progress_callback(run_idx, len(sizes), "Solving with CalculiX...")

            from fem.solver_runner import SolverRunner
            SolverRunner.solve(obj)

            # Results extraction
            result_obj = self.doc.getObject("CCX_Results") or self.doc.getObject(f"CCX_Results_{solver_obj.Name}")
            qoi_value = qoi_extractor.extract(result_obj) if result_obj else 0.0

            # format data
            run_data = {
                "Run": run_idx,
                "Size": [max_size, min_size],
                "Nodes": nodes,
                "Elements": elements,
                "QoI": qoi_value
            }

            # Save Data (+JSON)
            results.append(run_data)
            self.save_results(results)

        #Check covergence
        from core.convergence import check_convergence
        check_convergence(results, self.obj.Tolerance)
        return results

    def save_results(self, results: list):
        """Save resultes in backup folder"""

        user_dir = App.getUserAppDataDir()
        save_dir = os.path.join(user_dir, "Mod", "MeshStudy")
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir,"resources", "data", "backup_results.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)
        
        App.Console.PrintMessage(f"Results saved successfully to: {file_path}\n")

    def clear_results(self):
            """clear resultes in backup folder"""

            clear = []
            user_dir = App.getUserAppDataDir()
            save_dir = os.path.join(user_dir, "Mod", "MeshStudy")
            os.makedirs(save_dir, exist_ok=True)
            file_path = os.path.join(save_dir,"resources", "data", "backup_results.json")
    
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(clear, f, indent=4)
            