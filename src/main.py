"""Punto de entrada: login y registro, y redirección a la vista según el rol.
Autor: Roberto | Historia: [Controlador / Auth]"""
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMessageBox, QWidget

from controller.admin_controller import AdminController
from controller.auth_controller import AuthController
from controller.gerente_controller import GerenteController
from controller.simulador_controller import GeneradorLecturas
from model import usuario_model as um
from rutas import QSS_PATH, VIEWS_DIR
from view.admin_view import VentanaAdmin
from view.gerente_view import VentanaGerente


class VentanaLogin(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(VIEWS_DIR / "login.ui"), self)
        self.auth = AuthController()
        self.generador = GeneradorLecturas()
        self.ventana = None
        self.controlador = None
        for texto, rol, organizacion in um.PERFILES[1:]:      # el administrador no se auto-registra
            self.cmbRegRol.addItem(texto, (rol, organizacion))
        self.btnEntrar.clicked.connect(self.intentar_login)
        self.txtLoginPassword.returnPressed.connect(self.intentar_login)
        self.btnRegistrarse.clicked.connect(self.intentar_registro)

    def _mensaje(self, etiqueta, texto, ok):
        etiqueta.setStyleSheet(f"color: {'#3FB68B' if ok else '#E5574F'};")
        etiqueta.setText(texto)

    def intentar_login(self):
        usuario = self.auth.login(self.txtLoginUsuario.text(), self.txtLoginPassword.text())
        if not usuario:
            return self._mensaje(self.lblErrorLogin, "DNI o contraseña incorrectos.", False)
        self._mensaje(self.lblErrorLogin, "", True)
        self.abrir_vista(usuario)

    def intentar_registro(self):
        rol, organizacion = self.cmbRegRol.currentData()
        ok, texto = self.auth.registrar(
            self.txtRegDni.text(), self.txtRegNombre.text(), self.txtRegApellidos.text(),
            self.txtRegTelefono.text(), self.txtRegPassword.text(), rol, organizacion)
        self._mensaje(self.lblMensajeRegistro, texto, ok)
        if ok:
            self.tabLogin.setCurrentIndex(0)
            self.txtLoginUsuario.setText(self.txtRegDni.text().strip().upper())

    def abrir_vista(self, usuario):
        vista_ui = self.auth.vista_para_rol(usuario["rol"])
        nombre_rol = self.auth.nombre_rol(usuario["rol"])
        if vista_ui == "gerente.ui":
            self.ventana = VentanaGerente(self.generador.aforo_maximo)
            self.controlador = GerenteController(self.ventana, self.generador, usuario, nombre_rol)
        elif vista_ui == "admin.ui":
            self.ventana = VentanaAdmin()
            self.controlador = AdminController(self.ventana, usuario, nombre_rol)
        else:
            QMessageBox.information(self, "En desarrollo",
                                    f"La vista de «{nombre_rol}» se desarrolla en el sprint 3.")
            return
        self.ventana.btnCerrarSesion.clicked.connect(self.cerrar_sesion)
        self.txtLoginPassword.clear()
        self.hide()
        self.ventana.show()

    def cerrar_sesion(self):
        self.show()
        if self.ventana:
            self.ventana.close()
            self.ventana = self.controlador = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS_PATH.read_text(encoding="utf-8"))
    login = VentanaLogin()
    login.show()
    sys.exit(app.exec())
