# ============================================
# AguaParaíso - Clase Visitante
# Sistema ERP SmartPark Pro
# ============================================

from models.entidad import Entidad
from datetime import datetime


class Visitante(Entidad):
    """
    Representa un visitante del parque AguaParaíso.
    
    Registra los datos del visitante y su fecha de visita
    para su posterior análisis en el módulo de reporting.
    
    Attributes:
        __nombre (str): Nombre completo del visitante.
        __tipo (str): Tipo de visitante (Adulto, Nino, Residente).
        __fecha_visita (str): Fecha y hora de entrada al parque.
        __id_ticket (int): ID del ticket asociado al visitante.
    """

    TIPOS_VALIDOS = ['Adulto', 'Nino', 'Residente']

    def __init__(self, nombre, tipo):
        """
        Inicializa un visitante con fecha de visita actual.
        
        Args:
            nombre (str): Nombre completo del visitante.
            tipo (str): Tipo de visitante. Debe estar en TIPOS_VALIDOS.
            
        Raises:
            ValueError: Si el tipo no es válido.
        """
        super().__init__()
        self.__nombre = nombre
        self.__tipo = self.__validar_tipo(tipo)
        self.__fecha_visita = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__id_ticket = None

    def __validar_tipo(self, tipo):
        """
        Valida que el tipo de visitante sea válido.
        
        Args:
            tipo (str): Tipo a validar.
            
        Returns:
            str: Tipo validado.
            
        Raises:
            ValueError: Si el tipo no está en TIPOS_VALIDOS.
        """
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de visitante inválido: {tipo}")
        return tipo

    @property
    def nombre(self):
        """str: Nombre completo del visitante."""
        return self.__nombre

    @property
    def tipo(self):
        """str: Tipo de visitante."""
        return self.__tipo

    @property
    def fecha_visita(self):
        """str: Fecha y hora de entrada al parque."""
        return self.__fecha_visita

    @property
    def id_ticket(self):
        """int: ID del ticket asociado al visitante."""
        return self.__id_ticket

    @id_ticket.setter
    def id_ticket(self, valor):
        """
        Asigna el ID del ticket al visitante.
        
        Args:
            valor (int): ID del ticket a asociar.
        """
        self.__id_ticket = valor

    def to_dict(self):
        """
        Convierte el visitante a diccionario para persistir en la BD.
        
        Returns:
            dict: Diccionario con todos los atributos del visitante.
        """
        return {
            'nombre': self.__nombre,
            'tipo': self.__tipo,
            'fecha_visita': self.__fecha_visita,
            'id_ticket': self.__id_ticket
        }

    def __str__(self):
        """
        Representación textual del visitante.
        
        Returns:
            str: Cadena con nombre, tipo y fecha de visita.
        """
        return (f"Visitante: {self.__nombre} | "
                f"Tipo: {self.__tipo} | "
                f"Fecha: {self.__fecha_visita}")