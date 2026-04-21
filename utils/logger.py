# ============================================
# AguaParaíso - Sistema de Logging
# Sistema ERP SmartPark Pro
# ============================================

import os
from datetime import datetime


class Logger:
    """Gestiona el registro de eventos en log_parque.txt."""

    _ruta_log = None

    @classmethod
    def __obtener_ruta(cls):
        if cls._ruta_log is None:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cls._ruta_log = os.path.join(base, 'logs', 'log_parque.txt')
        return cls._ruta_log

    @classmethod
    def __escribir(cls, nivel, mensaje):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{fecha}] [{nivel}] {mensaje}\n"
        try:
            with open(cls.__obtener_ruta(), 'a', encoding='utf-8') as f:
                f.write(linea)
        except Exception as e:
            print(f"Error al escribir en log: {e}")

    @classmethod
    def info(cls, mensaje):
        cls.__escribir('INFO', mensaje)

    @classmethod
    def warning(cls, mensaje):
        cls.__escribir('WARNING', mensaje)

    @classmethod
    def error(cls, mensaje):
        cls.__escribir('ERROR', mensaje)