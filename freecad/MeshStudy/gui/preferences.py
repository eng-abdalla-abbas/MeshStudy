import FreeCAD as App
from PySide import QtGui
from pathlib import Path

PARAM_PATH = "User parameter:BaseApp/Preferences/Mod/MeshStudy"


class MeshStudyPreferences:
    def __init__(self):
        self.form = QtGui.QWidget()
        self.form.setWindowTitle("General")
        layout = QtGui.QFormLayout(self.form)

        self.enable_limits = QtGui.QCheckBox("Enable mesh limits")
        layout.addRow(self.enable_limits)

        self.max_nodes = QtGui.QSpinBox()
        self.max_nodes.setRange(1, 2_000_000_000)
        layout.addRow("Maximum nodes:", self.max_nodes)

        self.max_elements = QtGui.QSpinBox()
        self.max_elements.setRange(1, 2_000_000_000)
        layout.addRow("Maximum elements:", self.max_elements)

        self.enable_limits.toggled.connect(self.max_nodes.setEnabled)
        self.enable_limits.toggled.connect(self.max_elements.setEnabled)

    def loadSettings(self):
        prefs = App.ParamGet(PARAM_PATH)

        self.max_nodes.setValue(prefs.GetInt("MaxNodes", 1_000_000))
        self.max_elements.setValue(prefs.GetInt("MaxElements", 1_000_000))

        enabled = prefs.GetBool("EnableLimits", True)
        self.enable_limits.setChecked(enabled)
        self.max_nodes.setEnabled(enabled)
        self.max_elements.setEnabled(enabled)

    def saveSettings(self):
        prefs = App.ParamGet(PARAM_PATH)
        prefs.SetBool("EnableLimits", self.enable_limits.isChecked())
        prefs.SetInt("MaxNodes", self.max_nodes.value())
        prefs.SetInt("MaxElements", self.max_elements.value())