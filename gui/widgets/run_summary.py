try:
    from PySide2 import QtWidgets, QtCore
except ImportError:
    from PySide import QtWidgets, QtCore

class RunSummaryTable(QtWidgets.QTableWidget):
    """Summary Table"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(["Element Size [max, min]", "Elements", "Nodes", "QoI Value", "Rel Error (%)"])
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def populate_data(self, results_list: list):
        self.setRowCount(0)
        for row_idx, data in enumerate(results_list):
            self.insertRow(row_idx)
            
            #run_num = str(data.get("Run", row_idx + 1))
            size = str(data.get("Size", 0.0))
            elements = str(data.get("Elements", 0))
            nodes = str(data.get("Nodes", 0))
            qoi = f"{data.get('QoI', 0.0):.4f}"
            
            # Relative Error (after Run1)
            rel_error = "N/A"
            if row_idx > 0:
                prev_qoi = results_list[row_idx - 1].get("QoI", 0.0)
                curr_qoi = data.get("QoI", 0.0)
                if prev_qoi != 0:
                    err = abs(curr_qoi - prev_qoi) / abs(prev_qoi) * 100
                    rel_error = f"{err:.2f}%"

            #self.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(run_num))
            self.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(size))
            self.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(elements))
            self.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(nodes))
            self.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(qoi))
            self.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(rel_error))
            