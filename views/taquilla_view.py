# ============================================
# AguaParaíso - Vista Taquilla
# Sistema ERP SmartPark Pro
# ============================================

import customtkinter as ctk
from controllers.taquilla_controller import TaquillaController
from views.components.tabla_dinamica import TablaDinamica
from database.connection import Database
from utils.logger import Logger


class TaquillaView(ctk.CTkFrame):
    """Módulo completo de venta de tickets."""

    def __init__(self, parent, usuario):
        super().__init__(parent, fg_color="transparent")
        self.__usuario = usuario
        self.__controller = TaquillaController()
        self.__db = Database.obtener_instancia()
        self.__construir_ui()
        self.pack(fill="both", expand=True)

    def __construir_ui(self):
        ctk.CTkLabel(
            self, text="🎟️ Módulo Taquilla",
            font=("Arial", 22, "bold"), text_color="#1A6B9A"
        ).pack(pady=(20, 10), padx=20, anchor="w")

        self.__tabs = ctk.CTkTabview(self, fg_color="white")
        self.__tabs.pack(fill="both", expand=True, padx=20, pady=10)
        self.__tabs.add("Nueva venta")
        self.__tabs.add("Buscar ticket")
        self.__tabs.add("Cancelar ticket")
        self.__tabs.add("Tickets hoy")
        self.__tabs.add("Estadísticas")

        self.__construir_nueva_venta()
        self.__construir_buscar()
        self.__construir_cancelar()
        self.__construir_tickets_hoy()
        self.__construir_estadisticas()

    # ============================================
    # PESTAÑA 1: NUEVA VENTA
    # ============================================
    def __construir_nueva_venta(self):
        tab = self.__tabs.tab("Nueva venta")

        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        if not self.__controller.verificar_horario():
            ctk.CTkLabel(
                scroll,
                text="⛔ Fuera de horario — El parque abre de 10:00 a 19:00",
                font=("Arial", 14, "bold"),
                text_color="#922B21"
            ).pack(pady=30)
            return

        frame = ctk.CTkFrame(scroll, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        col_izq = ctk.CTkFrame(frame, fg_color="white", corner_radius=12,
                                border_width=1, border_color="#D6EAF8")
        col_izq.pack(side="left", fill="both", expand=True, padx=(0, 5))

        col_der = ctk.CTkFrame(frame, fg_color="white", corner_radius=12,
                                border_width=1, border_color="#D6EAF8")
        col_der.pack(side="right", fill="both", expand=True, padx=(5, 0))

        # ---- Columna izquierda: Datos del visitante ----
        ctk.CTkLabel(col_izq, text="Datos del visitante",
                     font=("Arial", 14, "bold"), text_color="#1A6B9A"
                     ).pack(pady=(15, 10), padx=15, anchor="w")

        ctk.CTkLabel(col_izq, text="Nombre completo",
                     font=("Arial", 11), anchor="w").pack(padx=15, fill="x")
        self.__entry_nombre = ctk.CTkEntry(
            col_izq, placeholder_text="Ej: Juan Garcia Lopez",
            font=("Arial", 12), height=36)
        self.__entry_nombre.pack(padx=15, pady=(3, 10), fill="x")

        ctk.CTkLabel(col_izq, text="Tipo de visitante",
                     font=("Arial", 11), anchor="w").pack(padx=15, fill="x")
        self.__sel_visitante = ctk.CTkComboBox(
            col_izq, values=["Adulto", "Nino", "Residente"],
            font=("Arial", 12), height=36,
            command=self.__actualizar_precio)
        self.__sel_visitante.pack(padx=15, pady=(3, 10), fill="x")

        ctk.CTkLabel(col_izq, text="Zona de destino",
                     font=("Arial", 11), anchor="w").pack(padx=15, fill="x")
        zonas = self.__db.consultar(
            "SELECT id_zona, nombre, estado, aforo_actual, aforo_maximo FROM zonas ORDER BY id_zona")
        self.__zonas_dict = {
            f"{z['nombre']} ({z['estado']}) — {z['aforo_actual']}/{z['aforo_maximo']}": z['id_zona']
            for z in zonas}
        self.__sel_zona = ctk.CTkComboBox(
            col_izq, values=list(self.__zonas_dict.keys()),
            font=("Arial", 11), height=36)
        self.__sel_zona.pack(padx=15, pady=(3, 10), fill="x")

        ctk.CTkLabel(col_izq, text="Numero de personas",
                     font=("Arial", 11), anchor="w").pack(padx=15, fill="x")
        self.__entry_cantidad = ctk.CTkEntry(
            col_izq, placeholder_text="1 (grupo de 5+ tiene 10% dto)",
            font=("Arial", 12), height=36)
        self.__entry_cantidad.insert(0, "1")
        self.__entry_cantidad.pack(padx=15, pady=(3, 10), fill="x")
        self.__entry_cantidad.bind("<KeyRelease>", lambda e: self.__actualizar_precio())

        # ---- Columna derecha: Tipo de ticket ----
        ctk.CTkLabel(col_der, text="Tipo de ticket",
                     font=("Arial", 14, "bold"), text_color="#1A6B9A"
                     ).pack(pady=(15, 10), padx=15, anchor="w")

        ctk.CTkLabel(col_der, text="Tipo de ticket",
                     font=("Arial", 11), anchor="w").pack(padx=15, fill="x")
        self.__sel_ticket = ctk.CTkComboBox(
            col_der, values=["Normal", "Premium", "TodoIncluido"],
            font=("Arial", 12), height=36,
            command=self.__actualizar_precio)
        self.__sel_ticket.pack(padx=15, pady=(3, 10), fill="x")

        self.__chk_fastpass = ctk.CTkCheckBox(
            col_der, text="Fast Pass (+28 EUR)",
            font=("Arial", 12),
            command=self.__actualizar_precio)
        self.__chk_fastpass.pack(padx=15, pady=(0, 10), anchor="w")

        ctk.CTkLabel(col_der, text="Método de pago",
                     font=("Arial", 11), anchor="w").pack(padx=15, fill="x")
        self.__sel_pago = ctk.CTkComboBox(
            col_der, values=["Tarjeta", "Efectivo"],
            font=("Arial", 12), height=36,
            command=self.__toggle_efectivo)
        self.__sel_pago.pack(padx=15, pady=(3, 10), fill="x")

        self.__frame_efectivo = ctk.CTkFrame(col_der, fg_color="transparent")
        self.__frame_efectivo.pack(padx=15, fill="x")
        ctk.CTkLabel(self.__frame_efectivo, text="Importe recibido (EUR)",
                     font=("Arial", 11), anchor="w").pack(fill="x")
        self.__entry_pago = ctk.CTkEntry(
            self.__frame_efectivo, placeholder_text="0.00",
            font=("Arial", 12), height=36)
        self.__entry_pago.pack(fill="x", pady=(3, 5))
        self.__frame_efectivo.pack_forget()

        frame_precio = ctk.CTkFrame(col_der, fg_color="#D6EAF8", corner_radius=8)
        frame_precio.pack(padx=15, pady=10, fill="x")

        ctk.CTkLabel(frame_precio, text="Precio total (IVA 10% incluido)",
                     font=("Arial", 10), text_color="#555555"
                     ).pack(pady=(8, 2))
        self.__lbl_precio = ctk.CTkLabel(
            frame_precio, text="27.50 EUR",
            font=("Arial", 26, "bold"), text_color="#1A6B9A")
        self.__lbl_precio.pack()

        self.__lbl_descuento = ctk.CTkLabel(
            frame_precio, text="",
            font=("Arial", 10), text_color="#1E8449")
        self.__lbl_descuento.pack(pady=(0, 8))

        self.__lbl_msg_venta = ctk.CTkLabel(
            col_der, text="", font=("Arial", 11))
        self.__lbl_msg_venta.pack(padx=15)

        ctk.CTkButton(
            col_der,
            text="✅ Vender Ticket",
            font=("Arial", 13, "bold"),
            fg_color="#1E8449", hover_color="#27AE60",
            height=44, corner_radius=8,
            command=self.__vender
        ).pack(padx=15, pady=10, fill="x")

        self.__frame_recibo = ctk.CTkFrame(
            scroll, fg_color="#F7FBFE", corner_radius=10,
            border_width=1, border_color="#D6EAF8")

        self.__actualizar_precio()

    def __toggle_efectivo(self, *args):
        if self.__sel_pago.get() == "Efectivo":
            self.__frame_efectivo.pack(padx=15, fill="x")
        else:
            self.__frame_efectivo.pack_forget()
        self.__actualizar_precio()

    def __actualizar_precio(self, *args):
        try:
            tipo = self.__sel_ticket.get()
            visitante = self.__sel_visitante.get()
            fp = self.__chk_fastpass.get()
            try:
                cantidad = int(self.__entry_cantidad.get() or 1)
            except ValueError:
                cantidad = 1

            _, total, descuento = self.__controller.calcular_precio(
                tipo, visitante, fp, cantidad)
            self.__lbl_precio.configure(text=f"{total} EUR")
            if descuento > 0:
                self.__lbl_descuento.configure(
                    text=f"✅ Descuento grupo aplicado: -{descuento:.2f} EUR")
            else:
                self.__lbl_descuento.configure(text="")
        except Exception:
            pass

    def __vender(self):
        try:
            nombre = self.__entry_nombre.get().strip()
            if not nombre:
                self.__lbl_msg_venta.configure(
                    text="❌ Introduce el nombre del visitante",
                    text_color="#E74C3C")
                return

            zona_key = self.__sel_zona.get()
            id_zona = self.__zonas_dict.get(zona_key)

            try:
                cantidad = int(self.__entry_cantidad.get() or 1)
            except ValueError:
                cantidad = 1

            pago_recibido = 0.0
            if self.__sel_pago.get() == "Efectivo":
                try:
                    pago_recibido = float(self.__entry_pago.get() or 0)
                except ValueError:
                    self.__lbl_msg_venta.configure(
                        text="❌ Introduce el importe recibido",
                        text_color="#E74C3C")
                    return

            ticket = self.__controller.vender_ticket(
                tipo=self.__sel_ticket.get(),
                tipo_visitante=self.__sel_visitante.get(),
                id_empleado=self.__usuario['id_empleado'],
                nombre_visitante=nombre,
                id_zona=id_zona,
                metodo_pago=self.__sel_pago.get(),
                fast_pass=self.__chk_fastpass.get(),
                cantidad=cantidad,
                pago_recibido=pago_recibido
            )

            self.__mostrar_recibo(ticket)
            self.__lbl_msg_venta.configure(
                text=f"✅ Ticket vendido: {ticket['localizador']}",
                text_color="#1E8449")
            self.__entry_nombre.delete(0, "end")
            self.__entry_cantidad.delete(0, "end")
            self.__entry_cantidad.insert(0, "1")
            self.__entry_pago.delete(0, "end")
            self.__cargar_tickets_hoy()
            self.__cargar_estadisticas()

        except Exception as e:
            self.__lbl_msg_venta.configure(
                text=f"❌ {e}", text_color="#E74C3C")

    def __mostrar_recibo(self, ticket):
        for w in self.__frame_recibo.winfo_children():
            w.destroy()

        self.__frame_recibo.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            self.__frame_recibo,
            text="🎟️ RECIBO DE COMPRA",
            font=("Arial", 14, "bold"), text_color="#1A6B9A"
        ).pack(pady=(15, 10))

        campos = [
            ("Localizador", ticket['localizador']),
            ("Visitante", ticket['nombre_visitante']),
            ("Tipo ticket", ticket['tipo']),
            ("Tipo visitante", ticket['tipo_visitante']),
            ("Zona destino", ticket['zona']),
            ("Fast Pass", "Sí" if ticket['fast_pass'] else "No"),
            ("Precio base", f"{ticket['precio_base']:.2f} EUR"),
            ("Descuento", f"-{ticket['descuento']:.2f} EUR" if ticket['descuento'] > 0 else "No"),
            ("Total con IVA", f"{ticket['precio_total']:.2f} EUR"),
            ("Método de pago", ticket['metodo_pago']),
        ]

        if ticket['metodo_pago'] == 'Efectivo':
            campos.append(("Cambio", f"{ticket['cambio']:.2f} EUR"))

        for i, (label, valor) in enumerate(campos):
            color = "#F7FBFE" if i % 2 == 0 else "white"
            f = ctk.CTkFrame(self.__frame_recibo, fg_color=color, corner_radius=4)
            f.pack(fill="x", padx=10, pady=1)
            ctk.CTkLabel(f, text=label, font=("Arial", 10, "bold"),
                         text_color="#1A6B9A", width=150, anchor="w"
                         ).pack(side="left", padx=10, pady=5)
            ctk.CTkLabel(f, text=str(valor), font=("Arial", 10),
                         text_color="#2C3E50", anchor="w"
                         ).pack(side="left", padx=5, pady=5)

        ctk.CTkLabel(
            self.__frame_recibo,
            text="¡Gracias por su visita a AguaParaíso!",
            font=("Arial", 10, "bold"), text_color="#1E8449"
        ).pack(pady=(5, 15))

    # ============================================
    # PESTAÑA 2: BUSCAR TICKET
    # ============================================
    def __construir_buscar(self):
        tab = self.__tabs.tab("Buscar ticket")
        frame = ctk.CTkFrame(tab, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Localizador del ticket",
                     font=("Arial", 12), anchor="w").pack(fill="x", pady=(10, 2))
        self.__entry_localizador = ctk.CTkEntry(
            frame, placeholder_text="Ej: AGP-2026-XXXXXXXX",
            font=("Arial", 12), height=38)
        self.__entry_localizador.pack(fill="x", pady=(2, 10))

        ctk.CTkButton(
            frame, text="🔍 Buscar",
            font=("Arial", 13, "bold"), fg_color="#1A6B9A",
            height=42, command=self.__buscar_ticket
        ).pack(fill="x", pady=5)

        self.__frame_resultado = ctk.CTkFrame(
            frame, fg_color="#F7FBFE", corner_radius=10,
            border_width=1, border_color="#D6EAF8")

    def __buscar_ticket(self):
        for w in self.__frame_resultado.winfo_children():
            w.destroy()

        localizador = self.__entry_localizador.get().strip().upper()
        if not localizador:
            return

        ticket = self.__controller.buscar_ticket(localizador)
        self.__frame_resultado.pack(fill="x", pady=10)

        if not ticket:
            ctk.CTkLabel(
                self.__frame_resultado,
                text="❌ Ticket no encontrado",
                font=("Arial", 12), text_color="#E74C3C"
            ).pack(pady=20)
            return

        campos = [
            ("Localizador", ticket['localizador']),
            ("Visitante", ticket['visitante'] or "—"),
            ("Tipo ticket", ticket['tipo']),
            ("Tipo visitante", ticket['tipo_visitante']),
            ("Zona destino", ticket['zona_nombre'] or "—"),
            ("Precio total", f"{ticket['precio_total']:.2f} EUR"),
            ("Fast Pass", "Sí" if ticket['fast_pass'] else "No"),
            ("Taquillero", ticket['taquillero']),
            ("Fecha", ticket['fecha']),
        ]

        ctk.CTkLabel(
            self.__frame_resultado,
            text="✅ Ticket encontrado",
            font=("Arial", 13, "bold"), text_color="#1E8449"
        ).pack(pady=(15, 10))

        for i, (label, valor) in enumerate(campos):
            color = "#F7FBFE" if i % 2 == 0 else "white"
            f = ctk.CTkFrame(self.__frame_resultado, fg_color=color, corner_radius=4)
            f.pack(fill="x", padx=10, pady=1)
            ctk.CTkLabel(f, text=label, font=("Arial", 10, "bold"),
                         text_color="#1A6B9A", width=150, anchor="w"
                         ).pack(side="left", padx=10, pady=5)
            ctk.CTkLabel(f, text=str(valor), font=("Arial", 10),
                         text_color="#2C3E50", anchor="w"
                         ).pack(side="left", padx=5, pady=5)

        ctk.CTkLabel(self.__frame_resultado, text="").pack(pady=5)

    # ============================================
    # PESTAÑA 3: CANCELAR TICKET
    # ============================================
    def __construir_cancelar(self):
        tab = self.__tabs.tab("Cancelar ticket")
        frame = ctk.CTkFrame(tab, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            frame,
            text="Introduce el localizador del ticket a cancelar",
            font=("Arial", 13), text_color="#555555"
        ).pack(pady=(10, 15))

        ctk.CTkLabel(frame, text="Localizador",
                     font=("Arial", 12), anchor="w").pack(fill="x", pady=(5, 2))
        self.__entry_cancel_loc = ctk.CTkEntry(
            frame, placeholder_text="Ej: AGP-2026-XXXXXXXX",
            font=("Arial", 12), height=38)
        self.__entry_cancel_loc.pack(fill="x", pady=(2, 10))

        ctk.CTkLabel(frame, text="Zona (para decrementar aforo)",
                     font=("Arial", 12), anchor="w").pack(fill="x", pady=(5, 2))
        zonas = self.__db.consultar("SELECT id_zona, nombre FROM zonas ORDER BY id_zona")
        self.__zonas_cancel = {z['nombre']: z['id_zona'] for z in zonas}
        self.__sel_zona_cancel = ctk.CTkComboBox(
            frame, values=list(self.__zonas_cancel.keys()),
            font=("Arial", 12), height=38)
        self.__sel_zona_cancel.pack(fill="x", pady=(2, 10))

        self.__lbl_cancel = ctk.CTkLabel(frame, text="", font=("Arial", 11))
        self.__lbl_cancel.pack(pady=5)

        ctk.CTkButton(
            frame,
            text="❌ Cancelar ticket",
            font=("Arial", 13, "bold"),
            fg_color="#922B21", hover_color="#CB4335",
            height=42, command=self.__cancelar_ticket
        ).pack(fill="x", pady=10)

    def __cancelar_ticket(self):
        try:
            localizador = self.__entry_cancel_loc.get().strip().upper()
            zona_nombre = self.__sel_zona_cancel.get()
            id_zona = self.__zonas_cancel.get(zona_nombre)

            if not localizador:
                self.__lbl_cancel.configure(
                    text="❌ Introduce el localizador",
                    text_color="#E74C3C")
                return

            self.__controller.cancelar_ticket(localizador, id_zona)
            self.__lbl_cancel.configure(
                text=f"✅ Ticket {localizador} cancelado correctamente",
                text_color="#1E8449")
            self.__entry_cancel_loc.delete(0, "end")
            self.__cargar_tickets_hoy()
            self.__cargar_estadisticas()

        except Exception as e:
            self.__lbl_cancel.configure(
                text=f"❌ {e}", text_color="#E74C3C")

    # ============================================
    # PESTAÑA 4: TICKETS HOY
    # ============================================
    def __construir_tickets_hoy(self):
        tab = self.__tabs.tab("Tickets hoy")
        ctk.CTkButton(
            tab, text="🔄 Actualizar",
            font=("Arial", 12), fg_color="#1A6B9A", width=130,
            command=self.__cargar_tickets_hoy
        ).pack(pady=10, anchor="e", padx=10)
        self.__frame_tickets = ctk.CTkFrame(tab, fg_color="transparent")
        self.__frame_tickets.pack(fill="both", expand=True, padx=10)
        self.__cargar_tickets_hoy()

    def __cargar_tickets_hoy(self):
        for w in self.__frame_tickets.winfo_children():
            w.destroy()
        tickets = self.__controller.obtener_tickets_hoy()
        columnas = ["Localizador", "Visitante", "Tipo", "Zona", "Total", "FP", "Hora"]
        datos = []
        for t in tickets:
            datos.append([
                t['localizador'],
                t['visitante'] or "—",
                t['tipo'],
                t['zona_nombre'] or "—",
                f"{t['precio_total']:.2f} EUR",
                "Sí" if t['fast_pass'] else "No",
                t['fecha'][-8:-3] if t['fecha'] else "—"
            ])
        TablaDinamica(self.__frame_tickets, columnas=columnas,
                      datos=datos).pack(fill="both", expand=True)

    # ============================================
    # PESTAÑA 5: ESTADÍSTICAS
    # ============================================
    def __construir_estadisticas(self):
        tab = self.__tabs.tab("Estadísticas")
        ctk.CTkButton(
            tab, text="🔄 Actualizar",
            font=("Arial", 12), fg_color="#1A6B9A", width=130,
            command=self.__cargar_estadisticas
        ).pack(pady=10, anchor="e", padx=10)
        self.__frame_stats = ctk.CTkFrame(tab, fg_color="transparent")
        self.__frame_stats.pack(fill="both", expand=True, padx=20, pady=10)
        self.__cargar_estadisticas()

    def __cargar_estadisticas(self):
        for w in self.__frame_stats.winfo_children():
            w.destroy()

        stats = self.__controller.estadisticas_taquilla()

        cards = [
            ("🎟️ Tickets vendidos hoy", str(stats['total_tickets']), "#1A6B9A"),
            ("💰 Ingresos hoy", f"{stats['total_ingresos']:.2f} EUR", "#1E8449"),
            ("📊 Ticket medio", f"{stats['ticket_medio']:.2f} EUR", "#6C3483"),
            ("🗺️ Zona más visitada", stats['zona_mas_visitada'], "#BA4A00"),
        ]

        frame_cards = ctk.CTkFrame(self.__frame_stats, fg_color="transparent")
        frame_cards.pack(fill="x", pady=10)

        for titulo, valor, color in cards:
            card = ctk.CTkFrame(
                frame_cards, fg_color=color,
                corner_radius=12, width=180, height=90
            )
            card.pack(side="left", padx=8, pady=5)
            card.pack_propagate(False)
            ctk.CTkLabel(card, text=titulo, font=("Arial", 10),
                         text_color="white").pack(pady=(12, 3))
            ctk.CTkLabel(card, text=valor, font=("Arial", 18, "bold"),
                         text_color="white").pack()

        ctk.CTkLabel(
            self.__frame_stats,
            text="Ingresos por tipo de ticket",
            font=("Arial", 14, "bold"), text_color="#1A6B9A"
        ).pack(pady=(20, 5), anchor="w")

        ingresos = self.__controller.ingresos_hoy()
        if ingresos:
            columnas = ["Tipo ticket", "Cantidad", "Total EUR"]
            datos = [[d['tipo'], str(d['cantidad']),
                      f"{d['total']:.2f}"] for d in ingresos]
            frame_tabla = ctk.CTkFrame(self.__frame_stats, fg_color="transparent")
            frame_tabla.pack(fill="x")
            TablaDinamica(frame_tabla, columnas=columnas,
                          datos=datos).pack(fill="x")
        else:
            ctk.CTkLabel(
                self.__frame_stats,
                text="Sin ventas hoy todavía",
                font=("Arial", 11), text_color="#AAAAAA"
            ).pack(pady=10)