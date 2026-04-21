# ============================================
# AguaParaíso - Vista Dashboard
# Sistema ERP SmartPark Pro
# ============================================

import customtkinter as ctk
from controllers.reporting_controller import ReportingController
from controllers.evento_controller import EventoController
from utils.logger import Logger
from config.settings import Settings


class DashboardView(ctk.CTk):
    """Ventana principal del sistema ERP AguaParaíso."""

    def __init__(self, usuario):
        super().__init__()
        self.__usuario = usuario
        self.__reporting = ReportingController()
        self.__eventos = EventoController()
        self.__intervalo = Settings.intervalo_eventos() * 1000

        self.__configurar_ventana()
        self.__construir_ui()
        self.after(100, self.__mostrar_home)
        self.after(self.__intervalo, self.__ciclo_eventos)

    def __configurar_ventana(self):
        self.title(f"AguaParaíso — {self.__usuario['rol']}")
        self.geometry("1200x700")
        self.state("zoomed")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color="#F0F8FF")

    def __construir_ui(self):
        # Header
        header = ctk.CTkFrame(self, height=60, fg_color="#1A6B9A", corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="🌊 AguaParaíso — SmartPark Pro",
            font=("Arial", 20, "bold"),
            text_color="white"
        ).pack(side="left", padx=20, pady=10)

        ctk.CTkLabel(
            header,
            text=f"👤 {self.__usuario['username']} — {self.__usuario['rol']}",
            font=("Arial", 12),
            text_color="white"
        ).pack(side="right", padx=20)

        # Layout principal
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Sidebar
        self.__construir_sidebar(main)

        # Contenido
        self.__frame_contenido = ctk.CTkFrame(
            main, fg_color="white", corner_radius=12,
            border_width=1, border_color="#D6EAF8"
        )
        self.__frame_contenido.pack(side="right", fill="both", expand=True, padx=(10, 0))

    def __construir_sidebar(self, parent):
        sidebar = ctk.CTkFrame(
            parent, width=200, fg_color="white",
            corner_radius=12, border_width=1, border_color="#D6EAF8"
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ctk.CTkLabel(
            sidebar,
            text="MENÚ",
            font=("Arial", 11, "bold"),
            text_color="#AAAAAA"
        ).pack(pady=(20, 10))

        rol = self.__usuario['rol']
        botones = self.__obtener_botones_por_rol(rol)

        for texto, comando in botones:
            ctk.CTkButton(
                sidebar,
                text=texto,
                font=("Arial", 12),
                fg_color="transparent",
                text_color="#2C3E50",
                hover_color="#D6EAF8",
                anchor="w",
                height=40,
                corner_radius=8,
                command=comando
            ).pack(fill="x", padx=10, pady=2)

        ctk.CTkButton(
            sidebar,
            text="🚪 Cerrar sesión",
            font=("Arial", 12),
            fg_color="#FADBD8",
            text_color="#922B21",
            hover_color="#F5B7B1",
            height=40,
            corner_radius=8,
            command=self.__cerrar_sesion
        ).pack(fill="x", padx=10, pady=10, side="bottom")

    def __obtener_botones_por_rol(self, rol):
        botones = [("🏠 Inicio", self.__mostrar_home)]

        if rol in ['Admin', 'Taquillero']:
            botones.append(("🎟️ Taquilla", self.__abrir_taquilla))
        if rol in ['Admin']:
            botones.append(("👷 Administrativo", self.__abrir_admin))
        if rol in ['Admin', 'Encargado', 'Tecnico', 'Camarero']:
            botones.append(("📦 Logística", self.__abrir_logistica))
        if rol in ['Admin', 'Encargado', 'Tecnico']:
            botones.append(("⚡ Eventos", self.__abrir_eventos))
        if rol in ['Admin', 'Enfermero']:
            botones.append(("🏥 Sanitario", self.__abrir_sanitario))
        if rol in ['Admin', 'Encargado']:
            botones.append(("🗺️ Zonas", self.__abrir_zonas))
            botones.append(("📊 Reporting", self.__abrir_reporting))
        botones.append(("👤 Mi perfil", self.__abrir_perfil))
        return botones

    def __limpiar_contenido(self):
        for widget in self.__frame_contenido.winfo_children():
            widget.destroy()

    def __mostrar_home(self):
        self.__limpiar_contenido()
        try:
            resumen = self.__reporting.resumen_dia()
            eventos = self.__eventos.obtener_eventos_activos()
        except Exception:
            return

        ctk.CTkLabel(
            self.__frame_contenido,
            text="Panel de Control",
            font=("Arial", 22, "bold"),
            text_color="#1A6B9A"
        ).pack(pady=(20, 10), padx=20, anchor="w")

        # Tarjetas resumen
        frame_cards = ctk.CTkFrame(self.__frame_contenido, fg_color="transparent")
        frame_cards.pack(fill="x", padx=20, pady=10)

        cards = [
            ("🎟️ Tickets hoy", str(resumen['total_tickets']), "#1A6B9A"),
            ("💰 Ingresos hoy", f"{resumen['total_ingresos']:.2f}€", "#1E8449"),
            ("⚡ Eventos activos", str(resumen['eventos_activos']), "#BA4A00"),
            ("🗺️ Zonas abiertas", str(resumen['zonas_abiertas']), "#6C3483"),
        ]

        for titulo, valor, color in cards:
            card = ctk.CTkFrame(
                frame_cards, fg_color=color,
                corner_radius=12, width=200, height=100
            )
            card.pack(side="left", padx=10, pady=5)
            card.pack_propagate(False)
            ctk.CTkLabel(card, text=titulo, font=("Arial", 11),
                         text_color="white").pack(pady=(15, 5))
            ctk.CTkLabel(card, text=valor, font=("Arial", 24, "bold"),
                         text_color="white").pack()

        # Alertas eventos activos
        if eventos:
            ctk.CTkLabel(
                self.__frame_contenido,
                text="⚠️ Eventos activos",
                font=("Arial", 16, "bold"),
                text_color="#BA4A00"
            ).pack(pady=(20, 5), padx=20, anchor="w")

            for ev in eventos[:5]:
                frame_ev = ctk.CTkFrame(
                    self.__frame_contenido,
                    fg_color="#FAE5D3",
                    corner_radius=8
                )
                frame_ev.pack(fill="x", padx=20, pady=3)
                ctk.CTkLabel(
                    frame_ev,
                    text=f"⚡ {ev['tipo']} — {ev['descripcion']}",
                    font=("Arial", 11),
                    text_color="#BA4A00"
                ).pack(padx=15, pady=8, anchor="w")

    def __ciclo_eventos(self):
        """Motor de eventos automático — se ejecuta cada X minutos."""
        try:
            evento = self.__eventos.generar_evento_aleatorio()
            if evento:
                Logger.warning(f"Evento automático generado: {evento.tipo} — {evento.descripcion}")
                self.__mostrar_home()
        except Exception as e:
            Logger.error(f"Error en ciclo de eventos: {e}")
        finally:
            self.after(self.__intervalo, self.__ciclo_eventos)

    def __abrir_taquilla(self):
        self.__limpiar_contenido()
        from views.taquilla_view import TaquillaView
        TaquillaView(self.__frame_contenido, self.__usuario)

    def __abrir_admin(self):
        self.__limpiar_contenido()
        from views.admin_view import AdminView
        AdminView(self.__frame_contenido, self.__usuario)

    def __abrir_logistica(self):
        self.__limpiar_contenido()
        from views.logistica_view import LogisticaView
        LogisticaView(self.__frame_contenido, self.__usuario)

    def __abrir_eventos(self):
        self.__limpiar_contenido()
        from views.eventos_view import EventosView
        EventosView(self.__frame_contenido, self.__usuario)

    def __abrir_sanitario(self):
        self.__limpiar_contenido()
        from views.sanitario_view import SanitarioView
        SanitarioView(self.__frame_contenido, self.__usuario)

    def __abrir_zonas(self):
        self.__limpiar_contenido()
        from views.zonas_view import ZonasView
        ZonasView(self.__frame_contenido, self.__usuario)

    def __abrir_reporting(self):
        self.__limpiar_contenido()
        from views.reporting_view import ReportingView
        ReportingView(self.__frame_contenido, self.__usuario)

    def __abrir_perfil(self):
        self.__limpiar_contenido()
        from views.perfil_view import PerfilView
        PerfilView(self.__frame_contenido, self.__usuario)

    def __cerrar_sesion(self):
        Logger.info(f"Cierre de sesión: {self.__usuario['username']}")
        self.destroy()
        from main import main
        main()