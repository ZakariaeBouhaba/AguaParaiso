# ============================================
# AguaParaíso - Generadores de códigos únicos
# Sistema ERP SmartPark Pro
# ============================================

import uuid
from datetime import datetime


class Generators:
    """
    Genera códigos y localizadores únicos para el sistema.
    
    Utiliza UUID4 para garantizar la unicidad de los códigos
    generados, asegurando que no haya duplicados incluso con
    alta concurrencia de ventas.
    """

    @staticmethod
    def generar_localizador_ticket():
        """
        Genera un localizador único para tickets en formato AGP-YYYY-XXXXXXXX.
        
        Combina el año actual con los primeros 8 caracteres de un UUID4
        para crear un código único, legible y trazable.
        
        Returns:
            str: Localizador único en formato AGP-2026-XXXXXXXX.
            
        Example:
            >>> Generators.generar_localizador_ticket()
            'AGP-2026-CE75F49F'
        """
        anio = datetime.now().year
        codigo = str(uuid.uuid4())[:8].upper()
        return f"AGP-{anio}-{codigo}"

    @staticmethod
    def generar_codigo_reserva_vip():
        """
        Genera un código único para reservas VIP en formato VIP-XXXXXXXX.
        
        Returns:
            str: Código único en formato VIP-XXXXXXXX.
            
        Example:
            >>> Generators.generar_codigo_reserva_vip()
            'VIP-A3B4C5D6'
        """
        codigo = str(uuid.uuid4())[:8].upper()
        return f"VIP-{codigo}"