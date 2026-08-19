import json
from objects.mesh_study import create_study_results
from PySide.QtWidgets import QMessageBox


def prompt_recovery(path):
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
        with open(path, "r") as f:
            r_list = json.load(f)
        create_study_results(r_list)

        return True
    else:
        # Code to handle forfeit/clean up recovery files
        with open(path, "w") as f:
            json.dump(r_list, f)
        print("User chose to forfeit.")

        return False