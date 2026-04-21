# ============================================
# AguaParaíso - Controlador Taquilla
# Sistema ERP SmartPark Pro
# ============================================

from database.connection import Database
from utils.logger import Logger
from utils.generators import Generators
from exceptions.exceptions import AforoCompletoError, DatosInvalidosError
from config.settings import Settings


class TaquillaController:
    """
    Controlador del módulo de taquilla.
    
    Gestiona la venta de tickets, cálculo de precios con IVA,
    generación de localizadores únicos y consulta de ventas.
    
    Attributes:
        __db: Instancia singleton de la base de datos.
        __iva: Porcentaje de IVA aplicado a los tickets.
    """

    PRECIOS = {
        'Normal': {'Adulto': 25.00, 'Nino': 15.00, 'Residente': 18.00},
        'Premium': {'Adulto': 45.00, 'Nino': 28.00, 'Residente': 35.00},
        'TodoIncluido': {'Adulto': 65.00, 'Nino': 40.00, 'Residente': 50.00},
    }
    PRECIO_FAST_PASS = 28.00

    def __init__(self):
        """Inicializa el controlador con la conexión a BD y el IVA configurado."""
        self.__db = Database.obtener_instancia()
        self.__iva = Settings.iva()

    def calcular_precio(self, tipo, tipo_visitante, fast_pass=False):
        """
        Calcula el precio base y total de un ticket con IVA.
        
        Args:
            tipo (str): Tipo de ticket (Normal, Premium, TodoIncluido).
            tipo_visitante (str): Tipo de visitante (Adulto, Nino, Residente).
            fast_pass (bool): Si se añade Fast Pass al ticket.
            
        Returns:
            tuple: (precio_base, precio_total) ambos en euros.
            
        Raises:
            DatosInvalidosError: Si el tipo de ticket o visitante no es válido.
        """
        try:
            base = self.PRECIOS[tipo][tipo_visitante]
            if fast_pass:
                base += self.PRECIO_FAST_PASS
            total = round(base * (1 + self.__iva / 100), 2)
            return base, total
        except KeyError:
            raise DatosInvalidosError('tipo', tipo, 'tipo de ticket o visitante inválido')

    def vender_ticket(self, tipo, tipo_visitante, id_empleado,
                      id_visitante=None, fast_pass=False):
        """
        Vende un ticket y lo persiste en la base de datos.
        
        Genera un localizador único en formato AGP-YYYY-XXXXXXXX,
        calcula el precio con IVA y registra la venta en SQLite.
        
        Args:
            tipo (str): Tipo de ticket.
            tipo_visitante (str): Tipo de visitante.
            id_empleado (int): ID del taquillero que realiza la venta.
            id_visitante (int, optional): ID del visitante si está registrado.
            fast_pass (bool): Si se añade Fast Pass.
            
        Returns:
            dict: Datos del ticket vendido incluyendo localizador y precio total.
            
        Raises:
            Exception: Si ocurre un error al insertar en la base de datos.
        """
        try:
            precio_base, precio_total = self.calcular_precio(tipo, tipo_visitante, fast_pass)
            localizador = Generators.generar_localizador_ticket()

            query = """
                INSERT INTO tickets
                (localizador, tipo, tipo_visitante, precio_base, iva,
                 precio_total, fast_pass, id_empleado, id_visitante)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                localizador, tipo, tipo_visitante, precio_base,
                self.__iva, precio_total,
                1 if fast_pass else 0,
                id_empleado, id_visitante
            )
            cursor = self.__db.ejecutar(query, params)
            id_ticket = cursor.lastrowid

            Logger.info(
                f"Ticket vendido: {localizador} | {tipo} | "
                f"{tipo_visitante} | {precio_total}€"
            )
            return {
                'id_ticket': id_ticket,
                'localizador': localizador,
                'tipo': tipo,
                'tipo_visitante': tipo_visitante,
                'precio_base': precio_base,
                'precio_total': precio_total,
                'fast_pass': fast_pass
            }

        except Exception as e:
            Logger.error(f"Error al vender ticket: {e}")
            raise

    def obtener_tickets_hoy(self):
        """
        Devuelve todos los tickets vendidos en el día actual.
        
        Returns:
            list: Lista de registros de tickets con datos del taquillero.
        """
        try:
            query = """
                SELECT t.*, e.nombre as taquillero
                FROM tickets t
                JOIN empleados e ON t.id_empleado = e.id_empleado
                WHERE DATE(t.fecha) = DATE('now')
                ORDER BY t.fecha DESC
            """
            return self.__db.consultar(query)
        except Exception as e:
            Logger.error(f"Error al obtener tickets: {e}")
            raise

    def obtener_todos_tickets(self):
        """
        Devuelve todos los tickets del sistema ordenados por fecha.
        
        Returns:
            list: Lista completa de tickets con datos del taquillero.
        """
        try:
            query = """
                SELECT t.*, e.nombre as taquillero
                FROM tickets t
                JOIN empleados e ON t.id_empleado = e.id_empleado
                ORDER BY t.fecha DESC
            """
            return self.__db.consultar(query)
        except Exception as e:
            Logger.error(f"Error al obtener tickets: {e}")
            raise

    def ingresos_hoy(self):
        """
        Calcula los ingresos del día agrupados por tipo de ticket.
        
        Utiliza SUM y GROUP BY para obtener estadísticas de ventas.
        
        Returns:
            list: Lista con tipo, cantidad y total de ingresos por tipo.
        """
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