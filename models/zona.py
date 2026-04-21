# ============================================
# AguaParaíso - Clase Zona
# Sistema ERP SmartPark Pro
# ============================================

from models.entidad import Entidad
from exceptions.exceptions import AforoCompletoError, ZonaCerradaError


class Zona(Entidad):
    """
    Representa una zona temática del parque AguaParaíso.
    
    Gestiona el aforo en tiempo real, el estado operativo y los
    horarios de apertura y cierre. Lanza excepciones específicas
    cuando se intenta acceder a una zona cerrada o con aforo completo.
    
    Attributes:
        __nombre (str): Nombre identificativo de la zona.
        __tipo (str): Tipo de zona (Toboganes, Piscinas, etc.).
        __aforo_maximo (int): Capacidad máxima de personas.
        __aforo_actual (int): Número de personas actualmente en la zona.
        __estado (str): Estado operativo (Abierta, Cerrada, Alerta).
        __hora_apertura (str): Hora de apertura en formato HH:MM.
        __hora_cierre (str): Hora de cierre en formato HH:MM.
    """

    TIPOS_VALIDOS = ['Toboganes', 'Piscinas', 'RioLento', 'Restauracion', 'Servicios', 'VIP']
    ESTADOS_VALIDOS = ['Abierta', 'Cerrada', 'Alerta']

    def __init__(self, nombre, tipo, aforo_maximo, hora_apertura, hora_cierre):
        """
        Inicializa una zona con aforo a 0 y estado Abierta.
        
        Args:
            nombre (str): Nombre de la zona.
            tipo (str): Tipo de zona. Debe estar en TIPOS_VALIDOS.
            aforo_maximo (int): Capacidad máxima de personas.
            hora_apertura (str): Hora de apertura en formato HH:MM.
            hora_cierre (str): Hora de cierre en formato HH:MM.
            
        Raises:
            ValueError: Si el tipo no es válido o el aforo no es positivo.
        """
        super().__init__()
        self.__nombre = nombre
        self.__tipo = self.__validar_tipo(tipo)
        self.__aforo_maximo = self.__validar_aforo_maximo(aforo_maximo)
        self.__aforo_actual = 0
        self.__estado = 'Abierta'
        self.__hora_apertura = hora_apertura
        self.__hora_cierre = hora_cierre

    @property
    def nombre(self):
        """str: Nombre identificativo de la zona."""
        return self.__nombre

    @property
    def tipo(self):
        """str: Tipo de zona."""
        return self.__tipo

    @property
    def aforo_maximo(self):
        """int: Capacidad máxima de personas."""
        return self.__aforo_maximo

    @property
    def aforo_actual(self):
        """int: Número de personas actualmente en la zona."""
        return self.__aforo_actual

    @property
    def estado(self):
        """str: Estado operativo de la zona."""
        return self.__estado

    @estado.setter
    def estado(self, valor):
        """
        Asigna el estado de la zona con validación.
        
        Args:
            valor (str): Nuevo estado. Debe estar en ESTADOS_VALIDOS.
            
        Raises:
            ValueError: Si el estado no es válido.
        """
        if valor not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: {valor}")
        self.__estado = valor

    @property
    def hora_apertura(self):
        """str: Hora de apertura en formato HH:MM."""
        return self.__hora_apertura

    @property
    def hora_cierre(self):
        """str: Hora de cierre en formato HH:MM."""
        return self.__hora_cierre

    def __validar_tipo(self, tipo):
        """
        Valida que el tipo de zona sea válido.
        
        Args:
            tipo (str): Tipo a validar.
            
        Returns:
            str: Tipo validado.
            
        Raises:
            ValueError: Si el tipo no está en TIPOS_VALIDOS.
        """
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de zona inválido: {tipo}")
        return tipo

    def __validar_aforo_maximo(self, aforo):
        """
        Valida que el aforo máximo sea un entero positivo.
        
        Args:
            aforo (int): Aforo a validar.
            
        Returns:
            int: Aforo validado.
            
        Raises:
            ValueError: Si el aforo no es entero positivo.
        """
        if not isinstance(aforo, int) or aforo <= 0:
            raise ValueError("El aforo máximo debe ser un entero positivo")
        return aforo

    def incrementar_aforo(self):
        """
        Incrementa el aforo actual en 1 cuando entra un visitante.
        
        Raises:
            ZonaCerradaError: Si la zona no está en estado Abierta.
            AforoCompletoError: Si el aforo actual ha alcanzado el máximo.
        """
        if self.__estado != 'Abierta':
            raise ZonaCerradaError(self.__nombre, self.__estado)
        if self.__aforo_actual >= self.__aforo_maximo:
            raise AforoCompletoError(self.__nombre, self.__aforo_actual, self.__aforo_maximo)
        self.__aforo_actual += 1

    def decrementar_aforo(self):
        """Decrementa el aforo actual en 1 cuando sale un visitante."""
        if self.__aforo_actual > 0:
            self.__aforo_actual -= 1

    def esta_disponible(self):
        """
        Comprueba si la zona está operativa y con aforo disponible.
        
        Returns:
            bool: True si está abierta y no ha alcanzado el aforo máximo.
        """
        return self.__estado == 'Abierta' and self.__aforo_actual < self.__aforo_maximo

    def porcentaje_ocupacion(self):
        """
        Calcula el porcentaje de ocupación actual de la zona.
        
        Returns:
            float: Porcentaje de ocupación redondeado a 2 decimales.
        """
        return round((self.__aforo_actual / self.__aforo_maximo) * 100, 2)

    def to_dict(self):
        """
        Convierte la zona a diccionario para persistir en la base de datos.
        
        Returns:
            dict: Diccionario con todos los atributos de la zona.
        """
        return {
            'id_zona': self.id,
            'nombre': self.__nombre,
            'tipo': self.__tipo,
            'aforo_maximo': self.__aforo_maximo,
            'aforo_actual': self.__aforo_actual,
            'estado': self.__estado,
            'hora_apertura': self.__hora_apertura,
            'hora_cierre': self.__hora_cierre,
            'fecha_creacion': self.fecha_creacion
        }

    def __str__(self):
        """
        Representación textual de la zona.
        
        Returns:
            str: Cadena con nombre, tipo, estado y aforo actual/máximo.
        """
        return (f"Zona: {self.__nombre} | Tipo: {self.__tipo} | "
                f"Estado: {self.__estado} | "
                f"Aforo: {self.__aforo_actual}/{self.__aforo_maximo}")