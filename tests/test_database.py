# ============================================
# AguaParaíso - Tests de Base de Datos
# Sistema ERP SmartPark Pro
# ============================================

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import Database


# ============================================
# TESTS DATABASE
# ============================================

class TestDatabase:

    def setup_method(self):
        self.db = Database.obtener_instancia()

    def test_singleton(self):
        db1 = Database.obtener_instancia()
        db2 = Database.obtener_instancia()
        assert db1 is db2

    def test_consultar_zonas(self):
        zonas = self.db.consultar("SELECT * FROM zonas")
        assert len(zonas) == 6

    def test_consultar_empleados(self):
        empleados = self.db.consultar("SELECT * FROM empleados")
        assert len(empleados) >= 20

    def test_consultar_uno(self):
        zona = self.db.consultar_uno(
            "SELECT * FROM zonas WHERE id_zona = ?", (1,))
        assert zona is not None
        assert zona['id_zona'] == 1

    def test_consultar_inexistente(self):
        zona = self.db.consultar_uno(
            "SELECT * FROM zonas WHERE id_zona = ?", (9999,))
        assert zona is None

    def test_foreign_keys_activas(self):
        resultado = self.db.consultar_uno("PRAGMA foreign_keys")
        assert resultado[0] == 1

    def test_insertar_y_consultar(self):
        self.db.ejecutar(
            "INSERT INTO visitantes (nombre, tipo, fecha_visita) VALUES (?, ?, datetime('now'))",
            ("Test Pytest", "Adulto")
        )
        visitante = self.db.consultar_uno(
            "SELECT * FROM visitantes WHERE nombre = ?",
            ("Test Pytest",)
        )
        assert visitante is not None
        assert visitante['nombre'] == "Test Pytest"

    def test_tablas_existen(self):
        tablas = self.db.consultar(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        nombres = [t['name'] for t in tablas]
        for tabla in ['zonas', 'atracciones', 'empleados', 'usuarios',
                      'visitantes', 'tickets', 'inventario', 'eventos', 'nominas']:
            assert tabla in nombres

    def test_triggers_existen(self):
        triggers = self.db.consultar(
            "SELECT name FROM sqlite_master WHERE type='trigger'"
        )
        assert len(triggers) >= 7