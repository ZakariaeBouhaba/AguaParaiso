# ============================================
# AguaParaíso - Clase Ticket
# Sistema ERP SmartPark Pro
# ============================================

from models.entidad import Entidad
import uuid


class Ticket(Entidad):
    """
    Representa una entrada al parque AguaParaíso.
    
    Genera automáticamente un localizador único en formato
    AGP-YYYY-XXXXXXXX y calcula el precio total aplicando
    el IVA del 10% sobre el precio base.
    
    Attributes:
        __tipo (str): Tipo de ticket (Normal, Premium, TodoIncluido).
        __tipo_visitante (str): Tipo de visitante (Adulto, Nino, Residente).
        __id_empleado (int): ID del taquillero que vendió el ticket.
        __id_visitante (int): ID del visitante si está registrado.
        __fast_pass (bool): Indica si incluye acceso prioritario Fast Pass.
        __localizador (str): Código único de identificación del ticket.
        __precio_base (float): Precio sin IVA en euros.
        __precio_total (float): Precio final con IVA en euros.
    """

    TIPOS_VALIDOS = ['Normal', 'Premium', 'TodoIncluido']
    TIPOS_VISITANTE_VALIDOS = ['Adulto', 'Nino', 'Residente']
    IVA = 10.0

    PRECIOS = {
        'Normal': {'Adulto': 25.00, 'Nino': 15.00, 'Residente': 18.00},
        'Premium': {'Adulto': 45.00, 'Nino': 28.00, 'Residente': 35.00},
        'TodoIncluido': {'Adulto': 65.00, 'Nino': 40.00, 'Residente': 50.00},
    }

    PRECIO_FAST_PASS = 28.00

    def __init__(self, tipo, tipo_visitante, id_empleado, id_visitante=None, fast_pass=False):
        """
        Inicializa un ticket generando localizador y calculando precio.
        
        Args:
            tipo (str): Tipo de ticket. Debe estar en TIPOS_VALIDOS.
            tipo_visitante (str): Tipo de visitante. Debe estar en TIPOS_VISITANTE_VALIDOS.
            id_empleado (int): ID del taquillero que realiza la venta.
            id_visitante (int, optional): ID del visitante si está registrado.
            fast_pass (bool): True si incluye acceso prioritario (+28€).
            
        Raises:
            ValueError: Si el tipo de ticket o visitante no es válido.
        """
        super().__init__()
        self.__tipo = self.__validar_tipo(tipo)
        self.__tipo_visitante = self.__validar_tipo_visitante(tipo_visitante)
        self.__id_empleado = id_empleado
        self.__id_visitante = id_visitante
        self.__fast_pass = fast_pass
        self.__localizador = self.__generar_localizador()
        self.__precio_base = self.__calcular_precio_base()
        self.__precio_total = self.__calcular_precio_total()

    def __validar_tipo(self, tipo):
        """
        Valida que el tipo de ticket sea válido.
        
        Args:
            tipo (str): Tipo a validar.
            
        Returns:
            str: Tipo validado.
            
        Raises:
            ValueError: Si el tipo no está en TIPOS_VALIDOS.
        """
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de ticket inválido: {tipo}")
        return tipo

    def __validar_tipo_visitante(self, tipo):
        """
        Valida que el tipo de visitante sea válido.
        
        Args:
            tipo (str): Tipo de visitante a validar.
            
        Returns:
            str: Tipo validado.
            
        Raises:
            ValueError: Si el tipo no está en TIPOS_VISITANTE_VALIDOS.
        """
        if tipo not in self.TIPOS_VISITANTE_VALIDOS:
            raise ValueError(f"Tipo de visitante inválido: {tipo}")
        return tipo

    def __generar_localizador(self):
        """
        Genera un localizador único en formato AGP-YYYY-XXXXXXXX.
        
        Utiliza UUID4 para garantizar la unicidad del código.
        
        Returns:
            str: Localizador único del ticket.
        """
        from datetime import datetime
        anio = datetime.now().year
        codigo = str(uuid.uuid4())[:8].upper()
        return f"AGP-{anio}-{codigo}"

    def __calcular_precio_base(self):
        """
        Calcula el precio base según tipo de ticket y visitante.
        
        Añade el precio del Fast Pass si está incluido.
        
        Returns:
            float: Precio base sin IVA en euros.
        """
        base = self.PRECIOS[self.__tipo][self.__tipo_visitante]
        if self.__fast_pass:
            base += self.PRECIO_FAST_PASS
        return base

    def __calcular_precio_total(self):
        """
        Calcula el precio total aplicando el IVA del 10%.
        
        Returns:
            float: Precio total con IVA redondeado a 2 decimales.
        """
        return round(self.__precio_base * (1 + self.IVA / 100), 2)

    @property
    def tipo(self):
        """str: Tipo de ticket."""
        return self.__tipo

    @property
    def tipo_visitante(self):
        """str: Tipo de visitante."""
        return self.__tipo_visitante

    @property
    def localizador(self):
        """str: Localizador único del ticket en formato AGP-YYYY-XXXXXXXX."""
        return self.__localizador

    @property
    def precio_base(self):
        """float: Precio base sin IVA en euros."""
        return self.__precio_base

    @property
    def precio_total(self):
        """float: Precio total con IVA en euros."""
        return self.__precio_total

    @property
    def fast_pass(self):
        """bool: True si el ticket incluye Fast Pass."""
        return self.__fast_pass

    @property
    def id_empleado(self):
        """int: ID del taquillero que realizó la venta."""
        return self.__id_empleado

    @property
    def id_visitante(self):
        """int: ID del visitante si está registrado."""
        return self.__id_visitante

    def to_dict(self):
        """
        Convierte el ticket a diccionario para persistir en la BD.
        
        Returns:
            dict: Diccionario con todos los atributos del ticket.
        """
        return {
            'localizador': self.__localizador,
            'tipo': self.__tipo,
            'tipo_visitante': self.__tipo_visitante,
            'precio_base': self.__precio_base,
            'iva': self.IVA,
            'precio_total': self.__precio_total,
            'fast_pass': 1 if self.__fast_pass else 0,
            'id_empleado': self.__id_empleado,
            'id_visitante': self.__id_visitante,
        }

    def __str__(self):
        """
        Representación textual del ticket.
        
        Returns:
            str: Cadena con localizador, tipo, visitante, fast pass y precio total.
        """
        return (f"Ticket: {self.__localizador} | Tipo: {self.__tipo} | "
                f"Visitante: {self.__tipo_visitante} | "
                f"Fast Pass: {'Sí' if self.__fast_pass else 'No'} | "
                f"Total: {self.__precio_total}€")