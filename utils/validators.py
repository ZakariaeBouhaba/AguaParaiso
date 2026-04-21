# ============================================
# AguaParaíso - Validadores de datos
# Sistema ERP SmartPark Pro
# ============================================

from exceptions.exceptions import DatosInvalidosError


class Validators:
    """Valida los datos de entrada del sistema."""

    @staticmethod
    def validar_texto(valor, campo, min_len=1, max_len=100):
        if not isinstance(valor, str) or len(valor.strip()) < min_len:
            raise DatosInvalidosError(campo, valor, f"debe tener al menos {min_len} caracteres")
        if len(valor) > max_len:
            raise DatosInvalidosError(campo, valor, f"no puede superar {max_len} caracteres")
        return valor.strip()

    @staticmethod
    def validar_numero_positivo(valor, campo):
        try:
            numero = float(valor)
            if numero <= 0:
                raise DatosInvalidosError(campo, valor, "debe ser mayor que 0")
            return numero
        except (TypeError, ValueError):
            raise DatosInvalidosError(campo, valor, "debe ser un número válido")

    @staticmethod
    def validar_entero_positivo(valor, campo):
        try:
            numero = int(valor)
            if numero <= 0:
                raise DatosInvalidosError(campo, valor, "debe ser un entero positivo")
            return numero
        except (TypeError, ValueError):
            raise DatosInvalidosError(campo, valor, "debe ser un número entero válido")

    @staticmethod
    def validar_opcion(valor, opciones_validas, campo):
        if valor not in opciones_validas:
            raise DatosInvalidosError(campo, valor, f"debe ser uno de: {', '.join(opciones_validas)}")
        return valor

    @staticmethod
    def validar_hora(valor, campo):
        try:
            partes = valor.split(':')
            if len(partes) != 2:
                raise ValueError
            hora, minuto = int(partes[0]), int(partes[1])
            if not (0 <= hora <= 23 and 0 <= minuto <= 59):
                raise ValueError
            return valor
        except (ValueError, AttributeError):
            raise DatosInvalidosError(campo, valor, "formato de hora inválido, use HH:MM")

    @staticmethod
    def validar_username(valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatosInvalidosError('username', valor, "debe tener al menos 3 caracteres")
        if ' ' in valor:
            raise DatosInvalidosError('username', valor, "no puede contener espacios")
        return valor.strip().lower()

    @staticmethod
    def validar_password(valor):
        if not isinstance(valor, str) or len(valor) < 6:
            raise DatosInvalidosError('password', valor, "debe tener al menos 6 caracteres")
        return valor