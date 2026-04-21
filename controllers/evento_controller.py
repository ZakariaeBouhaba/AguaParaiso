# ============================================
# AguaParaíso - Controlador Eventos
# Sistema ERP SmartPark Pro
# ============================================

from database.connection import Database
from utils.logger import Logger
from utils.events_engine import EventsEngine


class EventoController:
    """Gestiona los eventos aleatorios del parque."""

    def __init__(self):
        self.__db = Database.obtener_instancia()

    def generar_evento_aleatorio(self):
        """Genera y guarda un evento aleatorio."""
        try:
            zonas = self.__db.consultar(
                "SELECT id_zona FROM zonas WHERE estado = 'Abierta'"
            )
            ids_zonas = [z['id_zona'] for z in zonas]
            evento = EventsEngine.generar_evento(ids_zonas)
            if evento:
                return EventsEngine.procesar_evento(evento, self.__db)
            return None
        except Exception as e:
            Logger.error(f"Error al generar evento: {e}")
            raise

    def obtener_eventos_activos(self):
        """Devuelve todos los eventos activos."""
        try:
            query = """
                SELECT e.*, z.nombre as zona_nombre
                FROM eventos e
                LEFT JOIN zonas z ON e.id_zona = z.id_zona
                WHERE e.estado = 'Activo'
                ORDER BY e.fecha_inicio DESC
            """
            return self.__db.consultar(query)
        except Exception as e:
            Logger.error(f"Error al obtener eventos: {e}")
            raise

    def obtener_todos_eventos(self):
        """Devuelve todos los eventos."""
        try:
            query = """
                SELECT e.*, z.nombre as zona_nombre
                FROM eventos e
                LEFT JOIN zonas z ON e.id_zona = z.id_zona
                ORDER BY e.fecha_inicio DESC
            """
            return self.__db.consultar(query)
        except Exception as e:
            Logger.error(f"Error al obtener eventos: {e}")
            raise

    def resolver_evento(self, id_evento, id_empleado=None):
        """Marca un evento como resuelto."""
        try:
            query = """
                UPDATE eventos
                SET estado = 'Resuelto',
                    fecha_fin = datetime('now'),
                    id_empleado = ?
                WHERE id_evento = ?
            """
            self.__db.ejecutar(query, (id_empleado, id_evento))
            Logger.info(f"Evento resuelto: ID {id_evento}")
        except Exception as e:
            Logger.error(f"Error al resolver evento: {e}")
            raise