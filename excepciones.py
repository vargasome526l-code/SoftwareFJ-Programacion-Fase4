
# excepciones.py
# Excepciones personalizadas para el sistema Software FJ.


class ErrorSoftwareFJ(Exception):
    """Clase base para los errores propios del sistema."""
    pass


class ValidacionError(ErrorSoftwareFJ):
    """Error cuando un dato no cumple las validaciones."""
    pass


class ClienteError(ErrorSoftwareFJ):
    """Error relacionado con la gestion de clientes."""
    pass


class ServicioError(ErrorSoftwareFJ):
    """Error relacionado con los servicios."""
    pass


class ReservaError(ErrorSoftwareFJ):
    """Error relacionado con las reservas."""
    pass


class DisponibilidadError(ReservaError):
    """Error cuando un servicio no esta disponible."""
    pass
