# ============================================
# AguaParaíso - Vista Sanitario
# Sistema ERP SmartPark Pro
# ============================================

import customtkinter as ctk
from database.connection import Database
from utils.logger import Logger


class SanitarioView(ctk.CTkFrame):
    """Módulo sanitario."""

    def __init__(self, parent, usuario):
        super().__init__(parent, fg_color="transparent")
        self.__usuario = usuario
        self.__db = Database.obtener_instancia()
        self.__construir_ui()
        self.pack(fill="both", expand=True)

    def __construir_ui(self):
        ctk.CTkLabel(
            self, text="🏥 Módulo Sanitario",
            font=("Arial", 22, "bold"), text_color="#1A6B9A"
        ).pack(pady=(20, 10), padx=20, anchor="w")

        frame = ctk.CTkFrame(self, fg_color="white", corner_radius=12,
                              border_width=1, border_color="#D6EAF8")
        frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame, text="Registrar incidente sanitario",
                     font=("Arial", 16, "bold"), text_color="#1A6B9A"
                     ).pack(pady=(20, 15))

        ctk.CTkLabel(frame, text="Descripción del incidente",
                     font=("Arial", 12), anchor="w").pack(padx=20, fill="x")
        self.__entry_desc = ctk.CTkEntry(
            frame, placeholder_text="Describe el incidente...",
            font=("Arial", 12), height=38)
        self.__entry_desc.pack(padx=20, pady=(5, 15), fill="x")

        self.__lbl_msg = ctk.CTkLabel(frame, text="", font=("Arial", 11))
        self.__lbl_msg.pack()

        ctk.CTkButton(
            frame, text="🏥 Registrar incidente",
            font=("Arial", 13, "bold"), fg_color="#6C3483",
            hover_color="#8E44AD", height=42,
            command=self.__registrar
        ).pack(padx=20, pady=10, fill="x")

        # Protocolo emergencia
        ctk.CTkButton(
            frame, text="🚨 Activar protocolo de emergencia",
            font=("Arial", 13, "bold"), fg_color="#922B21",
            hover_color="#CB4335", height=42,
            command=self.__activar_emergencia
        ).pack(padx=20, pady=(0, 20), fill="x")

    def __registrar(self):
        try:
            desc = self.__entry_desc.get().strip()
            if not desc:
                self.__lbl_msg.configure(
                    text="❌ Introduce una descripción", text_color="#E74C3C")
                return
            query = """
                INSERT INTO eventos (tipo, descripcion, estado, fecha_inicio)
                VALUES ('Sanitario', ?, 'Activo', datetime('now'))
            """
            self.__db.ejecutar(query, (desc,))
            Logger.warning(f"Incidente sanitario registrado: {desc}")
            self.__lbl_msg.configure(
                text="✅ Incidente registrado correctamente",
                text_color="#1E8449")
            self.__entry_desc.delete(0, "end")
        except Exception as e:
            self.__lbl_msg.configure(text=f"❌ Error: {e}", text_color="#E74C3C")

    def __activar_emergencia(self):
        Logger.error("PROTOCOLO DE EMERGENCIA ACTIVADO")
        self.__lbl_msg.configure(
            text="🚨 Protocolo de emergencia activado — Llamar al 112",
            text_color="#922B21")