import FreeCAD as App
import FreeCADGui as Gui
import json
import os

from objects.mesh_study import create_mesh_study, create_study_results
from services.run_service import MeshStudyRunService
from gui.study_panel import MeshStudyTaskPanel
from gui.run_dialog import RunProgressDialog
from gui.results_view import ShowResults
from core.exceptions import MeshStudyError
from services.recover_results import prompt_recovery

user_dir = App.getUserAppDataDir()
backup_path = os.path.join(user_dir, 	"Mod", 	"MeshStudy", 	"resources", 	"data", 	"backup_results.json")

class CmdAddMeshStudy:
    """Add a Mesh Study object to the document"""
    
    def GetSelection(self, obj):
        selection = Gui.Selection.getSelection()
        if selection and selection[0].TypeId == "Fem::FemAnalysis":
            obj.TheStudyTarget = selection[0]
            for item in selection[0].Group:
                if item.TypeId == "Fem::FemMeshShapeBaseObjectPython":
                    obj.Mesher = "Gmsh"
                    obj.InitialMeshSize = item.CharacteristicLengthMax.Value
                    obj.MeshObject = item
                elif item.TypeId == "Fem::FemMeshShapeNetgenObject":
                    obj.Mesher = "Netgen"
                    obj.InitialMeshSize = item.MaxSize
                    obj.MeshObject = item
                elif item.TypeId == "Fem::FemSolverObjectPython":
                    obj.Solver = "CalculiX"
                    obj.SolverObject = item

    def Activated(self): 
        
        obj = create_mesh_study()
        self.GetSelection(obj)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(obj)
        obj.recompute()

        panel = MeshStudyTaskPanel(obj)
        Gui.Control.showDialog(panel)

    def doubleClicked(self, vobj):
            panel =  MeshStudyTaskPanel(vobj)
            Gui.Control.showDialog(panel)

    def GetResources(self): 
        
        icon_path = os.path.join(user_dir, "Mod", "MeshStudy",  "resources", "icons", "AddStudy.png")
    
        return {
            'Pixmap': icon_path if os.path.exists(icon_path) else '',
            'MenuText': 'Add Mesh Study',
            'ToolTip': 'Adds a Mesh Study object to the document'
        }
        

class CmdRunMeshStudy:
    """Mesh Study Run command"""
    
    def Activated(self): 

        # search for stored results (backup)
        if os.path.exists(backup_path):
            try:
                with open(backup_path) as f:
                    data = json.load(f)
                    if len(data) != 0:
                        prompt_recovery(backup_path)
                        return
            except:
                App.Console.PrintError("Backup Check Failed: can't open/read the backup data file.\n")
        else:
            with open(backup_path, "w") as f:
                clear = []
                json.dump(clear, f)


        doc = App.ActiveDocument
        if not doc:
            App.Console.PrintError("No active document found.\n")
            return

        
        # Get a list of all currently selected objects
        selection = Gui.Selection.getSelection()

        # Check if the user actually selected something
        if not selection:
            App.Console.PrintError("Please select a MeshStudy object first.\n")
            return

        obj = selection[0]

        # Verify it's actually a MeshStudy object
        if not hasattr(obj, "Proxy") or not type(obj.Proxy).__name__ == "MeshStudyProxy":
            App.Console.PrintError("Selected object is not a MeshStudy.\n")
            return   

        if not obj:
            App.Console.PrintError("No 'MeshStudy' object found in the active document.\n")
            return
        

        service = MeshStudyRunService(obj)
        dialog = RunProgressDialog(total_runs=obj.NumberOfRuns, parent=Gui.getMainWindow())
        dialog.show()

        try:
            dialog.show()
            
            def progress_update(step, total, msg):
                dialog.update_step(step, msg)

            results = service.execute(progress_callback=progress_update)
            dialog.accept()

            # result child object
            create_study_results(results)
            ShowResults(results)

            # delete backup data
            service.clear_results()

        except MeshStudyError as e:
            dialog.reject()
            App.Console.PrintError(f"Mesh Study Error: {str(e)}\n")
        except Exception as e:
            dialog.reject()
            App.Console.PrintError(f"Unexpected Error: {str(e)}\n")

    def GetResources(self): 

        icon_path = os.path.join(user_dir, "Mod", "MeshStudy",  "resources", "icons", "RunStudy.png")
    
        return {
            'Pixmap': icon_path if os.path.exists(icon_path) else '',
            'MenuText': 'Run Mesh Study',
            'ToolTip': 'Executes the mesh refinement study'
        }

class CmdShowResults:
    
    def Activated(self):

        # search for stored results (backup)
        if os.path.exists(backup_path):
            try:
                with open(backup_path) as f:
                    data = json.load(f)
                    if len(data) != 0:
                        prompt_recovery(backup_path)
                        return
            except:
                App.Console.PrintError("Backup Check Failed: can't open/read the backup data file.\n")
        else:
            with open(backup_path, "w") as f:
                clear = []
                json.dump(clear, f)
            
        # Show resultes
        selection = Gui.Selection.getSelection()
        if selection and selection[0].TypeId == "App::FeaturePython":
            try:
                results_attr = selection[0].Proxy.indexed_results
                r_list = json.loads(getattr(selection[0], results_attr)[0])
                ShowResults(r_list)
            except: 
                App.Console.PrintError(f"please select a result object from the tree view! (under the Mesh-Study object)\n")
        else:
            App.Console.PrintError(f"please select a result object from the tree view! (under the Mesh-Study object)\n")
            

    def GetResources(self):

        icon_path = os.path.join(user_dir, "Mod", "MeshStudy",  "resources", "icons", "ShowResults.png")

        return {
            'Pixmap': icon_path if os.path.exists(icon_path) else '',
            'MenuText': 'Show Results',
            'ToolTip': 'Shows Stored JSON Results'
        }

#class CmdEditMeshStudy():

def setup_commands():
    """setup all commandes for FreeCAD"""
    
    Gui.addCommand('AddMeshStudy', CmdAddMeshStudy())
    Gui.addCommand('RunMeshStudy', CmdRunMeshStudy())
    Gui.addCommand('ShowResults', CmdShowResults())
    return ["AddMeshStudy", "RunMeshStudy", "ShowResults"]