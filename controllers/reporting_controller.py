# ============================================
# AguaParaíso - Controlador Reporting
# Sistema ERP SmartPark Pro
# ============================================

from database.connection import Database
from utils.logger import Logger


class ReportingController:
    """
    Controlador del módulo de reporting y estadísticas.
    
    Genera informes y estadísticas del parque utilizando consultas
    SQL avanzadas con JOINs, GROUP BY y funciones de agregado
    SUM y AVG sobre los datos almacenados en SQLite.
    
    Attributes:
        __db: Instancia singleton de la base de datos.
    """

    def __init__(self):
        """Inicializa el controlador con la conexión a la base de datos."""
        self.__db = Database.obtener_instancia()

    def ganancias_por_tipo(self, fecha=None):
        """
        Devuelve las ganancias agrupadas por tipo de ticket.
        
        Utiliza SUM y AVG con GROUP BY para calcular el total
        e importe medio por cada tipo de entrada vendida.
        
        Args:
            fecha (str, optional): Fecha en formato YYYY-MM-DD.
                                   Si es None devuelve todas las ganancias.
                                   
        Returns:
            list: Lista con tipo, cantidad, total y media por tipo de ticket.
        """
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
        """
        Devuelve el porcentaje de ocupación actual por zona.
        
        Calcula el ratio aforo_actual/aforo_maximo para cada zona
        y lo expresa como porcentaje redondeado a 2 decimales.
        
        Returns:
            list: Lista de zonas con aforo actual, máximo y porcentaje.
        """
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
        """
        Devuelve el número de empleados activos agrupados por turno y zona.
        
        Utiliza JOIN entre empleados y zonas con GROUP BY para
        obtener la distribución del personal por turno y área.
        
        Returns:
            list: Lista con zona, turno y número de empleados activos.
        """
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

    def zonas_unicas_con_eventos(self):
        """
        Devuelve las zonas únicas que tienen eventos activos usando set.
        
        Utiliza un set de Python para garantizar la unicidad de zonas
        afectadas por eventos activos en tiempo real.
        
        Returns:
            set: Conjunto de IDs de zonas con eventos activos.
        """
        try:
            eventos = self.__db.consultar(
                "SELECT DISTINCT id_zona FROM eventos WHERE estado = 'Activo' AND id_zona IS NOT NULL"
            )
            return set(e['id_zona'] for e in eventos)
        except Exception as e:
            Logger.error(f"Error al obtener zonas con eventos: {e}")
            raise

    def tickets_ordenados_por_precio(self):
        """
        Devuelve todos los tickets ordenados por precio descendente.
        
        Aplica el algoritmo sorted() de Python sobre la lista de tickets
        usando precio_total como clave de ordenamiento.
        
        Returns:
            list: Lista de tickets ordenados de mayor a menor precio.
        """
        try:
            tickets = self.__db.consultar(
                "SELECT * FROM tickets ORDER BY precio_total DESC"
            )
            return sorted(tickets, key=lambda t: t['precio_total'], reverse=True)
        except Exception as e:
            Logger.error(f"Error al ordenar tickets: {e}")
            raise

    def empleados_filtrados_por_rol(self, rol):
        """
        Filtra y devuelve los empleados activos de un rol específico.
        
        Utiliza filter() con función lambda para aplicar el filtrado
        en memoria sobre la lista de empleados activos.
        
        Args:
            rol (str): Rol a filtrar (Socorrista, Tecnico, Taquillero...).
            
        Returns:
            list: Lista de empleados activos con el rol indicado.
        """
        try:
            empleados = self.__db.consultar(
                "SELECT * FROM empleados WHERE estado = 'Activo'"
            )
            return list(filter(lambda e: e['rol'] == rol, empleados))
        except Exception as e:
            Logger.error(f"Error al filtrar empleados: {e}")
            raise

    def visitantes_por_tipo(self):
        """
        Devuelve las ventas agrupadas por tipo de visitante.
        
        Utiliza SUM y AVG con GROUP BY para calcular el total
        e importe medio por cada tipo de visitante.
        
        Returns:
            list: Lista con tipo de visitante, cantidad, total y media.
        """
        try:
            query = """
                SELECT tipo_visitante, COUNT(*) as cantidad,
                       SUM(precio_total) as total,
                       AVG(precio_total) as media
                FROM tickets
                GROUP BY tipo_visitante
                ORDER BY cantidad DESC
            """
            return self.__db.consultar(query)
        except Exception as e:
            Logger.error(f"Error al obtener visitantes: {e}")
            raise

    def historico_ingresos_por_dia(self):
        """
        Devuelve el histórico de ingresos agrupados por día.
        
        Utiliza SUM y GROUP BY sobre la fecha para obtener
        el total de ingresos de cada día del histórico.
        
        Returns:
            list: Lista con fecha, cantidad de tickets y total de ingresos.
        """
        try:
            query = """
                SELECT DATE(fecha) as fecha,
                       COUNT(*) as cantidad,
                       SUM(precio_total) as total
                FROM tickets
                GROUP BY DATE(fecha)
                ORDER BY fecha DESC
            """
            return self.__db.consultar(query)
        except Exception as e:
            Logger.error(f"Error al obtener histórico: {e}")
            raise

    def resumen_dia(self, fecha=None):
        """
        Genera un resumen completo del día con las métricas principales.
        
        Consolida en un único diccionario los tickets vendidos,
        ingresos totales, eventos activos y zonas abiertas del día.
        
        Args:
            fecha (str, optional): Fecha en formato YYYY-MM-DD.
                                   Si es None usa la fecha actual.
                                   
        Returns:
            dict: Resumen con total_tickets, total_ingresos,
                  eventos_activos y zonas_abiertas.
        """
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