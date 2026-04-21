# ============================================
# AguaParaíso - Conexión SQLite3
# Sistema ERP SmartPark Pro
# ============================================

import sqlite3
import os
from utils.logger import Logger


class Database:
    """
    Gestiona la conexión con la base de datos SQLite3.
    
    Implementa el patrón Singleton para garantizar que existe
    una única instancia de conexión en todo el sistema. Activa
    las claves foráneas con PRAGMA foreign_keys = ON y configura
    row_factory para acceder a las columnas por nombre.
    
    Attributes:
        _instancia: Instancia única de la clase (Singleton).
        __ruta_db (str): Ruta absoluta al archivo de base de datos.
        __conexion: Conexión SQLite3 activa.
    """

    _instancia = None

    def __init__(self):
        """Inicializa la base de datos con la ruta al archivo .db."""
        self.__ruta_db = self.__obtener_ruta()
        self.__conexion = None

    @classmethod
    def obtener_instancia(cls):
        """
        Devuelve la instancia única de la base de datos (Singleton).
        
        Crea la instancia en el primer acceso y la reutiliza
        en todas las llamadas posteriores.
        
        Returns:
            Database: Instancia única de la base de datos.
        """
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def __obtener_ruta(self):
        """
        Calcula la ruta absoluta al archivo de base de datos.
        
        Returns:
            str: Ruta absoluta a data/aguaparaiso.db.
        """
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base, 'data', 'aguaparaiso.db')

    def conectar(self):
        """
        Abre la conexión con la base de datos SQLite3.
        
        Activa las claves foráneas y configura row_factory para
        acceder a los resultados por nombre de columna.
        
        Returns:
            sqlite3.Connection: Conexión activa a la base de datos.
            
        Raises:
            sqlite3.Error: Si no se puede establecer la conexión.
        """
        try:
            self.__conexion = sqlite3.connect(self.__ruta_db)
            self.__conexion.execute("PRAGMA foreign_keys = ON")
            self.__conexion.row_factory = sqlite3.Row
            return self.__conexion
        except sqlite3.Error as e:
            Logger.error(f"Error al conectar con la BD: {e}")
            raise

    def desconectar(self):
        """Cierra la conexión con la base de datos si está abierta."""
        if self.__conexion:
            self.__conexion.close()
            self.__conexion = None

    def ejecutar(self, query, params=()):
        """
        Ejecuta una consulta SQL de escritura con commit automático.
        
        Abre la conexión, ejecuta la query con los parámetros,
        hace commit y cierra la conexión. En caso de error hace
        rollback y registra el error en el log.
        
        Args:
            query (str): Consulta SQL a ejecutar.
            params (tuple): Parámetros para la consulta parametrizada.
            
        Returns:
            sqlite3.Cursor: Cursor con lastrowid disponible.
            
        Raises:
            sqlite3.Error: Si ocurre un error en la ejecución.
        """
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
        """
        Ejecuta una consulta SELECT y devuelve todos los resultados.
        
        Args:
            query (str): Consulta SELECT a ejecutar.
            params (tuple): Parámetros para la consulta parametrizada.
            
        Returns:
            list: Lista de filas como objetos sqlite3.Row accesibles por nombre.
            
        Raises:
            sqlite3.Error: Si ocurre un error en la consulta.
        """
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
        """
        Ejecuta una consulta SELECT y devuelve un único resultado.
        
        Args:
            query (str): Consulta SELECT a ejecutar.
            params (tuple): Parámetros para la consulta parametrizada.
            
        Returns:
            sqlite3.Row | None: Fila resultado o None si no hay resultados.
            
        Raises:
            sqlite3.Error: Si ocurre un error en la consulta.
        """
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