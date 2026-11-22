"""Módulos de simulación de aforo (S01), humo (S02), CO2 (S03) y ruido (S04).
Autor: Peihao  |  Historia: [Modelo / Sensores Bar]
Cada sensor tiene leer() y devuelve una lectura con la estructura de models/lectura.py."""
import random

from model.lectura import nueva_lectura


class SensorSimulado:
    """Sensor numérico simulado: el valor se mueve poco a poco entre un mínimo y un máximo."""

    def __init__(self, sensor_id, inicial, minimo, maximo, paso_min, paso_max, decimales=0):
        self.sensor_id = sensor_id
        self.valor = inicial
        self.minimo, self.maximo = minimo, maximo
        self.paso_min, self.paso_max = paso_min, paso_max
        self.decimales = decimales

    def leer(self):
        nuevo = self.valor + random.uniform(self.paso_min, self.paso_max)
        self.valor = max(self.minimo, min(self.maximo, nuevo))
        valor = round(self.valor, self.decimales) if self.decimales else int(round(self.valor))
        return nueva_lectura(self.sensor_id, valor)


class SensorAforo(SensorSimulado):
    """S01. Personas en el local. Puede superar el máximo unas pocas personas (para probar alertas)."""

    def __init__(self, aforo_maximo):
        super().__init__("S01", 10, 0, aforo_maximo + 5, -2, 3)


class SensorCO2(SensorSimulado):
    """S03. CO2 en ppm. Llega a superar un poco el umbral de config.json."""

    def __init__(self, umbral_ppm):
        super().__init__("S03", 450, 400, umbral_ppm + 150, -10, 15)


class SensorRuido(SensorSimulado):
    """S04. Nivel sonoro en dB."""

    def __init__(self):
        super().__init__("S04", 60, 50, 100, -5, 5)


class SensorHumo:
    """S02. 0 = sin detección, 1 = humo detectado. Detecciones raras que duran 3 lecturas."""

    def __init__(self, probabilidad=0.01):
        self.probabilidad = probabilidad
        self._restantes = 0

    def leer(self):
        if self._restantes > 0:
            self._restantes -= 1
            valor = 1
        elif random.random() < self.probabilidad:
            self._restantes = 2
            valor = 1
        else:
            valor = 0
        return nueva_lectura("S02", valor)
