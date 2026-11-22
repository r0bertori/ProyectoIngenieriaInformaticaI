"""Venta de alcohol en barra (S08), máquina de tabaco/tragaperras (S09) y consumo eléctrico (S07).
Autor: Diego  |  Historia: [Modelo / Consumo Bar]"""
import random
from datetime import datetime

from model.lectura import nueva_lectura


class ConsumoBar:
    UMBRAL_VACIADO = 85.0

    def __init__(self):
        self.consumiciones = 0
        self.recaudacion = 30.0
        self.potencia_kw = 2.5
        self.eventos = []

    def _evento(self, tipo, detalle):
        self.eventos.append({
            "momento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": tipo,
            "detalle": detalle,
        })
        del self.eventos[:-200]  # solo nos quedamos con los últimos 200

    def registrar_dispensacion(self, cantidad=1):
        if cantidad <= 0:
            return
        self.consumiciones += cantidad
        self._evento("dispensacion", f"{cantidad} consumición(es) en barra")

    def vaciar_maquinas(self):
        self.recaudacion = 0.0
        self._evento("vaciado", "Vaciado de la máquina de tabaco y tragaperras")

    def necesita_vaciado(self):
        return self.recaudacion >= self.UMBRAL_VACIADO

    def obtener_eventos(self, limite=20):
        return self.eventos[-limite:]

    def simular_paso(self):
        # alcohol en barra (S08)
        cantidad = random.choice([0, 0, 1, 2, 3])
        if cantidad:
            self.registrar_dispensacion(cantidad)

        # recaudación máquinas (S09)
        self.recaudacion = round(self.recaudacion + random.uniform(0.0, 2.5), 2)
        if self.recaudacion >= 100.0:
            self.vaciar_maquinas()

        # consumo eléctrico en kW (S07), sube un poco si hay movimiento
        variacion = random.uniform(-0.15, 0.35) + (0.1 * cantidad)
        self.potencia_kw = round(max(1.2, min(12.0, self.potencia_kw + variacion)), 2)

    def leer(self):
        self.simular_paso()
        return [
            nueva_lectura("S07", self.potencia_kw),
            nueva_lectura("S08", self.consumiciones),
            nueva_lectura("S09", int(round(self.recaudacion))),
        ]