
"""Modelo del sistema de control energético del bar."""


class ControlEnergetico:
    """Representa el estado de la iluminación y la climatización."""

    def __init__(self):
        # Estado inicial de la iluminación
        self.iluminacion_esencial = True
        self.iluminacion_no_esencial = True

        # Estado inicial de la climatización
        self.climatizacion_encendida = True
        self.temperatura_objetivo = 22.0

    def controlar_iluminacion(self, esencial=None, no_esencial=None):
        """Modifica el estado de la iluminación."""

        if esencial is not None:
            self.iluminacion_esencial = bool(esencial)

        if no_esencial is not None:
            self.iluminacion_no_esencial = bool(no_esencial)

    def controlar_climatizacion(
        self, encendida=None, temperatura=None
    ):
        """Modifica el estado de la climatización."""

        if encendida is not None:
            self.climatizacion_encendida = bool(encendida)

        if temperatura is not None:
            if not isinstance(temperatura, (int, float)):
                raise ValueError("La temperatura debe ser numérica.")

            self.temperatura_objetivo = float(temperatura)

    def obtener_estado(self):
        """Devuelve el estado actual de los sistemas."""

        return {
            "iluminacion": {
                "esencial": self.iluminacion_esencial,
                "no_esencial": self.iluminacion_no_esencial
            },
            "climatizacion": {
                "encendida": self.climatizacion_encendida,
                "temperatura_objetivo": self.temperatura_objetivo
            }
        }
