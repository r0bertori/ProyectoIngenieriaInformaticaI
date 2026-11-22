"""Sensores del bar: aforo, humo, CO2 y ruido (Peihao)."""
from config import DATA_DIR
from model.json_store import leer_json
from model.lecturas_base import LecturasBase, RUTA_HISTORIAL

RUTA_SENSORES = DATA_DIR / "sensores.json"


class SensoresModel(LecturasBase):
    SENSORES = ("S01", "S02", "S03", "S04")  # aforo, humo, CO2, ruido

    def __init__(self, ruta=RUTA_HISTORIAL, ruta_sensores=RUTA_SENSORES):
        super().__init__(ruta)
        self.ruta_sensores = ruta_sensores

    # --- definición del sensor (sensores.json) ---
    def definicion(self, sensor_id):
        """Dict con id, nombre, unidad, tipo, umbral_alerta y etiquetas (si es binario)."""
        self._comprobar(sensor_id)
        for s in leer_json(self.ruta_sensores)["sensores"]:
            if s["id"] == sensor_id:
                return s
        raise KeyError(f"{sensor_id} no está en sensores.json")

    # --- valores actuales ---
    def _valor(self, sensor_id, por_defecto=None):
        lectura = self.ultima_lectura(sensor_id)
        return lectura["valor"] if lectura else por_defecto

    def aforo_actual(self):
        """Personas en el local (0 si aún no hay lecturas)."""
        return self._valor("S01", 0)

    def hay_humo(self):
        return bool(self._valor("S02", 0))

    def co2_ppm(self):
        return self._valor("S03")

    def ruido_db(self):
        return self._valor("S04")

    # --- para vistas y alertas ---
    def ultimas(self, sensor_id, n=10):
        """Las n últimas lecturas de un sensor (para gráficas o tablas)."""
        return self.lecturas(sensor_id)[-n:]

    def texto(self, sensor_id):
        """Valor listo para mostrar: '42 personas', '812 ppm', 'Humo detectado'..."""
        lectura = self.ultima_lectura(sensor_id)
        if lectura is None:
            return "--"
        d = self.definicion(sensor_id)
        if d["tipo"] == "binario":
            return d["etiquetas"][str(lectura["valor"])]
        return f'{lectura["valor"]} {d["unidad"]}'.strip()

    def resumen(self):
        """Estado actual de los cuatro sensores: {id: {nombre, valor, texto, unidad, umbral, timestamp}}."""
        resultado = {}
        for sid in self.SENSORES:
            d = self.definicion(sid)
            lectura = self.ultima_lectura(sid)
            resultado[sid] = {
                "nombre": d["nombre"],
                "valor": lectura["valor"] if lectura else None,
                "texto": self.texto(sid),
                "unidad": d["unidad"],
                "umbral": d["umbral_alerta"],
                "timestamp": lectura["timestamp"] if lectura else None,
            }
        return resultado
