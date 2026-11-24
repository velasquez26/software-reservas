"""Reserva: une cliente, servicio, duración y estado, con historial de cambios."""
from datetime import datetime
from enum import Enum

from .base import EntidadFJ
from .bitacora import bitacora
from .catalogo import Servicio
from .clientes import Cliente
from .errores import (ErrorFJ, OperacionInvalidaError, ReservaError,
                      ServicioError, ServicioNoDisponibleError)


class Estado(Enum):
    """Estados posibles de una reserva."""
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    PROCESADA = "procesada"
    CANCELADA = "cancelada"


class Reserva(EntidadFJ):
    """Reserva de un servicio hecha por un cliente."""

    PREFIJO = "RES"

    def __init__(self, cliente, servicio, horas) -> None:
        """Valida tipos, disponibilidad y duración antes de crear la reserva."""
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ReservaError("Se necesita un Cliente y un Servicio válidos.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"'{servicio.nombre}' no está disponible por ahora.")
        try:
            servicio.validar_parametros(horas)
        except ServicioError as causa:
            # Encadenamiento: la causa original queda accesible en __cause__
            raise ReservaError("No se creó la reserva: duración no admitida.") from causa
        self.cliente, self.servicio, self.horas = cliente, servicio, horas
        self._estado = Estado.PENDIENTE
        self._historial = []
        super().__init__()
        self._anotar("creada")

    @property
    def estado(self) -> Estado:
        """Estado actual."""
        return self._estado

    @property
    def historial(self) -> list:
        """Copia de la lista de cambios (no se puede alterar desde fuera)."""
        return list(self._historial)

    def _anotar(self, evento: str) -> None:
        """Agrega un evento al historial con la hora actual."""
        self._historial.append((datetime.now().strftime("%H:%M:%S"), evento))

    def confirmar(self) -> None:
        """Pasa de PENDIENTE a CONFIRMADA."""
        if self._estado is not Estado.PENDIENTE:
            raise OperacionInvalidaError(f"{self.codigo}: no se confirma una reserva {self._estado.value}.")
        self._estado = Estado.CONFIRMADA
        self._anotar("confirmada")

    def cancelar(self) -> None:
        """Cancela la reserva salvo que ya esté procesada o cancelada."""
        if self._estado in (Estado.CANCELADA, Estado.PROCESADA):
            raise OperacionInvalidaError(f"{self.codigo}: no se cancela una reserva {self._estado.value}.")
        self._estado = Estado.CANCELADA
        self._anotar("cancelada")

    def procesar(self) -> float:
        """Confirma (si hace falta) y cobra. Demuestra try/except/else/finally."""
        total = 0.0
        try:
            if self._estado is Estado.PENDIENTE:
                self.confirmar()
            if self._estado is not Estado.CONFIRMADA:
                raise OperacionInvalidaError(f"{self.codigo}: solo se procesa una reserva confirmada.")
            total = self.servicio.cotizar_para(self.horas, self.cliente)
        except ErrorFJ as causa:
            bitacora.error("Fallo al procesar %s: %s", self.codigo, causa)
            raise ReservaError(f"{self.codigo} no pudo procesarse.") from causa
        else:
            self._estado = Estado.PROCESADA          # solo si todo salió bien
            self._anotar(f"procesada (${total:,.2f})")
            bitacora.info("%s procesada por $%s", self.codigo, f"{total:,.2f}")
            return total
        finally:
            bitacora.info("Intento de procesamiento de %s terminado (estado: %s)",
                          self.codigo, self._estado.value)

    def resumen(self) -> str:
        """Descripción en una línea."""
        return (f"{self.codigo} · {self.cliente.nombre} → {self.servicio.nombre} "
                f"· {self.horas} h · {self._estado.value}")
