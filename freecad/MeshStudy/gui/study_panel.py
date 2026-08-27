import FreeCAD as App
import FreeCADGui as Gui

from PySide import QtWidgets

class MeshStudyTaskPanel:
    
    def __init__(self, study_obj):
        self.obj = study_obj
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle("Mesh Study Configuration")

        layout = QtWidgets.QFormLayout(self.form)

        #Enteries
        self.size_spin = QtWidgets.QDoubleSpinBox()
        self.size_spin.setDecimals(2)
        self.size_spin.setSuffix(" mm")
        self.size_spin.setValue(self.obj.InitialMeshSize)
        
        self.runs_spin = QtWidgets.QSpinBox()
        self.runs_spin.setRange(2, 20)
        self.runs_spin.setValue(self.obj.NumberOfRuns)

        self.factor_spin = QtWidgets.QDoubleSpinBox()
        self.factor_spin.setRange(0.1, 0.99)
        self.factor_spin.setSingleStep(0.05)
        self.factor_spin.setValue(self.obj.RefinementFactor)

        self.qoi_combo = QtWidgets.QComboBox()
        self.qoi_combo.addItems(["Displacement", "Stress"])
        self.qoi_combo.setCurrentText(self.obj.QuantityOfInterest)

        self.tol_spin = QtWidgets.QDoubleSpinBox()
        self.tol_spin.setRange(0.01, 20.0)
        self.tol_spin.setSuffix(" %")
        self.tol_spin.setValue(self.obj.Tolerance)

        layout.addRow("Initial mesh size:", self.size_spin)
        layout.addRow("Number of Runs:", self.runs_spin)
        layout.addRow("Refinement Factor:", self.factor_spin)
        layout.addRow("Target QoI:", self.qoi_combo)
        layout.addRow("Tolerance:", self.tol_spin)

    def accept(self):
        """"accept change"""
        self.obj.InitialMeshSize = self.size_spin.value()
        self.obj.NumberOfRuns = self.runs_spin.value()
        self.obj.RefinementFactor = self.factor_spin.value()
        self.obj.QuantityOfInterest = self.qoi_combo.currentText()
        self.obj.Tolerance = self.tol_spin.value()
        self.obj.recompute()
        Gui.Control.closeDialog()
        return True

    def reject(self):
        
        Gui.Control.closeDialog()
        return True