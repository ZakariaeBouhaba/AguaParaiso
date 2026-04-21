# ============================================
# AguaParaíso - Configuración del sistema
# Sistema ERP SmartPark Pro
# ============================================

import configparser
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Carga y gestiona la configuración del sistema."""

    _config = None

    @classmethod
    def __cargar(cls):
        if cls._config is None:
            cls._config = configparser.ConfigParser()
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ruta = os.path.join(base, 'config', 'config.ini')
            cls._config.read(ruta, encoding='utf-8')
        return cls._config

    @classmethod
    def get(cls, seccion, clave):
        return cls.__cargar()[seccion][clave]

    @classmethod
    def get_float(cls, seccion, clave):
        return float(cls.__cargar()[seccion][clave])

    @classmethod
    def get_int(cls, seccion, clave):
        return int(cls.__cargar()[seccion][clave])

    @classmethod
    def nombre_parque(cls):
        return cls.get('parque', 'nombre')

    @classmethod
    def iva(cls):
        return cls.get_float('taquilla', 'iva')

    @classmethod
    def max_intentos_login(cls):
        return cls.get_int('seguridad', 'max_intentos_login')

    @classmethod
    def minutos_bloqueo(cls):
        return cls.get_int('seguridad', 'minutos_bloqueo')

    @classmethod
    def intervalo_eventos(cls):
        return cls.get_int('eventos', 'intervalo_segundos')

    @classmethod
    def probabilidades_eventos(cls):
        return {
            'Averia': cls.get_float('eventos', 'probabilidad_averia'),
            'Climatico': cls.get_float('eventos', 'probabilidad_climatico'),
            'Sanitario': cls.get_float('eventos', 'probabilidad_sanitario'),
            'Stock': cls.get_float('eventos', 'probabilidad_stock'),
        }