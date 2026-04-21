# ============================================
# AguaParaíso - Clase Nomina
# Sistema ERP SmartPark Pro
# ============================================

from models.entidad import Entidad


class Nomina(Entidad):
    """
    Representa la nómina mensual de un empleado del parque.
    
    Calcula automáticamente el salario neto aplicando el IRPF
    según la categoría del empleado y añadiendo el bonus de
    temporada alta de 200€ en los meses de julio y agosto.
    
    Attributes:
        __id_empleado (int): ID del empleado al que pertenece la nómina.
        __mes (str): Mes de la nómina en formato YYYY-MM.
        __sueldo_base (float): Sueldo base mensual en euros.
        __categoria (str): Categoría laboral para calcular el IRPF.
        __tipo_contrato (str): Tipo de contrato del empleado.
        __horas_extra (int): Número de horas extra realizadas.
        __descuentos (float): Descuentos aplicados en euros.
        __bonus (float): Bonus de temporada alta en euros.
        __irpf (float): Porcentaje de IRPF aplicado.
        __total_neto (float): Salario neto final en euros.
    """

    PRECIO_HORA_EXTRA = 9.0
    BONUS_TEMPORADA_ALTA = 200.0
    MESES_TEMPORADA_ALTA = ['2025-07', '2025-08', '2026-07', '2026-08']

    def __init__(self, id_empleado, mes, sueldo_base, categoria,
                 tipo_contrato, horas_extra=0, descuentos=0.0):
        """
        Inicializa la nómina calculando automáticamente bonus, IRPF y neto.
        
        Args:
            id_empleado (int): ID del empleado.
            mes (str): Mes en formato YYYY-MM.
            sueldo_base (float): Sueldo base mensual en euros.
            categoria (str): Categoría laboral (Junior, Senior, Jefe).
            tipo_contrato (str): Tipo de contrato (Fijo, Temporal).
            horas_extra (int): Horas extra a 9€/hora.
            descuentos (float): Descuentos a aplicar en euros.
        """
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
        """
        Calcula el bonus de temporada alta.
        
        Aplica 200€ de bonus en los meses de julio y agosto.
        
        Returns:
            float: Importe del bonus en euros.
        """
        if self.__mes in self.MESES_TEMPORADA_ALTA:
            return self.BONUS_TEMPORADA_ALTA
        return 0.0

    def __calcular_irpf(self):
        """
        Calcula el porcentaje de IRPF según la categoría.
        
        Returns:
            float: Porcentaje de IRPF (0.15, 0.20 o 0.24).
        """
        irpf = {'Junior': 0.15, 'Senior': 0.20, 'Jefe': 0.24}
        return irpf.get(self.__categoria, 0.15)

    def __calcular_neto(self):
        """
        Calcula el salario neto aplicando IRPF sobre el bruto.
        
        Returns:
            float: Salario neto redondeado a 2 decimales.
        """
        bruto = (self.__sueldo_base +
                 (self.__horas_extra * self.PRECIO_HORA_EXTRA) +
                 self.__bonus - self.__descuentos)
        return round(bruto * (1 - self.__irpf), 2)

    @property
    def id_empleado(self):
        """int: ID del empleado al que pertenece la nómina."""
        return self.__id_empleado

    @property
    def mes(self):
        """str: Mes de la nómina en formato YYYY-MM."""
        return self.__mes

    @property
    def sueldo_base(self):
        """float: Sueldo base mensual en euros."""
        return self.__sueldo_base

    @property
    def horas_extra(self):
        """int: Número de horas extra realizadas."""
        return self.__horas_extra

    @property
    def bonus(self):
        """float: Bonus de temporada alta en euros."""
        return self.__bonus

    @property
    def descuentos(self):
        """float: Descuentos aplicados en euros."""
        return self.__descuentos

    @property
    def irpf(self):
        """float: Porcentaje de IRPF aplicado."""
        return self.__irpf

    @property
    def tipo_contrato(self):
        """str: Tipo de contrato del empleado."""
        return self.__tipo_contrato

    @property
    def total_neto(self):
        """float: Salario neto final en euros."""
        return self.__total_neto

    def to_dict(self):
        """
        Convierte la nómina a diccionario para persistir en la BD.
        
        Returns:
            dict: Diccionario con todos los atributos de la nómina.
        """
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
        """
        Representación textual de la nómina.
        
        Returns:
            str: Cadena con mes, empleado, bruto y neto.
        """
        bruto = (self.__sueldo_base +
                 self.__horas_extra * self.PRECIO_HORA_EXTRA +
                 self.__bonus)
        return (f"Nómina: {self.__mes} | "
                f"Empleado ID: {self.__id_empleado} | "
                f"Bruto: {bruto}€ | "
                f"Neto: {self.__total_neto}€")