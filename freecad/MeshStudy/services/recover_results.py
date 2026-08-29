import json
from freecad.MeshStudy.objects.mesh_study import create_study_results
from PySide.QtWidgets import QMessageBox
from ..__init__ import BACKUP_PATH


def prompt_recovery():
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Data Recovery Found")
    msg_box.setText("Recovered data from a previous session was detected.")
    msg_box.setInformativeText("Would you like to recover this data or forfeit it?")
    msg_box.setIcon(QMessageBox.Warning)
    
    # Custom buttons
    recover_btn = msg_box.addButton("Recover Data", QMessageBox.AcceptRole)
    forfeit_btn = msg_box.addButton("Forfeit Data", QMessageBox.RejectRole)
    
    # Set default focused button
    msg_box.setDefaultButton(recover_btn)
    
    msg_box.exec_()

    r_list =  []
    if msg_box.clickedButton() == recover_btn:

        # Code to handle recovery
        with open(BACKUP_PATH, "r") as f:
            r_list = json.load(f)
        create_study_results(r_list)
        
        print("Data recovered successfully.")

        # clear backup file
        r_list =  []
        with open(BACKUP_PATH, "w") as f:
            json.dump(r_list, f)

        return True
    else:
        # Code to handle forfeit/clean up recovery files
        with open(BACKUP_PATH, "w") as f:
            json.dump(r_list, f)

        print("User chose to forfeit.")

        return False