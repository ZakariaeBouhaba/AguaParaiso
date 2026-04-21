# ============================================
# AguaParaíso - Clase Atraccion y subclases
# Sistema ERP SmartPark Pro
# ============================================

from abc import abstractmethod
from models.entidad import Entidad
from exceptions.exceptions import AforoCompletoError, ZonaCerradaError


class Atraccion(Entidad):
    """Clase base abstracta para todas las atracciones."""

    TIPOS_VALIDOS = ['Adrenalina', 'Familia', 'Relax', 'Infantil']
    ESTADOS_VALIDOS = ['Activa', 'Cerrada', 'Mantenimiento']

    def __init__(self, nombre, tipo, altura_minima, aforo_maximo, id_zona):
        super().__init__()
        self.__nombre = nombre
        self.__tipo = self.__validar_tipo(tipo)
        self.__altura_minima = self.__validar_altura(altura_minima)
        self.__aforo_maximo = aforo_maximo
        self.__estado = 'Activa'
        self.__id_zona = id_zona

    @property
    def nombre(self):
        return self.__nombre

    @property
    def tipo(self):
        return self.__tipo

    @property
    def altura_minima(self):
        return self.__altura_minima

    @property
    def aforo_maximo(self):
        return self.__aforo_maximo

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        if valor not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: {valor}")
        self.__estado = valor

    @property
    def id_zona(self):
        return self.__id_zona

    def __validar_tipo(self, tipo):
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo inválido: {tipo}")
        return tipo

    def __validar_altura(self, altura):
        if altura < 0:
            raise ValueError("La altura mínima no puede ser negativa")
        return altura

    def esta_disponible(self):
        return self.__estado == 'Activa'

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class AtraccionTobogan(Atraccion):
    """Tobogán con velocidad máxima."""

    def __init__(self, nombre, tipo, altura_minima, aforo_maximo, id_zona, velocidad_max):
        super().__init__(nombre, tipo, altura_minima, aforo_maximo, id_zona)
        self.__velocidad_max = velocidad_max

    @property
    def velocidad_max(self):
        return self.__velocidad_max

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'tipo': self.tipo,
            'altura_minima': self.altura_minima,
            'aforo_maximo': self.aforo_maximo,
            'estado': self.estado,
            'id_zona': self.id_zona,
            'velocidad_max': self.__velocidad_max
        }

    def __str__(self):
        return (f"Tobogán: {self.nombre} | Tipo: {self.tipo} | "
                f"Altura mín: {self.altura_minima}m | "
                f"Velocidad máx: {self.__velocidad_max}km/h | "
                f"Estado: {self.estado}")


class AtraccionPiscina(Atraccion):
    """Piscina con temperatura y sistema de olas."""

    def __init__(self, nombre, tipo, altura_minima, aforo_maximo, id_zona, temperatura=26.0):
        super().__init__(nombre, tipo, altura_minima, aforo_maximo, id_zona)
        self.__temperatura = temperatura
        self.__olas_activas = False

    @property
    def temperatura(self):
        return self.__temperatura

    @temperatura.setter
    def temperatura(self, valor):
        if valor < 18.0 or valor > 32.0:
            from exceptions.exceptions import TemperaturaInvalidaError
            raise TemperaturaInvalidaError(valor)
        self.__temperatura = valor

    @property
    def olas_activas(self):
        return self.__olas_activas

    def activar_olas(self):
        self.__olas_activas = True

    def desactivar_olas(self):
        self.__olas_activas = False

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'tipo': self.tipo,
            'altura_minima': self.altura_minima,
            'aforo_maximo': self.aforo_maximo,
            'estado': self.estado,
            'id_zona': self.id_zona,
            'temperatura': self.__temperatura,
            'olas_activas': self.__olas_activas
        }

    def __str__(self):
        return (f"Piscina: {self.nombre} | Tipo: {self.tipo} | "
                f"Temperatura: {self.__temperatura}°C | "
                f"Olas: {'Sí' if self.__olas_activas else 'No'} | "
                f"Estado: {self.estado}")


class AtraccionRio(Atraccion):
    """Río lento con gestión de flotadores."""

    def __init__(self, nombre, tipo, altura_minima, aforo_maximo, id_zona, num_flotadores):
        super().__init__(nombre, tipo, altura_minima, aforo_maximo, id_zona)
        self.__num_flotadores = num_flotadores
        self.__flotadores_disponibles = num_flotadores

    @property
    def flotadores_disponibles(self):
        return self.__flotadores_disponibles

    def alquilar_flotador(self):
        if self.__flotadores_disponibles <= 0:
            from exceptions.exceptions import StockInsuficienteError
            raise StockInsuficienteError('Flotadores', 0, 1)
        self.__flotadores_disponibles -= 1

    def devolver_flotador(self):
        if self.__flotadores_disponibles < self.__num_flotadores:
            self.__flotadores_disponibles += 1

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'tipo': self.tipo,
            'altura_minima': self.altura_minima,
            'aforo_maximo': self.aforo_maximo,
            'estado': self.estado,
            'id_zona': self.id_zona,
            'num_flotadores': self.__num_flotadores,
            'flotadores_disponibles': self.__flotadores_disponibles
        }

    def __str__(self):
        return (f"Río: {self.nombre} | Tipo: {self.tipo} | "
                f"Flotadores: {self.__flotadores_disponibles}/{self.__num_flotadores} | "
                f"Estado: {self.estado}")