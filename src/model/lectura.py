"""Estructura común de una lectura (la misma que tendrán los datos reales).
Autor: Roberto (generador de simulación)."""
from datetime import datetime


def nueva_lectura(sensor_id, valor, **extra):
    """Devuelve {'sensor_id', 'fecha', 'hora', 'valor', ...extra}."""
    ahora = datetime.now()
    lectura = {
        "sensor_id": sensor_id,
        "fecha": ahora.strftime("%Y-%m-%d"),
        "hora": ahora.strftime("%H:%M"),
        "valor": valor,
    }
    lectura.update(extra)
    return lectura
