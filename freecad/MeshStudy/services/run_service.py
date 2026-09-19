import FreeCAD as App
import json
import os
from PySide import QtCore
from freecad.MeshStudy.strategies.registry import get_qoi_extractor, get_refinement_strategy
from freecad.MeshStudy.core.exceptions import MeshStudyError, MeshError
from ..__init__ import BACKUP_PATH, DATA_DIR
from freecad.MeshStudy.objects.mesh_study import check_study_parameters

class MeshStudyRunService:
    """The main excutive file, and the absloute coordinator"""
    
    def __init__(self, study_obj):
        self.obj = study_obj
        self.doc = study_obj.Document

    def execute(self, progress_callback=None, dialog=None) -> list:

        obj = self.obj
        
        # Verify it's actually a MeshStudy object
        if not hasattr(obj, "Proxy") or not type(obj.Proxy).__name__ == "MeshStudyProxy":
            raise MeshStudyError("Selected object is not a MeshStudy.")   

        # Check the study parameters
        para_errors = check_study_parameters(obj)
        if para_errors:
            for err in para_errors:
                App.Console.PrintError(f"{err}\n")
            raise MeshStudyError("Invalid parameters for the MeshStudy object.")
        
        # get the Refinement method
        qoi_extractor = get_qoi_extractor(self.obj.QuantityOfInterest)
        refinement_strat = get_refinement_strategy()
        
        # Calculate the Sizes with the method
        sizes = refinement_strat.calculate_sizes(
            self.obj.InitialMeshSize, 
            self.obj.NumberOfRuns, 
            self.obj.RefinementFactor
        )
        mesh_obj = obj.MeshObject
        solver_obj = obj.SolverObject
        results = []
        
        # Repeate along the runs
        for run_idx, (max_size, min_size) in enumerate(sizes, start=1):
            if progress_callback:
                progress_callback(run_idx, len(sizes), f"Meshing (Size: {min_size})...")

            # Meshing
            from freecad.MeshStudy.fem.mesh_runner import MeshRunner
            MeshRunner.generate(self.obj, (max_size, min_size))

            # Check mesh
            if not mesh_obj.FemMesh or mesh_obj.FemMesh.Nodes == 0:
                raise MeshError("Meshing failed or returned zero nodes.")

            # Check Elementes and nodes number
            nodes = len(mesh_obj.FemMesh.Nodes)
            elements = len(mesh_obj.FemMesh.Volumes)

            # Waiting intervals
            if progress_callback:
                progress_callback(run_idx, len(sizes), "Waiting interval (a chance to stop)...")

            # Wait for stop
            end_time = QtCore.QTime.currentTime().addSecs(3)
            while QtCore.QTime.currentTime() < end_time:

                QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents, 100)
                if dialog and dialog.is_stoped():
                    break

            # check if stoped
            if dialog and dialog.is_stoped():
                break
                
            # Running CalculiX
            if progress_callback:
                progress_callback(run_idx, len(sizes), "Solving with CalculiX...")

            from freecad.MeshStudy.fem.solver_runner import SolverRunner
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
        from freecad.MeshStudy.core.convergence import check_convergence
        check_convergence(results, self.obj.Tolerance)
        return results

    def save_results(self, results: list):
        """Save resultes in backup folder"""

        os.makedirs(DATA_DIR, exist_ok = True)
        with open(BACKUP_PATH, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)

    def clear_results(self):
            """clear resultes in backup folder"""

            clear = []
            with open(BACKUP_PATH, "w", encoding="utf-8") as f:
                json.dump(clear, f, indent=4)
            