import FreeCADGui as Gui
import FreeCAD as App
import os
import pivy.coin as coin
from ..__init__ import ADDON_PATH

class MeshStudyViewProvider:
    def __init__(self, vobj):
        vobj.Proxy = self
        self.ObjectName = vobj.Object.Name
        self.DocName = vobj.Object.Document.Name

    def attach(self, vobj):
        self.ObjectName = vobj.Object.Name
        self.DocName = vobj.Object.Document.Name
        node = coin.SoGroup()
        vobj.addDisplayMode(node, "Default")

    @property
    def Object(self):
        doc = App.getDocument(getattr(self, "DocName", ""))
        if not doc:
            doc = App.ActiveDocument
        return doc.getObject(self.ObjectName)

    def claimChildren(self):
        # Making sure there is an object
        obj = self.Object
        if obj and hasattr(obj, "Group"):
            return obj.Group if obj.Group else []
        return []
    
    def getIcon(self):
        """Tree object icon path"""

        icon_path = os.path.join(ADDON_PATH, "..", "..", "Resources", "Icons", "MeshStudy.png")

        return icon_path if os.path.exists(icon_path) else ""

    def doubleClicked(self, vobj):

        from freecad.MeshStudy.gui.study_panel import MeshStudyTaskPanel
        panel = MeshStudyTaskPanel(self.Object)
        Gui.Control.showDialog(panel)

        return True
    
    def getDisplayModes(self, vobj):
        return ["Default"]

    def getDefaultDisplayMode(self):
        return "Default"

    def setDisplayMode(self, mode):
        return mode


class StudyResultViewProvider:
    # Table-Chart view provider
    def __init__(self, vobj):
        vobj.Proxy = self
        self.ObjectName = vobj.Object.Name
        self.DocName = vobj.Object.Document.Name

    def attach(self, vobj):
        self.ObjectName = vobj.Object.Name
        self.DocName = vobj.Object.Document.Name
        node = coin.SoGroup()
        vobj.addDisplayMode(node, "Default")

    @property
    def Object(self):
        doc = App.getDocument(getattr(self, "DocName", ""))
        if not doc:
            doc = App.ActiveDocument
        return doc.getObject(self.ObjectName)

    def getIcon(self):
        """Tree object icon path"""
        icon_path = os.path.join(ADDON_PATH, "..", "..", "Resources", "Icons", "Result.png")
    
        return icon_path if os.path.exists(icon_path) else ""

    def doubleClicked(self, vobj):

        import json
        from freecad.MeshStudy.gui.results_view import ShowResults

        results_attr = self.Object.Proxy.indexed_results
        r_list = json.loads(getattr(self.Object, results_attr)[0])

        ShowResults(r_list)
        
        return True

    def getDisplayModes(self, vobj):
        return ["Default"]

    def getDefaultDisplayMode(self):
        return "Default"

    def setDisplayMode(self, mode):
        return mode
