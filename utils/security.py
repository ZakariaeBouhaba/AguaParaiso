# ============================================
# AguaParaíso - Seguridad del sistema
# Sistema ERP SmartPark Pro
# ============================================

import bcrypt
from datetime import datetime, timedelta
from config.settings import Settings


class Security:
    """
    Gestiona la seguridad del sistema ERP AguaParaíso.
    
    Proporciona métodos para el hashing seguro de contraseñas
    con bcrypt, verificación de credenciales y control del
    tiempo de bloqueo de usuarios tras intentos fallidos.
    """

    @staticmethod
    def hashear_password(password):
        """
        Genera un hash seguro bcrypt de la contraseña con salt automático.
        
        Bcrypt genera un salt aleatorio en cada llamada, garantizando
        que dos hashes de la misma contraseña sean siempre diferentes.
        
        Args:
            password (str): Contraseña en texto plano a hashear.
            
        Returns:
            str: Hash bcrypt de la contraseña listo para almacenar en BD.
        """
        return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    @staticmethod
    def verificar_password(password, password_hash):
        """
        Verifica si una contraseña coincide con su hash bcrypt.
        
        Args:
            password (str): Contraseña en texto plano a verificar.
            password_hash (str): Hash bcrypt almacenado en la BD.
            
        Returns:
            bool: True si la contraseña es correcta.
        """
        return bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )

    @staticmethod
    def usuario_bloqueado(fecha_bloqueo):
        """
        Comprueba si un usuario sigue dentro del período de bloqueo.
        
        El tiempo de bloqueo se configura en config.ini bajo
        la clave [seguridad] minutos_bloqueo.
        
        Args:
            fecha_bloqueo (str): Fecha y hora del bloqueo en formato YYYY-MM-DD HH:MM:SS.
            
        Returns:
            bool: True si el usuario sigue bloqueado.
        """
        if not fecha_bloqueo:
            return False
        minutos = Settings.minutos_bloqueo()
        tiempo_bloqueo = datetime.strptime(fecha_bloqueo, "%Y-%m-%d %H:%M:%S")
        return datetime.now() < tiempo_bloqueo + timedelta(minutes=minutos)

    @staticmethod
    def tiempo_restante_bloqueo(fecha_bloqueo):
        """
        Calcula los minutos restantes de bloqueo de un usuario.
        
        Args:
            fecha_bloqueo (str): Fecha y hora del bloqueo en formato YYYY-MM-DD HH:MM:SS.
            
        Returns:
            int: Minutos restantes de bloqueo. 0 si ya no está bloqueado.
        """
        if not fecha_bloqueo:
            return 0
        minutos = Settings.minutos_bloqueo()
        tiempo_bloqueo = datetime.strptime(fecha_bloqueo, "%Y-%m-%d %H:%M:%S")
        fin_bloqueo = tiempo_bloqueo + timedelta(minutes=minutos)
        restante = (fin_bloqueo - datetime.now()).seconds // 60
        return max(0, restante)