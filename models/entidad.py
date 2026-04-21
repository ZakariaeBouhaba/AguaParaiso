# ============================================
# AguaParaíso - Clase base Entidad
# Sistema ERP SmartPark Pro
# ============================================

from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):
    """
    Clase base abstracta para todas las entidades del sistema AguaParaíso.
    
    Define los atributos comunes a todas las entidades: ID único y
    fecha de creación. Obliga a las subclases a implementar los
    métodos to_dict() y __str__() para garantizar la serialización
    y representación textual de cada entidad.
    
    Attributes:
        __id (int): Identificador único asignado por la base de datos.
        __fecha_creacion (str): Fecha y hora de creación del objeto.
    """

    def __init__(self):
        """Inicializa la entidad con ID None y fecha de creación actual."""
        self.__id = None
        self.__fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def id(self):
        """int: Identificador único de la entidad."""
        return self.__id

    @id.setter
    def id(self, valor):
        """
        Asigna el ID de la entidad con validación de tipo y valor.
        
        Args:
            valor (int | None): ID a asignar. Debe ser entero positivo o None.
            
        Raises:
            ValueError: Si el valor no es entero o es negativo.
        """
        if valor is not None and not isinstance(valor, int):
            raise ValueError("El ID debe ser un entero")
        if valor is not None and valor < 0:
            raise ValueError("El ID no puede ser negativo")
        self.__id = valor

    @property
    def fecha_creacion(self):
        """str: Fecha y hora de creación en formato YYYY-MM-DD HH:MM:SS."""
        return self.__fecha_creacion

    @abstractmethod
    def to_dict(self):
        """
        Convierte la entidad a diccionario para persistir en la base de datos.
        
        Returns:
            dict: Diccionario con los atributos de la entidad.
        """
        pass

    @abstractmethod
    def __str__(self):
        """
        Representación en texto de la entidad.
        
        Returns:
            str: Cadena descriptiva de la entidad.
        """
        pass

    def es_nuevo(self):
        """
        Comprueba si la entidad es nueva (sin ID asignado).
        
        Returns:
            bool: True si la entidad no tiene ID, False en caso contrario.
        """
        return self.__id is None