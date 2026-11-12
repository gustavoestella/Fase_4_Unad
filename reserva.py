"""Ciclo de vida de una reserva y restricciones de transición."""
from entidad import Entidad
from cliente import Cliente
from servicios import Servicio
from excepciones import ReservaInvalida, OperacionNoPermitida

class Reserva(Entidad):
    def __init__(self, codigo, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ReservaInvalida('Cliente y servicio deben ser objetos válidos')
        if not isinstance(codigo, str) or not codigo.strip():
            raise ReservaInvalida('Código de reserva obligatorio')
        self.duracion = servicio.validar(duracion)
        self.codigo = codigo.strip()
        self.cliente = cliente
        self.servicio = servicio
        self.estado = 'PENDIENTE'
        self.total = None

    def procesar(self, impuesto=0, descuento=0):
        if self.estado != 'PENDIENTE':
            raise OperacionNoPermitida('Solo se procesan reservas pendientes')
        self.total = self.servicio.calcular_costo(self.duracion, impuesto, descuento)
        return self.total

    def confirmar(self):
        if self.estado != 'PENDIENTE' or self.total is None:
            raise OperacionNoPermitida('Primero debe procesarse una reserva pendiente')
        self.estado = 'CONFIRMADA'

    def cancelar(self):
        if self.estado == 'CANCELADA':
            raise OperacionNoPermitida('La reserva ya fue cancelada')
        self.estado = 'CANCELADA'

    def describir(self):
        return f'Reserva {self.codigo}: {self.cliente.nombre} / {self.servicio.nombre} / {self.estado}'
