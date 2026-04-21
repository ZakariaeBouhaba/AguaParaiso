# ============================================
# AguaParaíso - Controlador Logística
# Sistema ERP SmartPark Pro
# ============================================

from database.connection import Database
from utils.logger import Logger
from exceptions.exceptions import StockInsuficienteError


class LogisticaController:
    """Gestiona el inventario del parque."""

    def __init__(self):
        self.__db = Database.obtener_instancia()

    def obtener_inventario(self, id_zona=None):
        """Devuelve el inventario completo o por zona."""
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
        """Devuelve productos con stock bajo mínimo."""
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
        """Repone el stock de un producto."""
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
        """Consume stock de un producto."""
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
        """Devuelve un producto por ID."""
        try:
            return self.__db.consultar_uno(
                "SELECT * FROM inventario WHERE id_producto = ?",
                (id_producto,)
            )
        except Exception as e:
            Logger.error(f"Error al obtener producto: {e}")
            raise