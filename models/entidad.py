# ============================================
# AguaParaíso - Clase base Entidad
# Sistema ERP SmartPark Pro
# ============================================

from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):
    """Clase base abstracta para todas las entidades del sistema."""

    def __init__(self):
        self.__id = None
        self.__fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        if valor is not None and not isinstance(valor, int):
            raise ValueError("El ID debe ser un entero")
        if valor is not None and valor < 0:
            raise ValueError("El ID no puede ser negativo")
        self.__id = valor

    @property
    def fecha_creacion(self):
        return self.__fecha_creacion

    @abstractmethod
    def to_dict(self):
        """Convierte la entidad a diccionario para persistir en BD."""
        pass

    @abstractmethod
    def __str__(self):
        """Representación en texto de la entidad."""
        pass

    def es_nuevo(self):
        """Devuelve True si la entidad no tiene ID asignado todavía."""
        return self.__id is None