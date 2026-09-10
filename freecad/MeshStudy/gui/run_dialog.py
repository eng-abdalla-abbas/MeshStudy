from PySide import QtWidgets

from freecad.MeshStudy.gui.widgets.progress_bar import StudyProgressBar

class RunProgressDialog(QtWidgets.QDialog):

    def __init__(self, total_runs: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Executing Mesh Study...")
        self.setMinimumWidth(400)
        self.setModal(True)

        layout = QtWidgets.QVBoxLayout(self)

        self.progress_widget = StudyProgressBar(self)
        self.total_runs = total_runs

        self.stop_button = QtWidgets.QPushButton("Stop Study", self)
        self.stop_button.clicked.connect(self.on_stop_clicked)
        self.stoped = False

        layout.addWidget(self.progress_widget)
        layout.addWidget(self.stop_button)

    def update_step(self, step: int, status_msg: str):
        self.progress_widget.update_progress(step, self.total_runs, status_msg)
        QtWidgets.QApplication.processEvents()

    def on_stop_clicked(self):

        self.stop_button.setEnabled(False)
        self.stop_button.setText("Stopping...")

        self.stoped = True

    def is_stoped(self):
        return self.stoped