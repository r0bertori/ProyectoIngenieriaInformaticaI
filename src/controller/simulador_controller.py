"""Generador de lecturas simuladas para los sensores del sprint 2 (aforo, humo, CO2, ruido y consumo del bar).
Autor: Roberto  |  Historia: [Controlador / Simulación]
Entrega al resto de la aplicación la misma estructura que tendrían los datos reales."""
import json

from model.consumo_bar import ConsumoBar
from model.sensores_bar import SensorAforo, SensorCO2, SensorHumo, SensorRuido
from rutas import DATA_DIR


class GeneradorLecturas:
    def __init__(self):
        with open(DATA_DIR / "config.json", encoding="utf-8") as f:
            parametros = json.load(f)["parametros_activos"]
        self.aforo_maximo = parametros["aforo_maximo"]
        self.umbral_co2 = parametros["umbral_co2_ppm"]
        # S01-S04: módulos de Peihao
        self.sensores = [SensorAforo(self.aforo_maximo), SensorHumo(),
                         SensorCO2(self.umbral_co2), SensorRuido()]
        # S08-S09: módulo de Diego
        self.consumo = ConsumoBar()

    def generar_paso(self):
        """Devuelve una lectura por sensor: S01, S02, S03, S04, S08 y S09."""
        lecturas = [s.leer() for s in self.sensores]
        lecturas += self.consumo.leer()
        return sorted(lecturas, key=lambda l: l["sensor_id"])
