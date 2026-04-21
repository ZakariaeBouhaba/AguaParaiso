# ============================================
# AguaParaíso - Vista Eventos
# Sistema ERP SmartPark Pro
# ============================================

import customtkinter as ctk
from controllers.evento_controller import EventoController
from views.components.tabla_dinamica import TablaDinamica


class EventosView(ctk.CTkFrame):
    """Módulo de gestión de eventos."""

    def __init__(self, parent, usuario):
        super().__init__(parent, fg_color="transparent")
        self.__usuario = usuario
        self.__controller = EventoController()
        self.__construir_ui()
        self.pack(fill="both", expand=True)

    def __construir_ui(self):
        ctk.CTkLabel(
            self, text="⚡ Módulo Eventos",
            font=("Arial", 22, "bold"), text_color="#1A6B9A"
        ).pack(pady=(20, 10), padx=20, anchor="w")

        frame_btn = ctk.CTkFrame(self, fg_color="transparent")
        frame_btn.pack(fill="x", padx=20, pady=5)

        ctk.CTkButton(
            frame_btn, text="🔄 Actualizar",
            font=("Arial", 12), fg_color="#1A6B9A", width=130,
            command=self.__cargar_eventos
        ).pack(side="left", padx=5)

        if self.__usuario['rol'] == 'Admin':
            ctk.CTkButton(
                frame_btn, text="⚡ Generar evento",
                font=("Arial", 12), fg_color="#BA4A00", width=150,
                command=self.__generar_evento
            ).pack(side="left", padx=5)

        self.__lbl_msg = ctk.CTkLabel(self, text="", font=("Arial", 11))
        self.__lbl_msg.pack()

        self.__frame_tabla = ctk.CTkFrame(self, fg_color="transparent")
        self.__frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        self.__cargar_eventos()

    def __cargar_eventos(self):
        for w in self.__frame_tabla.winfo_children():
            w.destroy()
        eventos = self.__controller.obtener_todos_eventos()
        columnas = ["ID", "Tipo", "Descripción", "Zona", "Estado", "Inicio"]
        datos = []
        for e in eventos:
            datos.append([
                str(e['id_evento']), e['tipo'],
                e['descripcion'][:40] + "..." if len(e['descripcion']) > 40 else e['descripcion'],
                e['zona_nombre'] or "Global",
                e['estado'], e['fecha_inicio']
            ])
        TablaDinamica(self.__frame_tabla, columnas=columnas,
                      datos=datos).pack(fill="both", expand=True)

    def __generar_evento(self):
        try:
            evento = self.__controller.generar_evento_aleatorio()
            if evento:
                self.__lbl_msg.configure(
                    text=f"✅ Evento generado: {evento.tipo} — {evento.descripcion}",
                    text_color="#1E8449")
            else:
                self.__lbl_msg.configure(
                    text="ℹ️ No se generó evento esta vez",
                    text_color="#555555")
            self.__cargar_eventos()
        except Exception as e:
            self.__lbl_msg.configure(text=f"❌ Error: {e}", text_color="#E74C3C")