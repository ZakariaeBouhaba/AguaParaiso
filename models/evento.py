# ============================================
# AguaParaíso - Clase Evento
# Sistema ERP SmartPark Pro
# ============================================

from models.entidad import Entidad
from datetime import datetime


class Evento(Entidad):
    """
    Representa un evento aleatorio generado en el parque AguaParaíso.
    
    Los eventos son generados por el motor de eventos aleatorios
    basado en probabilidades configuradas en config.ini. Pueden ser
    de tipo Averia, Climatico, Sanitario, Stock o Aforo.
    
    Attributes:
        __tipo (str): Tipo de evento.
        __descripcion (str): Descripción detallada del evento.
        __id_zona (int): ID de la zona afectada (puede ser None si es global).
        __id_empleado (int): ID del empleado asignado a resolverlo.
        __estado (str): Estado del evento (Activo, Resuelto).
        __fecha_inicio (str): Fecha y hora de inicio del evento.
        __fecha_fin (str): Fecha y hora de resolución del evento.
    """

    TIPOS_VALIDOS = ['Averia', 'Climatico', 'Sanitario', 'Stock', 'Aforo']
    ESTADOS_VALIDOS = ['Activo', 'Resuelto']

    def __init__(self, tipo, descripcion, id_zona=None, id_empleado=None):
        """
        Inicializa un evento con estado Activo y fecha de inicio actual.
        
        Args:
            tipo (str): Tipo de evento. Debe estar en TIPOS_VALIDOS.
            descripcion (str): Descripción detallada del incidente.
            id_zona (int, optional): ID de la zona afectada.
            id_empleado (int, optional): ID del empleado asignado.
            
        Raises:
            ValueError: Si el tipo no está en TIPOS_VALIDOS.
        """
        super().__init__()
        self.__tipo = self.__validar_tipo(tipo)
        self.__descripcion = descripcion
        self.__id_zona = id_zona
        self.__id_empleado = id_empleado
        self.__estado = 'Activo'
        self.__fecha_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__fecha_fin = None

    def __validar_tipo(self, tipo):
        """
        Valida que el tipo de evento sea válido.
        
        Args:
            tipo (str): Tipo a validar.
            
        Returns:
            str: Tipo validado.
            
        Raises:
            ValueError: Si el tipo no está en TIPOS_VALIDOS.
        """
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de evento inválido: {tipo}")
        return tipo

    @property
    def tipo(self):
        """str: Tipo de evento."""
        return self.__tipo

    @property
    def descripcion(self):
        """str: Descripción detallada del evento."""
        return self.__descripcion

    @property
    def id_zona(self):
        """int: ID de la zona afectada o None si es global."""
        return self.__id_zona

    @property
    def id_empleado(self):
        """int: ID del empleado asignado a resolver el evento."""
        return self.__id_empleado

    @property
    def estado(self):
        """str: Estado actual del evento (Activo o Resuelto)."""
        return self.__estado

    @property
    def fecha_inicio(self):
        """str: Fecha y hora de inicio del evento."""
        return self.__fecha_inicio

    @property
    def fecha_fin(self):
        """str: Fecha y hora de resolución o None si sigue activo."""
        return self.__fecha_fin

    def resolver(self, id_empleado=None):
        """
        Marca el evento como resuelto registrando la fecha de fin.
        
        Args:
            id_empleado (int, optional): ID del empleado que resuelve el evento.
        """
        self.__estado = 'Resuelto'
        self.__fecha_fin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if id_empleado:
            self.__id_empleado = id_empleado

    def esta_activo(self):
        """
        Comprueba si el evento sigue activo.
        
        Returns:
            bool: True si el estado es Activo.
        """
        return self.__estado == 'Activo'

    def to_dict(self):
        """
        Convierte el evento a diccionario para persistir en la BD.
        
        Returns:
            dict: Diccionario con todos los atributos del evento.
        """
        return {
            'tipo': self.__tipo,
            'descripcion': self.__descripcion,
            'id_zona': self.__id_zona,
            'estado': self.__estado,
            'fecha_inicio': self.__fecha_inicio,
            'fecha_fin': self.__fecha_fin,
            'id_empleado': self.__id_empleado
        }

    def __str__(self):
        """
        Representación textual del evento.
        
        Returns:
            str: Cadena con tipo, estado y descripción.
        """
        return (f"Evento: {self.__tipo} | "
                f"Estado: {self.__estado} | "
                f"Descripción: {self.__descripcion}")