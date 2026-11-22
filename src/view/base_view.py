from PySide6.QtWidgets import QWidget, QMessageBox

class BaseView(QWidget):
    """Clase base para estandarizar el comportamiento de las vistas en PyQt/PySide6."""
    def __init__(self, parent=None):
        super().__init__(parent)

    def mostrar_mensaje(self, titulo: str, mensaje: str):
        """Muestra un cuadro de diálogo informativo."""
        QMessageBox.information(self, titulo, mensaje)

    def mostrar_error(self, titulo: str, mensaje: str):
        """Muestra un cuadro de diálogo crítico de error."""
        QMessageBox.critical(self, titulo, mensaje)