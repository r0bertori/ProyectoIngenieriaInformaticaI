
"""Recepción de avisos energéticos enviados por el Ayuntamiento."""

import json

from model.aviso_energetico import AvisoEnergetico
from rutas import DATA_DIR


class AyuntamientoController:
    """Lee y procesa las consignas energéticas del Ayuntamiento."""

    def __init__(self, ruta_avisos=None):
        self.ruta_avisos = (
            ruta_avisos
            if ruta_avisos is not None
            else DATA_DIR / "avisos_energeticos.json"
        )

    def cargar_avisos(self):
        """Lee el JSON y devuelve una lista de objetos AvisoEnergetico."""

        with open(self.ruta_avisos, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, dict) or not isinstance(
            datos.get("avisos"), list
        ):
            raise ValueError(
                "El archivo debe contener una lista llamada 'avisos'."
            )

        avisos = []

        for indice, datos_aviso in enumerate(datos["avisos"]):
            try:
                aviso = AvisoEnergetico.from_dict(datos_aviso)
                avisos.append(aviso)
            except (KeyError, TypeError, ValueError) as error:
                raise ValueError(
                    f"Error en el aviso de la posición {indice}: {error}"
                ) from error

        return avisos

    def obtener_ultimo_aviso(self):
        """Devuelve el último aviso recibido o None si no hay avisos."""

        avisos = self.cargar_avisos()

        if not avisos:
            return None

        return avisos[-1]
