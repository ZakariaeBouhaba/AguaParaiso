# ============================================
# AguaParaíso - Excepciones personalizadas
# Sistema ERP SmartPark Pro
# ============================================


class AguaParaisoException(Exception):
    """Clase base para todas las excepciones del sistema AguaParaíso."""

    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

    def __str__(self):
        return f"[AguaParaíso Error] {self.mensaje}"


class AforoCompletoError(AguaParaisoException):
    """Se lanza cuando una zona o atracción supera su aforo máximo."""

    def __init__(self, zona, aforo_actual, aforo_maximo):
        self.zona = zona
        self.aforo_actual = aforo_actual
        self.aforo_maximo = aforo_maximo
        mensaje = (
            f"Aforo completo en '{zona}': "
            f"{aforo_actual}/{aforo_maximo} personas"
        )
        super().__init__(mensaje)


class TemperaturaInvalidaError(AguaParaisoException):
    """Se lanza cuando la temperatura del agua está fuera de rango seguro."""

    def __init__(self, temperatura, minima=18.0, maxima=32.0):
        self.temperatura = temperatura
        self.minima = minima
        self.maxima = maxima
        mensaje = (
            f"Temperatura inválida: {temperatura}°C. "
            f"Rango permitido: {minima}°C - {maxima}°C"
        )
        super().__init__(mensaje)


class StockInsuficienteError(AguaParaisoException):
    """Se lanza cuando el stock de un producto está por debajo del mínimo."""

    def __init__(self, producto, stock_actual, stock_minimo):
        self.producto = producto
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        mensaje = (
            f"Stock insuficiente de '{producto}': "
            f"{stock_actual} unidades (mínimo: {stock_minimo})"
        )
        super().__init__(mensaje)


class SaldoInsuficienteError(AguaParaisoException):
    """Se lanza cuando el pago de un ticket es insuficiente."""

    def __init__(self, precio_total, pago_recibido):
        self.precio_total = precio_total
        self.pago_recibido = pago_recibido
        mensaje = (
            f"Saldo insuficiente: se requieren {precio_total:.2f}€ "
            f"pero se recibieron {pago_recibido:.2f}€"
        )
        super().__init__(mensaje)


class ZonaCerradaError(AguaParaisoException):
    """Se lanza cuando se intenta acceder a una zona cerrada o en alerta."""

    def __init__(self, zona, estado):
        self.zona = zona
        self.estado = estado
        mensaje = (
            f"La zona '{zona}' no está disponible. "
            f"Estado actual: {estado}"
        )
        super().__init__(mensaje)


class CredencialesInvalidasError(AguaParaisoException):
    """Se lanza cuando las credenciales de login son incorrectas."""

    def __init__(self, username):
        self.username = username
        mensaje = f"Credenciales incorrectas para el usuario '{username}'"
        super().__init__(mensaje)


class UsuarioBloqueadoError(AguaParaisoException):
    """Se lanza cuando un usuario está bloqueado por intentos fallidos."""

    def __init__(self, username, minutos=15):
        self.username = username
        self.minutos = minutos
        mensaje = (
            f"Usuario '{username}' bloqueado por {minutos} minutos "
            f"debido a demasiados intentos fallidos"
        )
        super().__init__(mensaje)


class DatosInvalidosError(AguaParaisoException):
    """Se lanza cuando los datos de un formulario no son válidos."""

    def __init__(self, campo, valor, motivo):
        self.campo = campo
        self.valor = valor
        self.motivo = motivo
        mensaje = (
            f"Datos inválidos en el campo '{campo}': "
            f"'{valor}' — {motivo}"
        )
        super().__init__(mensaje)