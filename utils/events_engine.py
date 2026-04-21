# ============================================
# AguaParaíso - Motor de Eventos Aleatorios
# Sistema ERP SmartPark Pro
# ============================================

import random
from config.settings import Settings
from models.evento import Evento
from utils.logger import Logger


class EventsEngine:
    """
    Motor de generación de eventos aleatorios del parque.
    
    Implementa un sistema de probabilidades configurable desde
    config.ini para simular incidencias reales del parque como
    averías, eventos climáticos, incidentes sanitarios y
    problemas de stock.
    
    Las probabilidades configurables son:
    - Avería: 5% por defecto
    - Climático: 3% por defecto
    - Sanitario: 2% por defecto
    - Stock: 10% por defecto
    """

    DESCRIPCIONES = {
        'Averia': [
            "Fallo mecánico en tobogán, requiere revisión técnica",
            "Fuga de agua detectada en tubería",
            "Avería en sistema de bombeo",
            "Fallo eléctrico en zona de atracciones",
        ],
        'Climatico': [
            "Tormenta leve, cierre temporal de zonas exteriores",
            "Ola de calor extrema, protocolo de hidratación activado",
            "Viento fuerte, suspensión de atracciones exteriores",
        ],
        'Sanitario': [
            "Visitante con mareo leve atendido en enfermería",
            "Golpe de calor detectado, protocolo sanitario activado",
            "Accidente leve en atracción, enfermero en zona",
        ],
        'Stock': [
            "Stock bajo mínimo detectado en zona de restauración",
            "Producto agotado en inventario",
            "Reposición urgente necesaria",
        ],
    }

    @classmethod
    def generar_evento(cls, zonas_activas):
        """
        Genera un evento aleatorio basado en probabilidades configuradas.
        
        Obtiene las probabilidades desde config.ini y genera un número
        aleatorio entre 0 y 1 para determinar si se produce un evento
        y de qué tipo. Selecciona aleatoriamente una zona activa y una
        descripción del catálogo de descripciones predefinidas.
        
        Args:
            zonas_activas (list): Lista de IDs de zonas con estado Abierta.
            
        Returns:
            Evento | None: Objeto Evento si se genera uno, None en caso contrario.
        """
        probabilidades = Settings.probabilidades_eventos()
        numero = random.random()
        acumulado = 0.0

        for tipo, prob in probabilidades.items():
            acumulado += prob
            if numero < acumulado:
                descripcion = random.choice(cls.DESCRIPCIONES[tipo])
                id_zona = random.choice(zonas_activas) if zonas_activas else None
                evento = Evento(tipo, descripcion, id_zona)
                Logger.warning(f"Evento generado: {tipo} — {descripcion}")
                return evento

        return None

    @classmethod
    def procesar_evento(cls, evento, db):
        """
        Persiste un evento generado en la base de datos SQLite.
        
        Inserta el evento en la tabla eventos y actualiza el ID
        del objeto con el lastrowid devuelto por SQLite.
        
        Args:
            evento (Evento): Objeto evento a persistir.
            db (Database): Instancia de la base de datos.
            
        Returns:
            Evento: El mismo evento con el ID asignado por la BD.
            
        Raises:
            Exception: Si ocurre un error al insertar en la BD.
        """
        try:
            query = """
                INSERT INTO eventos (tipo, descripcion, id_zona, estado, fecha_inicio)
                VALUES (?, ?, ?, ?, ?)
            """
            params = (
                evento.tipo,
                evento.descripcion,
                evento.id_zona,
                evento.estado,
                evento.fecha_inicio
            )
            cursor = db.ejecutar(query, params)
            evento.id = cursor.lastrowid
            Logger.info(f"Evento guardado en BD: ID {evento.id}")
            return evento
        except Exception as e:
            Logger.error(f"Error al guardar evento: {e}")
            raise