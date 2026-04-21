# ============================================
# AguaParaíso - Clase ParqueTematico
# Sistema ERP SmartPark Pro
# ============================================

from datetime import datetime


class ParqueTematico:
    """
    Clase raíz que representa el parque AguaParaíso.
    
    Coordina y gestiona todas las zonas, empleados y eventos
    activos del parque. Proporciona métodos de consulta usando
    estructuras de datos avanzadas como sets, sorted() y filter().
    
    Attributes:
        __nombre (str): Nombre del parque.
        __temporada (str): Temporada actual del parque.
        __estado (str): Estado operativo del parque.
        __zonas (dict): Diccionario de zonas indexadas por nombre.
        __empleados (dict): Diccionario de empleados indexados por ID.
        __eventos_activos (list): Lista de eventos activos en el parque.
    """

    ESTADOS_VALIDOS = ['Abierto', 'Cerrado', 'AlertaClimatica',
                       'EmergenciaSanitaria', 'AforoCompleto']

    def __init__(self, nombre, temporada='verano'):
        """
        Inicializa el parque con estado Abierto y estructuras vacías.
        
        Args:
            nombre (str): Nombre del parque.
            temporada (str): Temporada actual. Por defecto 'verano'.
        """
        self.__nombre = nombre
        self.__temporada = temporada
        self.__estado = 'Abierto'
        self.__zonas = {}
        self.__empleados = {}
        self.__eventos_activos = []

    @property
    def nombre(self):
        """str: Nombre del parque."""
        return self.__nombre

    @property
    def temporada(self):
        """str: Temporada actual del parque."""
        return self.__temporada

    @property
    def estado(self):
        """str: Estado operativo del parque."""
        return self.__estado

    @estado.setter
    def estado(self, valor):
        """
        Asigna el estado operativo del parque con validación.
        
        Args:
            valor (str): Nuevo estado. Debe estar en ESTADOS_VALIDOS.
            
        Raises:
            ValueError: Si el estado no es válido.
        """
        if valor not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: {valor}")
        self.__estado = valor

    def esta_abierto(self):
        """
        Comprueba si el parque está operativo.
        
        Returns:
            bool: True si el estado es Abierto.
        """
        return self.__estado == 'Abierto'

    def agregar_zona(self, zona):
        """
        Añade una zona al parque indexada por nombre.
        
        Args:
            zona (Zona): Objeto zona a añadir.
        """
        self.__zonas[zona.nombre] = zona

    def obtener_zona(self, nombre):
        """
        Devuelve una zona por su nombre.
        
        Args:
            nombre (str): Nombre de la zona.
            
        Returns:
            Zona | None: La zona encontrada o None si no existe.
        """
        return self.__zonas.get(nombre)

    def obtener_zonas(self):
        """
        Devuelve todas las zonas del parque.
        
        Returns:
            list: Lista de todas las zonas.
        """
        return list(self.__zonas.values())

    def agregar_evento(self, evento):
        """
        Añade un evento a la lista de eventos activos.
        
        Args:
            evento (Evento): Objeto evento a añadir.
        """
        self.__eventos_activos.append(evento)

    def obtener_eventos_activos(self):
        """
        Devuelve solo los eventos que siguen activos.
        
        Returns:
            list: Lista de eventos con estado Activo.
        """
        return [e for e in self.__eventos_activos if e.esta_activo()]

    def total_visitantes(self):
        """
        Calcula el total de visitantes actuales en el parque.
        
        Suma el aforo actual de todas las zonas.
        
        Returns:
            int: Total de visitantes en el parque.
        """
        return sum(z.aforo_actual for z in self.__zonas.values())

    def obtener_tipos_zonas(self):
        """
        Devuelve los tipos únicos de zonas usando set.
        
        Utiliza un set de Python para garantizar la unicidad
        de los tipos de zonas presentes en el parque.
        
        Returns:
            set: Conjunto de tipos de zonas únicos.
        """
        return set(zona.tipo for zona in self.__zonas.values())

    def obtener_zonas_ordenadas_por_aforo(self):
        """
        Devuelve las zonas ordenadas por ocupación descendente.
        
        Utiliza sorted() con función lambda para ordenar
        las zonas de mayor a menor aforo actual.
        
        Returns:
            list: Lista de zonas ordenadas por aforo descendente.
        """
        return sorted(
            self.__zonas.values(),
            key=lambda z: z.aforo_actual,
            reverse=True
        )

    def obtener_zonas_disponibles(self):
        """
        Filtra y devuelve solo las zonas disponibles.
        
        Utiliza filter() con función lambda para obtener
        únicamente las zonas que están abiertas y con aforo.
        
        Returns:
            list: Lista de zonas disponibles para acceso.
        """
        return list(filter(
            lambda z: z.esta_disponible(),
            self.__zonas.values()
        ))

    def obtener_zonas_por_tipo(self, tipo):
        """
        Filtra zonas por tipo usando comprensión de lista.
        
        Args:
            tipo (str): Tipo de zona a filtrar.
            
        Returns:
            list: Lista de zonas del tipo indicado.
        """
        return [z for z in self.__zonas.values() if z.tipo == tipo]

    def __str__(self):
        """
        Representación textual del parque.
        
        Returns:
            str: Cadena con nombre, estado, temporada y número de zonas.
        """
        return (f"Parque: {self.__nombre} | "
                f"Estado: {self.__estado} | "
                f"Temporada: {self.__temporada} | "
                f"Zonas: {len(self.__zonas)}")