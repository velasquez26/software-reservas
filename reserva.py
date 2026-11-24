"""Clase Reserva: integra cliente, servicio, duración y estado."""
from cliente import Cliente
from entidades import EntidadBase
from excepciones import (
    OperacionNoPermitidaError,
    ReservaError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    SoftwareFJError,
)
from logger import log
from servicios import Servicio

PENDIENTE, CONFIRMADA, CANCELADA = "PENDIENTE", "CONFIRMADA", "CANCELADA"


class Reserva(EntidadBase):
    """Reserva de un servicio por parte de un cliente."""

    def __init__(self, cliente, servicio, horas) -> None:
        super().__init__()
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ReservaError("Una reserva requiere un Cliente y un Servicio válidos.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible.")
        try:
            servicio.validar_parametros(horas)
        except ServicioInvalidoError as error:
            # Encadenamiento: conservamos la causa original con "from"
            raise ReservaError("No se pudo crear la reserva por parámetros inválidos.") from error
        self.cliente, self.servicio, self.horas = cliente, servicio, horas
        self._estado = PENDIENTE

    @property
    def estado(self) -> str:
        return self._estado

    def confirmar(self) -> None:
        """Confirma la reserva (solo si está pendiente)."""
        if self._estado != PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado}."
            )
        self._estado = CONFIRMADA

    def cancelar(self) -> None:
        """Cancela la reserva (no se puede cancelar dos veces)."""
        if self._estado == CANCELADA:
            raise OperacionNoPermitidaError("La reserva ya estaba cancelada.")
        self._estado = CANCELADA

    def procesar(self, impuesto=0.19, descuento=0.0) -> float:
        """Confirma la reserva y calcula el costo. Usa try/except/else/finally."""
        total = None
        try:
            self.confirmar()
            total = self.servicio.calcular_costo(self.horas, impuesto, descuento)
        except SoftwareFJError as error:
            log.error("Fallo procesando reserva #%s: %s", self.id, error)
            raise ReservaError(f"La reserva #{self.id} no pudo procesarse.") from error
        else:
            # Solo se ejecuta si no hubo excepción
            log.info("Reserva #%s procesada. Total: $%s", self.id, f"{total:,.2f}")
            return total
        finally:
            # Se ejecuta siempre, haya error o no
            log.info("Fin de procesamiento de reserva #%s (estado: %s)", self.id, self._estado)

    def describir(self) -> str:
        return (f"Reserva #{self.id} [{self._estado}] {self.cliente.nombre} -> "
                f"{self.servicio.nombre} ({self.horas} h)")
