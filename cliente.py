"""Cliente con atributos encapsulados y validación."""
from entidad import Entidad
from excepciones import DatoInvalido

class Cliente(Entidad):
    def __init__(self, identificacion: str, nombre: str, correo: str):
       if not isinstance(identificacion, str) or not identificacion.strip():
    raise DatoInvalido('La identificación es obligatoria')

if not identificacion.strip().isdigit():
    raise DatoInvalido('La identificación debe contener únicamente números')
        if not isinstance(nombre, str) or len(nombre.strip()) < 2:
            raise DatoInvalido('El nombre debe tener al menos dos caracteres')
        if not isinstance(correo, str) or correo.count('@') != 1 or '.' not in correo.split('@')[-1]:
            raise DatoInvalido('Correo electrónico inválido')
        self.__identificacion = identificacion.strip()
        self.__nombre = nombre.strip()
        self.__correo = correo.strip()

    @property
    def identificacion(self):
        return self.__identificacion

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    def describir(self):
        return f'Cliente {self.__nombre} (ID {self.__identificacion})'
