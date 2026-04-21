# ============================================
# AguaParaíso - Clase Nomina
# Sistema ERP SmartPark Pro
# ============================================

from models.entidad import Entidad


class Nomina(Entidad):
    """Representa la nómina mensual de un empleado."""

    PRECIO_HORA_EXTRA = 9.0
    BONUS_TEMPORADA_ALTA = 200.0
    MESES_TEMPORADA_ALTA = ['2025-07', '2025-08', '2026-07', '2026-08']

    def __init__(self, id_empleado, mes, sueldo_base, categoria,
                 tipo_contrato, horas_extra=0, descuentos=0.0):
        super().__init__()
        self.__id_empleado = id_empleado
        self.__mes = mes
        self.__sueldo_base = sueldo_base
        self.__categoria = categoria
        self.__tipo_contrato = tipo_contrato
        self.__horas_extra = horas_extra
        self.__descuentos = descuentos
        self.__bonus = self.__calcular_bonus()
        self.__irpf = self.__calcular_irpf()
        self.__total_neto = self.__calcular_neto()

    def __calcular_bonus(self):
        if self.__mes in self.MESES_TEMPORADA_ALTA:
            return self.BONUS_TEMPORADA_ALTA
        return 0.0

    def __calcular_irpf(self):
        irpf = {'Junior': 0.15, 'Senior': 0.20, 'Jefe': 0.24}
        return irpf.get(self.__categoria, 0.15)

    def __calcular_neto(self):
        bruto = (self.__sueldo_base +
                 (self.__horas_extra * self.PRECIO_HORA_EXTRA) +
                 self.__bonus - self.__descuentos)
        return round(bruto * (1 - self.__irpf), 2)

    @property
    def id_empleado(self):
        return self.__id_empleado

    @property
    def mes(self):
        return self.__mes

    @property
    def sueldo_base(self):
        return self.__sueldo_base

    @property
    def horas_extra(self):
        return self.__horas_extra

    @property
    def bonus(self):
        return self.__bonus

    @property
    def descuentos(self):
        return self.__descuentos

    @property
    def irpf(self):
        return self.__irpf

    @property
    def tipo_contrato(self):
        return self.__tipo_contrato

    @property
    def total_neto(self):
        return self.__total_neto

    def to_dict(self):
        return {
            'id_empleado': self.__id_empleado,
            'mes': self.__mes,
            'sueldo_base': self.__sueldo_base,
            'horas_extra': self.__horas_extra,
            'bonus': self.__bonus,
            'descuentos': self.__descuentos,
            'irpf': self.__irpf * 100,
            'tipo_contrato': self.__tipo_contrato,
            'total_neto': self.__total_neto
        }

    def __str__(self):
        return (f"Nómina: {self.__mes} | "
                f"Empleado ID: {self.__id_empleado} | "
                f"Bruto: {self.__sueldo_base + self.__horas_extra * self.PRECIO_HORA_EXTRA + self.__bonus}€ | "
                f"Neto: {self.__total_neto}€")