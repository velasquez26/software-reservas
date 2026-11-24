"""Clase Cliente con encapsulación y validaciones robustas."""
import re

from entidades import EntidadBase
from excepciones import ClienteInvalidoError, ParametroFaltanteError

_PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class Cliente(EntidadBase):
    """Cliente de Software FJ. Los datos personales son atributos privados."""

    def __init__(self, nombre=None, correo=None, telefono=None) -> None:
        super().__init__()
        # Los setters validan; si fallan, el objeto no llega a crearse.
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # ---- nombre ----
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor) -> None:
        if valor is None:
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(f"Nombre inválido: {valor!r} (mínimo 3 letras).")
        if any(ch.isdigit() for ch in valor):
            raise ClienteInvalidoError(f"El nombre no puede contener números: {valor!r}.")
        self.__nombre = valor.strip().title()

    # ---- correo ----
    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor) -> None:
        if valor is None:
            raise ParametroFaltanteError("El correo del cliente es obligatorio.")
        if not isinstance(valor, str) or not _PATRON_CORREO.match(valor.strip()):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}.")
        self.__correo = valor.strip().lower()

    # ---- teléfono ----
    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor) -> None:
        if valor is None:
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")
        limpio = str(valor).replace(" ", "")
        if not limpio.isdigit() or not 7 <= len(limpio) <= 10:
            raise ClienteInvalidoError(f"Teléfono inválido: {valor!r} (7 a 10 dígitos).")
        self.__telefono = limpio

    def describir(self) -> str:
        return f"Cliente #{self.id}: {self.nombre} | {self.correo} | {self.telefono}"
