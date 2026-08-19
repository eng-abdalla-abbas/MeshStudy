import FreeCAD as App
import os
import sys
import shutil

class SolverRunner:
    @staticmethod
    def find_calculix():
        prefs = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Fem/Ccx")
        configured = prefs.GetString("ccxBinaryPath", "")
        if configured and shutil.which(configured):
            return shutil.which(configured)

        ccx = shutil.which("ccx")
        if ccx: return ccx

        freecad_bin = os.path.dirname(sys.executable)
        ccx = os.path.join(freecad_bin, "ccx.exe")
        if os.path.isfile(ccx): return ccx
        return None

    @staticmethod
    def solve(obj):
        import FemGui
        FemGui.setActiveAnalysis(obj.TheStudyTarget)
        
        ccx = SolverRunner.find_calculix()
        if ccx is None:
            App.Console.PrintError("CalculiX not found!\n")
            return

        from femtools import ccxtools
        fea = ccxtools.FemToolsCcx()
        fea.purge_results()
        fea.run()