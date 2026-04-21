# ============================================
# AguaParaíso - Clase Inventario
# Sistema ERP SmartPark Pro
# ============================================

from models.entidad import Entidad
from exceptions.exceptions import StockInsuficienteError


class Inventario(Entidad):
    """
    Representa un producto del inventario del parque AguaParaíso.
    
    Gestiona el stock de productos en las diferentes zonas del parque,
    con alertas automáticas cuando el stock cae por debajo del mínimo.
    
    Attributes:
        __nombre (str): Nombre del producto.
        __id_zona (int): ID de la zona donde se almacena.
        __stock_actual (int): Unidades disponibles actualmente.
        __stock_minimo (int): Umbral mínimo de stock antes de alerta.
        __precio_coste (float): Precio de coste unitario en euros.
        __precio_venta (float): Precio de venta unitario en euros.
        __proveedor (str): Nombre del proveedor del producto.
        __frecuencia_reposicion (str): Frecuencia de reposición (Diario/Semanal/Mensual).
    """

    FRECUENCIAS_VALIDAS = ['Diario', 'Semanal', 'Mensual']

    def __init__(self, nombre, id_zona, stock_actual, stock_minimo,
                 precio_coste, precio_venta, proveedor, frecuencia_reposicion):
        """
        Inicializa un producto del inventario.
        
        Args:
            nombre (str): Nombre del producto.
            id_zona (int): ID de la zona donde se almacena.
            stock_actual (int): Unidades disponibles actualmente.
            stock_minimo (int): Umbral mínimo antes de alerta.
            precio_coste (float): Precio de coste unitario en euros.
            precio_venta (float): Precio de venta unitario en euros.
            proveedor (str): Nombre del proveedor.
            frecuencia_reposicion (str): Frecuencia de reposición.
            
        Raises:
            ValueError: Si el precio de venta es menor que el de coste.
        """
        super().__init__()
        self.__nombre = nombre
        self.__id_zona = id_zona
        self.__stock_actual = stock_actual
        self.__stock_minimo = stock_minimo
        self.__precio_coste = precio_coste
        self.__precio_venta = self.__validar_precio_venta(precio_coste, precio_venta)
        self.__proveedor = proveedor
        self.__frecuencia_reposicion = self.__validar_frecuencia(frecuencia_reposicion)

    def __validar_precio_venta(self, coste, venta):
        """
        Valida que el precio de venta sea mayor que el de coste.
        
        Args:
            coste (float): Precio de coste unitario.
            venta (float): Precio de venta unitario.
            
        Returns:
            float: Precio de venta validado.
            
        Raises:
            ValueError: Si el precio de venta es menor o igual al de coste.
        """
        if venta <= coste:
            raise ValueError("El precio de venta debe ser mayor que el precio de coste")
        return venta

    def __validar_frecuencia(self, frecuencia):
        """
        Valida que la frecuencia de reposición sea válida.
        
        Args:
            frecuencia (str): Frecuencia a validar.
            
        Returns:
            str: Frecuencia validada.
            
        Raises:
            ValueError: Si la frecuencia no está en FRECUENCIAS_VALIDAS.
        """
        if frecuencia not in self.FRECUENCIAS_VALIDAS:
            raise ValueError(f"Frecuencia inválida: {frecuencia}")
        return frecuencia

    @property
    def nombre(self):
        """str: Nombre del producto."""
        return self.__nombre

    @property
    def id_zona(self):
        """int: ID de la zona donde se almacena el producto."""
        return self.__id_zona

    @property
    def stock_actual(self):
        """int: Unidades disponibles actualmente."""
        return self.__stock_actual

    @property
    def stock_minimo(self):
        """int: Umbral mínimo de stock antes de generar alerta."""
        return self.__stock_minimo

    @property
    def precio_coste(self):
        """float: Precio de coste unitario en euros."""
        return self.__precio_coste

    @property
    def precio_venta(self):
        """float: Precio de venta unitario en euros."""
        return self.__precio_venta

    @property
    def proveedor(self):
        """str: Nombre del proveedor del producto."""
        return self.__proveedor

    @property
    def frecuencia_reposicion(self):
        """str: Frecuencia de reposición del producto."""
        return self.__frecuencia_reposicion

    def esta_bajo_minimo(self):
        """
        Comprueba si el stock actual está por debajo del mínimo.
        
        Returns:
            bool: True si stock_actual < stock_minimo.
        """
        return self.__stock_actual < self.__stock_minimo

    def consumir(self, cantidad=1):
        """
        Consume una cantidad del stock del producto.
        
        Args:
            cantidad (int): Unidades a consumir.
            
        Raises:
            StockInsuficienteError: Si el stock actual es menor que la cantidad.
        """
        if self.__stock_actual < cantidad:
            raise StockInsuficienteError(self.__nombre, self.__stock_actual, cantidad)
        self.__stock_actual -= cantidad

    def reponer(self, cantidad):
        """
        Repone una cantidad al stock del producto.
        
        Args:
            cantidad (int): Unidades a añadir al stock.
            
        Raises:
            ValueError: Si la cantidad es menor o igual a cero.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad a reponer debe ser mayor que 0")
        self.__stock_actual += cantidad

    def beneficio_unitario(self):
        """
        Calcula el beneficio unitario del producto.
        
        Returns:
            float: Diferencia entre precio de venta y coste redondeada a 2 decimales.
        """
        return round(self.__precio_venta - self.__precio_coste, 2)

    def to_dict(self):
        """
        Convierte el producto a diccionario para persistir en la BD.
        
        Returns:
            dict: Diccionario con todos los atributos del producto.
        """
        return {
            'nombre': self.__nombre,
            'id_zona': self.__id_zona,
            'stock_actual': self.__stock_actual,
            'stock_minimo': self.__stock_minimo,
            'precio_coste': self.__precio_coste,
            'precio_venta': self.__precio_venta,
            'proveedor': self.__proveedor,
            'frecuencia_reposicion': self.__frecuencia_reposicion
        }

    def __str__(self):
        """
        Representación textual del producto con alerta si el stock es bajo.
        
        Returns:
            str: Cadena con nombre, stock actual/mínimo y precio de venta.
        """
        alerta = " ⚠️ STOCK BAJO" if self.esta_bajo_minimo() else ""
        return (f"Producto: {self.__nombre} | "
                f"Stock: {self.__stock_actual}/{self.__stock_minimo} | "
                f"Precio venta: {self.__precio_venta}€{alerta}")