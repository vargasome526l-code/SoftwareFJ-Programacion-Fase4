
# clientes.py
# Gestion de clientes de Software FJ.

from entidades import Entidad
from excepciones import ValidacionError, ClienteError


class Cliente(Entidad):
    """Representa a un cliente registrado en el sistema."""

    def __init__(self, identificador, nombre, documento, correo, telefono):
        # Validamos los datos antes de crear el cliente.
        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValidacionError("El nombre no puede estar vacio.")

        if not isinstance(documento, str) or not documento.strip():
            raise ValidacionError("El documento es obligatorio.")

        if not isinstance(correo, str) or "@" not in correo or "." not in correo:
            raise ValidacionError("El correo ingresado no es valido.")

        if not isinstance(telefono, str) or not telefono.strip():
            raise ValidacionError("El telefono es obligatorio.")

        # Atributos encapsulados.
        self.__nombre = nombre.strip()
        self.__documento = documento.strip()
        self.__correo = correo.strip()
        self.__telefono = telefono.strip()

    @property
    def nombre(self):
        return self.__nombre

    @property
    def documento(self):
        return self.__documento

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def describir(self):
        """Devuelve una descripcion del cliente."""
        return (
            f"Cliente: {self.__nombre} | "
            f"Documento: {self.__documento} | "
            f"Correo: {self.__correo}"
        )

    def actualizar_correo(self, nuevo_correo):
        """Actualiza el correo si cumple con el formato basico."""
        if not isinstance(nuevo_correo, str) or "@" not in nuevo_correo or "." not in nuevo_correo:
            raise ClienteError("No se pudo actualizar: correo invalido.")

        self.__correo = nuevo_correo.strip()
