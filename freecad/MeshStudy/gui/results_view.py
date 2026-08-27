from PySide import QtWidgets

import FreeCADGui as Gui
from freecad.MeshStudy.gui.widgets.run_summary import RunSummaryTable
from freecad.MeshStudy.gui.widgets.convergence_chart import ConvergenceChartWidget

class ResultsViewDialog(QtWidgets.QDialog):

    def __init__(self, results_data: list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mesh Study Results & Convergence")
        self.resize(700, 500)

        layout = QtWidgets.QVBoxLayout(self)

        self.tabs = QtWidgets.QTabWidget(self)
        
        self.table_widget = RunSummaryTable(self)
        self.table_widget.populate_data(results_data)

        self.chart_widget = ConvergenceChartWidget(self)
        self.chart_widget.plot_results(results_data)

        self.tabs.addTab(self.table_widget, "Summary Table")
        self.tabs.addTab(self.chart_widget, "Convergence Chart")

        # close/continue
        btn_layout = QtWidgets.QHBoxLayout()
        self.btn_continue = QtWidgets.QPushButton("Continue Refining", self)
        self.btn_close = QtWidgets.QPushButton("Close", self)
        self.btn_close.clicked.connect(self.accept)

        btn_layout.addWidget(self.btn_continue)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_close)

        layout.addWidget(self.tabs)
        layout.addLayout(btn_layout)

def ShowResults(results):
    
    if results:
        res_view = ResultsViewDialog(results, parent=Gui.getMainWindow())
        res_view.exec_()
    