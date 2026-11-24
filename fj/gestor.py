"""Gestor central: guarda clientes, servicios y reservas en listas en memoria."""
from .bitacora import bitacora
from .catalogo import Servicio
from .clientes import Cliente
from .errores import ErrorFJ, ReservaError
from .reservas import Estado, Reserva


class GestorFJ:
    """Fachada para operar el sistema sin base de datos."""

    def __init__(self) -> None:
        """Inicia las tres colecciones vacías."""
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []

    def registrar_cliente(self, **datos) -> Cliente:
        """Crea un cliente con los datos dados y lo guarda."""
        cliente = Cliente(**datos)
        self._clientes.append(cliente)
        bitacora.info("Cliente registrado: %s", cliente.resumen())
        return cliente

    def registrar_servicio(self, clase, **datos) -> Servicio:
        """Crea un servicio de la clase indicada y lo guarda."""
        servicio = clase(**datos)
        self._servicios.append(servicio)
        bitacora.info("Servicio registrado: %s", servicio.resumen())
        return servicio

    def reservar(self, cliente, servicio, horas) -> Reserva:
        """Crea una reserva y la guarda."""
        reserva = Reserva(cliente, servicio, horas)
        self._reservas.append(reserva)
        bitacora.info("Reserva creada: %s", reserva.resumen())
        return reserva

    def buscar_reserva(self, codigo: str) -> Reserva:
        """Devuelve la reserva con ese código o lanza ReservaError."""
        for reserva in self._reservas:
            if reserva.codigo == codigo:
                return reserva
        raise ReservaError(f"No existe la reserva {codigo!r}.")

    @property
    def clientes(self) -> list:
        """Copia de la lista de clientes."""
        return list(self._clientes)

    @property
    def servicios(self) -> list:
        """Copia de la lista de servicios."""
        return list(self._servicios)

    def resumen_final(self) -> str:
        """Texto con totales por estado y recaudo de reservas procesadas."""
        por_estado = {e: 0 for e in Estado}
        recaudo = 0.0
        for r in self._reservas:
            por_estado[r.estado] += 1
            if r.estado is Estado.PROCESADA:
                recaudo += r.servicio.cotizar_para(r.horas, r.cliente)
        partes = ", ".join(f"{n} {e.value}(s)" for e, n in por_estado.items())
        return (f"{len(self._clientes)} clientes · {len(self._servicios)} servicios · "
                f"{len(self._reservas)} reservas ({partes}) · recaudo ${recaudo:,.2f}")
