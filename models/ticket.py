# ============================================
# AguaParaíso - Clase Ticket
# Sistema ERP SmartPark Pro
# ============================================

from models.entidad import Entidad
import uuid


class Ticket(Entidad):
    """Representa una entrada al parque AguaParaíso."""

    TIPOS_VALIDOS = ['Normal', 'Premium', 'TodoIncluido']
    TIPOS_VISITANTE_VALIDOS = ['Adulto', 'Nino', 'Residente']
    IVA = 10.0

    PRECIOS = {
        'Normal': {'Adulto': 25.00, 'Nino': 15.00, 'Residente': 18.00},
        'Premium': {'Adulto': 45.00, 'Nino': 28.00, 'Residente': 35.00},
        'TodoIncluido': {'Adulto': 65.00, 'Nino': 40.00, 'Residente': 50.00},
    }

    PRECIO_FAST_PASS = 28.00

    def __init__(self, tipo, tipo_visitante, id_empleado, id_visitante=None, fast_pass=False):
        super().__init__()
        self.__tipo = self.__validar_tipo(tipo)
        self.__tipo_visitante = self.__validar_tipo_visitante(tipo_visitante)
        self.__id_empleado = id_empleado
        self.__id_visitante = id_visitante
        self.__fast_pass = fast_pass
        self.__localizador = self.__generar_localizador()
        self.__precio_base = self.__calcular_precio_base()
        self.__precio_total = self.__calcular_precio_total()

    def __validar_tipo(self, tipo):
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de ticket inválido: {tipo}")
        return tipo

    def __validar_tipo_visitante(self, tipo):
        if tipo not in self.TIPOS_VISITANTE_VALIDOS:
            raise ValueError(f"Tipo de visitante inválido: {tipo}")
        return tipo

    def __generar_localizador(self):
        from datetime import datetime
        anio = datetime.now().year
        codigo = str(uuid.uuid4())[:8].upper()
        return f"AGP-{anio}-{codigo}"

    def __calcular_precio_base(self):
        base = self.PRECIOS[self.__tipo][self.__tipo_visitante]
        if self.__fast_pass:
            base += self.PRECIO_FAST_PASS
        return base

    def __calcular_precio_total(self):
        return round(self.__precio_base * (1 + self.IVA / 100), 2)

    @property
    def tipo(self):
        return self.__tipo

    @property
    def tipo_visitante(self):
        return self.__tipo_visitante

    @property
    def localizador(self):
        return self.__localizador

    @property
    def precio_base(self):
        return self.__precio_base

    @property
    def precio_total(self):
        return self.__precio_total

    @property
    def fast_pass(self):
        return self.__fast_pass

    @property
    def id_empleado(self):
        return self.__id_empleado

    @property
    def id_visitante(self):
        return self.__id_visitante

    def to_dict(self):
        return {
            'localizador': self.__localizador,
            'tipo': self.__tipo,
            'tipo_visitante': self.__tipo_visitante,
            'precio_base': self.__precio_base,
            'iva': self.IVA,
            'precio_total': self.__precio_total,
            'fast_pass': 1 if self.__fast_pass else 0,
            'id_empleado': self.__id_empleado,
            'id_visitante': self.__id_visitante,
        }

    def __str__(self):
        return (f"Ticket: {self.__localizador} | Tipo: {self.__tipo} | "
                f"Visitante: {self.__tipo_visitante} | "
                f"Fast Pass: {'Sí' if self.__fast_pass else 'No'} | "
                f"Total: {self.__precio_total}€")