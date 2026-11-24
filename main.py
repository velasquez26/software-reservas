"""Software FJ - Simulación de 12 operaciones (válidas e inválidas).

El programa NO se detiene ante errores: cada operación se ejecuta dentro de
una función que captura y registra la excepción en logs/eventos.log.
"""
from cliente import Cliente
from excepciones import SoftwareFJError
from logger import log
from reserva import Reserva
from servicios import Asesoria, AlquilerEquipo, SalaReserva

clientes, servicios, reservas = [], [], []  # "base de datos" en memoria (listas)


def ejecutar(numero, titulo, operacion):
    """Ejecuta una operación; si falla, registra el error y continúa."""
    print(f"\n[{numero:02d}] {titulo}")
    try:
        resultado = operacion()
    except SoftwareFJError as error:
        causa = f" (causa: {error.__cause__})" if error.__cause__ else ""
        print(f"     ✗ Error controlado: {error}{causa}")
        log.error("Operación %02d '%s' falló: %s%s", numero, titulo, error, causa)
    except Exception as error:  # error inesperado: tampoco detiene el sistema
        print(f"     ✗ Error inesperado: {error!r}")
        log.critical("Operación %02d error inesperado: %r", numero, error)
    else:
        print(f"     ✓ OK: {resultado}")
        log.info("Operación %02d '%s' exitosa", numero, titulo)
    finally:
        log.info("Operación %02d finalizada", numero)


def registrar_cliente(*args):
    c = Cliente(*args)
    clientes.append(c)
    return c.describir()


def registrar_servicio(clase, *args):
    s = clase(*args)
    servicios.append(s)
    return s.describir()


def crear_reserva(cliente, servicio, horas):
    r = Reserva(cliente, servicio, horas)
    reservas.append(r)
    return r.describir()


def main():
    log.info("=== Inicio de la simulación Software FJ ===")

    # --- Clientes ---
    ejecutar(1, "Registrar cliente válido",
             lambda: registrar_cliente("laura gómez", "laura@mail.com", "3101234567"))
    ejecutar(2, "Registrar cliente con correo inválido",
             lambda: registrar_cliente("Pedro Ruiz", "pedro-arroba-mail", "3109876543"))
    ejecutar(3, "Registrar cliente sin teléfono (parámetro faltante)",
             lambda: registrar_cliente("Ana Díaz", "ana@mail.com"))
    ejecutar(4, "Registrar segundo cliente válido",
             lambda: registrar_cliente("Carlos Pérez", "carlos@mail.com", "6012345678"))

    # --- Servicios ---
    ejecutar(5, "Crear sala válida", lambda: registrar_servicio(SalaReserva, "Sala Innovación", 50000, 12))
    ejecutar(6, "Crear equipo con tarifa negativa",
             lambda: registrar_servicio(AlquilerEquipo, "Portátil Pro", -100))
    ejecutar(7, "Crear asesoría válida", lambda: registrar_servicio(Asesoria, "Asesoría Python", 80000, "senior"))
    ejecutar(8, "Crear equipo válido", lambda: registrar_servicio(AlquilerEquipo, "Proyector HD", 15000, "proyector"))

    # --- Reservas ---
    ejecutar(9, "Reserva exitosa de sala (3 h)", lambda: crear_reserva(clientes[0], servicios[0], 3))
    ejecutar(10, "Reserva con duración inválida (20 h) -> excepción encadenada",
             lambda: crear_reserva(clientes[0], servicios[0], 20))

    def reserva_no_disponible():
        servicios[1].disponible = False  # la asesoría deja de estar disponible
        return crear_reserva(clientes[1], servicios[1], 2)
    ejecutar(11, "Reserva de servicio no disponible", reserva_no_disponible)

    ejecutar(12, "Procesar reserva con IVA y 10 % de descuento",
             lambda: f"Total ${reservas[0].procesar(0.19, 0.10):,.2f} | {reservas[0].describir()}")
    ejecutar(13, "Procesar de nuevo la misma reserva (operación no permitida)",
             lambda: reservas[0].procesar())
    ejecutar(14, "Cancelar reserva dos veces",
             lambda: (reservas[0].cancelar(), reservas[0].cancelar()))
    ejecutar(15, "Costo con descuento fuera de rango (cálculo inconsistente)",
             lambda: servicios[0].calcular_costo(2, 0.19, 1.5))

    print("\nResumen final:", len(clientes), "clientes,", len(servicios), "servicios,",
          len(reservas), "reservas.")
    print("El sistema siguió funcionando. Revisa logs/eventos.log")
    log.info("=== Fin de la simulación ===")


if __name__ == "__main__":
    main()
