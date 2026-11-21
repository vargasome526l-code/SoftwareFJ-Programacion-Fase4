
# main.py
# Punto de entrada y pruebas del sistema Software FJ.

import logging
import os

from clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from sistema import SistemaGestion
from excepciones import ValidacionError, ClienteError, ServicioError, ReservaError


# Crear carpeta de registros.
os.makedirs("logs", exist_ok=True)

# Configurar registro de eventos y errores.
logging.basicConfig(
    filename="logs/sistema.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger("SoftwareFJ")

# Crear el sistema.
sistema = SistemaGestion()

print("=" * 55)
print(" SISTEMA INTEGRAL DE GESTION - SOFTWARE FJ")
print("=" * 55)


def ejecutar_operacion(numero, descripcion, funcion):
    """Ejecuta una operacion controlando los posibles errores."""

    print(f"\nOperacion {numero}: {descripcion}")

    try:
        resultado = funcion()
        print(f"[OK] {resultado}")
        logger.info("Operacion %s exitosa: %s", numero, descripcion)

    except Exception as error:
        print(f"[ERROR CONTROLADO] {error}")
        logger.error(
            "Operacion %s fallida: %s | Error: %s",
            numero,
            descripcion,
            error
        )


# --------------------------------------------------
# PRUEBA 1: Registrar un cliente valido.
# --------------------------------------------------

cliente1 = Cliente(
    "C001",
    "Carlos Perez",
    "12345678",
    "carlos@email.com",
    "3001234567"
)

ejecutar_operacion(
    1,
    "Registro de cliente valido",
    lambda: sistema.registrar_cliente(cliente1)
)


# --------------------------------------------------
# PRUEBA 2: Intentar registrar un cliente invalido.
# --------------------------------------------------

def registrar_cliente_invalido():
    cliente = Cliente(
        "C002",
        "",
        "87654321",
        "invalido",
        "3007654321"
    )
    return sistema.registrar_cliente(cliente)

ejecutar_operacion(
    2,
    "Registro de cliente con datos invalidos",
    registrar_cliente_invalido
)


# --------------------------------------------------
# PRUEBA 3: Intentar registrar un cliente duplicado.
# --------------------------------------------------

cliente_duplicado = Cliente(
    "C003",
    "Carlos Perez Otro",
    "12345678",
    "otro@email.com",
    "3011111111"
)

ejecutar_operacion(
    3,
    "Registro de cliente con documento duplicado",
    lambda: sistema.registrar_cliente(cliente_duplicado)
)


# --------------------------------------------------
# PRUEBA 4: Registrar un servicio de reserva de sala.
# --------------------------------------------------

servicio1 = ReservaSala("S001", 50000, 10)

ejecutar_operacion(
    4,
    "Registro de servicio de reserva de sala",
    lambda: sistema.registrar_servicio(servicio1)
)


# --------------------------------------------------
# PRUEBA 5: Registrar alquiler de equipos.
# --------------------------------------------------

servicio2 = AlquilerEquipo(
    "S002",
    30000,
    "Computador portatil",
    2
)

ejecutar_operacion(
    5,
    "Registro de servicio de alquiler de equipos",
    lambda: sistema.registrar_servicio(servicio2)
)


# --------------------------------------------------
# PRUEBA 6: Registrar asesoria especializada.
# --------------------------------------------------

servicio3 = Asesoria("S003", 80000, "Desarrollo de software")

ejecutar_operacion(
    6,
    "Registro de servicio de asesoria",
    lambda: sistema.registrar_servicio(servicio3)
)


# --------------------------------------------------
# PRUEBA 7: Crear servicio con tarifa invalida.
# --------------------------------------------------

def crear_servicio_invalido():
    return ReservaSala("S004", -1000, 5)

ejecutar_operacion(
    7,
    "Creacion de servicio con tarifa negativa",
    crear_servicio_invalido
)


# --------------------------------------------------
# PRUEBA 8: Crear y procesar reserva correctamente.
# --------------------------------------------------

def crear_y_procesar_reserva():
    reserva = sistema.crear_reserva(
        "R001",
        cliente1,
        servicio1,
        2
    )

    resultado = reserva.procesar()

    return (
        f"{resultado['mensaje']} | "
        f"Total: ${resultado['total']:,.2f}"
    )

ejecutar_operacion(
    8,
    "Creacion y procesamiento de reserva valida",
    crear_y_procesar_reserva
)


# --------------------------------------------------
# PRUEBA 9: Crear reserva con cliente no registrado.
# --------------------------------------------------

def reserva_cliente_no_registrado():
    cliente_temporal = Cliente(
        "C099",
        "Cliente Temporal",
        "99999999",
        "temporal@email.com",
        "3009999999"
    )

    return sistema.crear_reserva(
        "R002",
        cliente_temporal,
        servicio1,
        1
    )

ejecutar_operacion(
    9,
    "Reserva con cliente no registrado",
    reserva_cliente_no_registrado
)


# --------------------------------------------------
# PRUEBA 10: Cancelar reserva e intentar calcular costo.
# --------------------------------------------------

def cancelar_y_calcular():
    reserva = sistema.crear_reserva(
        "R003",
        cliente1,
        servicio2,
        1
    )

    reserva.cancelar()

    return reserva.calcular_total()

ejecutar_operacion(
    10,
    "Cancelar reserva e intentar calcular su costo",
    cancelar_y_calcular
)


# --------------------------------------------------
# RESUMEN FINAL DEL SISTEMA.
# --------------------------------------------------

print("\n" + "=" * 55)
print(" RESUMEN FINAL")
print("=" * 55)

print(f"Clientes registrados: {len(sistema.listar_clientes())}")
print(f"Servicios registrados: {len(sistema.listar_servicios())}")
print(f"Reservas creadas: {len(sistema.listar_reservas())}")

print("\nTodas las operaciones finalizaron.")
print("El sistema sigue funcionando a pesar de los errores controlados.")
print("Consulte logs/sistema.log para ver el registro de eventos.")
print("=" * 55)
