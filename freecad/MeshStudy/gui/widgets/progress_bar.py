from PySide import QtWidgets

class StudyProgressBar(QtWidgets.QWidget):
    """Study progress bar"""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QtWidgets.QLabel("Ready", self)
        self.pbar = QtWidgets.QProgressBar(self)
        self.pbar.setRange(0, 100)
        self.pbar.setValue(0)

        layout.addWidget(self.label)
        layout.addWidget(self.pbar)

    def update_progress(self, current_step: int, total_steps: int, message: str = ""):
        percent = int((current_step / max(total_steps, 1)) * 100)
        self.pbar.setValue(percent)
        self.label.setText(f"Run {current_step}/{total_steps} - {message}")

    def reset(self):
        self.pbar.setValue(0)
        self.label.setText("Ready")