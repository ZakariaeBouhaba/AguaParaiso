# ============================================
# AguaParaíso - Vista Zonas
# Sistema ERP SmartPark Pro
# ============================================

import customtkinter as ctk
from database.connection import Database
from views.components.tabla_dinamica import TablaDinamica


class ZonasView(ctk.CTkFrame):
    """Módulo de gestión de zonas."""

    def __init__(self, parent, usuario):
        super().__init__(parent, fg_color="transparent")
        self.__usuario = usuario
        self.__db = Database.obtener_instancia()
        self.__construir_ui()
        self.pack(fill="both", expand=True)

    def __construir_ui(self):
        ctk.CTkLabel(
            self, text="🗺️ Módulo Zonas",
            font=("Arial", 22, "bold"), text_color="#1A6B9A"
        ).pack(pady=(20, 10), padx=20, anchor="w")

        frame_btn = ctk.CTkFrame(self, fg_color="transparent")
        frame_btn.pack(fill="x", padx=20, pady=5)

        ctk.CTkButton(
            frame_btn, text="🔄 Actualizar",
            font=("Arial", 12), fg_color="#1A6B9A", width=130,
            command=self.__cargar_zonas
        ).pack(side="left", padx=5)

        self.__frame_tabla = ctk.CTkFrame(self, fg_color="transparent")
        self.__frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        self.__cargar_zonas()

    def __cargar_zonas(self):
        for w in self.__frame_tabla.winfo_children():
            w.destroy()
        zonas = self.__db.consultar(
            "SELECT * FROM zonas ORDER BY id_zona")
        columnas = ["ID", "Nombre", "Tipo", "Aforo actual", "Aforo máx", "Estado"]
        datos = [[str(z['id_zona']), z['nombre'], z['tipo'],
                  str(z['aforo_actual']), str(z['aforo_maximo']),
                  z['estado']] for z in zonas]
        TablaDinamica(self.__frame_tabla, columnas=columnas,
                      datos=datos).pack(fill="both", expand=True)