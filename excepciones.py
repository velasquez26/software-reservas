"""Excepciones personalizadas del sistema Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base: todas las excepciones del sistema heredan de ella."""


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no son válidos."""


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parámetro obligatorio."""


class ServicioInvalidoError(SoftwareFJError):
    """Se lanza cuando los parámetros de un servicio son inválidos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta usar un servicio no disponible."""


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo de costos da un resultado inconsistente."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta una operación no permitida en el estado actual."""


class ReservaError(SoftwareFJError):
    """Se lanza cuando falla la creación o el procesamiento de una reserva."""
