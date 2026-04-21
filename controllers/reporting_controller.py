# ============================================
# AguaParaíso - Controlador Reporting
# Sistema ERP SmartPark Pro
# ============================================

from database.connection import Database
from utils.logger import Logger


class ReportingController:
    """Gestiona las estadísticas y reportes del parque."""

    def __init__(self):
        self.__db = Database.obtener_instancia()

    def ganancias_por_tipo(self, fecha=None):
        """Devuelve ganancias agrupadas por tipo de ticket."""
        try:
            if fecha:
                query = """
                    SELECT tipo, COUNT(*) as cantidad,
                           SUM(precio_total) as total,
                           AVG(precio_total) as media
                    FROM tickets
                    WHERE DATE(fecha) = ?
                    GROUP BY tipo
                    ORDER BY total DESC
                """
                return self.__db.consultar(query, (fecha,))
            else:
                query = """
                    SELECT tipo, COUNT(*) as cantidad,
                           SUM(precio_total) as total,
                           AVG(precio_total) as media
                    FROM tickets
                    GROUP BY tipo
                    ORDER BY total DESC
                """
                return self.__db.consultar(query)
        except Exception as e:
            Logger.error(f"Error al obtener ganancias: {e}")
            raise

    def ocupacion_por_zona(self):
        """Devuelve el porcentaje de ocupación por zona."""
        try:
            query = """
                SELECT z.nombre,
                       z.aforo_actual,
                       z.aforo_maximo,
                       z.estado,
                       ROUND(z.aforo_actual * 100.0 / z.aforo_maximo, 2) as porcentaje
                FROM zonas z
                ORDER BY porcentaje DESC
            """
            return self.__db.consultar(query)
        except Exception as e:
            Logger.error(f"Error al obtener ocupación: {e}")
            raise

    def empleados_activos_por_turno(self):
        """Devuelve empleados activos agrupados por turno y zona."""
        try:
            query = """
                SELECT z.nombre as zona, e.turno,
                       COUNT(*) as num_empleados
                FROM empleados e
                JOIN zonas z ON e.id_zona = z.id_zona
                WHERE e.estado = 'Activo'
                GROUP BY z.id_zona, e.turno
                ORDER BY z.nombre, e.turno
            """
            return self.__db.consultar(query)
        except Exception as e:
            Logger.error(f"Error al obtener empleados: {e}")
            raise

    def resumen_dia(self, fecha=None):
        """Devuelve un resumen completo del día."""
        try:
            if fecha:
                query_tickets = """
                    SELECT COUNT(*) as total_tickets,
                           SUM(precio_total) as total_ingresos
                    FROM tickets WHERE DATE(fecha) = ?
                """
                tickets = self.__db.consultar_uno(query_tickets, (fecha,))
            else:
                query_tickets = """
                    SELECT COUNT(*) as total_tickets,
                           SUM(precio_total) as total_ingresos
                    FROM tickets WHERE DATE(fecha) = DATE('now')
                """
                tickets = self.__db.consultar_uno(query_tickets)

            query_eventos = """
                SELECT COUNT(*) as total
                FROM eventos WHERE estado = 'Activo'
            """
            eventos = self.__db.consultar_uno(query_eventos)

            query_zonas = """
                SELECT COUNT(*) as total
                FROM zonas WHERE estado = 'Abierta'
            """
            zonas = self.__db.consultar_uno(query_zonas)

            resumen = {
                'total_tickets': tickets['total_tickets'] or 0,
                'total_ingresos': tickets['total_ingresos'] or 0.0,
                'eventos_activos': eventos['total'] or 0,
                'zonas_abiertas': zonas['total'] or 0,
            }

            Logger.info(f"Resumen del día generado: {resumen}")
            return resumen

        except Exception as e:
            Logger.error(f"Error al generar resumen: {e}")
            raise