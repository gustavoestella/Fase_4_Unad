"""Simulación controlada de operaciones válidas e inválidas para la UNAD."""
from datetime import datetime
from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reserva import Reserva
from excepciones import ErrorSistema, DatoInvalido
from registro_logs import logger

clientes, servicios, reservas = [], [], []


def ejecutar(numero, titulo, accion):
    """Capturar errores y continuar con la siguiente operación."""
    print(f'\nOPERACIÓN {numero:02d}: {titulo}')
    try:
        resultado = accion()
    except ErrorSistema as error:
        print(f'ERROR CONTROLADO: {error}')
        logger.error('Operación %s: %s', numero, error, exc_info=True)
    except Exception:
        print('ERROR INESPERADO: consultar sistema.log')
        logger.exception('Error inesperado en operación %s', numero)
    else:
        print(f'CORRECTO: {resultado}')
        logger.info('Operación %s completada: %s', numero, titulo)
    finally:
        print(f'FIN DE OPERACIÓN {numero:02d}')


def registrar_cliente(identificacion, nombre, correo):
    if any(c.identificacion == identificacion for c in clientes):
        raise DatoInvalido('La identificación ya está registrada')
    cliente = Cliente(identificacion, nombre, correo)
    clientes.append(cliente)
    return cliente.describir()


def registrar_servicio(servicio):
    if any(s.codigo == servicio.codigo for s in servicios):
        raise DatoInvalido('Código de servicio duplicado')
    servicios.append(servicio)
    return servicio.describir()


def crear_reserva(codigo, cliente, servicio, duracion, impuesto=0, descuento=0):
    if any(r.codigo == codigo for r in reservas):
        raise DatoInvalido('Código de reserva duplicado')
    reserva = Reserva(codigo, cliente, servicio, duracion)
    reserva.procesar(impuesto, descuento)
    reservas.append(reserva)
    reserva.confirmar()
    return f'{reserva.describir()} | Total ${reserva.total:,.2f}'


def demo():
    print('SOFTWARE FJ - SISTEMA DE CLIENTES, SERVICIOS Y RESERVAS')
    print('Fecha y hora:', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    ejecutar(1, 'Cliente válido', lambda: registrar_cliente('101', 'Ana Torres', 'ana@ejemplo.com'))
    ejecutar(2, 'Cliente con correo inválido', lambda: registrar_cliente('102', 'Luis Díaz', 'correo-invalido'))
    ejecutar(3, 'Segundo cliente válido', lambda: registrar_cliente('103', 'Sara Ríos', 'sara@ejemplo.com'))
    ejecutar(4, 'Cliente duplicado', lambda: registrar_cliente('101', 'Otro Nombre', 'otro@ejemplo.com'))
    ejecutar(5, 'Sala válida', lambda: registrar_servicio(ReservaSala('S01', 50000)))
    ejecutar(6, 'Equipo válido', lambda: registrar_servicio(AlquilerEquipo('E01', 30000)))
    ejecutar(7, 'Asesoría válida', lambda: registrar_servicio(Asesoria('A01', 80000)))
    ejecutar(8, 'Servicio con tarifa negativa', lambda: registrar_servicio(ReservaSala('S02', -1)))
    ejecutar(9, 'Reserva de sala exitosa', lambda: crear_reserva('R01', clientes[0], servicios[0], 2, impuesto=19))
    ejecutar(10, 'Reserva con duración inválida', lambda: crear_reserva('R02', clientes[0], servicios[1], -3))
    ejecutar(11, 'Reserva de asesoría con descuento', lambda: crear_reserva('R03', clientes[1], servicios[2], 3, descuento=10))
    ejecutar(12, 'Servicio no disponible', lambda: crear_reserva('R04', clientes[0], ReservaSala('S03', 45000, False), 1))
    ejecutar(13, 'Impuesto inconsistente', lambda: crear_reserva('R05', clientes[0], servicios[0], 1, impuesto=150))
    ejecutar(14, 'Cancelación válida', lambda: cancelar_reserva(reservas[0]))
    ejecutar(15, 'Cancelación repetida', lambda: cancelar_reserva(reservas[0]))
    print(f'\nRESUMEN: {len(clientes)} clientes, {len(servicios)} servicios, {len(reservas)} reservas creadas.')
    print('Los eventos y errores se guardaron en sistema.log')


def cancelar_reserva(reserva):
    reserva.cancelar()
    return reserva.describir()

if __name__ == '__main__':
    demo()
