"""Software FJ · simulación de 15 operaciones (válidas e inválidas).

Cada paso se ejecuta dentro de `paso()`, que captura cualquier error, lo
registra en logs/bitacora_fj.log y deja que el programa siga con el siguiente.
"""
from fj.bitacora import bitacora
from fj.catalogo import AlquilerEquipo, AsesoriaTecnica, SalaReuniones
from fj.errores import ErrorFJ
from fj.gestor import GestorFJ

fj = GestorFJ()
memoria = {}  # guarda objetos creados para usarlos en pasos posteriores


def paso(numero: int, titulo: str, accion) -> None:
    """Ejecuta una acción mostrando el resultado sin permitir que detenga el programa."""
    print(f"\n── Paso {numero:02d}: {titulo}")
    try:
        resultado = accion()
    except ErrorFJ as error:
        causa = f"  ⟵ causa: {error.__cause__}" if error.__cause__ else ""
        print(f"   ✗ Error controlado → {error}{causa}")
        bitacora.error("Paso %02d (%s): %s%s", numero, titulo, error, causa.replace("  ⟵ ", " | "))
    except Exception as error:  # fallo imprevisto: se registra y se sigue
        print(f"   ✗ Error inesperado → {error!r}")
        bitacora.critical("Paso %02d (%s) falló de forma inesperada: %r", numero, titulo, error)
    else:
        print(f"   ✓ {resultado}")
        bitacora.info("Paso %02d (%s) completado", numero, titulo)
    finally:
        bitacora.info("Paso %02d cerrado", numero)


def guardar(clave, objeto):
    """Guarda un objeto en `memoria` y lo devuelve (para encadenar en lambdas)."""
    memoria[clave] = objeto
    return objeto


def main() -> None:
    """Corre los 15 pasos de la simulación y muestra el resumen final."""
    bitacora.info("===== INICIO DE LA SIMULACIÓN =====")

    # ---- Clientes (2 válidos, 3 inválidos) ----
    paso(1, "Cliente válido (premium)", lambda: guardar("valentina", fj.registrar_cliente(
        nombre="valentina rojas", documento="1032456789", correo="vale.rojas@correo.co",
        telefono="3004567890", tipo="premium")))
    paso(2, "Cliente con documento con letras", lambda: fj.registrar_cliente(
        nombre="Andrés Mora", documento="10A45", correo="andres@correo.co", telefono="3112223344"))
    paso(3, "Cliente sin correo (dato ausente)", lambda: fj.registrar_cliente(
        nombre="Julián Cárdenas", documento="80123456", telefono="3201112233"))
    paso(4, "Cliente de categoría inexistente", lambda: fj.registrar_cliente(
        nombre="Marcela Ortiz", documento="52987654", correo="marce@correo.co",
        telefono="3159998877", tipo="vip"))
    paso(5, "Cliente regular válido", lambda: guardar("camilo", fj.registrar_cliente(
        nombre="Camilo Barrera", documento="79456123", correo="camilo.b@correo.co",
        telefono="6014445566")))

    # ---- Servicios (3 válidos, 2 inválidos) ----
    paso(6, "Sala con proyector", lambda: guardar("sala", fj.registrar_servicio(
        SalaReuniones, nombre="Magdalena", tarifa_hora=60000, aforo=12, con_proyector=True)))
    paso(7, "Equipo con depósito fuera de rango", lambda: fj.registrar_servicio(
        AlquilerEquipo, nombre="Servidor Rack", tarifa_hora=25000, porcentaje_deposito=0.9))
    paso(8, "Equipo válido", lambda: guardar("equipo", fj.registrar_servicio(
        AlquilerEquipo, nombre="Portátil Gamer", tarifa_hora=9000, categoria="cómputo")))
    paso(9, "Asesoría válida (nivel experto)", lambda: guardar("asesoria", fj.registrar_servicio(
        AsesoriaTecnica, nombre="Arquitectura de software", tarifa_hora=85000,
        especialidad="backend", nivel="experto")))
    paso(10, "Asesoría sin tarifa", lambda: fj.registrar_servicio(
        AsesoriaTecnica, nombre="Seguridad web", tarifa_hora=None))

    # ---- Reservas y cálculos ----
    paso(11, "Reserva correcta: sala 4 h para Valentina",
         lambda: guardar("r1", fj.reservar(memoria["valentina"], memoria["sala"], 4)).resumen())
    paso(12, "Reserva con duración inválida (asesoría de 7 h)",
         lambda: fj.reservar(memoria["camilo"], memoria["asesoria"], 7))

    def servicio_apagado():
        memoria["equipo"].habilitar(False)
        return fj.reservar(memoria["camilo"], memoria["equipo"], 24)
    paso(13, "Reserva de equipo no disponible", servicio_apagado)

    paso(14, "Procesar reserva RES-001 (IVA + descuento premium)",
         lambda: f"Total cobrado: ${memoria['r1'].procesar():,.2f} → {memoria['r1'].resumen()}")
    paso(15, "Cancelar una reserva ya procesada", lambda: memoria["r1"].cancelar())

    # ---- Extras de demostración (cálculo y sobrecarga) ----
    paso(16, "Cotización con descuento absurdo (150 %)",
         lambda: memoria["sala"].cotizar(3, impuesto=0.19, descuento=1.5))
    paso(17, "Variantes de cotizar() sobre la misma asesoría (2 h)", lambda: (
        f"base ${memoria['asesoria'].cotizar(2):,.0f} | con IVA ${memoria['asesoria'].cotizar_con_iva(2):,.0f} "
        f"| IVA+10% desc ${memoria['asesoria'].cotizar(2, 0.19, 0.10):,.0f}"))

    print("\n══════════════════════════════════════════════")
    print("RESUMEN:", fj.resumen_final())
    print("El programa terminó sin interrupciones. Detalle en logs/bitacora_fj.log")
    bitacora.info("===== FIN DE LA SIMULACIÓN =====")
    bitacora.info("RESUMEN: %s", fj.resumen_final())


if __name__ == "__main__":
    main()
