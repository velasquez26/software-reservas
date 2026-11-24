"""Cliente: datos personales encapsulados y validados."""
import re

from .base import EntidadFJ
from .errores import DatoInvalidoError, ParametroAusenteError

_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")
TIPOS_CLIENTE = {"regular": 0.0, "premium": 0.08}  # tipo -> descuento de fidelidad


def _exigir(valor, etiqueta: str):
    """Lanza ParametroAusenteError si el valor llegó vacío o None."""
    if valor is None or (isinstance(valor, str) and not valor.strip()):
        raise ParametroAusenteError(f"Falta el dato obligatorio: {etiqueta}.")
    return valor


class Cliente(EntidadFJ):
    """Persona que contrata servicios de Software FJ."""

    PREFIJO = "CLI"

    def __init__(self, nombre=None, documento=None, correo=None,
                 telefono=None, tipo="regular") -> None:
        """Valida cada dato mediante los setters; solo si todo es válido se crea."""
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        self.tipo = tipo
        super().__init__()  # el código se asigna al final, ya validado

    # ---------- nombre ----------
    @property
    def nombre(self) -> str:
        """Nombre completo del cliente."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor) -> None:
        """Exige texto de al menos 3 letras, sin dígitos."""
        valor = _exigir(valor, "nombre")
        if not isinstance(valor, str) or len(valor.strip()) < 3 or any(c.isdigit() for c in valor):
            raise DatoInvalidoError(f"Nombre no válido: {valor!r}.")
        self.__nombre = valor.strip().title()

    # ---------- documento ----------
    @property
    def documento(self) -> str:
        """Documento de identidad (solo dígitos)."""
        return self.__documento

    @documento.setter
    def documento(self, valor) -> None:
        """Exige entre 6 y 12 dígitos."""
        valor = str(_exigir(valor, "documento")).strip()
        if not valor.isdigit() or not 6 <= len(valor) <= 12:
            raise DatoInvalidoError(f"Documento no válido: {valor!r} (6 a 12 dígitos).")
        self.__documento = valor

    # ---------- correo ----------
    @property
    def correo(self) -> str:
        """Correo electrónico en minúsculas."""
        return self.__correo

    @correo.setter
    def correo(self, valor) -> None:
        """Exige un formato básico usuario@dominio.ext."""
        valor = _exigir(valor, "correo")
        if not isinstance(valor, str) or not _CORREO.match(valor.strip()):
            raise DatoInvalidoError(f"Correo no válido: {valor!r}.")
        self.__correo = valor.strip().lower()

    # ---------- teléfono ----------
    @property
    def telefono(self) -> str:
        """Teléfono de contacto (solo dígitos)."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor) -> None:
        """Exige entre 7 y 10 dígitos (se ignoran espacios)."""
        valor = str(_exigir(valor, "teléfono")).replace(" ", "")
        if not valor.isdigit() or not 7 <= len(valor) <= 10:
            raise DatoInvalidoError(f"Teléfono no válido: {valor!r}.")
        self.__telefono = valor

    # ---------- tipo ----------
    @property
    def tipo(self) -> str:
        """Categoría del cliente: 'regular' o 'premium'."""
        return self.__tipo

    @tipo.setter
    def tipo(self, valor) -> None:
        """Solo acepta las categorías definidas en TIPOS_CLIENTE."""
        if valor not in TIPOS_CLIENTE:
            raise DatoInvalidoError(f"Tipo de cliente desconocido: {valor!r}.")
        self.__tipo = valor

    @property
    def descuento_fidelidad(self) -> float:
        """Fracción de descuento que le corresponde por su categoría."""
        return TIPOS_CLIENTE[self.__tipo]

    def resumen(self) -> str:
        """Descripción en una línea."""
        return f"{self.codigo} · {self.nombre} ({self.tipo}) · {self.correo}"
