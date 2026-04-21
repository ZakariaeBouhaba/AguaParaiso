# ============================================
# AguaParaíso - Vista Taquilla
# Sistema ERP SmartPark Pro
# ============================================

import customtkinter as ctk
from controllers.taquilla_controller import TaquillaController
from views.components.tabla_dinamica import TablaDinamica
from utils.logger import Logger


class TaquillaView(ctk.CTkFrame):
    """Módulo de venta de tickets."""

    def __init__(self, parent, usuario):
        super().__init__(parent, fg_color="transparent")
        self.__usuario = usuario
        self.__controller = TaquillaController()
        self.__construir_ui()
        self.pack(fill="both", expand=True)

    def __construir_ui(self):
        # Título
        ctk.CTkLabel(
            self,
            text="🎟️ Módulo Taquilla",
            font=("Arial", 22, "bold"),
            text_color="#1A6B9A"
        ).pack(pady=(20, 10), padx=20, anchor="w")

        # Frame principal
        frame_main = ctk.CTkFrame(self, fg_color="transparent")
        frame_main.pack(fill="both", expand=True, padx=20, pady=10)

        # Panel izquierdo — formulario
        frame_form = ctk.CTkFrame(
            frame_main, fg_color="white", corner_radius=12,
            border_width=1, border_color="#D6EAF8", width=350
        )
        frame_form.pack(side="left", fill="y", padx=(0, 10))
        frame_form.pack_propagate(False)

        ctk.CTkLabel(
            frame_form,
            text="Nueva venta",
            font=("Arial", 16, "bold"),
            text_color="#1A6B9A"
        ).pack(pady=(20, 15))

        # Tipo visitante
        ctk.CTkLabel(frame_form, text="Tipo visitante",
                     font=("Arial", 12), anchor="w").pack(padx=20, fill="x")
        self.__tipo_visitante = ctk.CTkComboBox(
            frame_form,
            values=["Adulto", "Nino", "Residente"],
            font=("Arial", 12), width=300,
            command=self.__actualizar_precio
        )
        self.__tipo_visitante.pack(padx=20, pady=(5, 15))

        # Tipo ticket
        ctk.CTkLabel(frame_form, text="Tipo ticket",
                     font=("Arial", 12), anchor="w").pack(padx=20, fill="x")
        self.__tipo_ticket = ctk.CTkComboBox(
            frame_form,
            values=["Normal", "Premium", "TodoIncluido"],
            font=("Arial", 12), width=300,
            command=self.__actualizar_precio
        )
        self.__tipo_ticket.pack(padx=20, pady=(5, 15))

        # Fast Pass
        self.__fast_pass = ctk.CTkCheckBox(
            frame_form,
            text="Fast Pass (+28€)",
            font=("Arial", 12),
            command=self.__actualizar_precio
        )
        self.__fast_pass.pack(padx=20, pady=(0, 15), anchor="w")

        # Precio
        frame_precio = ctk.CTkFrame(frame_form, fg_color="#D6EAF8", corner_radius=8)
        frame_precio.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(
            frame_precio,
            text="Precio total (IVA 10% incluido)",
            font=("Arial", 11),
            text_color="#555555"
        ).pack(pady=(10, 2))

        self.__lbl_precio = ctk.CTkLabel(
            frame_precio,
            text="27.50€",
            font=("Arial", 28, "bold"),
            text_color="#1A6B9A"
        )
        self.__lbl_precio.pack(pady=(0, 10))

        # Mensaje
        self.__lbl_mensaje = ctk.CTkLabel(
            frame_form, text="", font=("Arial", 11)
        )
        self.__lbl_mensaje.pack(pady=5)

        # Botón vender
        ctk.CTkButton(
            frame_form,
            text="✅ Vender Ticket",
            font=("Arial", 14, "bold"),
            fg_color="#1E8449",
            hover_color="#27AE60",
            height=45,
            corner_radius=8,
            command=self.__vender
        ).pack(padx=20, pady=10, fill="x")

        # Panel derecho — tabla tickets
        frame_tabla = ctk.CTkFrame(
            frame_main, fg_color="white", corner_radius=12,
            border_width=1, border_color="#D6EAF8"
        )
        frame_tabla.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(
            frame_tabla,
            text="Tickets vendidos hoy",
            font=("Arial", 16, "bold"),
            text_color="#1A6B9A"
        ).pack(pady=(20, 10), padx=20, anchor="w")

        self.__frame_tabla = ctk.CTkFrame(frame_tabla, fg_color="transparent")
        self.__frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.__actualizar_tabla()
        self.__actualizar_precio()

    def __actualizar_precio(self, *args):
        try:
            tipo = self.__tipo_ticket.get()
            visitante = self.__tipo_visitante.get()
            fp = self.__fast_pass.get()
            _, total = self.__controller.calcular_precio(tipo, visitante, fp)
            self.__lbl_precio.configure(text=f"{total}€")
        except Exception:
            pass

    def __vender(self):
        try:
            tipo = self.__tipo_ticket.get()
            visitante = self.__tipo_visitante.get()
            fp = self.__fast_pass.get()
            id_empleado = self.__usuario['id_empleado']

            ticket = self.__controller.vender_ticket(
                tipo, visitante, id_empleado, fast_pass=fp
            )

            self.__lbl_mensaje.configure(
                text=f"✅ Ticket vendido: {ticket['localizador']}",
                text_color="#1E8449"
            )
            self.__actualizar_tabla()

        except Exception as e:
            self.__lbl_mensaje.configure(
                text=f"❌ Error: {e}",
                text_color="#E74C3C"
            )
            Logger.error(f"Error al vender ticket: {e}")

    def __actualizar_tabla(self):
        for w in self.__frame_tabla.winfo_children():
            w.destroy()

        tickets = self.__controller.obtener_tickets_hoy()
        columnas = ["Localizador", "Tipo", "Visitante", "Total", "Fast Pass"]
        datos = []
        for t in tickets:
            datos.append([
                t['localizador'],
                t['tipo'],
                t['tipo_visitante'],
                f"{t['precio_total']}€",
                "Sí" if t['fast_pass'] else "No"
            ])

        TablaDinamica(
            self.__frame_tabla,
            columnas=columnas,
            datos=datos
        ).pack(fill="both", expand=True)