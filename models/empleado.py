# ============================================
# AguaParaíso - Clase Empleado y subclases
# Sistema ERP SmartPark Pro
# ============================================

from abc import abstractmethod
from models.entidad import Entidad


class Empleado(Entidad):
    """Clase base abstracta para todos los empleados."""

    ROLES_VALIDOS = ['Socorrista', 'Tecnico', 'Taquillero', 'Camarero',
                     'PersonalVIP', 'Vigilante', 'Limpiador', 'Administrativo', 'Enfermero']
    CATEGORIAS_VALIDAS = ['Junior', 'Senior', 'Jefe']
    TURNOS_VALIDOS = ['Manana', 'Tarde', 'Mantenimiento']
    ESTADOS_VALIDOS = ['Activo', 'Baja', 'Vacaciones']
    CONTRATOS_VALIDOS = ['Fijo', 'Temporal']

    def __init__(self, nombre, rol, categoria, turno, id_zona, sueldo_base, contrato):
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
        return self.__nombre

    @property
    def rol(self):
        return self.__rol

    @property
    def categoria(self):
        return self.__categoria

    @property
    def turno(self):
        return self.__turno

    @property
    def id_zona(self):
        return self.__id_zona

    @property
    def sueldo_base(self):
        return self.__sueldo_base

    @property
    def contrato(self):
        return self.__contrato

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        if valor not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: {valor}")
        self.__estado = valor

    def __validar(self, valor, validos, campo):
        if valor not in validos:
            raise ValueError(f"{campo} inválido: {valor}")
        return valor

    def __validar_sueldo(self, sueldo):
        if sueldo <= 0:
            raise ValueError("El sueldo base debe ser mayor que 0")
        return sueldo

    def calcular_nomina(self, horas_extra=0, bonus=0.0, descuentos=0.0):
        """Calcula el salario neto aplicando IRPF."""
        irpf = {'Junior': 0.15, 'Senior': 0.20, 'Jefe': 0.24}
        bruto = self.sueldo_base + (horas_extra * 9) + bonus - descuentos
        neto = bruto * (1 - irpf[self.categoria])
        return round(neto, 2)
    
    def dar_de_baja(self):
        self.__estado = 'Baja'

    def to_dict(self):
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
        pass


class EmpleadoTecnico(Empleado):
    def __init__(self, nombre, categoria, turno, id_zona, sueldo_base, contrato, especialidad):
        super().__init__(nombre, 'Tecnico', categoria, turno, id_zona, sueldo_base, contrato)
        self.__especialidad = especialidad

    @property
    def especialidad(self):
        return self.__especialidad

    def __str__(self):
        return (f"Técnico: {self.nombre} | Especialidad: {self.__especialidad} | "
                f"Turno: {self.turno} | Estado: {self.estado}")


class EmpleadoSocorrista(Empleado):
    def __init__(self, nombre, categoria, turno, id_zona, sueldo_base, contrato, certificacion):
        super().__init__(nombre, 'Socorrista', categoria, turno, id_zona, sueldo_base, contrato)
        self.__certificacion = certificacion

    @property
    def certificacion(self):
        return self.__certificacion

    def __str__(self):
        return (f"Socorrista: {self.nombre} | Certificación: {self.__certificacion} | "
                f"Turno: {self.turno} | Estado: {self.estado}")


class EmpleadoAdmin(Empleado):
    def __init__(self, nombre, categoria, turno, id_zona, sueldo_base, contrato, nivel_acceso):
        super().__init__(nombre, 'Administrativo', categoria, turno, id_zona, sueldo_base, contrato)
        self.__nivel_acceso = nivel_acceso

    @property
    def nivel_acceso(self):
        return self.__nivel_acceso

    def __str__(self):
        return (f"Administrativo: {self.nombre} | Nivel acceso: {self.__nivel_acceso} | "
                f"Turno: {self.turno} | Estado: {self.estado}")