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
    """Gestiona la venta de tickets."""

    def __init__(self):
        self.__db = Database.obtener_instancia()
        self.__iva = Settings.iva()

    PRECIOS = {
        'Normal': {'Adulto': 25.00, 'Nino': 15.00, 'Residente': 18.00},
        'Premium': {'Adulto': 45.00, 'Nino': 28.00, 'Residente': 35.00},
        'TodoIncluido': {'Adulto': 65.00, 'Nino': 40.00, 'Residente': 50.00},
    }
    PRECIO_FAST_PASS = 28.00

    def calcular_precio(self, tipo, tipo_visitante, fast_pass=False):
        """Calcula el precio total de un ticket."""
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
        """Vende un ticket y lo guarda en la BD."""
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
        """Devuelve los tickets vendidos hoy."""
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
        """Devuelve todos los tickets."""
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
        """Devuelve el total de ingresos del día."""
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