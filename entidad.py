"""Contrato abstracto de las entidades del sistema."""
from abc import ABC, abstractmethod

class Entidad(ABC):
    @abstractmethod
    def describir(self) -> str:
        """Producir una descripción pública de la entidad."""
