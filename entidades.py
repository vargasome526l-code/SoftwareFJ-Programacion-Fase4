
# entidades.py
# Define la clase abstracta base para las entidades del sistema.

from abc import ABC, abstractmethod


class Entidad(ABC):
    """Clase abstracta que representa una entidad general del sistema."""

    def __init__(self, identificador):
        # Encapsulamos el identificador de la entidad.
        self._identificador = identificador

    @property
    def identificador(self):
        """Permite consultar el identificador sin modificarlo directamente."""
        return self._identificador

    @abstractmethod
    def describir(self):
        """Método abstracto que cada entidad debe implementar."""
        pass
