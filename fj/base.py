"""Clase abstracta que modela cualquier entidad del sistema."""
from abc import ABC, abstractmethod
from datetime import datetime


class EntidadFJ(ABC):
    """Entidad general: tiene un código legible (p. ej. CLI-001) y un resumen.

    El código se asigna al FINAL de la construcción de cada subclase, así que
    un objeto que falla sus validaciones no consume número de consecutivo.
    """

    PREFIJO = "ENT"          # cada subclase define el suyo
    _consecutivos: dict = {}  # contador compartido, uno por prefijo

    def __init__(self) -> None:
        """Asigna el siguiente código disponible para el prefijo de la clase."""
        numero = EntidadFJ._consecutivos.get(self.PREFIJO, 0) + 1
        EntidadFJ._consecutivos[self.PREFIJO] = numero
        self._codigo = f"{self.PREFIJO}-{numero:03d}"
        self._creada_en = datetime.now()

    @property
    def codigo(self) -> str:
        """Código único y de solo lectura de la entidad."""
        return self._codigo

    @abstractmethod
    def resumen(self) -> str:
        """Texto corto que describe a la entidad."""

    def __str__(self) -> str:
        """Al imprimir la entidad se muestra su resumen."""
        return self.resumen()
