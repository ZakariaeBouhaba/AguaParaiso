# ============================================
# AguaParaíso - Sistema de Logging
# Sistema ERP SmartPark Pro
# ============================================

import os
from datetime import datetime


class Logger:
    """
    Gestiona el registro de eventos del sistema en un archivo externo.
    
    Registra todos los eventos críticos del sistema diferenciando
    tres niveles de severidad: INFO, WARNING y ERROR. Los registros
    se guardan en logs/log_parque.txt con marca de tiempo.
    
    Attributes:
        _ruta_log (str): Ruta al archivo de log. Se inicializa en el
                         primer uso mediante inicialización lazy.
    """

    _ruta_log = None

    @classmethod
    def __obtener_ruta(cls):
        """
        Obtiene la ruta al archivo de log usando inicialización lazy.
        
        Returns:
            str: Ruta absoluta al archivo log_parque.txt.
        """
        if cls._ruta_log is None:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cls._ruta_log = os.path.join(base, 'logs', 'log_parque.txt')
        return cls._ruta_log

    @classmethod
    def __escribir(cls, nivel, mensaje):
        """
        Escribe una línea en el archivo de log con nivel y timestamp.
        
        Formato: [YYYY-MM-DD HH:MM:SS] [NIVEL] mensaje
        
        Args:
            nivel (str): Nivel del log (INFO, WARNING, ERROR).
            mensaje (str): Mensaje a registrar.
        """
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{fecha}] [{nivel}] {mensaje}\n"
        try:
            with open(cls.__obtener_ruta(), 'a', encoding='utf-8') as f:
                f.write(linea)
        except Exception as e:
            print(f"Error al escribir en log: {e}")

    @classmethod
    def info(cls, mensaje):
        """
        Registra un evento informativo en el log.
        
        Usar para eventos normales del sistema como ventas,
        accesos correctos o actualizaciones de datos.
        
        Args:
            mensaje (str): Mensaje informativo a registrar.
        """
        cls.__escribir('INFO', mensaje)

    @classmethod
    def warning(cls, mensaje):
        """
        Registra una advertencia en el log.
        
        Usar para eventos que requieren atención pero no son
        críticos, como stock bajo o aforo al límite.
        
        Args:
            mensaje (str): Mensaje de advertencia a registrar.
        """
        cls.__escribir('WARNING', mensaje)

    @classmethod
    def error(cls, mensaje):
        """
        Registra un error crítico en el log.
        
        Usar para errores de base de datos, excepciones no
        controladas o fallos críticos del sistema.
        
        Args:
            mensaje (str): Mensaje de error a registrar.
        """
        cls.__escribir('ERROR', mensaje)