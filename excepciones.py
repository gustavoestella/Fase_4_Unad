"""Excepciones de dominio de Software FJ."""
class ErrorSistema(Exception):
    """Error recuperable del negocio."""
class DatoInvalido(ErrorSistema): pass
class ServicioNoDisponible(ErrorSistema): pass
class ReservaInvalida(ErrorSistema): pass
class OperacionNoPermitida(ErrorSistema): pass 
