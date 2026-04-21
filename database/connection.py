# ============================================
# AguaParaíso - Conexión SQLite3
# Sistema ERP SmartPark Pro
# ============================================

import sqlite3
import os
from utils.logger import Logger


class Database:
    """Gestiona la conexión con la base de datos SQLite3."""

    _instancia = None

    def __init__(self):
        self.__ruta_db = self.__obtener_ruta()
        self.__conexion = None

    @classmethod
    def obtener_instancia(cls):
        """Patrón Singleton — una sola conexión en todo el sistema."""
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def __obtener_ruta(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base, 'data', 'aguaparaiso.db')

    def conectar(self):
        """Abre la conexión con la base de datos."""
        try:
            self.__conexion = sqlite3.connect(self.__ruta_db)
            self.__conexion.execute("PRAGMA foreign_keys = ON")
            self.__conexion.row_factory = sqlite3.Row
            return self.__conexion
        except sqlite3.Error as e:
            Logger.error(f"Error al conectar con la BD: {e}")
            raise

    def desconectar(self):
        """Cierra la conexión con la base de datos."""
        if self.__conexion:
            self.__conexion.close()
            self.__conexion = None

    def ejecutar(self, query, params=()):
        """Ejecuta una consulta SQL y hace commit."""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor
        except sqlite3.Error as e:
            conn.rollback()
            Logger.error(f"Error al ejecutar query: {e} | Query: {query}")
            raise
        finally:
            self.desconectar()

    def consultar(self, query, params=()):
        """Ejecuta una consulta SELECT y devuelve los resultados."""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            Logger.error(f"Error al consultar: {e} | Query: {query}")
            raise
        finally:
            self.desconectar()

    def consultar_uno(self, query, params=()):
        """Ejecuta una consulta SELECT y devuelve un solo resultado."""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        except sqlite3.Error as e:
            Logger.error(f"Error al consultar: {e} | Query: {query}")
            raise
        finally:
            self.desconectar()