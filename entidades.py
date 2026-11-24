"""Clase abstracta que representa las entidades generales del sistema."""
from abc import ABC, abstractmethod
from itertools import count


class EntidadBase(ABC):
    """Entidad general: toda entidad tiene un id único y se puede describir."""

    _contador = count(1)  # generador compartido de identificadores

    def __init__(self) -> None:
        self._id = next(EntidadBase._contador)  # id encapsulado (solo lectura)

    @property
    def id(self) -> int:
        """Identificador único de la entidad."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción legible de la entidad."""
