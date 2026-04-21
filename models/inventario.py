# ============================================
# AguaParaíso - Clase Inventario
# Sistema ERP SmartPark Pro
# ============================================

from models.entidad import Entidad
from exceptions.exceptions import StockInsuficienteError


class Inventario(Entidad):
    """Representa un producto del inventario del parque."""

    FRECUENCIAS_VALIDAS = ['Diario', 'Semanal', 'Mensual']

    def __init__(self, nombre, id_zona, stock_actual, stock_minimo,
                 precio_coste, precio_venta, proveedor, frecuencia_reposicion):
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
        if venta <= coste:
            raise ValueError("El precio de venta debe ser mayor que el precio de coste")
        return venta

    def __validar_frecuencia(self, frecuencia):
        if frecuencia not in self.FRECUENCIAS_VALIDAS:
            raise ValueError(f"Frecuencia inválida: {frecuencia}")
        return frecuencia

    @property
    def nombre(self):
        return self.__nombre

    @property
    def id_zona(self):
        return self.__id_zona

    @property
    def stock_actual(self):
        return self.__stock_actual

    @property
    def stock_minimo(self):
        return self.__stock_minimo

    @property
    def precio_coste(self):
        return self.__precio_coste

    @property
    def precio_venta(self):
        return self.__precio_venta

    @property
    def proveedor(self):
        return self.__proveedor

    @property
    def frecuencia_reposicion(self):
        return self.__frecuencia_reposicion

    def esta_bajo_minimo(self):
        return self.__stock_actual < self.__stock_minimo

    def consumir(self, cantidad=1):
        if self.__stock_actual < cantidad:
            raise StockInsuficienteError(self.__nombre, self.__stock_actual, cantidad)
        self.__stock_actual -= cantidad

    def reponer(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a reponer debe ser mayor que 0")
        self.__stock_actual += cantidad

    def beneficio_unitario(self):
        return round(self.__precio_venta - self.__precio_coste, 2)

    def to_dict(self):
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
        alerta = " ⚠️ STOCK BAJO" if self.esta_bajo_minimo() else ""
        return (f"Producto: {self.__nombre} | "
                f"Stock: {self.__stock_actual}/{self.__stock_minimo} | "
                f"Precio venta: {self.__precio_venta}€{alerta}")