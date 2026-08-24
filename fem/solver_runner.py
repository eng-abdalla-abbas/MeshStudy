import FreeCAD as App
import os
import sys
import shutil
from core.exceptions import SolverError

class SolverRunner:
    @staticmethod
    def find_calculix():
        prefs = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Fem/Ccx")
        path = prefs.GetString("ccxBinaryPath", "")

        if path and os.path.isfile(path):
            return path

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
            raise SolverError("CalculiX executable not found. please check fem workbench prefrences.")

        prefs = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Fem/Ccx")
        prefs.SetString("ccxBinaryPath", ccx)

        from femtools import ccxtools

        fea = ccxtools.FemToolsCcx()
        fea.purge_results()
        fea.run()