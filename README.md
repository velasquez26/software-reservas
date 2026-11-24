# Software FJ · Sistema de reservas

Proyecto individual de **Programación (213023) – UNAD, Fase 4**.
Autor: *TU NOMBRE AQUÍ*

Aplicación en Python orientada a objetos, **sin base de datos**, que gestiona clientes,
servicios y reservas de Software FJ y sigue funcionando aunque ocurran errores.

## Ejecutar

    py main.py          (Windows)
    python3 main.py     (Mac / Linux)

Los eventos y errores quedan en `logs/bitacora_fj.log`.

## Estructura

| Archivo | Contenido |
|---|---|
| `main.py` | Simulación de 17 pasos (válidos e inválidos) |
| `fj/errores.py` | Jerarquía de excepciones propias (`ErrorFJ` y 7 hijas) |
| `fj/bitacora.py` | Configuración del archivo de log |
| `fj/base.py` | Clase abstracta `EntidadFJ` (códigos CLI-001, SRV-001, RES-001) |
| `fj/clientes.py` | `Cliente` con atributos privados, validaciones y categoría regular/premium |
| `fj/catalogo.py` | `Servicio` (abstracta) + `SalaReuniones`, `AlquilerEquipo`, `AsesoriaTecnica` |
| `fj/reservas.py` | `Reserva` con estados, historial, confirmar/cancelar/procesar |
| `fj/gestor.py` | `GestorFJ`: listas en memoria y resumen final |

## Conceptos aplicados

- **Abstracción:** `EntidadFJ` y `Servicio` son clases abstractas.
- **Herencia y polimorfismo:** cada servicio sobrescribe `validar_parametros`, `costo_base` y `resumen`.
- **Encapsulación:** datos del cliente privados, con *setters* que validan.
- **Sobrecarga (simulada):** `cotizar()` con parámetros opcionales, `cotizar_con_iva()` y `cotizar_para()`.
- **Excepciones:** personalizadas, `try/except/else/finally` y encadenamiento con `raise ... from`.
