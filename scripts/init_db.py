# ============================================
# AguaParaíso - Inicializar Base de Datos
# Sistema ERP SmartPark Pro
# ============================================

import sqlite3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import Logger


def init_db():
    """Inicializa la base de datos con schema y datos de prueba."""

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_db = os.path.join(base, 'data', 'aguaparaiso.db')
    ruta_schema = os.path.join(base, 'database', 'sql', 'schema.sql')
    ruta_triggers = os.path.join(base, 'database', 'sql', 'triggers.sql')
    ruta_seed = os.path.join(base, 'database', 'sql', 'seed.sql')

    print("Inicializando base de datos AguaParaíso...")

    try:
        conn = sqlite3.connect(ruta_db)
        conn.execute("PRAGMA foreign_keys = ON")

        # Schema
        print("Creando tablas...")
        with open(ruta_schema, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())

        # Triggers
        print("Creando triggers...")
        with open(ruta_triggers, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())

        # Seed
        print("Insertando datos de prueba...")
        with open(ruta_seed, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())

        conn.commit()
        conn.close()

        Logger.info("Base de datos inicializada correctamente")
        print("Base de datos inicializada correctamente.")

    except Exception as e:
        Logger.error(f"Error al inicializar BD: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    init_db()