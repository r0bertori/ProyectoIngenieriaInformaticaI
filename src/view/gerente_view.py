"""Vista del Gerente del bar (PyQt). Autor: Rodrigo | Historia: [Vista - Gerente]"""
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

from rutas import VIEWS_DIR


class VentanaGerente(QWidget):
    def __init__(self, aforo_maximo=60):
        super().__init__()
        uic.loadUi(str(VIEWS_DIR / "gerente.ui"), self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.aforo_maximo = aforo_maximo
        self.barAforo.setMaximum(aforo_maximo)

    def set_usuario(self, nombre, rol):
        self.lblNombreUsuario.setText(nombre)
        self.lblRolUsuario.setText(rol)

    def actualizar(self, v):
        """v = {'S01': lectura, ...}. Rellena los paneles de aforo, calidad del aire y consumo."""
        aforo = int(v["S01"]["valor"])
        self.lblAforoValor.setText(f"{aforo} / {self.aforo_maximo}")
        self.barAforo.setValue(min(aforo, self.aforo_maximo))
        self.lblAireValor.setText(f"CO2: {v['S03']['valor']} ppm")
        self.lblAireHumo.setText("Humo detectado" if v["S02"]["valor"] else "Sin detección de humo")
        self.lblConsumoValor.setText(f"{v['S08']['valor']} consumiciones")
        self.lblConsumoMaquinas.setText(f"Máquinas: recaudación al {v['S09']['valor']} %")
