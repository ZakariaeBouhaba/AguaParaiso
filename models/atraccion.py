# ============================================
# AguaParaíso - Clase Atraccion y subclases
# Sistema ERP SmartPark Pro
# ============================================

from abc import abstractmethod
from models.entidad import Entidad
from exceptions.exceptions import AforoCompletoError, ZonaCerradaError


class Atraccion(Entidad):
    """
    Clase base abstracta para todas las atracciones del parque.
    
    Define los atributos y comportamientos comunes a todas las
    atracciones. Las subclases concretas implementan los detalles
    específicos de cada tipo de atracción.
    
    Attributes:
        __nombre (str): Nombre de la atracción.
        __tipo (str): Tipo de atracción (Adrenalina, Familia, Relax, Infantil).
        __altura_minima (float): Altura mínima requerida en metros.
        __aforo_maximo (int): Capacidad máxima de personas.
        __estado (str): Estado operativo (Activa, Cerrada, Mantenimiento).
        __id_zona (int): ID de la zona a la que pertenece.
    """

    TIPOS_VALIDOS = ['Adrenalina', 'Familia', 'Relax', 'Infantil']
    ESTADOS_VALIDOS = ['Activa', 'Cerrada', 'Mantenimiento']

    def __init__(self, nombre, tipo, altura_minima, aforo_maximo, id_zona):
        """
        Inicializa una atracción con estado Activa.
        
        Args:
            nombre (str): Nombre de la atracción.
            tipo (str): Tipo de atracción. Debe estar en TIPOS_VALIDOS.
            altura_minima (float): Altura mínima requerida en metros.
            aforo_maximo (int): Capacidad máxima de personas.
            id_zona (int): ID de la zona a la que pertenece.
            
        Raises:
            ValueError: Si el tipo no es válido o la altura es negativa.
        """
        super().__init__()
        self.__nombre = nombre
        self.__tipo = self.__validar_tipo(tipo)
        self.__altura_minima = self.__validar_altura(altura_minima)
        self.__aforo_maximo = aforo_maximo
        self.__estado = 'Activa'
        self.__id_zona = id_zona

    @property
    def nombre(self):
        """str: Nombre de la atracción."""
        return self.__nombre

    @property
    def tipo(self):
        """str: Tipo de atracción."""
        return self.__tipo

    @property
    def altura_minima(self):
        """float: Altura mínima requerida en metros."""
        return self.__altura_minima

    @property
    def aforo_maximo(self):
        """int: Capacidad máxima de personas."""
        return self.__aforo_maximo

    @property
    def estado(self):
        """str: Estado operativo de la atracción."""
        return self.__estado

    @estado.setter
    def estado(self, valor):
        """
        Asigna el estado de la atracción con validación.
        
        Args:
            valor (str): Nuevo estado. Debe estar en ESTADOS_VALIDOS.
            
        Raises:
            ValueError: Si el estado no es válido.
        """
        if valor not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: {valor}")
        self.__estado = valor

    @property
    def id_zona(self):
        """int: ID de la zona a la que pertenece la atracción."""
        return self.__id_zona

    def __validar_tipo(self, tipo):
        """
        Valida que el tipo de atracción sea válido.
        
        Args:
            tipo (str): Tipo a validar.
            
        Returns:
            str: Tipo validado.
            
        Raises:
            ValueError: Si el tipo no está en TIPOS_VALIDOS.
        """
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo inválido: {tipo}")
        return tipo

    def __validar_altura(self, altura):
        """
        Valida que la altura mínima no sea negativa.
        
        Args:
            altura (float): Altura a validar en metros.
            
        Returns:
            float: Altura validada.
            
        Raises:
            ValueError: Si la altura es negativa.
        """
        if altura < 0:
            raise ValueError("La altura mínima no puede ser negativa")
        return altura

    def esta_disponible(self):
        """
        Comprueba si la atracción está operativa.
        
        Returns:
            bool: True si el estado es Activa.
        """
        return self.__estado == 'Activa'

    @abstractmethod
    def to_dict(self):
        """
        Convierte la atracción a diccionario para persistir en la BD.
        
        Returns:
            dict: Diccionario con los atributos de la atracción.
        """
        pass

    @abstractmethod
    def __str__(self):
        """
        Representación textual de la atracción.
        
        Returns:
            str: Cadena descriptiva de la atracción.
        """
        pass


class AtraccionTobogan(Atraccion):
    """
    Tobogán acuático con velocidad máxima y altura mínima requerida.
    
    Attributes:
        __velocidad_max (float): Velocidad máxima en km/h.
    """

    def __init__(self, nombre, tipo, altura_minima, aforo_maximo, id_zona, velocidad_max):
        """
        Inicializa un tobogán con su velocidad máxima.
        
        Args:
            nombre (str): Nombre del tobogán.
            tipo (str): Tipo de atracción.
            altura_minima (float): Altura mínima requerida en metros.
            aforo_maximo (int): Capacidad máxima.
            id_zona (int): ID de la zona.
            velocidad_max (float): Velocidad máxima en km/h.
        """
        super().__init__(nombre, tipo, altura_minima, aforo_maximo, id_zona)
        self.__velocidad_max = velocidad_max

    @property
    def velocidad_max(self):
        """float: Velocidad máxima del tobogán en km/h."""
        return self.__velocidad_max

    def to_dict(self):
        """
        Convierte el tobogán a diccionario.
        
        Returns:
            dict: Diccionario con atributos del tobogán.
        """
        return {
            'nombre': self.nombre,
            'tipo': self.tipo,
            'altura_minima': self.altura_minima,
            'aforo_maximo': self.aforo_maximo,
            'estado': self.estado,
            'id_zona': self.id_zona,
            'velocidad_max': self.__velocidad_max
        }

    def __str__(self):
        """
        Representación textual del tobogán.
        
        Returns:
            str: Cadena con nombre, tipo, altura mínima, velocidad y estado.
        """
        return (f"Tobogán: {self.nombre} | Tipo: {self.tipo} | "
                f"Altura mín: {self.altura_minima}m | "
                f"Velocidad máx: {self.__velocidad_max}km/h | "
                f"Estado: {self.estado}")


class AtraccionPiscina(Atraccion):
    """
    Piscina acuática con control de temperatura y sistema de olas.
    
    Attributes:
        __temperatura (float): Temperatura del agua en grados Celsius.
        __olas_activas (bool): Indica si el sistema de olas está activado.
    """

    def __init__(self, nombre, tipo, altura_minima, aforo_maximo, id_zona, temperatura=26.0):
        """
        Inicializa una piscina con temperatura y olas desactivadas.
        
        Args:
            nombre (str): Nombre de la piscina.
            tipo (str): Tipo de atracción.
            altura_minima (float): Altura mínima requerida.
            aforo_maximo (int): Capacidad máxima.
            id_zona (int): ID de la zona.
            temperatura (float): Temperatura inicial del agua en °C.
        """
        super().__init__(nombre, tipo, altura_minima, aforo_maximo, id_zona)
        self.__temperatura = temperatura
        self.__olas_activas = False

    @property
    def temperatura(self):
        """float: Temperatura actual del agua en grados Celsius."""
        return self.__temperatura

    @temperatura.setter
    def temperatura(self, valor):
        """
        Asigna la temperatura del agua con validación de rango seguro.
        
        Args:
            valor (float): Nueva temperatura en °C. Rango: 18.0 - 32.0.
            
        Raises:
            TemperaturaInvalidaError: Si la temperatura está fuera del rango.
        """
        if valor < 18.0 or valor > 32.0:
            from exceptions.exceptions import TemperaturaInvalidaError
            raise TemperaturaInvalidaError(valor)
        self.__temperatura = valor

    @property
    def olas_activas(self):
        """bool: True si el sistema de olas está activado."""
        return self.__olas_activas

    def activar_olas(self):
        """Activa el sistema de olas de la piscina."""
        self.__olas_activas = True

    def desactivar_olas(self):
        """Desactiva el sistema de olas de la piscina."""
        self.__olas_activas = False

    def to_dict(self):
        """
        Convierte la piscina a diccionario.
        
        Returns:
            dict: Diccionario con atributos de la piscina.
        """
        return {
            'nombre': self.nombre,
            'tipo': self.tipo,
            'altura_minima': self.altura_minima,
            'aforo_maximo': self.aforo_maximo,
            'estado': self.estado,
            'id_zona': self.id_zona,
            'temperatura': self.__temperatura,
            'olas_activas': self.__olas_activas
        }

    def __str__(self):
        """
        Representación textual de la piscina.
        
        Returns:
            str: Cadena con nombre, tipo, temperatura, olas y estado.
        """
        return (f"Piscina: {self.nombre} | Tipo: {self.tipo} | "
                f"Temperatura: {self.__temperatura}°C | "
                f"Olas: {'Sí' if self.__olas_activas else 'No'} | "
                f"Estado: {self.estado}")


class AtraccionRio(Atraccion):
    """
    Río lento con gestión de flotadores disponibles.
    
    Attributes:
        __num_flotadores (int): Número total de flotadores.
        __flotadores_disponibles (int): Flotadores disponibles para alquilar.
    """

    def __init__(self, nombre, tipo, altura_minima, aforo_maximo, id_zona, num_flotadores):
        """
        Inicializa un río lento con todos sus flotadores disponibles.
        
        Args:
            nombre (str): Nombre del río.
            tipo (str): Tipo de atracción.
            altura_minima (float): Altura mínima requerida.
            aforo_maximo (int): Capacidad máxima.
            id_zona (int): ID de la zona.
            num_flotadores (int): Número total de flotadores disponibles.
        """
        super().__init__(nombre, tipo, altura_minima, aforo_maximo, id_zona)
        self.__num_flotadores = num_flotadores
        self.__flotadores_disponibles = num_flotadores

    @property
    def flotadores_disponibles(self):
        """int: Número de flotadores disponibles para alquilar."""
        return self.__flotadores_disponibles

    def alquilar_flotador(self):
        """
        Alquila un flotador reduciendo el stock disponible en 1.
        
        Raises:
            StockInsuficienteError: Si no hay flotadores disponibles.
        """
        if self.__flotadores_disponibles <= 0:
            from exceptions.exceptions import StockInsuficienteError
            raise StockInsuficienteError('Flotadores', 0, 1)
        self.__flotadores_disponibles -= 1

    def devolver_flotador(self):
        """Devuelve un flotador incrementando el stock disponible en 1."""
        if self.__flotadores_disponibles < self.__num_flotadores:
            self.__flotadores_disponibles += 1

    def to_dict(self):
        """
        Convierte el río a diccionario.
        
        Returns:
            dict: Diccionario con atributos del río lento.
        """
        return {
            'nombre': self.nombre,
            'tipo': self.tipo,
            'altura_minima': self.altura_minima,
            'aforo_maximo': self.aforo_maximo,
            'estado': self.estado,
            'id_zona': self.id_zona,
            'num_flotadores': self.__num_flotadores,
            'flotadores_disponibles': self.__flotadores_disponibles
        }

    def __str__(self):
        """
        Representación textual del río lento.
        
        Returns:
            str: Cadena con nombre, tipo, flotadores y estado.
        """
        return (f"Río: {self.nombre} | Tipo: {self.tipo} | "
                f"Flotadores: {self.__flotadores_disponibles}/{self.__num_flotadores} | "
                f"Estado: {self.estado}")