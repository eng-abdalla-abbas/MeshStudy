import FreeCADGui as Gui
import os


class MeshStudyViewProvider:
    # icons - paneles management
    def __init__(self, vobj):

        self.Object = vobj.Object
        vobj.Proxy = self

    def claimChildren(self):
        return self.Object.Group
    
    def getIcon(self):
        """Tree object icon path"""
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "resources", "icons", "MeshStudy.svg"
        )
        return icon_path if os.path.exists(icon_path) else ""

    def doubleClicked(self, vobj):

        from gui.study_panel import MeshStudyTaskPanel
        panel = MeshStudyTaskPanel(vobj.Object)
        Gui.Control.showDialog(panel)

        return True


class StudyResultViewProvider:
    # icons - paneles management
    def __init__(self, vobj):
        self.obj = vobj.Object

        vobj.Proxy = self
    
    def getIcon(self):
        """Tree object icon path"""
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "resources", "icons", "MeshStudy.svg"
        )
        return icon_path if os.path.exists(icon_path) else ""

    def doubleClicked(self, vobj):

        import json
        from gui.results_view import ShowResults

        results_attr = self.obj.Proxy.indexed_results
        r_list = json.loads(getattr(self.Object, results_attr)[0])

        ShowResults(r_list)
        
        return True
