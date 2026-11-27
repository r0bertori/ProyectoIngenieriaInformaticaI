
"""Modelo de avisos de restricción energética enviados por el Ayuntamiento."""


class AvisoEnergetico:
    """Representa una consigna energética recibida del Ayuntamiento."""

    NIVELES_VALIDOS = ("normal", "moderado", "alto", "critico")

    def __init__(
        self,
        id_aviso,
        fecha,
        nivel_restriccion,
        apagar_iluminacion_no_esencial=False,
        limitar_climatizacion=False,
        temperatura_objetivo=None
    ):
        if not id_aviso:
            raise ValueError("El aviso debe tener un identificador.")

        if nivel_restriccion not in self.NIVELES_VALIDOS:
            raise ValueError("Nivel de restricción no válido.")

        if temperatura_objetivo is not None:
            if not isinstance(temperatura_objetivo, (int, float)):
                raise ValueError("La temperatura objetivo debe ser numérica.")

        self.id_aviso = id_aviso
        self.fecha = fecha
        self.nivel_restriccion = nivel_restriccion
        self.apagar_iluminacion_no_esencial = bool(
            apagar_iluminacion_no_esencial
        )
        self.limitar_climatizacion = bool(limitar_climatizacion)
        self.temperatura_objetivo = temperatura_objetivo

    def to_dict(self):
        """Convierte el aviso en un diccionario compatible con JSON."""
        return {
            "id_aviso": self.id_aviso,
            "fecha": self.fecha,
            "nivel_restriccion": self.nivel_restriccion,
            "apagar_iluminacion_no_esencial":
                self.apagar_iluminacion_no_esencial,
            "limitar_climatizacion": self.limitar_climatizacion,
            "temperatura_objetivo": self.temperatura_objetivo
        }

    @classmethod
    def from_dict(cls, datos):
        """Crea un aviso energético a partir de un diccionario."""
        return cls(
            id_aviso=datos["id_aviso"],
            fecha=datos["fecha"],
            nivel_restriccion=datos["nivel_restriccion"],
            apagar_iluminacion_no_esencial=datos.get(
                "apagar_iluminacion_no_esencial", False
            ),
            limitar_climatizacion=datos.get(
                "limitar_climatizacion", False
            ),
            temperatura_objetivo=datos.get("temperatura_objetivo")
        )
