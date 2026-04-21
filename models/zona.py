# ============================================
# AguaParaíso - Clase Zona
# Sistema ERP SmartPark Pro
# ============================================

from models.entidad import Entidad
from exceptions.exceptions import AforoCompletoError, ZonaCerradaError


class Zona(Entidad):
    """Representa una zona del parque AguaParaíso."""

    TIPOS_VALIDOS = ['Toboganes', 'Piscinas', 'RioLento', 'Restauracion', 'Servicios', 'VIP']
    ESTADOS_VALIDOS = ['Abierta', 'Cerrada', 'Alerta']

    def __init__(self, nombre, tipo, aforo_maximo, hora_apertura, hora_cierre):
        super().__init__()
        self.__nombre = nombre
        self.__tipo = self.__validar_tipo(tipo)
        self.__aforo_maximo = self.__validar_aforo_maximo(aforo_maximo)
        self.__aforo_actual = 0
        self.__estado = 'Abierta'
        self.__hora_apertura = hora_apertura
        self.__hora_cierre = hora_cierre

    # ---- Propiedades ----
    @property
    def nombre(self):
        return self.__nombre

    @property
    def tipo(self):
        return self.__tipo

    @property
    def aforo_maximo(self):
        return self.__aforo_maximo

    @property
    def aforo_actual(self):
        return self.__aforo_actual

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        if valor not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: {valor}")
        self.__estado = valor

    @property
    def hora_apertura(self):
        return self.__hora_apertura

    @property
    def hora_cierre(self):
        return self.__hora_cierre

    # ---- Validaciones privadas ----
    def __validar_tipo(self, tipo):
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de zona inválido: {tipo}")
        return tipo

    def __validar_aforo_maximo(self, aforo):
        if not isinstance(aforo, int) or aforo <= 0:
            raise ValueError("El aforo máximo debe ser un entero positivo")
        return aforo

    # ---- Métodos de negocio ----
    def incrementar_aforo(self):
        """Incrementa el aforo actual en 1."""
        if self.__estado != 'Abierta':
            raise ZonaCerradaError(self.__nombre, self.__estado)
        if self.__aforo_actual >= self.__aforo_maximo:
            raise AforoCompletoError(self.__nombre, self.__aforo_actual, self.__aforo_maximo)
        self.__aforo_actual += 1

    def decrementar_aforo(self):
        """Decrementa el aforo actual en 1."""
        if self.__aforo_actual > 0:
            self.__aforo_actual -= 1

    def esta_disponible(self):
        """Devuelve True si la zona está abierta y con aforo disponible."""
        return self.__estado == 'Abierta' and self.__aforo_actual < self.__aforo_maximo

    def porcentaje_ocupacion(self):
        """Devuelve el porcentaje de ocupación de la zona."""
        return round((self.__aforo_actual / self.__aforo_maximo) * 100, 2)

    # ---- Métodos abstractos implementados ----
    def to_dict(self):
        return {
            'id_zona': self.id,
            'nombre': self.__nombre,
            'tipo': self.__tipo,
            'aforo_maximo': self.__aforo_maximo,
            'aforo_actual': self.__aforo_actual,
            'estado': self.__estado,
            'hora_apertura': self.__hora_apertura,
            'hora_cierre': self.__hora_cierre,
            'fecha_creacion': self.fecha_creacion
        }

    def __str__(self):
        return (f"Zona: {self.__nombre} | Tipo: {self.__tipo} | "
                f"Estado: {self.__estado} | "
                f"Aforo: {self.__aforo_actual}/{self.__aforo_maximo}")