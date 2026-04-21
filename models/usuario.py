# ============================================
# AguaParaíso - Clase Usuario
# Sistema ERP SmartPark Pro
# ============================================

from models.entidad import Entidad
from datetime import datetime, timedelta
import bcrypt


class Usuario(Entidad):
    """Representa un usuario del sistema ERP."""

    ROLES_VALIDOS = ['Admin', 'Encargado', 'Taquillero', 'Tecnico', 'Camarero', 'Enfermero']
    MAX_INTENTOS = 3
    MINUTOS_BLOQUEO = 15

    def __init__(self, username, password, rol, id_empleado):
        super().__init__()
        self.__username = username
        self.__password_hash = self.__hashear_password(password)
        self.__rol = self.__validar_rol(rol)
        self.__id_empleado = id_empleado
        self.__intentos_fallidos = 0
        self.__bloqueado = False
        self.__fecha_bloqueo = None
        self.__ultimo_acceso = None

    def __hashear_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def __validar_rol(self, rol):
        if rol not in self.ROLES_VALIDOS:
            raise ValueError(f"Rol inválido: {rol}")
        return rol

    @property
    def username(self):
        return self.__username

    @property
    def rol(self):
        return self.__rol

    @property
    def id_empleado(self):
        return self.__id_empleado

    @property
    def bloqueado(self):
        return self.__bloqueado

    @property
    def intentos_fallidos(self):
        return self.__intentos_fallidos

    @property
    def ultimo_acceso(self):
        return self.__ultimo_acceso

    def verificar_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.__password_hash.encode('utf-8'))

    def esta_bloqueado(self):
        """Comprueba si el usuario sigue bloqueado."""
        if not self.__bloqueado:
            return False
        if self.__fecha_bloqueo:
            tiempo_bloqueo = datetime.strptime(self.__fecha_bloqueo, "%Y-%m-%d %H:%M:%S")
            if datetime.now() > tiempo_bloqueo + timedelta(minutes=self.MINUTOS_BLOQUEO):
                self.__bloqueado = False
                self.__intentos_fallidos = 0
                self.__fecha_bloqueo = None
                return False
        return True

    def registrar_intento_fallido(self):
        self.__intentos_fallidos += 1
        if self.__intentos_fallidos >= self.MAX_INTENTOS:
            self.__bloqueado = True
            self.__fecha_bloqueo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def registrar_acceso_correcto(self):
        self.__intentos_fallidos = 0
        self.__bloqueado = False
        self.__fecha_bloqueo = None
        self.__ultimo_acceso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            'username': self.__username,
            'password_hash': self.__password_hash,
            'rol': self.__rol,
            'id_empleado': self.__id_empleado,
            'intentos_fallidos': self.__intentos_fallidos,
            'bloqueado': 1 if self.__bloqueado else 0,
            'fecha_bloqueo': self.__fecha_bloqueo,
            'ultimo_acceso': self.__ultimo_acceso
        }

    def __str__(self):
        return (f"Usuario: {self.__username} | "
                f"Rol: {self.__rol} | "
                f"Bloqueado: {'Sí' if self.__bloqueado else 'No'}")