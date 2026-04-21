# ============================================
# AguaParaíso - Generadores de datos únicos
# Sistema ERP SmartPark Pro
# ============================================

import uuid
from datetime import datetime


class Generators:
    """Genera localizadores y códigos únicos para el sistema."""

    @staticmethod
    def generar_localizador_ticket():
        """Genera un localizador único para tickets: AGP-2026-XXXXXXXX"""
        anio = datetime.now().year
        codigo = str(uuid.uuid4())[:8].upper()
        return f"AGP-{anio}-{codigo}"

    @staticmethod
    def generar_codigo_reserva_vip():
        """Genera un código único para reservas VIP: VIP-XXXXXXXX"""
        codigo = str(uuid.uuid4())[:8].upper()
        return f"VIP-{codigo}"