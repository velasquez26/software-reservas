"""Jerarquía de excepciones propias de Software FJ.

Todas heredan de ErrorFJ, de modo que el programa pueda capturar cualquier
fallo del dominio con un único `except ErrorFJ`.
"""


class ErrorFJ(Exception):
    """Error base del dominio de Software FJ."""


class DatoInvalidoError(ErrorFJ):
    """Un dato recibido no cumple las reglas de validación."""


class ParametroAusenteError(ErrorFJ):
    """Falta un parámetro obligatorio (llegó vacío o None)."""


class ServicioError(ErrorFJ):
    """Problema en la definición o parámetros de un servicio."""


class ServicioNoDisponibleError(ErrorFJ):
    """El servicio existe, pero en este momento no se puede reservar."""


class CalculoError(ErrorFJ):
    """El cálculo de costos produjo un resultado o recibió datos incoherentes."""


class OperacionInvalidaError(ErrorFJ):
    """La operación no está permitida en el estado actual del objeto."""


class ReservaError(ErrorFJ):
    """La reserva no pudo crearse o procesarse."""
