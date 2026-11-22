"""Conecta el generador de lecturas con la vista del Gerente (tiempo real).
Autor: Rodrigo | Historia: [Vista - Gerente]"""
from PyQt6.QtCore import QTimer


class GerenteController:
    def __init__(self, vista, generador, usuario, nombre_rol, intervalo_ms=2000):
        self.vista = vista
        self.generador = generador
        vista.set_usuario(f"{usuario['nombre']} {usuario['apellidos']}", nombre_rol)
        self.timer = QTimer(vista)          # al cerrar la ventana, el temporizador se destruye con ella
        self.timer.timeout.connect(self.actualizar)
        self.timer.start(intervalo_ms)
        self.actualizar()

    def actualizar(self):
        lecturas = self.generador.generar_paso()
        self.vista.actualizar({l["sensor_id"]: l for l in lecturas})
