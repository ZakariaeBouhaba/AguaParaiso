# ============================================
# AguaParaíso - Reset Base de Datos
# Sistema ERP SmartPark Pro
# ============================================

import sqlite3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import Logger
from utils.security import Security


def reset_db():
    """Elimina y reinicia la base de datos con datos de prueba."""

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_db = os.path.join(base, 'data', 'aguaparaiso.db')
    ruta_schema = os.path.join(base, 'database', 'sql', 'schema.sql')
    ruta_triggers = os.path.join(base, 'database', 'sql', 'triggers.sql')
    ruta_seed = os.path.join(base, 'database', 'sql', 'seed.sql')

    # Crear carpetas necesarias si no existen
    os.makedirs(os.path.join(base, 'data'), exist_ok=True)
    os.makedirs(os.path.join(base, 'logs'), exist_ok=True)

    print("Reseteando base de datos AguaParaiso...")

    try:
        # Eliminar BD existente
        if os.path.exists(ruta_db):
            os.remove(ruta_db)
            print("Base de datos eliminada.")

        # Recrear
        conn = sqlite3.connect(ruta_db)
        conn.execute("PRAGMA foreign_keys = ON")

        print("Creando tablas...")
        with open(ruta_schema, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())

        print("Creando triggers...")
        with open(ruta_triggers, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())

        print("Insertando datos de prueba...")
        with open(ruta_seed, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())

        conn.commit()
        conn.close()

        # Regenerar contraseñas
        print("Configurando contrasenas...")
        from database.connection import Database
        db = Database.obtener_instancia()
        h = Security.hashear_password('admin123')
        usuarios = ['admin', 'maria.taquilla', 'juan.taquilla',
                    'antonio.tecnico', 'roberto.camarero', 'alejandro.enfermero']
        for u in usuarios:
            db.ejecutar(
                'UPDATE usuarios SET password_hash = ? WHERE username = ?',
                (h, u)
            )

        Logger.info("Base de datos reseteada correctamente")
        print("Base de datos reseteada correctamente.")
        print("Todos los usuarios tienen contrasena: admin123")

    except Exception as e:
        Logger.error(f"Error al resetear BD: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    confirmacion = input("Estas seguro? Se perderan todos los datos. (s/n): ")
    if confirmacion.lower() == 's':
        reset_db()
    else:
        print("Operacion cancelada.")