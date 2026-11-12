"""Servicios especializados; todos implementan el mismo contrato."""
from abc import abstractmethod
from decimal import Decimal, InvalidOperation
from entidad import Entidad
from excepciones import DatoInvalido, ServicioNoDisponible


def numero_positivo(valor, campo, permite_cero=False):
    """Convertir datos numéricos y encadenar errores de conversión."""
    try:
        n = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError) as error:
        raise DatoInvalido(f'{campo} debe ser numérico') from error
    if not n.is_finite() or (n < 0 if permite_cero else n <= 0):
        raise DatoInvalido(f'{campo} fuera de rango')
    return n

class Servicio(Entidad):
    def __init__(self, codigo, nombre, disponible=True):
        if not isinstance(codigo, str) or not codigo.strip():
            raise DatoInvalido('Código de servicio obligatorio')
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatoInvalido('Nombre de servicio obligatorio')
        if not isinstance(disponible, bool):
            raise DatoInvalido('Disponibilidad debe ser booleana')
        self.codigo = codigo.strip()
        self.nombre = nombre.strip()
        self.disponible = disponible

    def validar(self, duracion):
        if not self.disponible:
            raise ServicioNoDisponible(f'{self.nombre} no está disponible')
        return numero_positivo(duracion, 'Duración')

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        """Variantes de cálculo mediante parámetros opcionales."""

    def _total(self, subtotal, impuesto, descuento):
        tasa = numero_positivo(impuesto, 'Impuesto', permite_cero=True)
        rebaja = numero_positivo(descuento, 'Descuento', permite_cero=True)
        if tasa > 100 or rebaja > 100:
            raise DatoInvalido('Impuesto y descuento no pueden superar 100%')
        return (subtotal * (Decimal('1') - rebaja / 100) * (Decimal('1') + tasa / 100)).quantize(Decimal('0.01'))

    def describir(self):
        return f'{self.codigo}: {self.nombre}'

class ReservaSala(Servicio):
    def __init__(self, codigo, tarifa_hora, disponible=True):
        super().__init__(codigo, 'Reserva de sala', disponible)
        self.tarifa_hora = numero_positivo(tarifa_hora, 'Tarifa de sala')

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        return self._total(self.validar(duracion) * self.tarifa_hora, impuesto, descuento)

class AlquilerEquipo(Servicio):
    def __init__(self, codigo, tarifa_hora, disponible=True):
        super().__init__(codigo, 'Alquiler de equipo', disponible)
        self.tarifa_hora = numero_positivo(tarifa_hora, 'Tarifa de equipo')

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        return self._total(self.validar(duracion) * self.tarifa_hora, impuesto, descuento)

class Asesoria(Servicio):
    def __init__(self, codigo, tarifa_hora, disponible=True):
        super().__init__(codigo, 'Asesoría especializada', disponible)
        self.tarifa_hora = numero_positivo(tarifa_hora, 'Tarifa de asesoría')

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        return self._total(self.validar(duracion) * self.tarifa_hora, impuesto, descuento)
