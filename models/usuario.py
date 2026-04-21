# ============================================
# AguaParaíso - Clase Usuario
# Sistema ERP SmartPark Pro
# ============================================

from models.entidad import Entidad
from datetime import datetime, timedelta
import bcrypt


class Usuario(Entidad):
    """
    Representa un usuario del sistema ERP AguaParaíso.
    
    Gestiona la autenticación con bcrypt, el control de intentos
    fallidos y el bloqueo automático tras 3 intentos incorrectos
    durante 15 minutos.
    
    Attributes:
        __username (str): Nombre de usuario único en el sistema.
        __password_hash (str): Hash bcrypt de la contraseña.
        __rol (str): Rol del usuario en el sistema.
        __id_empleado (int): ID del empleado asociado.
        __intentos_fallidos (int): Contador de intentos de login fallidos.
        __bloqueado (bool): True si el usuario está bloqueado.
        __fecha_bloqueo (str): Fecha y hora del bloqueo.
        __ultimo_acceso (str): Fecha y hora del último acceso correcto.
    """

    ROLES_VALIDOS = ['Admin', 'Encargado', 'Taquillero', 'Tecnico', 'Camarero', 'Enfermero']
    MAX_INTENTOS = 3
    MINUTOS_BLOQUEO = 15

    def __init__(self, username, password, rol, id_empleado):
        """
        Inicializa un usuario hasheando la contraseña con bcrypt.
        
        Args:
            username (str): Nombre de usuario único.
            password (str): Contraseña en texto plano (se hashea automáticamente).
            rol (str): Rol del usuario. Debe estar en ROLES_VALIDOS.
            id_empleado (int): ID del empleado asociado.
            
        Raises:
            ValueError: Si el rol no es válido.
        """
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
        """
        Genera un hash seguro bcrypt de la contraseña.
        
        Args:
            password (str): Contraseña en texto plano.
            
        Returns:
            str: Hash bcrypt de la contraseña.
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def __validar_rol(self, rol):
        """
        Valida que el rol sea válido.
        
        Args:
            rol (str): Rol a validar.
            
        Returns:
            str: Rol validado.
            
        Raises:
            ValueError: Si el rol no está en ROLES_VALIDOS.
        """
        if rol not in self.ROLES_VALIDOS:
            raise ValueError(f"Rol inválido: {rol}")
        return rol

    @property
    def username(self):
        """str: Nombre de usuario único en el sistema."""
        return self.__username

    @property
    def rol(self):
        """str: Rol del usuario en el sistema."""
        return self.__rol

    @property
    def id_empleado(self):
        """int: ID del empleado asociado al usuario."""
        return self.__id_empleado

    @property
    def bloqueado(self):
        """bool: True si el usuario está bloqueado."""
        return self.__bloqueado

    @property
    def intentos_fallidos(self):
        """int: Número de intentos de login fallidos."""
        return self.__intentos_fallidos

    @property
    def ultimo_acceso(self):
        """str: Fecha y hora del último acceso correcto."""
        return self.__ultimo_acceso

    def verificar_password(self, password):
        """
        Verifica si la contraseña proporcionada coincide con el hash.
        
        Args:
            password (str): Contraseña en texto plano a verificar.
            
        Returns:
            bool: True si la contraseña es correcta.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.__password_hash.encode('utf-8'))

    def esta_bloqueado(self):
        """
        Comprueba si el usuario sigue bloqueado.
        
        Desbloquea automáticamente si han pasado los 15 minutos.
        
        Returns:
            bool: True si el usuario está bloqueado.
        """
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
        """
        Registra un intento de login fallido.
        
        Bloquea el usuario automáticamente tras MAX_INTENTOS fallos.
        """
        self.__intentos_fallidos += 1
        if self.__intentos_fallidos >= self.MAX_INTENTOS:
            self.__bloqueado = True
            self.__fecha_bloqueo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def registrar_acceso_correcto(self):
        """
        Registra un acceso correcto y resetea los intentos fallidos.
        
        Desbloquea el usuario y actualiza la fecha de último acceso.
        """
        self.__intentos_fallidos = 0
        self.__bloqueado = False
        self.__fecha_bloqueo = None
        self.__ultimo_acceso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """
        Convierte el usuario a diccionario para persistir en la BD.
        
        Returns:
            dict: Diccionario con todos los atributos del usuario.
        """
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
        """
        Representación textual del usuario.
        
        Returns:
            str: Cadena con username, rol y estado de bloqueo.
        """
        return (f"Usuario: {self.__username} | "
                f"Rol: {self.__rol} | "
                f"Bloqueado: {'Sí' if self.__bloqueado else 'No'}")