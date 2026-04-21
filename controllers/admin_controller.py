# ============================================
# AguaParaíso - Controlador Administrativo
# Sistema ERP SmartPark Pro
# ============================================

from database.connection import Database
from utils.logger import Logger
from utils.validators import Validators
from utils.security import Security
from exceptions.exceptions import DatosInvalidosError


class AdminController:
    """
    Controlador del módulo administrativo.
    
    Gestiona las altas y bajas de empleados, el cálculo de nóminas
    con IRPF y bonus de temporada alta, y la consulta de registros
    de recursos humanos.
    
    Attributes:
        __db: Instancia singleton de la base de datos.
    """

    def __init__(self):
        """Inicializa el controlador con la conexión a la base de datos."""
        self.__db = Database.obtener_instancia()

    def obtener_empleados(self):
        """
        Devuelve todos los empleados con el nombre de su zona asignada.
        
        Utiliza JOIN entre empleados y zonas para enriquecer los datos.
        
        Returns:
            list: Lista de empleados ordenados alfabéticamente por nombre.
        """
        try:
            query = """
                SELECT e.*, z.nombre as zona_nombre
                FROM empleados e
                JOIN zonas z ON e.id_zona = z.id_zona
                ORDER BY e.nombre
            """
            return self.__db.consultar(query)
        except Exception as e:
            Logger.error(f"Error al obtener empleados: {e}")
            raise

    def obtener_empleado(self, id_empleado):
        """
        Devuelve un empleado por su ID.
        
        Args:
            id_empleado (int): ID único del empleado.
            
        Returns:
            dict | None: Datos del empleado o None si no existe.
        """
        try:
            query = "SELECT * FROM empleados WHERE id_empleado = ?"
            return self.__db.consultar_uno(query, (id_empleado,))
        except Exception as e:
            Logger.error(f"Error al obtener empleado {id_empleado}: {e}")
            raise

    def alta_empleado(self, datos):
        """
        Da de alta un nuevo empleado en el sistema.
        
        Valida los datos del formulario antes de persistir en la BD.
        
        Args:
            datos (dict): Diccionario con los campos del empleado:
                - nombre (str): Nombre completo.
                - rol (str): Rol en el parque.
                - categoria (str): Junior, Senior o Jefe.
                - turno (str): Manana, Tarde o Mantenimiento.
                - id_zona (int): ID de la zona asignada.
                - sueldo_base (float): Sueldo base mensual en euros.
                - contrato (str): Fijo o Temporal.
                
        Returns:
            int: ID del empleado recién creado.
            
        Raises:
            DatosInvalidosError: Si los datos no pasan la validación.
        """
        try:
            Validators.validar_texto(datos['nombre'], 'nombre')
            Validators.validar_numero_positivo(datos['sueldo_base'], 'sueldo_base')

            query = """
                INSERT INTO empleados
                (nombre, rol, categoria, turno, estado, id_zona, sueldo_base, contrato)
                VALUES (?, ?, ?, ?, 'Activo', ?, ?, ?)
            """
            params = (
                datos['nombre'], datos['rol'], datos['categoria'],
                datos['turno'], datos['id_zona'],
                datos['sueldo_base'], datos['contrato']
            )
            cursor = self.__db.ejecutar(query, params)
            id_empleado = cursor.lastrowid

            Logger.info(f"Empleado dado de alta: {datos['nombre']} (ID: {id_empleado})")
            return id_empleado

        except Exception as e:
            Logger.error(f"Error al dar de alta empleado: {e}")
            raise

    def baja_empleado(self, id_empleado):
        """
        Da de baja a un empleado y deshabilita su usuario del sistema.
        
        Actualiza el estado del empleado a 'Baja' y bloquea su acceso
        al sistema ERP deshabilitando su usuario asociado.
        
        Args:
            id_empleado (int): ID del empleado a dar de baja.
        """
        try:
            query = "UPDATE empleados SET estado = 'Baja' WHERE id_empleado = ?"
            self.__db.ejecutar(query, (id_empleado,))

            query_user = "UPDATE usuarios SET bloqueado = 1 WHERE id_empleado = ?"
            self.__db.ejecutar(query_user, (id_empleado,))

            Logger.info(f"Empleado dado de baja: ID {id_empleado}")

        except Exception as e:
            Logger.error(f"Error al dar de baja empleado: {e}")
            raise

    def calcular_nomina(self, id_empleado, mes, horas_extra=0, descuentos=0.0):
        """
        Calcula y registra la nómina mensual de un empleado.
        
        Aplica el IRPF según la categoría del empleado y añade
        el bonus de 200€ para los meses de temporada alta (julio/agosto).
        
        Args:
            id_empleado (int): ID del empleado.
            mes (str): Mes en formato YYYY-MM.
            horas_extra (int): Número de horas extra realizadas.
            descuentos (float): Descuentos a aplicar en euros.
            
        Returns:
            float: Total neto de la nómina en euros.
            
        Raises:
            DatosInvalidosError: Si el empleado no existe.
        """
        try:
            empleado = self.obtener_empleado(id_empleado)
            if not empleado:
                raise DatosInvalidosError('id_empleado', id_empleado, 'no existe')

            meses_alta = ['2025-07', '2025-08', '2026-07', '2026-08']
            bonus = 200.0 if mes in meses_alta else 0.0

            irpf_map = {'Junior': 15.0, 'Senior': 20.0, 'Jefe': 24.0}
            irpf = irpf_map.get(empleado['categoria'], 15.0)

            bruto = (empleado['sueldo_base'] +
                     (horas_extra * 9) + bonus - descuentos)
            total_neto = round(bruto * (1 - irpf / 100), 2)

            query = """
                INSERT INTO nominas
                (id_empleado, mes, sueldo_base, horas_extra, bonus,
                 descuentos, irpf, tipo_contrato, total_neto)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                id_empleado, mes, empleado['sueldo_base'],
                horas_extra, bonus, descuentos, irpf,
                empleado['contrato'], total_neto
            )
            self.__db.ejecutar(query, params)
            Logger.info(f"Nómina calculada: empleado {id_empleado}, mes {mes}, neto {total_neto}€")
            return total_neto

        except Exception as e:
            Logger.error(f"Error al calcular nómina: {e}")
            raise

    def obtener_nominas(self, id_empleado=None):
        """
        Devuelve las nóminas de un empleado o todas las del sistema.
        
        Utiliza JOIN con empleados para incluir el nombre en los resultados.
        
        Args:
            id_empleado (int, optional): ID del empleado. Si es None devuelve todas.
            
        Returns:
            list: Lista de nóminas ordenadas por mes descendente.
        """
        try:
            if id_empleado:
                query = """
                    SELECT n.*, e.nombre as empleado_nombre
                    FROM nominas n
                    JOIN empleados e ON n.id_empleado = e.id_empleado
                    WHERE n.id_empleado = ?
                    ORDER BY n.mes DESC
                """
                return self.__db.consultar(query, (id_empleado,))
            else:
                query = """
                    SELECT n.*, e.nombre as empleado_nombre
                    FROM nominas n
                    JOIN empleados e ON n.id_empleado = e.id_empleado
                    ORDER BY n.mes DESC
                """
                return self.__db.consultar(query)
        except Exception as e:
            Logger.error(f"Error al obtener nóminas: {e}")
            raise