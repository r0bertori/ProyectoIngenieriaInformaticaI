"""Vista del Administrador (PyQt). Autor: Rodrigo | Historia: [Vista - Administrador]"""
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

from rutas import VIEWS_DIR


class VentanaAdmin(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(VIEWS_DIR / "admin.ui"), self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

    def set_usuario(self, nombre, rol):
        self.lblNombreUsuario.setText(nombre)
        self.lblRolUsuario.setText(rol)
