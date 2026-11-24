# Software FJ - Sistema de Gestión de Clientes, Servicios y Reservas

Proyecto de Programación (213023, UNAD) - Fase 4. POO + manejo avanzado de excepciones, sin base de datos.

## Ejecutar
    python main.py

Los errores y eventos se registran en `logs/eventos.log`.

## Archivos
| Archivo | Contenido |
|---|---|
| excepciones.py | Excepciones personalizadas |
| logger.py | Configuración del log |
| entidades.py | Clase abstracta `EntidadBase` |
| cliente.py | `Cliente` con validaciones y encapsulación |
| servicios.py | `Servicio` (abstracta) + `SalaReserva`, `AlquilerEquipo`, `Asesoria` |
| reserva.py | `Reserva` (confirmar, cancelar, procesar) |
| main.py | 15 operaciones simuladas (válidas e inválidas) |
