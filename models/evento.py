# ============================================
# AguaParaíso - Clase Evento
# Sistema ERP SmartPark Pro
# ============================================

from models.entidad import Entidad
from datetime import datetime


class Evento(Entidad):
    """Representa un evento aleatorio en el parque."""

    TIPOS_VALIDOS = ['Averia', 'Climatico', 'Sanitario', 'Stock', 'Aforo']
    ESTADOS_VALIDOS = ['Activo', 'Resuelto']

    def __init__(self, tipo, descripcion, id_zona=None, id_empleado=None):
        super().__init__()
        self.__tipo = self.__validar_tipo(tipo)
        self.__descripcion = descripcion
        self.__id_zona = id_zona
        self.__id_empleado = id_empleado
        self.__estado = 'Activo'
        self.__fecha_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__fecha_fin = None

    def __validar_tipo(self, tipo):
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de evento inválido: {tipo}")
        return tipo

    @property
    def tipo(self):
        return self.__tipo

    @property
    def descripcion(self):
        return self.__descripcion

    @property
    def id_zona(self):
        return self.__id_zona

    @property
    def id_empleado(self):
        return self.__id_empleado

    @property
    def estado(self):
        return self.__estado

    @property
    def fecha_inicio(self):
        return self.__fecha_inicio

    @property
    def fecha_fin(self):
        return self.__fecha_fin

    def resolver(self, id_empleado=None):
        """Marca el evento como resuelto."""
        self.__estado = 'Resuelto'
        self.__fecha_fin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if id_empleado:
            self.__id_empleado = id_empleado

    def esta_activo(self):
        return self.__estado == 'Activo'

    def to_dict(self):
        return {
            'tipo': self.__tipo,
            'descripcion': self.__descripcion,
            'id_zona': self.__id_zona,
            'estado': self.__estado,
            'fecha_inicio': self.__fecha_inicio,
            'fecha_fin': self.__fecha_fin,
            'id_empleado': self.__id_empleado
        }

    def __str__(self):
        return (f"Evento: {self.__tipo} | "
                f"Estado: {self.__estado} | "
                f"Descripción: {self.__descripcion}")