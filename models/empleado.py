# ============================================
# AguaParaíso - Clase Empleado y subclases
# Sistema ERP SmartPark Pro
# ============================================

from abc import abstractmethod
from models.entidad import Entidad


class Empleado(Entidad):
    """
    Clase base abstracta para todos los empleados del parque.
    
    Gestiona los datos personales y laborales del empleado,
    incluyendo el cálculo de nóminas con IRPF según categoría
    y bonus de temporada alta en julio y agosto.
    
    Attributes:
        __nombre (str): Nombre completo del empleado.
        __rol (str): Rol en el parque (Socorrista, Tecnico, etc.).
        __categoria (str): Categoría laboral (Junior, Senior, Jefe).
        __turno (str): Turno de trabajo (Manana, Tarde, Mantenimiento).
        __id_zona (int): ID de la zona asignada.
        __sueldo_base (float): Sueldo base mensual en euros.
        __contrato (str): Tipo de contrato (Fijo, Temporal).
        __estado (str): Estado laboral (Activo, Baja, Vacaciones).
    """

    ROLES_VALIDOS = ['Socorrista', 'Tecnico', 'Taquillero', 'Camarero',
                     'PersonalVIP', 'Vigilante', 'Limpiador', 'Administrativo', 'Enfermero']
    CATEGORIAS_VALIDAS = ['Junior', 'Senior', 'Jefe']
    TURNOS_VALIDOS = ['Manana', 'Tarde', 'Mantenimiento']
    ESTADOS_VALIDOS = ['Activo', 'Baja', 'Vacaciones']
    CONTRATOS_VALIDOS = ['Fijo', 'Temporal']

    def __init__(self, nombre, rol, categoria, turno, id_zona, sueldo_base, contrato):
        """
        Inicializa un empleado con estado Activo.
        
        Args:
            nombre (str): Nombre completo del empleado.
            rol (str): Rol en el parque. Debe estar en ROLES_VALIDOS.
            categoria (str): Categoría laboral. Debe estar en CATEGORIAS_VALIDAS.
            turno (str): Turno de trabajo. Debe estar en TURNOS_VALIDOS.
            id_zona (int): ID de la zona asignada.
            sueldo_base (float): Sueldo base mensual en euros.
            contrato (str): Tipo de contrato. Debe estar en CONTRATOS_VALIDOS.
            
        Raises:
            ValueError: Si alguno de los valores no es válido.
        """
        super().__init__()
        self.__nombre = nombre
        self.__rol = self.__validar(rol, self.ROLES_VALIDOS, 'rol')
        self.__categoria = self.__validar(categoria, self.CATEGORIAS_VALIDAS, 'categoria')
        self.__turno = self.__validar(turno, self.TURNOS_VALIDOS, 'turno')
        self.__id_zona = id_zona
        self.__sueldo_base = self.__validar_sueldo(sueldo_base)
        self.__contrato = self.__validar(contrato, self.CONTRATOS_VALIDOS, 'contrato')
        self.__estado = 'Activo'

    @property
    def nombre(self):
        """str: Nombre completo del empleado."""
        return self.__nombre

    @property
    def rol(self):
        """str: Rol del empleado en el parque."""
        return self.__rol

    @property
    def categoria(self):
        """str: Categoría laboral del empleado."""
        return self.__categoria

    @property
    def turno(self):
        """str: Turno de trabajo del empleado."""
        return self.__turno

    @property
    def id_zona(self):
        """int: ID de la zona asignada al empleado."""
        return self.__id_zona

    @property
    def sueldo_base(self):
        """float: Sueldo base mensual en euros."""
        return self.__sueldo_base

    @property
    def contrato(self):
        """str: Tipo de contrato del empleado."""
        return self.__contrato

    @property
    def estado(self):
        """str: Estado laboral actual del empleado."""
        return self.__estado

    @estado.setter
    def estado(self, valor):
        """
        Asigna el estado laboral con validación.
        
        Args:
            valor (str): Nuevo estado. Debe estar en ESTADOS_VALIDOS.
            
        Raises:
            ValueError: Si el estado no es válido.
        """
        if valor not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: {valor}")
        self.__estado = valor

    def __validar(self, valor, validos, campo):
        """
        Valida que un valor esté en la lista de valores permitidos.
        
        Args:
            valor (str): Valor a validar.
            validos (list): Lista de valores permitidos.
            campo (str): Nombre del campo para el mensaje de error.
            
        Returns:
            str: Valor validado.
            
        Raises:
            ValueError: Si el valor no está en la lista de permitidos.
        """
        if valor not in validos:
            raise ValueError(f"{campo} inválido: {valor}")
        return valor

    def __validar_sueldo(self, sueldo):
        """
        Valida que el sueldo base sea positivo.
        
        Args:
            sueldo (float): Sueldo a validar.
            
        Returns:
            float: Sueldo validado.
            
        Raises:
            ValueError: Si el sueldo es menor o igual a cero.
        """
        if sueldo <= 0:
            raise ValueError("El sueldo base debe ser mayor que 0")
        return sueldo

    def calcular_nomina(self, horas_extra=0, bonus=0.0, descuentos=0.0):
        """
        Calcula el salario neto aplicando IRPF según categoría.
        
        Aplica los siguientes porcentajes de IRPF:
        - Junior: 15%
        - Senior: 20%
        - Jefe: 24%
        
        Args:
            horas_extra (int): Número de horas extra a 9€/hora.
            bonus (float): Bonus adicional en euros.
            descuentos (float): Descuentos a aplicar en euros.
            
        Returns:
            float: Salario neto mensual en euros redondeado a 2 decimales.
        """
        irpf = {'Junior': 0.15, 'Senior': 0.20, 'Jefe': 0.24}
        bruto = self.sueldo_base + (horas_extra * 9) + bonus - descuentos
        neto = bruto * (1 - irpf[self.categoria])
        return round(neto, 2)

    def dar_de_baja(self):
        """Da de baja al empleado cambiando su estado a Baja."""
        self.__estado = 'Baja'

    def to_dict(self):
        """
        Convierte el empleado a diccionario para persistir en la BD.
        
        Returns:
            dict: Diccionario con todos los atributos del empleado.
        """
        return {
            'nombre': self.__nombre,
            'rol': self.__rol,
            'categoria': self.__categoria,
            'turno': self.__turno,
            'id_zona': self.__id_zona,
            'sueldo_base': self.__sueldo_base,
            'contrato': self.__contrato,
            'estado': self.__estado,
            'fecha_alta': self.fecha_creacion
        }

    @abstractmethod
    def __str__(self):
        """
        Representación textual del empleado.
        
        Returns:
            str: Cadena descriptiva del empleado.
        """
        pass


class EmpleadoTecnico(Empleado):
    """
    Técnico de mantenimiento con especialidad asignada.
    
    Attributes:
        __especialidad (str): Área de especialización técnica.
    """

    def __init__(self, nombre, categoria, turno, id_zona, sueldo_base, contrato, especialidad):
        """
        Inicializa un técnico con su especialidad.
        
        Args:
            nombre (str): Nombre completo.
            categoria (str): Categoría laboral.
            turno (str): Turno de trabajo.
            id_zona (int): ID de la zona asignada.
            sueldo_base (float): Sueldo base en euros.
            contrato (str): Tipo de contrato.
            especialidad (str): Área de especialización técnica.
        """
        super().__init__(nombre, 'Tecnico', categoria, turno, id_zona, sueldo_base, contrato)
        self.__especialidad = especialidad

    @property
    def especialidad(self):
        """str: Área de especialización del técnico."""
        return self.__especialidad

    def __str__(self):
        return (f"Técnico: {self.nombre} | Especialidad: {self.__especialidad} | "
                f"Turno: {self.turno} | Estado: {self.estado}")


class EmpleadoSocorrista(Empleado):
    """
    Socorrista con certificación oficial de salvamento acuático.
    
    Attributes:
        __certificacion (str): Certificación oficial de socorrismo.
    """

    def __init__(self, nombre, categoria, turno, id_zona, sueldo_base, contrato, certificacion):
        """
        Inicializa un socorrista con su certificación.
        
        Args:
            nombre (str): Nombre completo.
            categoria (str): Categoría laboral.
            turno (str): Turno de trabajo.
            id_zona (int): ID de la zona asignada.
            sueldo_base (float): Sueldo base en euros.
            contrato (str): Tipo de contrato.
            certificacion (str): Certificación oficial de socorrismo.
        """
        super().__init__(nombre, 'Socorrista', categoria, turno, id_zona, sueldo_base, contrato)
        self.__certificacion = certificacion

    @property
    def certificacion(self):
        """str: Certificación oficial del socorrista."""
        return self.__certificacion

    def __str__(self):
        return (f"Socorrista: {self.nombre} | Certificación: {self.__certificacion} | "
                f"Turno: {self.turno} | Estado: {self.estado}")


class EmpleadoAdmin(Empleado):
    """
    Empleado administrativo con nivel de acceso al sistema ERP.
    
    Attributes:
        __nivel_acceso (int): Nivel de acceso al sistema (1-3).
    """

    def __init__(self, nombre, categoria, turno, id_zona, sueldo_base, contrato, nivel_acceso):
        """
        Inicializa un administrativo con su nivel de acceso.
        
        Args:
            nombre (str): Nombre completo.
            categoria (str): Categoría laboral.
            turno (str): Turno de trabajo.
            id_zona (int): ID de la zona asignada.
            sueldo_base (float): Sueldo base en euros.
            contrato (str): Tipo de contrato.
            nivel_acceso (int): Nivel de acceso al sistema ERP.
        """
        super().__init__(nombre, 'Administrativo', categoria, turno, id_zona, sueldo_base, contrato)
        self.__nivel_acceso = nivel_acceso

    @property
    def nivel_acceso(self):
        """int: Nivel de acceso al sistema ERP."""
        return self.__nivel_acceso

    def __str__(self):
        return (f"Administrativo: {self.nombre} | Nivel acceso: {self.__nivel_acceso} | "
                f"Turno: {self.turno} | Estado: {self.estado}")