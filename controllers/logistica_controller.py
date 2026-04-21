# ============================================
# AguaParaíso - Controlador Logística
# Sistema ERP SmartPark Pro
# ============================================

from database.connection import Database
from utils.logger import Logger
from exceptions.exceptions import StockInsuficienteError


class LogisticaController:
    """
    Controlador del módulo de logística e inventario.
    
    Gestiona el control de stock de productos en las diferentes
    zonas del parque, alertas de stock mínimo y reposiciones.
    
    Attributes:
        __db: Instancia singleton de la base de datos.
    """

    def __init__(self):
        """Inicializa el controlador con la conexión a la base de datos."""
        self.__db = Database.obtener_instancia()

    def obtener_inventario(self, id_zona=None):
        """
        Devuelve el inventario completo o filtrado por zona.
        
        Utiliza JOIN con zonas para incluir el nombre de cada zona.
        
        Args:
            id_zona (int, optional): ID de la zona a filtrar. Si es None devuelve todo.
            
        Returns:
            list: Lista de productos con datos de zona ordenados alfabéticamente.
        """
        try:
            if id_zona:
                query = """
                    SELECT i.*, z.nombre as zona_nombre
                    FROM inventario i
                    JOIN zonas z ON i.id_zona = z.id_zona
                    WHERE i.id_zona = ?
                    ORDER BY i.nombre
                """
                return self.__db.consultar(query, (id_zona,))
            else:
                query = """
                    SELECT i.*, z.nombre as zona_nombre
                    FROM inventario i
                    JOIN zonas z ON i.id_zona = z.id_zona
                    ORDER BY z.nombre, i.nombre
                """
                return self.__db.consultar(query)
        except Exception as e:
            Logger.error(f"Error al obtener inventario: {e}")
            raise

    def obtener_alertas_stock(self):
        """
        Devuelve los productos cuyo stock actual está por debajo del mínimo.
        
        Estos productos generan automáticamente un evento de tipo Stock
        mediante el trigger tr_stock_bajo_minimo de la base de datos.
        
        Returns:
            list: Lista de productos con stock bajo ordenados por stock ascendente.
        """
        try:
            query = """
                SELECT i.*, z.nombre as zona_nombre
                FROM inventario i
                JOIN zonas z ON i.id_zona = z.id_zona
                WHERE i.stock_actual < i.stock_minimo
                ORDER BY i.stock_actual ASC
            """
            return self.__db.consultar(query)
        except Exception as e:
            Logger.error(f"Error al obtener alertas: {e}")
            raise

    def reponer_stock(self, id_producto, cantidad):
        """
        Repone el stock de un producto sumando la cantidad indicada.
        
        Actualiza stock_actual y registra la fecha de última reposición.
        
        Args:
            id_producto (int): ID del producto a reponer.
            cantidad (int): Cantidad de unidades a añadir al stock.
            
        Raises:
            ValueError: Si la cantidad es menor o igual a cero.
        """
        try:
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que 0")

            query = """
                UPDATE inventario
                SET stock_actual = stock_actual + ?,
                    ultima_reposicion = datetime('now')
                WHERE id_producto = ?
            """
            self.__db.ejecutar(query, (cantidad, id_producto))
            Logger.info(f"Stock repuesto: producto {id_producto} +{cantidad} unidades")

        except Exception as e:
            Logger.error(f"Error al reponer stock: {e}")
            raise

    def consumir_stock(self, id_producto, cantidad=1):
        """
        Consume stock de un producto restando la cantidad indicada.
        
        Verifica que haya suficiente stock antes de consumir.
        El trigger tr_stock_bajo_minimo se activa automáticamente
        si el stock cae por debajo del mínimo tras el consumo.
        
        Args:
            id_producto (int): ID del producto a consumir.
            cantidad (int): Cantidad de unidades a consumir.
            
        Raises:
            StockInsuficienteError: Si el stock actual es menor que la cantidad.
            ValueError: Si el producto no existe.
        """
        try:
            producto = self.__db.consultar_uno(
                "SELECT * FROM inventario WHERE id_producto = ?",
                (id_producto,)
            )
            if not producto:
                raise ValueError(f"Producto {id_producto} no encontrado")

            if producto['stock_actual'] < cantidad:
                raise StockInsuficienteError(
                    producto['nombre'],
                    producto['stock_actual'],
                    cantidad
                )

            query = """
                UPDATE inventario
                SET stock_actual = stock_actual - ?
                WHERE id_producto = ?
            """
            self.__db.ejecutar(query, (cantidad, id_producto))
            Logger.info(f"Stock consumido: producto {id_producto} -{cantidad} unidades")

        except Exception as e:
            Logger.error(f"Error al consumir stock: {e}")
            raise

    def obtener_producto(self, id_producto):
        """
        Devuelve los datos de un producto por su ID.
        
        Args:
            id_producto (int): ID único del producto.
            
        Returns:
            dict | None: Datos del producto o None si no existe.
        """
        try:
            return self.__db.consultar_uno(
                "SELECT * FROM inventario WHERE id_producto = ?",
                (id_producto,)
            )
        except Exception as e:
            Logger.error(f"Error al obtener producto: {e}")
            raise