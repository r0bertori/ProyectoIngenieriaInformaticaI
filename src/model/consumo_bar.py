"""Venta de alcohol en barra (S08) y máquina de tabaco/tragaperras (S09), con datos simulados.
Autor: Diego  |  Historia: [Modelo / Consumo Bar]"""
import random
from datetime import datetime

from model.lectura import nueva_lectura


class ConsumoBar:
    def __init__(self):
        self.consumiciones = 0       # bebidas dispensadas hoy
        self.recaudacion = 30.0      # % de llenado de la recaudación de las máquinas
        self.eventos = []            # registro de eventos (dispensación y vaciado)

    def _evento(self, tipo, detalle):
        self.eventos.append({"momento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             "tipo": tipo, "detalle": detalle})
        del self.eventos[:-200]      # solo se guardan los últimos 200

    def registrar_dispensacion(self, cantidad=1):
        self.consumiciones += cantidad
        self._evento("dispensacion", f"{cantidad} consumición(es) en barra")

    def vaciar_maquinas(self):
        self.recaudacion = 0.0
        self._evento("vaciado", "Vaciado de la máquina de tabaco y tragaperras")

    def simular_paso(self):
        cantidad = random.choice([0, 0, 1, 2, 3])
        if cantidad:
            self.registrar_dispensacion(cantidad)
        self.recaudacion += random.uniform(0, 2)
        if self.recaudacion >= 100:
            self.vaciar_maquinas()

    def leer(self):
        """Devuelve [lectura S08 (consumiciones del día), lectura S09 (% de recaudación)]."""
        self.simular_paso()
        return [nueva_lectura("S08", self.consumiciones),
                nueva_lectura("S09", int(round(self.recaudacion)))]
