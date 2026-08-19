try:
    from PySide2 import QtWidgets
except ImportError:
    from PySide import QtWidgets

def show_limit_warning(parent, message: str) -> bool:
    """Limites Warning message"""
    reply = QtWidgets.QMessageBox.warning(
        parent,
        "Safety Limit Exceeded",
        f"{message}\n\nDo you want to continue anyway?",
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        QtWidgets.QMessageBox.No
    )
    return reply == QtWidgets.QMessageBox.Yes

def show_divergence_alert(parent, message: str):
    """Divergence Alert message"""
    QtWidgets.QMessageBox.critical(
        parent,
        "Divergence Warning",
        f"The study appears to be diverging:\n{message}",
        QtWidgets.QMessageBox.Ok
    )