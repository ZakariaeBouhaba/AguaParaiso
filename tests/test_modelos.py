# ============================================
# AguaParaíso - Tests de Modelos
# Sistema ERP SmartPark Pro
# ============================================

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.zona import Zona
from models.atraccion import AtraccionTobogan, AtraccionPiscina, AtraccionRio
from models.empleado import EmpleadoSocorrista, EmpleadoTecnico, EmpleadoAdmin
from models.ticket import Ticket
from models.visitante import Visitante
from models.inventario import Inventario
from models.evento import Evento
from models.nomina import Nomina
from exceptions.exceptions import (
    AforoCompletoError, TemperaturaInvalidaError,
    StockInsuficienteError, ZonaCerradaError
)


# ============================================
# TESTS ZONA
# ============================================

class TestZona:

    def test_crear_zona(self):
        z = Zona("Cascada del Trueno", "Toboganes", 200, "10:00", "19:00")
        assert z.nombre == "Cascada del Trueno"
        assert z.tipo == "Toboganes"
        assert z.aforo_maximo == 200
        assert z.aforo_actual == 0
        assert z.estado == "Abierta"

    def test_incrementar_aforo(self):
        z = Zona("Laguna Cristal", "Piscinas", 400, "10:00", "19:00")
        z.incrementar_aforo()
        assert z.aforo_actual == 1

    def test_aforo_completo_lanza_excepcion(self):
        z = Zona("Zona Test", "Toboganes", 1, "10:00", "19:00")
        z.incrementar_aforo()
        with pytest.raises(AforoCompletoError):
            z.incrementar_aforo()

    def test_zona_cerrada_lanza_excepcion(self):
        z = Zona("Zona Test", "Toboganes", 100, "10:00", "19:00")
        z.estado = "Cerrada"
        with pytest.raises(ZonaCerradaError):
            z.incrementar_aforo()

    def test_porcentaje_ocupacion(self):
        z = Zona("Zona Test", "Toboganes", 100, "10:00", "19:00")
        z.incrementar_aforo()
        z.incrementar_aforo()
        assert z.porcentaje_ocupacion() == 2.0

    def test_tipo_invalido(self):
        with pytest.raises(ValueError):
            Zona("Test", "TipoInvalido", 100, "10:00", "19:00")


# ============================================
# TESTS ATRACCION
# ============================================

class TestAtraccion:

    def test_crear_tobogan(self):
        a = AtraccionTobogan("Rayo Negro", "Adrenalina", 1.40, 20, 1, 80)
        assert a.nombre == "Rayo Negro"
        assert a.tipo == "Adrenalina"
        assert a.altura_minima == 1.40
        assert a.estado == "Activa"

    def test_crear_piscina(self):
        p = AtraccionPiscina("Laguna Olímpica", "Relax", 0, 400, 2, 26.0)
        assert p.temperatura == 26.0
        assert not p.olas_activas

    def test_piscina_temperatura_invalida(self):
        p = AtraccionPiscina("Test", "Relax", 0, 100, 2, 26.0)
        with pytest.raises(TemperaturaInvalidaError):
            p.temperatura = 35.0

    def test_crear_rio(self):
        r = AtraccionRio("Río Oasis", "Relax", 0, 120, 3, 50)
        assert r.flotadores_disponibles == 50

    def test_alquilar_flotador(self):
        r = AtraccionRio("Río Test", "Relax", 0, 50, 3, 10)
        r.alquilar_flotador()
        assert r.flotadores_disponibles == 9

    def test_flotadores_agotados(self):
        r = AtraccionRio("Río Test", "Relax", 0, 50, 3, 1)
        r.alquilar_flotador()
        with pytest.raises(StockInsuficienteError):
            r.alquilar_flotador()


# ============================================
# TESTS EMPLEADO
# ============================================

class TestEmpleado:

    def test_crear_socorrista(self):
        e = EmpleadoSocorrista("Pedro García", "Senior", "Manana", 1, 1400.0, "Temporal", "RLSF")
        assert e.nombre == "Pedro García"
        assert e.rol == "Socorrista"
        assert e.estado == "Activo"

    def test_calcular_nomina_junior(self):
        e = EmpleadoSocorrista("Test", "Junior", "Manana", 1, 1400.0, "Temporal", "RLSF")
        neto = e.calcular_nomina()
        assert neto == round(1400 * 0.85, 2)

    def test_calcular_nomina_senior(self):
        e = EmpleadoSocorrista("Test", "Senior", "Manana", 1, 1400.0, "Temporal", "RLSF")
        neto = e.calcular_nomina()
        assert neto == round(1400 * 0.80, 2)

    def test_calcular_nomina_con_extras(self):
        e = EmpleadoSocorrista("Test", "Senior", "Manana", 1, 1400.0, "Temporal", "RLSF")
        neto = e.calcular_nomina(horas_extra=3, bonus=200.0)
        assert neto == round((1400 + 27 + 200) * 0.80, 2)

    def test_dar_de_baja(self):
        e = EmpleadoTecnico("Test", "Junior", "Manana", 1, 1800.0, "Fijo", "Electricidad")
        e.dar_de_baja()
        assert e.estado == "Baja"
    def test_rol_invalido(self):
        with pytest.raises(ValueError):
            EmpleadoTecnico("Test", "CategoriaInvalida", "Manana", 1, 1800.0, "Fijo", "Electricidad")


# ============================================
# TESTS TICKET
# ============================================

class TestTicket:

    def test_crear_ticket_normal_adulto(self):
        t = Ticket("Normal", "Adulto", 1)
        assert t.tipo == "Normal"
        assert t.tipo_visitante == "Adulto"
        assert t.precio_base == 25.00
        assert t.precio_total == 27.50

    def test_crear_ticket_con_fast_pass(self):
        t = Ticket("Normal", "Adulto", 1, fast_pass=True)
        assert t.precio_base == 53.00
        assert t.precio_total == 58.30

    def test_localizador_formato(self):
        t = Ticket("Normal", "Adulto", 1)
        assert t.localizador.startswith("AGP-")
        assert len(t.localizador) > 8

    def test_tipo_invalido(self):
        with pytest.raises(ValueError):
            Ticket("TipoInvalido", "Adulto", 1)


# ============================================
# TESTS INVENTARIO
# ============================================

class TestInventario:

    def test_crear_inventario(self):
        i = Inventario("Agua botella", 4, 100, 50, 0.50, 2.50, "Proveedor", "Diario")
        assert i.nombre == "Agua botella"
        assert i.stock_actual == 100

    def test_consumir_stock(self):
        i = Inventario("Test", 4, 100, 50, 0.50, 2.50, "Proveedor", "Diario")
        i.consumir(10)
        assert i.stock_actual == 90

    def test_stock_insuficiente(self):
        i = Inventario("Test", 4, 5, 50, 0.50, 2.50, "Proveedor", "Diario")
        with pytest.raises(StockInsuficienteError):
            i.consumir(10)

    def test_reponer_stock(self):
        i = Inventario("Test", 4, 10, 50, 0.50, 2.50, "Proveedor", "Diario")
        i.reponer(40)
        assert i.stock_actual == 50

    def test_esta_bajo_minimo(self):
        i = Inventario("Test", 4, 30, 50, 0.50, 2.50, "Proveedor", "Diario")
        assert i.esta_bajo_minimo()


# ============================================
# TESTS EVENTO
# ============================================

class TestEvento:

    def test_crear_evento(self):
        e = Evento("Averia", "Fallo en tobogán", 1)
        assert e.tipo == "Averia"
        assert e.estado == "Activo"
        assert e.esta_activo()

    def test_resolver_evento(self):
        e = Evento("Averia", "Fallo en tobogán", 1)
        e.resolver(id_empleado=5)
        assert e.estado == "Resuelto"
        assert not e.esta_activo()
        assert e.fecha_fin is not None

    def test_tipo_invalido(self):
        with pytest.raises(ValueError):
            Evento("TipoInvalido", "Test", 1)


# ============================================
# TESTS NOMINA
# ============================================

class TestNomina:

    def test_crear_nomina(self):
        n = Nomina(1, "2026-06", 1400.0, "Senior", "Temporal")
        assert n.sueldo_base == 1400.0
        assert n.bonus == 0.0
        assert n.total_neto == round(1400 * 0.80, 2)

    def test_nomina_temporada_alta(self):
        n = Nomina(1, "2026-07", 1400.0, "Senior", "Temporal")
        assert n.bonus == 200.0
        assert n.total_neto == round(1600 * 0.80, 2)

    def test_nomina_con_horas_extra(self):
        n = Nomina(1, "2026-06", 1400.0, "Junior", "Fijo", horas_extra=5)
        assert n.total_neto == round((1400 + 45) * 0.85, 2)