# ============================================
# AguaParaíso - Clase ParqueTematico
# Sistema ERP SmartPark Pro
# ============================================

from datetime import datetime


class ParqueTematico:
    """Clase raíz que representa el parque AguaParaíso."""

    def __init__(self, nombre, temporada='verano'):
        self.__nombre = nombre
        self.__temporada = temporada
        self.__estado = 'Abierto'
        self.__zonas = {}
        self.__empleados = {}
        self.__eventos_activos = []

    ESTADOS_VALIDOS = ['Abierto', 'Cerrado', 'AlertaClimatica', 'EmergenciaSanitaria', 'AforoCompleto']

    @property
    def nombre(self):
        return self.__nombre

    @property
    def temporada(self):
        return self.__temporada

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        if valor not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: {valor}")
        self.__estado = valor

    def esta_abierto(self):
        return self.__estado == 'Abierto'

    def agregar_zona(self, zona):
        self.__zonas[zona.nombre] = zona

    def obtener_zona(self, nombre):
        return self.__zonas.get(nombre)

    def obtener_zonas(self):
        return list(self.__zonas.values())

    def agregar_evento(self, evento):
        self.__eventos_activos.append(evento)

    def obtener_eventos_activos(self):
        return [e for e in self.__eventos_activos if e.esta_activo()]

    def total_visitantes(self):
        return sum(z.aforo_actual for z in self.__zonas.values())

    def __str__(self):
        return (f"Parque: {self.__nombre} | "
                f"Estado: {self.__estado} | "
                f"Temporada: {self.__temporada} | "
                f"Zonas: {len(self.__zonas)}")