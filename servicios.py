"""Clase abstracta Servicio y tres servicios especializados (polimorfismo)."""
from abc import ABC, abstractmethod

from entidades import EntidadBase
from excepciones import (
    CalculoInconsistenteError,
    ParametroFaltanteError,
    ServicioInvalidoError,
)

IVA_POR_DEFECTO = 0.19  # 19 % de IVA en Colombia


class Servicio(EntidadBase, ABC):
    """Servicio ofrecido por Software FJ."""

    def __init__(self, nombre=None, tarifa_hora=None) -> None:
        super().__init__()
        if not nombre:
            raise ParametroFaltanteError("El servicio necesita un nombre.")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa inválida: {tarifa_hora!r}.")
        self._nombre = nombre
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self._disponible = bool(valor)

    # ---- métodos abstractos: cada servicio los sobrescribe ----
    @abstractmethod
    def validar_parametros(self, horas) -> None:
        """Valida la duración (y otros datos propios del servicio)."""

    @abstractmethod
    def _costo_base(self, horas: float) -> float:
        """Costo sin impuestos ni descuentos."""

    @abstractmethod
    def describir(self) -> str:
        """Descripción del servicio."""

    # ---- método sobrecargado (parámetros opcionales) ----
    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0) -> float:
        """Sobrecarga simulada con parámetros opcionales:
        - calcular_costo(h)                      -> costo base
        - calcular_costo(h, impuesto=0.19)       -> con impuesto
        - calcular_costo(h, descuento=0.10)      -> con descuento
        - calcular_costo(h, 0.19, 0.10)          -> con ambos
        """
        self.validar_parametros(horas)
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise CalculoInconsistenteError(
                f"Impuesto ({impuesto}) y descuento ({descuento}) deben estar entre 0 y 1."
            )
        total = self._costo_base(horas) * (1 - descuento) * (1 + impuesto)
        if total < 0:
            raise CalculoInconsistenteError("El costo calculado es negativo.")
        return round(total, 2)

    def calcular_costo_con_iva(self, horas) -> float:
        """Variante de conveniencia: aplica el IVA por defecto."""
        return self.calcular_costo(horas, impuesto=IVA_POR_DEFECTO)


class SalaReserva(Servicio):
    """Reserva de salas: el costo depende de las horas y de la capacidad."""

    def __init__(self, nombre=None, tarifa_hora=None, capacidad=10) -> None:
        super().__init__(nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}.")
        self._capacidad = capacidad

    def validar_parametros(self, horas) -> None:
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 12:
            raise ServicioInvalidoError(f"Una sala se reserva de 1 a 12 horas, no {horas!r}.")

    def _costo_base(self, horas: float) -> float:
        return self._tarifa_hora * horas

    def describir(self) -> str:
        return f"Sala '{self.nombre}' (capacidad {self._capacidad}) - ${self._tarifa_hora:,.0f}/h"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: se cobra un depósito fijo además de las horas."""

    DEPOSITO = 20000.0

    def __init__(self, nombre=None, tarifa_hora=None, tipo_equipo="portátil") -> None:
        super().__init__(nombre, tarifa_hora)
        self._tipo_equipo = tipo_equipo

    def validar_parametros(self, horas) -> None:
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 72:
            raise ServicioInvalidoError(f"Un equipo se alquila de 1 a 72 horas, no {horas!r}.")

    def _costo_base(self, horas: float) -> float:
        return self._tarifa_hora * horas + self.DEPOSITO

    def describir(self) -> str:
        return f"Equipo '{self.nombre}' ({self._tipo_equipo}) - ${self._tarifa_hora:,.0f}/h + depósito"


class Asesoria(Servicio):
    """Asesoría especializada: el nivel del asesor multiplica la tarifa."""

    MULTIPLICADORES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, nombre=None, tarifa_hora=None, nivel="junior") -> None:
        super().__init__(nombre, tarifa_hora)
        if nivel not in self.MULTIPLICADORES:
            raise ServicioInvalidoError(f"Nivel de asesor inválido: {nivel!r}.")
        self._nivel = nivel

    def validar_parametros(self, horas) -> None:
        if not isinstance(horas, (int, float)) or not 0.5 <= horas <= 8:
            raise ServicioInvalidoError(f"Una asesoría dura de 0.5 a 8 horas, no {horas!r}.")

    def _costo_base(self, horas: float) -> float:
        return self._tarifa_hora * self.MULTIPLICADORES[self._nivel] * horas

    def describir(self) -> str:
        return f"Asesoría '{self.nombre}' (nivel {self._nivel}) - ${self._tarifa_hora:,.0f}/h"
