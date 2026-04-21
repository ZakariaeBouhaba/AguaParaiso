# ============================================
# AguaParaíso - Clase Visitante
# Sistema ERP SmartPark Pro
# ============================================

from models.entidad import Entidad
from datetime import datetime


class Visitante(Entidad):
    """Representa un visitante del parque AguaParaíso."""

    TIPOS_VALIDOS = ['Adulto', 'Nino', 'Residente']

    def __init__(self, nombre, tipo):
        super().__init__()
        self.__nombre = nombre
        self.__tipo = self.__validar_tipo(tipo)
        self.__fecha_visita = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__id_ticket = None

    def __validar_tipo(self, tipo):
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de visitante inválido: {tipo}")
        return tipo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def tipo(self):
        return self.__tipo

    @property
    def fecha_visita(self):
        return self.__fecha_visita

    @property
    def id_ticket(self):
        return self.__id_ticket

    @id_ticket.setter
    def id_ticket(self, valor):
        self.__id_ticket = valor

    def to_dict(self):
        return {
            'nombre': self.__nombre,
            'tipo': self.__tipo,
            'fecha_visita': self.__fecha_visita,
            'id_ticket': self.__id_ticket
        }

    def __str__(self):
        return (f"Visitante: {self.__nombre} | "
                f"Tipo: {self.__tipo} | "
                f"Fecha: {self.__fecha_visita}")