
# sistema.py
# Administrador central del sistema Software FJ.

import logging

from clientes import Cliente
from servicios import Servicio
from reservas import Reserva
from excepciones import ClienteError, ServicioError, ReservaError, ValidacionError


class SistemaGestion:
    """Administra clientes, servicios y reservas del sistema."""

    def __init__(self):
        # Listas que almacenan los objetos registrados.
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

        # Logger para registrar eventos del sistema.
        self.logger = logging.getLogger("SoftwareFJ")

    def registrar_cliente(self, cliente):
        """Registra un cliente y evita documentos duplicados."""

        if not isinstance(cliente, Cliente):
            raise ValidacionError("El objeto ingresado no es un cliente valido.")

        for existente in self.__clientes:
            if existente.documento == cliente.documento:
                self.logger.warning("Intento de registrar cliente duplicado.")
                raise ClienteError("Ya existe un cliente con ese documento.")

            if existente.identificador == cliente.identificador:
                raise ClienteError("El identificador del cliente ya existe.")

        self.__clientes.append(cliente)
        self.logger.info("Cliente registrado: %s", cliente.nombre)

        return "Cliente registrado exitosamente."

    def registrar_servicio(self, servicio):
        """Registra un servicio en el sistema."""

        if not isinstance(servicio, Servicio):
            raise ValidacionError("El objeto ingresado no es un servicio valido.")

        for existente in self.__servicios:
            if existente.identificador == servicio.identificador:
                self.logger.warning("Intento de registrar servicio duplicado.")
                raise ServicioError("El identificador del servicio ya existe.")

        self.__servicios.append(servicio)
        self.logger.info("Servicio registrado: %s", servicio.nombre)

        return "Servicio registrado exitosamente."

    def buscar_cliente(self, documento):
        """Busca un cliente por su documento."""

        for cliente in self.__clientes:
            if cliente.documento == documento:
                return cliente

        raise ClienteError("No se encontro el cliente solicitado.")

    def buscar_servicio(self, identificador):
        """Busca un servicio por su identificador."""

        for servicio in self.__servicios:
            if servicio.identificador == identificador:
                return servicio

        raise ServicioError("No se encontro el servicio solicitado.")

    
    def crear_reserva(self, identificador, cliente, servicio, duracion):
        """Crea una reserva verificando clientes y servicios registrados."""

        # Buscar al cliente en la lista de clientes.
        cliente_encontrado = None

        for c in self.__clientes:
            if c.identificador == cliente.identificador:
                cliente_encontrado = c
                break

        # Buscar el servicio en la lista de servicios.
        servicio_encontrado = None

        for s in self.__servicios:
            if s.identificador == servicio.identificador:
                servicio_encontrado = s
                break

        # Verificar que el cliente exista.
        if cliente_encontrado is None:
            raise ReservaError("El cliente no se encuentra registrado.")

        # Verificar que el servicio exista.
        if servicio_encontrado is None:
            raise ReservaError("El servicio no se encuentra registrado.")

        # Verificar que el identificador de reserva no este duplicado.
        for existente in self.__reservas:
            if existente.identificador == identificador:
                raise ReservaError("Ya existe una reserva con ese identificador.")

        # Crear y almacenar la reserva.
        reserva = Reserva(
            identificador,
            cliente_encontrado,
            servicio_encontrado,
            duracion
        )

        self.__reservas.append(reserva)
        self.logger.info("Reserva creada: %s", identificador)

        return reserva


    def listar_clientes(self):
        """Retorna la lista de clientes registrados."""
        return list(self.__clientes)

    def listar_servicios(self):
        """Retorna la lista de servicios registrados."""
        return list(self.__servicios)

    def listar_reservas(self):
        """Retorna la lista de reservas creadas."""
        return list(self.__reservas)

    def mostrar_resumen(self):
        """Genera un resumen de los elementos almacenados."""

        return (
            f"Clientes registrados: {len(self.__clientes)} | "
            f"Servicios registrados: {len(self.__servicios)} | "
            f"Reservas creadas: {len(self.__reservas)}"
        )
