import FreeCAD as App
import FreeCADGui as Gui
import os

class MeshStudy(Gui.Workbench):
    MenuText = "Mesh Study v0.1"
    ToolTip = "A professional Workbench for Mesh Convergence Study"

    try:
    # Dynamic Path
        user_dir = App.getUserAppDataDir()
        icon_path = os.path.join(user_dir, "Mod", "MeshStudy",  "resources", "icons", "Workbench.png")
        Icon = icon_path if os.path.exists(icon_path) else ""
        print(icon_path)
    except:
        print("image path error (initgui.py)")
        pass

    def Initialize(self):

        from gui.commands import setup_commands
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