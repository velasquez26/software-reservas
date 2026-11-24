"""Catálogo de servicios: clase abstracta Servicio y tres especializaciones."""
from abc import ABC, abstractmethod

from .base import EntidadFJ
from .errores import CalculoError, ParametroAusenteError, ServicioError

IVA = 0.19  # impuesto general aplicado en las cotizaciones con IVA


class Servicio(EntidadFJ, ABC):
    """Servicio que Software FJ puede ofrecer a sus clientes."""

    PREFIJO = "SRV"

    def __init__(self, nombre=None, tarifa_hora=None) -> None:
        """Valida los datos comunes a todos los servicios."""
        if not nombre or not str(nombre).strip():
            raise ParametroAusenteError("El servicio necesita un nombre.")
        if isinstance(tarifa_hora, bool) or not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioError(f"Tarifa por hora no válida: {tarifa_hora!r}.")
        self._nombre = str(nombre).strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True
        # Las subclases llaman a super().__init__() y luego validan sus extras;
        # el código definitivo lo fija EntidadFJ.__init__ al final.

    @property
    def nombre(self) -> str:
        """Nombre comercial del servicio."""
        return self._nombre

    @property
    def disponible(self) -> bool:
        """True si el servicio puede reservarse ahora."""
        return self._disponible

    def habilitar(self, estado: bool) -> None:
        """Activa o desactiva el servicio."""
        self._disponible = bool(estado)

    # ----- métodos que cada servicio sobrescribe (polimorfismo) -----
    @abstractmethod
    def validar_parametros(self, horas) -> None:
        """Lanza ServicioError si la duración no es válida para este servicio."""

    @abstractmethod
    def costo_base(self, horas: float) -> float:
        """Costo sin impuestos ni descuentos."""

    # ----- cotización: variantes "sobrecargadas" -----
    def cotizar(self, horas, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """Cotiza con parámetros opcionales (equivale a varias sobrecargas):

        cotizar(h)                  -> costo base
        cotizar(h, impuesto=0.19)   -> con impuesto
        cotizar(h, descuento=0.1)   -> con descuento
        cotizar(h, 0.19, 0.1)       -> con ambos
        """
        self.validar_parametros(horas)
        for etiqueta, tasa in (("impuesto", impuesto), ("descuento", descuento)):
            if not isinstance(tasa, (int, float)) or not 0 <= tasa < 1:
                raise CalculoError(f"El {etiqueta} debe estar entre 0 y 1 (recibido: {tasa!r}).")
        total = self.costo_base(horas) * (1 - descuento) * (1 + impuesto)
        if total <= 0:
            raise CalculoError("El costo calculado no es positivo.")
        return round(total, 2)

    def cotizar_con_iva(self, horas) -> float:
        """Variante rápida: aplica el IVA general."""
        return self.cotizar(horas, impuesto=IVA)

    def cotizar_para(self, horas, cliente) -> float:
        """Variante por cliente: IVA más el descuento de fidelidad que le toque."""
        return self.cotizar(horas, IVA, cliente.descuento_fidelidad)


def _es_numero(valor) -> bool:
    """True si es int o float (se excluye bool)."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


class SalaReuniones(Servicio):
    """Reserva de salas: el costo sube si se pide proyector."""

    RECARGO_PROYECTOR = 12000.0  # por hora

    def __init__(self, nombre=None, tarifa_hora=None, aforo=8, con_proyector=False) -> None:
        super().__init__(nombre, tarifa_hora)
        if not isinstance(aforo, int) or isinstance(aforo, bool) or aforo <= 0:
            raise ServicioError(f"Aforo no válido: {aforo!r}.")
        self._aforo, self._con_proyector = aforo, bool(con_proyector)
        EntidadFJ.__init__(self)

    def validar_parametros(self, horas) -> None:
        """Las salas se reservan por horas completas, de 1 a 10."""
        if not _es_numero(horas) or horas != int(horas) or not 1 <= horas <= 10:
            raise ServicioError(f"Sala '{self.nombre}': se reserva de 1 a 10 horas enteras, no {horas!r}.")

    def costo_base(self, horas: float) -> float:
        """Tarifa por hora (+ proyector si aplica)."""
        extra = self.RECARGO_PROYECTOR if self._con_proyector else 0.0
        return (self._tarifa_hora + extra) * horas

    def resumen(self) -> str:
        """Descripción de la sala."""
        pry = "con proyector" if self._con_proyector else "sin proyector"
        return f"{self.codigo} · Sala {self.nombre} · aforo {self._aforo} · {pry} · ${self._tarifa_hora:,.0f}/h"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: se suma un depósito proporcional al valor del alquiler."""

    def __init__(self, nombre=None, tarifa_hora=None, categoria="computo", porcentaje_deposito=0.15) -> None:
        super().__init__(nombre, tarifa_hora)
        if not _es_numero(porcentaje_deposito) or not 0 <= porcentaje_deposito <= 0.5:
            raise ServicioError(f"Depósito no válido: {porcentaje_deposito!r} (0 a 0.5).")
        self._categoria, self._deposito = str(categoria), float(porcentaje_deposito)
        EntidadFJ.__init__(self)

    def validar_parametros(self, horas) -> None:
        """Se alquila de 1 a 96 horas (hasta 4 días)."""
        if not _es_numero(horas) or not 1 <= horas <= 96:
            raise ServicioError(f"Equipo '{self.nombre}': se alquila de 1 a 96 horas, no {horas!r}.")

    def costo_base(self, horas: float) -> float:
        """Valor del alquiler más el depósito."""
        alquiler = self._tarifa_hora * horas
        return alquiler * (1 + self._deposito)

    def resumen(self) -> str:
        """Descripción del equipo."""
        return f"{self.codigo} · Equipo {self.nombre} [{self._categoria}] · ${self._tarifa_hora:,.0f}/h + {self._deposito:.0%} depósito"


class AsesoriaTecnica(Servicio):
    """Asesoría especializada: el nivel del consultor multiplica la tarifa."""

    NIVELES = {"basico": 1.0, "avanzado": 1.4, "experto": 1.9}

    def __init__(self, nombre=None, tarifa_hora=None, especialidad="software", nivel="basico") -> None:
        super().__init__(nombre, tarifa_hora)
        if nivel not in self.NIVELES:
            raise ServicioError(f"Nivel de consultor desconocido: {nivel!r}.")
        self._especialidad, self._nivel = str(especialidad), nivel
        EntidadFJ.__init__(self)

    def validar_parametros(self, horas) -> None:
        """Entre 0.5 y 6 horas, en bloques de media hora."""
        if not _es_numero(horas) or not 0.5 <= horas <= 6 or (horas * 2) != int(horas * 2):
            raise ServicioError(f"Asesoría '{self.nombre}': de 0.5 a 6 h en bloques de 0.5, no {horas!r}.")

    def costo_base(self, horas: float) -> float:
        """Tarifa × multiplicador del nivel × horas."""
        return self._tarifa_hora * self.NIVELES[self._nivel] * horas

    def resumen(self) -> str:
        """Descripción de la asesoría."""
        return f"{self.codigo} · Asesoría {self.nombre} ({self._especialidad}, {self._nivel}) · ${self._tarifa_hora:,.0f}/h"
