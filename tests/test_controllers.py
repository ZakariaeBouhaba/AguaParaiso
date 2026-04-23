# ============================================
# AguaParaíso - Tests de Controladores
# Sistema ERP SmartPark Pro
# ============================================

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.taquilla_controller import TaquillaController
from controllers.admin_controller import AdminController
from controllers.logistica_controller import LogisticaController
from controllers.evento_controller import EventoController
from controllers.reporting_controller import ReportingController


# ============================================
# TESTS TAQUILLA
# ============================================

class TestTaquillaController:

    def setup_method(self):
        self.controller = TaquillaController()

    def test_calcular_precio_normal_adulto(self):
        base, total = self.controller.calcular_precio("Normal", "Adulto")
        assert base == 25.00
        assert total == 27.50

    def test_calcular_precio_premium_nino(self):
        base, total = self.controller.calcular_precio("Premium", "Nino")
        assert base == 28.00
        assert total == 30.80

    def test_calcular_precio_con_fast_pass(self):
        base, total = self.controller.calcular_precio("Normal", "Adulto", fast_pass=True)
        assert base == 53.00
        assert total == 58.30

    def test_vender_ticket(self):
        ticket = self.controller.vender_ticket("Normal", "Adulto", 1)
        assert ticket['localizador'].startswith("AGP-")
        assert ticket['precio_total'] == 27.50

    def test_obtener_tickets_hoy(self):
        tickets = self.controller.obtener_tickets_hoy()
        assert isinstance(tickets, list)

    def test_ingresos_hoy(self):
        ingresos = self.controller.ingresos_hoy()
        assert isinstance(ingresos, list)


# ============================================
# TESTS ADMIN
# ============================================

class TestAdminController:

    def setup_method(self):
        self.controller = AdminController()

    def test_obtener_empleados(self):
        empleados = self.controller.obtener_empleados()
        assert len(empleados) > 0

    def test_obtener_empleado_existente(self):
        empleado = self.controller.obtener_empleado(1)
        assert empleado is not None

    def test_obtener_empleado_inexistente(self):
        empleado = self.controller.obtener_empleado(99999)
        assert empleado is None

    def test_alta_empleado(self):
        datos = {
            'nombre': 'Test Empleado pytest',
            'rol': 'Socorrista',
            'categoria': 'Junior',
            'turno': 'Manana',
            'id_zona': 1,
            'sueldo_base': 1400.0,
            'contrato': 'Temporal'
        }
        id_emp = self.controller.alta_empleado(datos)
        assert id_emp > 0

    def test_calcular_nomina(self):
        neto = self.controller.calcular_nomina(1, "2026-06", horas_extra=0)
        assert neto > 0

    def test_obtener_nominas(self):
        nominas = self.controller.obtener_nominas()
        assert isinstance(nominas, list)


# ============================================
# TESTS LOGISTICA
# ============================================

class TestLogisticaController:

    def setup_method(self):
        self.controller = LogisticaController()

    def test_obtener_inventario(self):
        inventario = self.controller.obtener_inventario()
        assert len(inventario) > 0

    def test_obtener_inventario_por_zona(self):
        inventario = self.controller.obtener_inventario(id_zona=4)
        assert isinstance(inventario, list)

    def test_obtener_alertas_stock(self):
        alertas = self.controller.obtener_alertas_stock()
        assert isinstance(alertas, list)

    def test_reponer_stock(self):
        self.controller.reponer_stock(1, 10)
        producto = self.controller.obtener_producto(1)
        assert producto is not None


# ============================================
# TESTS EVENTOS
# ============================================

class TestEventoController:

    def setup_method(self):
        self.controller = EventoController()

    def test_obtener_eventos_activos(self):
        eventos = self.controller.obtener_eventos_activos()
        assert isinstance(eventos, list)

    def test_obtener_todos_eventos(self):
        eventos = self.controller.obtener_todos_eventos()
        assert isinstance(eventos, list)

    def test_generar_evento_aleatorio(self):
        resultado = self.controller.generar_evento_aleatorio()
        assert resultado is None or hasattr(resultado, 'tipo')


# ============================================
# TESTS REPORTING
# ============================================

class TestReportingController:

    def setup_method(self):
        self.controller = ReportingController()

    def test_ganancias_por_tipo(self):
        ganancias = self.controller.ganancias_por_tipo()
        assert isinstance(ganancias, list)

    def test_ocupacion_por_zona(self):
        ocupacion = self.controller.ocupacion_por_zona()
        assert len(ocupacion) == 6

    def test_empleados_activos_por_turno(self):
        empleados = self.controller.empleados_activos_por_turno()
        assert isinstance(empleados, list)

    def test_resumen_dia(self):
        resumen = self.controller.resumen_dia()
        assert 'total_tickets' in resumen
        assert 'total_ingresos' in resumen
        assert 'eventos_activos' in resumen
        assert 'zonas_abiertas' in resumen

    def test_visitantes_por_tipo(self):
        datos = self.controller.visitantes_por_tipo()
        assert isinstance(datos, list)

    def test_historico_ingresos_por_dia(self):
        datos = self.controller.historico_ingresos_por_dia()
        assert isinstance(datos, list)