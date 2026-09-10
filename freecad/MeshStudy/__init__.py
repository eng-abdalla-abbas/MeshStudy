import FreeCAD
import os

ADDON_PATH = os.path.dirname(__file__)
DATA_DIR = os.path.join(FreeCAD.getUserAppDataDir(), "MeshStudyWorkbench")
BACKUP_PATH = os.path.join(DATA_DIR, "backup_results.json")
