# ============================================
# AguaParaíso - Controlador Taquilla
# Sistema ERP SmartPark Pro
# ============================================

from database.connection import Database
from utils.logger import Logger
from utils.generators import Generators
from exceptions.exceptions import AforoCompletoError, DatosInvalidosError, ZonaCerradaError
from config.settings import Settings
from datetime import datetime


class TaquillaController:
    """
    Controlador del módulo de taquilla.
    
    Gestiona la venta de tickets, calculo de precios con IVA,
    generacion de localizadores unicos, busqueda y cancelacion
    de tickets, y estadisticas de taquilla en tiempo real.
    """

    PRECIOS = {
        'Normal': {'Adulto': 25.00, 'Nino': 15.00, 'Residente': 18.00},
        'Premium': {'Adulto': 45.00, 'Nino': 28.00, 'Residente': 35.00},
        'TodoIncluido': {'Adulto': 65.00, 'Nino': 40.00, 'Residente': 50.00},
    }
    PRECIO_FAST_PASS = 28.00
    DESCUENTO_GRUPO = 0.10
    HORA_APERTURA = 10
    HORA_CIERRE = 19

    def __init__(self):
        """Inicializa el controlador con la conexion a BD y el IVA configurado."""
        self.__db = Database.obtener_instancia()
        self.__iva = Settings.iva()

    def verificar_horario(self):
        """
        Verifica si el parque esta en horario de apertura.
        
        Returns:
            bool: True si esta en horario de venta.
        """
        hora_actual = datetime.now().hour
        return self.HORA_APERTURA <= hora_actual < self.HORA_CIERRE

    def calcular_precio(self, tipo, tipo_visitante, fast_pass=False, cantidad=1):
        """
        Calcula el precio base y total de un ticket con IVA y descuentos.
        
        Args:
            tipo (str): Tipo de ticket.
            tipo_visitante (str): Tipo de visitante.
            fast_pass (bool): Si se anade Fast Pass.
            cantidad (int): Numero de tickets para descuento de grupo.
            
        Returns:
            tuple: (precio_base, precio_total, descuento_aplicado)
        """
        try:
            base = self.PRECIOS[tipo][tipo_visitante]
            if fast_pass:
                base += self.PRECIO_FAST_PASS

            descuento = 0.0
            if cantidad >= 5:
                descuento = base * self.DESCUENTO_GRUPO
                base = base - descuento

            total = round(base * (1 + self.__iva / 100), 2)
            return base, total, descuento
        except KeyError:
            raise DatosInvalidosError('tipo', tipo, 'tipo de ticket o visitante invalido')

    def vender_ticket(self, tipo, tipo_visitante, id_empleado, nombre_visitante,
                      id_zona, metodo_pago='Tarjeta', fast_pass=False,
                      cantidad=1, pago_recibido=0.0):
        """
        Vende un ticket registrando visitante, zona y metodo de pago.
        
        Args:
            tipo (str): Tipo de ticket.
            tipo_visitante (str): Tipo de visitante.
            id_empleado (int): ID del taquillero.
            nombre_visitante (str): Nombre completo del visitante.
            id_zona (int): ID de la zona de destino.
            metodo_pago (str): Efectivo o Tarjeta.
            fast_pass (bool): Si incluye Fast Pass.
            cantidad (int): Numero de personas para descuento grupo.
            pago_recibido (float): Importe recibido si es efectivo.
            
        Returns:
            dict: Datos completos del ticket vendido incluyendo cambio.
        """
        try:
            # Verificar horario
            if not self.verificar_horario():
                raise DatosInvalidosError('horario', datetime.now().hour,
                    f'el parque abre de {self.HORA_APERTURA}:00 a {self.HORA_CIERRE}:00')

            # Verificar zona
            zona = self.__db.consultar_uno(
                "SELECT * FROM zonas WHERE id_zona = ?", (id_zona,))
            if not zona:
                raise DatosInvalidosError('zona', id_zona, 'zona no encontrada')
            if zona['estado'] != 'Abierta':
                raise ZonaCerradaError(zona['nombre'], zona['estado'])
            if zona['aforo_actual'] >= zona['aforo_maximo']:
                raise AforoCompletoError(zona['nombre'],
                    zona['aforo_actual'], zona['aforo_maximo'])

            precio_base, precio_total, descuento = self.calcular_precio(
                tipo, tipo_visitante, fast_pass, cantidad)

            # Calcular cambio si es efectivo
            cambio = 0.0
            if metodo_pago == 'Efectivo':
                if pago_recibido < precio_total:
                    from exceptions.exceptions import SaldoInsuficienteError
                    raise SaldoInsuficienteError(precio_total, pago_recibido)
                cambio = round(pago_recibido - precio_total, 2)

            # Registrar visitante
            self.__db.ejecutar(
                "INSERT INTO visitantes (nombre, tipo, fecha_visita) VALUES (?, ?, datetime('now'))",
                (nombre_visitante, tipo_visitante)
            )
            id_visitante = self.__db.consultar_uno(
                "SELECT id_visitante FROM visitantes ORDER BY id_visitante DESC LIMIT 1"
            )['id_visitante']

            localizador = Generators.generar_localizador_ticket()

            # Insertar ticket con id_zona
            query = """
                INSERT INTO tickets
                (localizador, tipo, tipo_visitante, precio_base, iva,
                 precio_total, fast_pass, id_empleado, id_visitante, id_zona)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                localizador, tipo, tipo_visitante, precio_base,
                self.__iva, precio_total,
                1 if fast_pass else 0,
                id_empleado, id_visitante, id_zona
            )
            cursor = self.__db.ejecutar(query, params)
            id_ticket = cursor.lastrowid

            # Incrementar aforo de la zona
            self.__db.ejecutar(
                "UPDATE zonas SET aforo_actual = aforo_actual + 1 WHERE id_zona = ?",
                (id_zona,)
            )

            Logger.info(
                f"Ticket vendido: {localizador} | {tipo} | "
                f"{tipo_visitante} | {precio_total}EUR | Zona: {zona['nombre']}"
            )

            return {
                'id_ticket': id_ticket,
                'localizador': localizador,
                'tipo': tipo,
                'tipo_visitante': tipo_visitante,
                'nombre_visitante': nombre_visitante,
                'zona': zona['nombre'],
                'precio_base': precio_base,
                'descuento': descuento,
                'precio_total': precio_total,
                'fast_pass': fast_pass,
                'metodo_pago': metodo_pago,
                'cambio': cambio
            }

        except (AforoCompletoError, ZonaCerradaError, DatosInvalidosError):
            raise
        except Exception as e:
            Logger.error(f"Error al vender ticket: {e}")
            raise

    def buscar_ticket(self, localizador):
        """
        Busca un ticket por su localizador.
        
        Args:
            localizador (str): Codigo localizador del ticket.
            
        Returns:
            dict | None: Datos del ticket o None si no existe.
        """
        try:
            query = """
                SELECT t.*, e.nombre as taquillero, v.nombre as visitante,
                       z.nombre as zona_nombre
                FROM tickets t
                JOIN empleados e ON t.id_empleado = e.id_empleado
                LEFT JOIN visitantes v ON t.id_visitante = v.id_visitante
                LEFT JOIN zonas z ON t.id_zona = z.id_zona
                WHERE t.localizador = ?
            """
            return self.__db.consultar_uno(query, (localizador,))
        except Exception as e:
            Logger.error(f"Error al buscar ticket: {e}")
            raise

    def cancelar_ticket(self, localizador, id_zona):
        """
        Cancela un ticket y decrementa el aforo de la zona.
        
        Args:
            localizador (str): Localizador del ticket a cancelar.
            id_zona (int): ID de la zona para decrementar aforo.
        """
        try:
            ticket = self.buscar_ticket(localizador)
            if not ticket:
                raise DatosInvalidosError('localizador', localizador, 'ticket no encontrado')

            self.__db.ejecutar(
                "DELETE FROM tickets WHERE localizador = ?",
                (localizador,)
            )
            self.__db.ejecutar(
                "UPDATE zonas SET aforo_actual = MAX(0, aforo_actual - 1) WHERE id_zona = ?",
                (id_zona,)
            )
            Logger.info(f"Ticket cancelado: {localizador}")

        except Exception as e:
            Logger.error(f"Error al cancelar ticket: {e}")
            raise

    def obtener_tickets_hoy(self):
        """Devuelve todos los tickets vendidos hoy."""
        try:
            query = """
                SELECT t.*, e.nombre as taquillero, v.nombre as visitante,
                       z.nombre as zona_nombre
                FROM tickets t
                JOIN empleados e ON t.id_empleado = e.id_empleado
                LEFT JOIN visitantes v ON t.id_visitante = v.id_visitante
                LEFT JOIN zonas z ON t.id_zona = z.id_zona
                WHERE DATE(t.fecha) = DATE('now')
                ORDER BY t.fecha DESC
            """
            return self.__db.consultar(query)
        except Exception as e:
            Logger.error(f"Error al obtener tickets: {e}")
            raise

    def estadisticas_taquilla(self):
        """
        Devuelve estadisticas en tiempo real de la taquilla.
        
        Returns:
            dict: Tickets vendidos, ingresos, zona mas visitada y ticket medio.
        """
        try:
            query_resumen = """
                SELECT COUNT(*) as total_tickets,
                       SUM(precio_total) as total_ingresos,
                       AVG(precio_total) as ticket_medio
                FROM tickets WHERE DATE(fecha) = DATE('now')
            """
            resumen = self.__db.consultar_uno(query_resumen)

            query_zona = """
                SELECT z.nombre, COUNT(*) as visitas
                FROM tickets t
                JOIN zonas z ON t.id_zona = z.id_zona
                WHERE DATE(t.fecha) = DATE('now')
                GROUP BY t.id_zona
                ORDER BY visitas DESC
                LIMIT 1
            """
            zona_top = self.__db.consultar_uno(query_zona)

            return {
                'total_tickets': resumen['total_tickets'] or 0,
                'total_ingresos': resumen['total_ingresos'] or 0.0,
                'ticket_medio': resumen['ticket_medio'] or 0.0,
                'zona_mas_visitada': zona_top['nombre'] if zona_top else 'Sin datos',
            }
        except Exception as e:
            Logger.error(f"Error al obtener estadisticas: {e}")
            raise

    def ingresos_hoy(self):
        """Devuelve los ingresos del dia agrupados por tipo."""
        try:
            query = """
                SELECT tipo, COUNT(*) as cantidad,
                       SUM(precio_total) as total
                FROM tickets
                WHERE DATE(fecha) = DATE('now')
                GROUP BY tipo
            """
            return self.__db.consultar(query)
        except Exception as e:
            Logger.error(f"Error al calcular ingresos: {e}")
            raise

    def obtener_todos_tickets(self):
        """Devuelve todos los tickets del sistema."""
        try:
            query = """
                SELECT t.*, e.nombre as taquillero, v.nombre as visitante,
                       z.nombre as zona_nombre
                FROM tickets t
                JOIN empleados e ON t.id_empleado = e.id_empleado
                LEFT JOIN visitantes v ON t.id_visitante = v.id_visitante
                LEFT JOIN zonas z ON t.id_zona = z.id_zona
                ORDER BY t.fecha DESC
            """
            return self.__db.consultar(query)
        except Exception as e:
            Logger.error(f"Error al obtener tickets: {e}")
            raise