# ============================================
# AguaParaíso - Seguridad del sistema
# Sistema ERP SmartPark Pro
# ============================================

import bcrypt
from datetime import datetime, timedelta
from config.settings import Settings


class Security:
    """Gestiona la seguridad del sistema."""

    @staticmethod
    def hashear_password(password):
        """Genera un hash seguro de la contraseña."""
        return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    @staticmethod
    def verificar_password(password, password_hash):
        """Verifica si la contraseña coincide con el hash."""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )

    @staticmethod
    def usuario_bloqueado(fecha_bloqueo):
        """Comprueba si el usuario sigue bloqueado."""
        if not fecha_bloqueo:
            return False
        minutos = Settings.minutos_bloqueo()
        tiempo_bloqueo = datetime.strptime(fecha_bloqueo, "%Y-%m-%d %H:%M:%S")
        return datetime.now() < tiempo_bloqueo + timedelta(minutes=minutos)

    @staticmethod
    def tiempo_restante_bloqueo(fecha_bloqueo):
        """Devuelve los minutos restantes de bloqueo."""
        if not fecha_bloqueo:
            return 0
        minutos = Settings.minutos_bloqueo()
        tiempo_bloqueo = datetime.strptime(fecha_bloqueo, "%Y-%m-%d %H:%M:%S")
        fin_bloqueo = tiempo_bloqueo + timedelta(minutes=minutos)
        restante = (fin_bloqueo - datetime.now()).seconds // 60
        return max(0, restante)