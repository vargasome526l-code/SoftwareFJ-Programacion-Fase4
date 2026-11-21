
# servicios.py
# Definicion de servicios ofrecidos por Software FJ.

from abc import ABC, abstractmethod
from entidades import Entidad
from excepciones import ServicioError, ValidacionError


class Servicio(Entidad, ABC):
    """Clase abstracta base para todos los servicios."""

    def __init__(self, identificador, nombre, tarifa_base):
        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValidacionError("El nombre del servicio es obligatorio.")

        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise ServicioError("La tarifa base debe ser mayor que cero.")

        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @abstractmethod
    def validar_parametros(self, **kwargs):
        """Valida los parametros especificos de cada servicio."""
        pass

    @abstractmethod
    def calcular_subtotal(self, duracion):
        """Calcula el costo base de cada servicio."""
        pass

    def calcular_costo(self, duracion, descuento=0, impuesto=0.19):
        """Calcula el costo con descuento opcional e impuesto."""

        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ServicioError("La duracion debe ser mayor que cero.")

        if not isinstance(descuento, (int, float)) or not 0 <= descuento <= 100:
            raise ServicioError("El descuento debe estar entre 0 y 100.")

        if not isinstance(impuesto, (int, float)) or not 0 <= impuesto <= 1:
            raise ServicioError("El impuesto debe estar entre 0 y 1.")

        subtotal = self.calcular_subtotal(duracion)
        valor_descuento = subtotal * (descuento / 100)
        subtotal_con_descuento = subtotal - valor_descuento
        total = subtotal_con_descuento * (1 + impuesto)

        return round(total, 2)

    def describir(self):
        return f"Servicio: {self._nombre} | Tarifa base: ${self._tarifa_base:,.2f}"


class ReservaSala(Servicio):
    """Servicio de reserva de salas por hora."""

    def __init__(self, identificador, tarifa_base, capacidad):
        super().__init__(identificador, "Reserva de sala", tarifa_base)
        self.capacidad = capacidad
        self.validar_parametros(capacidad=capacidad)

    def validar_parametros(self, **kwargs):
        capacidad = kwargs.get("capacidad")

        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioError("La capacidad de la sala debe ser un entero positivo.")

    def calcular_subtotal(self, duracion):
        return self.tarifa_base * duracion

    def describir(self):
        return f"{super().describir()} | Capacidad: {self.capacidad} personas"


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos por dia."""

    def __init__(self, identificador, tarifa_base, equipo, unidades=1):
        super().__init__(identificador, "Alquiler de equipo", tarifa_base)
        self.equipo = equipo
        self.unidades = unidades
        self.validar_parametros(equipo=equipo, unidades=unidades)

    def validar_parametros(self, **kwargs):
        equipo = kwargs.get("equipo")
        unidades = kwargs.get("unidades")

        if not isinstance(equipo, str) or not equipo.strip():
            raise ServicioError("Debe especificar el equipo que se alquilara.")

        if not isinstance(unidades, int) or unidades <= 0:
            raise ServicioError("Las unidades deben ser un entero positivo.")

    def calcular_subtotal(self, duracion):
        return self.tarifa_base * duracion * self.unidades

    def describir(self):
        return f"{super().describir()} | Equipo: {self.equipo} | Unidades: {self.unidades}"


class Asesoria(Servicio):
    """Servicio de asesoria especializada por hora."""

    def __init__(self, identificador, tarifa_base, especialidad):
        super().__init__(identificador, "Asesoria especializada", tarifa_base)
        self.especialidad = especialidad
        self.validar_parametros(especialidad=especialidad)

    def validar_parametros(self, **kwargs):
        especialidad = kwargs.get("especialidad")

        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ServicioError("Debe especificar la especialidad de la asesoria.")

    def calcular_subtotal(self, duracion):
        return self.tarifa_base * duracion

    def describir(self):
        return f"{super().describir()} | Especialidad: {self.especialidad}"
