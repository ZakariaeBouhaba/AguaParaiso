# ============================================
# AguaParaíso - Controlador Eventos
# Sistema ERP SmartPark Pro
# ============================================

from database.connection import Database
from utils.logger import Logger
from utils.events_engine import EventsEngine


class EventoController:
    """
    Controlador del módulo de eventos aleatorios.
    
    Gestiona la generación automática de eventos basados en
    probabilidades configurables, su persistencia en la base de
    datos y su resolución por parte del personal técnico.
    
    Attributes:
        __db: Instancia singleton de la base de datos.
    """

    def __init__(self):
        """Inicializa el controlador con la conexión a la base de datos."""
        self.__db = Database.obtener_instancia()

    def generar_evento_aleatorio(self):
        """
        Genera un evento aleatorio basado en probabilidades configuradas.
        
        Obtiene las zonas abiertas, genera un número aleatorio y lo
        compara con las probabilidades definidas en config.ini para
        determinar si se genera un evento y de qué tipo.
        
        Returns:
            Evento | None: El evento generado y persistido, o None si
                          no se generó ningún evento en esta iteración.
        """
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
        """
        Devuelve todos los eventos con estado Activo.
        
        Utiliza LEFT JOIN con zonas para incluir el nombre de zona
        incluso cuando el evento no está asociado a una zona específica.
        
        Returns:
            list: Lista de eventos activos ordenados por fecha descendente.
        """
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
        """
        Devuelve todos los eventos del sistema independientemente del estado.
        
        Returns:
            list: Lista completa de eventos ordenados por fecha descendente.
        """
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
        """
        Marca un evento como resuelto y registra la fecha de resolución.
        
        El trigger tr_evento_resuelto de la base de datos actualiza
        automáticamente la fecha_fin al cambiar el estado a Resuelto.
        
        Args:
            id_evento (int): ID del evento a resolver.
            id_empleado (int, optional): ID del empleado que resuelve el evento.
        """
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