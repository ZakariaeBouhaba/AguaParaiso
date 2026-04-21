# ============================================
# AguaParaíso - Jerarquía de Excepciones
# Sistema ERP SmartPark Pro
# ============================================


class AguaParaisoException(Exception):
    """
    Clase base para todas las excepciones del sistema AguaParaíso.
    
    Todas las excepciones custom del sistema heredan de esta clase,
    lo que permite capturar cualquier excepción del sistema con un
    único bloque except AguaParaisoException.
    
    Attributes:
        mensaje (str): Descripción detallada del error.
    """

    def __init__(self, mensaje):
        """
        Inicializa la excepción con un mensaje descriptivo.
        
        Args:
            mensaje (str): Descripción del error ocurrido.
        """
        self.mensaje = mensaje
        super().__init__(self.mensaje)

    def __str__(self):
        """
        Representación textual de la excepción.
        
        Returns:
            str: Mensaje de error con prefijo del sistema.
        """
        return f"[AguaParaíso Error] {self.mensaje}"


class AforoCompletoError(AguaParaisoException):
    """
    Se lanza cuando una zona o atracción supera su aforo máximo.
    
    Attributes:
        zona (str): Nombre de la zona con aforo completo.
        aforo_actual (int): Número actual de personas en la zona.
        aforo_maximo (int): Capacidad máxima permitida.
    """

    def __init__(self, zona, aforo_actual, aforo_maximo):
        """
        Inicializa el error con los datos de aforo de la zona.
        
        Args:
            zona (str): Nombre de la zona afectada.
            aforo_actual (int): Número actual de personas.
            aforo_maximo (int): Capacidad máxima permitida.
        """
        self.zona = zona
        self.aforo_actual = aforo_actual
        self.aforo_maximo = aforo_maximo
        mensaje = (
            f"Aforo completo en '{zona}': "
            f"{aforo_actual}/{aforo_maximo} personas"
        )
        super().__init__(mensaje)


class TemperaturaInvalidaError(AguaParaisoException):
    """
    Se lanza cuando la temperatura del agua está fuera del rango seguro.
    
    El rango seguro para las piscinas del parque es de 18°C a 32°C.
    
    Attributes:
        temperatura (float): Temperatura inválida detectada.
        minima (float): Temperatura mínima permitida.
        maxima (float): Temperatura máxima permitida.
    """

    def __init__(self, temperatura, minima=18.0, maxima=32.0):
        """
        Inicializa el error con la temperatura inválida y el rango permitido.
        
        Args:
            temperatura (float): Temperatura inválida detectada.
            minima (float): Temperatura mínima permitida en °C.
            maxima (float): Temperatura máxima permitida en °C.
        """
        self.temperatura = temperatura
        self.minima = minima
        self.maxima = maxima
        mensaje = (
            f"Temperatura inválida: {temperatura}°C. "
            f"Rango permitido: {minima}°C - {maxima}°C"
        )
        super().__init__(mensaje)


class StockInsuficienteError(AguaParaisoException):
    """
    Se lanza cuando el stock de un producto está por debajo del mínimo necesario.
    
    Attributes:
        producto (str): Nombre del producto con stock insuficiente.
        stock_actual (int): Stock disponible actualmente.
        stock_minimo (int): Stock mínimo requerido para la operación.
    """

    def __init__(self, producto, stock_actual, stock_minimo):
        """
        Inicializa el error con los datos de stock del producto.
        
        Args:
            producto (str): Nombre del producto afectado.
            stock_actual (int): Unidades disponibles actualmente.
            stock_minimo (int): Unidades mínimas requeridas.
        """
        self.producto = producto
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        mensaje = (
            f"Stock insuficiente de '{producto}': "
            f"{stock_actual} unidades (mínimo: {stock_minimo})"
        )
        super().__init__(mensaje)


class SaldoInsuficienteError(AguaParaisoException):
    """
    Se lanza cuando el pago recibido es insuficiente para cubrir el precio del ticket.
    
    Attributes:
        precio_total (float): Precio total a pagar en euros.
        pago_recibido (float): Importe recibido del cliente en euros.
    """

    def __init__(self, precio_total, pago_recibido):
        """
        Inicializa el error con el precio y el pago recibido.
        
        Args:
            precio_total (float): Precio total del ticket en euros.
            pago_recibido (float): Importe recibido del cliente en euros.
        """
        self.precio_total = precio_total
        self.pago_recibido = pago_recibido
        mensaje = (
            f"Saldo insuficiente: se requieren {precio_total:.2f}€ "
            f"pero se recibieron {pago_recibido:.2f}€"
        )
        super().__init__(mensaje)


class ZonaCerradaError(AguaParaisoException):
    """
    Se lanza cuando se intenta acceder a una zona cerrada o en estado de alerta.
    
    Attributes:
        zona (str): Nombre de la zona no disponible.
        estado (str): Estado actual de la zona.
    """

    def __init__(self, zona, estado):
        """
        Inicializa el error con el nombre y estado de la zona.
        
        Args:
            zona (str): Nombre de la zona afectada.
            estado (str): Estado actual de la zona (Cerrada o Alerta).
        """
        self.zona = zona
        self.estado = estado
        mensaje = (
            f"La zona '{zona}' no está disponible. "
            f"Estado actual: {estado}"
        )
        super().__init__(mensaje)


class CredencialesInvalidasError(AguaParaisoException):
    """
    Se lanza cuando las credenciales de login son incorrectas.
    
    Attributes:
        username (str): Nombre de usuario con credenciales inválidas.
    """

    def __init__(self, username):
        """
        Inicializa el error con el nombre de usuario.
        
        Args:
            username (str): Nombre de usuario que intentó acceder.
        """
        self.username = username
        mensaje = f"Credenciales incorrectas para el usuario '{username}'"
        super().__init__(mensaje)


class UsuarioBloqueadoError(AguaParaisoException):
    """
    Se lanza cuando un usuario está bloqueado por demasiados intentos fallidos.
    
    El sistema bloquea automáticamente al usuario durante 15 minutos
    tras 3 intentos de login fallidos consecutivos.
    
    Attributes:
        username (str): Nombre de usuario bloqueado.
        minutos (int): Duración del bloqueo en minutos.
    """

    def __init__(self, username, minutos=15):
        """
        Inicializa el error con el usuario bloqueado y duración.
        
        Args:
            username (str): Nombre de usuario bloqueado.
            minutos (int): Duración del bloqueo en minutos.
        """
        self.username = username
        self.minutos = minutos
        mensaje = (
            f"Usuario '{username}' bloqueado por {minutos} minutos "
            f"debido a demasiados intentos fallidos"
        )
        super().__init__(mensaje)


class DatosInvalidosError(AguaParaisoException):
    """
    Se lanza cuando los datos de un formulario no superan la validación.
    
    Attributes:
        campo (str): Nombre del campo con datos inválidos.
        valor: Valor inválido proporcionado.
        motivo (str): Descripción del motivo de la invalidez.
    """

    def __init__(self, campo, valor, motivo):
        """
        Inicializa el error con los detalles del campo inválido.
        
        Args:
            campo (str): Nombre del campo con datos inválidos.
            valor: Valor inválido proporcionado por el usuario.
            motivo (str): Descripción del motivo por el que es inválido.
        """
        self.campo = campo
        self.valor = valor
        self.motivo = motivo
        mensaje = (
            f"Datos inválidos en el campo '{campo}': "
            f"'{valor}' — {motivo}"
        )
        super().__init__(mensaje)