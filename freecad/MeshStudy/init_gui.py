import FreeCADGui as Gui
import os
from .__init__ import ADDON_PATH

class MeshStudy(Gui.Workbench):
    MenuText = "Mesh Study"
    ToolTip = "A professional Workbench for Mesh Convergence Study"

    try:
    # Dynamic Path
        icon_path = os.path.join(ADDON_PATH, "..", ".." ,"Resources", "Icons", "Workbench.png")
        print(icon_path)
        Icon = icon_path if os.path.exists(icon_path) else ""
    except:
        print("image path error (initgui.py)")
        pass

    def Initialize(self):

        from freecad.MeshStudy.gui.commands import setup_commands
        self.list = setup_commands()
        
        self.appendToolbar("Mesh Study Tools", self.list)
        self.appendMenu("Mesh Study", self.list)

    def Activated(self):
        pass

    def Deactivated(self):
        pass

    def ContextMenu(self):
        self.appendContextMenu("Mesh Study", self.list)

    def GetClassName(self): 
        return "Gui::PythonWorkbench"
       
Gui.addWorkbench(MeshStudy())