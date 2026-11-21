
# reservas.py
# Gestion de reservas de Software FJ.

from entidades import Entidad
from clientes import Cliente
from servicios import Servicio
from excepciones import ReservaError, DisponibilidadError, ValidacionError


class Reserva(Entidad):
    """Representa una reserva de un cliente para un servicio."""

    ESTADOS_VALIDOS = ("Pendiente", "Confirmada", "Cancelada")

    def __init__(self, identificador, cliente, servicio, duracion):
        super().__init__(identificador)

        # Validar que el cliente sea una instancia de Cliente.
        if not isinstance(cliente, Cliente):
            raise ValidacionError("La reserva requiere un cliente valido.")

        # Validar que el servicio sea una instancia de Servicio.
        if not isinstance(servicio, Servicio):
            raise ValidacionError("La reserva requiere un servicio valido.")

        # Validar la duracion de la reserva.
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ReservaError("La duracion debe ser mayor que cero.")

        # Datos encapsulados de la reserva.
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    def confirmar(self):
        """Confirma una reserva que se encuentre pendiente."""

        if self.__estado == "Cancelada":
            raise DisponibilidadError(
                "No se puede confirmar una reserva cancelada."
            )

        if self.__estado == "Confirmada":
            raise ReservaError("La reserva ya se encuentra confirmada.")

        self.__estado = "Confirmada"
        return "Reserva confirmada exitosamente."

    def cancelar(self):
        """Cancela una reserva que no haya sido cancelada."""

        if self.__estado == "Cancelada":
            raise ReservaError("La reserva ya se encuentra cancelada.")

        self.__estado = "Cancelada"
        return "Reserva cancelada exitosamente."

    def calcular_total(self, descuento=0, impuesto=0.19):
        """Calcula el costo total usando el servicio asociado."""

        if self.__estado == "Cancelada":
            raise ReservaError(
                "No se puede calcular el costo de una reserva cancelada."
            )

        return self.__servicio.calcular_costo(
            self.__duracion,
            descuento,
            impuesto
        )

    def procesar(self):
        """Confirma la reserva y calcula su valor."""

        try:
            mensaje = self.confirmar()
            total = self.calcular_total()

            return {
                "mensaje": mensaje,
                "reserva": self.identificador,
                "cliente": self.__cliente.nombre,
                "servicio": self.__servicio.nombre,
                "duracion": self.__duracion,
                "estado": self.__estado,
                "total": total
            }

        except ReservaError:
            raise

        except Exception as error:
            raise ReservaError(
                "Ocurrio un error inesperado al procesar la reserva."
            ) from error

    def describir(self):
        """Devuelve informacion general de la reserva."""

        return (
            f"Reserva: {self.identificador} | "
            f"Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | "
            f"Duracion: {self.__duracion} | "
            f"Estado: {self.__estado}"
        )
