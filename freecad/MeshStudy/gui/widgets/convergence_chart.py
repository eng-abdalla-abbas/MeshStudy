from PySide import QtWidgets

HAS_MATPLOTLIB = True
try:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
except ImportError:
    HAS_MATPLOTLIB = False

class ConvergenceChartWidget(QtWidgets.QWidget):
    ""
    """Convergence Charte"""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        
        if HAS_MATPLOTLIB:
            self.figure = Figure(figsize=(5, 3), dpi=100)
            self.canvas = FigureCanvas(self.figure)
            layout.addWidget(self.canvas)
            self.ax = self.figure.add_subplot(111)
            self.ax.set_title("Mesh Convergence Curve")
            self.ax.set_xlabel("Elements Count")
            self.ax.set_ylabel("Quantity of Interest (QoI)")
            self.ax.grid(True)
        else:
            self.label = QtWidgets.QLabel("Matplotlib non-installed. Chart disabled.", self)
            layout.addWidget(self.label)

    def plot_results(self, results_list: list):
        if not HAS_MATPLOTLIB or not results_list:
            return

        elements = [d.get("Elements", 0) for d in results_list]
        qoi_vals = [d.get("QoI", 0.0) for d in results_list]

        self.ax.clear()
        self.ax.plot(elements, qoi_vals, marker='o', color='#007acc', linewidth=2, label="QoI")
        self.ax.set_title("Mesh Convergence Curve")
        self.ax.set_xlabel("Elements Count")
        self.ax.set_ylabel("QoI Value")
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.legend()
        self.canvas.draw()