# ============================================
# AguaParaíso - Vista Eventos
# Sistema ERP SmartPark Pro
# ============================================

import customtkinter as ctk
from controllers.evento_controller import EventoController
from database.connection import Database
from views.components.tabla_dinamica import TablaDinamica
from utils.logger import Logger


class EventosView(ctk.CTkFrame):
    """Módulo de gestión de eventos e incidencias del parque."""

    def __init__(self, parent, usuario):
        super().__init__(parent, fg_color="transparent")
        self.__usuario = usuario
        self.__controller = EventoController()
        self.__db = Database.obtener_instancia()
        self.__construir_ui()
        self.pack(fill="both", expand=True)

    def __construir_ui(self):
        ctk.CTkLabel(
            self, text="⚡ Módulo Eventos",
            font=("Arial", 22, "bold"), text_color="#1A6B9A"
        ).pack(pady=(20, 10), padx=20, anchor="w")

        self.__tabs = ctk.CTkTabview(self, fg_color="white")
        self.__tabs.pack(fill="both", expand=True, padx=20, pady=10)
        self.__tabs.add("Eventos activos")
        self.__tabs.add("Historial")
        self.__tabs.add("Registrar incidencia")
        self.__tabs.add("Resolver evento")

        self.__construir_tab_activos()
        self.__construir_tab_historial()
        self.__construir_tab_registrar()
        self.__construir_tab_resolver()

    def __construir_tab_activos(self):
        tab = self.__tabs.tab("Eventos activos")

        ctk.CTkButton(
            tab, text="🔄 Actualizar",
            font=("Arial", 12), fg_color="#1A6B9A", width=130,
            command=self.__cargar_activos
        ).pack(pady=10, anchor="e", padx=10)

        self.__frame_activos = ctk.CTkFrame(tab, fg_color="transparent")
        self.__frame_activos.pack(fill="both", expand=True, padx=10, pady=5)
        self.__cargar_activos()

    def __cargar_activos(self):
        for w in self.__frame_activos.winfo_children():
            w.destroy()
        eventos = self.__controller.obtener_eventos_activos()
        columnas = ["ID", "Tipo", "Descripción", "Zona", "Estado", "Inicio"]
        datos = []
        for e in eventos:
            datos.append([
                str(e['id_evento']),
                e['tipo'],
                e['descripcion'],
                e['zona_nombre'] or "Global",
                e['estado'],
                e['fecha_inicio']
            ])
        TablaDinamica(self.__frame_activos, columnas=columnas,
                      datos=datos).pack(fill="both", expand=True)

    def __construir_tab_historial(self):
        tab = self.__tabs.tab("Historial")

        ctk.CTkButton(
            tab, text="🔄 Actualizar",
            font=("Arial", 12), fg_color="#1A6B9A", width=130,
            command=self.__cargar_historial
        ).pack(pady=10, anchor="e", padx=10)

        self.__frame_historial = ctk.CTkFrame(tab, fg_color="transparent")
        self.__frame_historial.pack(fill="both", expand=True, padx=10)
        self.__cargar_historial()

    def __cargar_historial(self):
        for w in self.__frame_historial.winfo_children():
            w.destroy()
        eventos = self.__controller.obtener_todos_eventos()
        columnas = ["ID", "Tipo", "Descripción", "Zona", "Estado", "Inicio", "Fin"]
        datos = []
        for e in eventos:
            datos.append([
                str(e['id_evento']),
                e['tipo'],
                e['descripcion'],
                e['zona_nombre'] or "Global",
                e['estado'],
                e['fecha_inicio'],
                e['fecha_fin'] or "—"
            ])
        TablaDinamica(self.__frame_historial, columnas=columnas,
                      datos=datos).pack(fill="both", expand=True)

    def __construir_tab_registrar(self):
        tab = self.__tabs.tab("Registrar incidencia")

        frame = ctk.CTkFrame(tab, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(
            frame,
            text="Registrar nueva incidencia en el parque",
            font=("Arial", 13), text_color="#555555"
        ).pack(pady=(10, 15))

        # Tipo de incidencia
        ctk.CTkLabel(frame, text="Tipo de incidencia",
                     font=("Arial", 12), anchor="w").pack(fill="x", pady=(5, 2))
        self.__sel_tipo = ctk.CTkComboBox(
            frame,
            values=["Averia", "Climatico", "Sanitario", "Stock", "Aforo"],
            font=("Arial", 12), height=38
        )
        self.__sel_tipo.pack(fill="x", pady=(2, 10))

        # Zona afectada
        ctk.CTkLabel(frame, text="Zona afectada",
                     font=("Arial", 12), anchor="w").pack(fill="x", pady=(5, 2))

        zonas = self.__db.consultar("SELECT id_zona, nombre FROM zonas ORDER BY id_zona")
        nombres_zonas = ["Global"] + [z['nombre'] for z in zonas]
        self.__ids_zonas = {z['nombre']: z['id_zona'] for z in zonas}

        self.__sel_zona = ctk.CTkComboBox(
            frame,
            values=nombres_zonas,
            font=("Arial", 12), height=38
        )
        self.__sel_zona.pack(fill="x", pady=(2, 10))

        # Descripción
        ctk.CTkLabel(frame, text="Descripción de la incidencia",
                     font=("Arial", 12), anchor="w").pack(fill="x", pady=(5, 2))
        self.__entry_desc = ctk.CTkEntry(
            frame,
            placeholder_text="Describe la incidencia con detalle...",
            font=("Arial", 12), height=38
        )
        self.__entry_desc.pack(fill="x", pady=(2, 10))

        # Empleado responsable
        ctk.CTkLabel(frame, text="ID Empleado responsable (opcional)",
                     font=("Arial", 12), anchor="w").pack(fill="x", pady=(5, 2))
        self.__entry_emp = ctk.CTkEntry(
            frame,
            placeholder_text="Ej: 3",
            font=("Arial", 12), height=38
        )
        self.__entry_emp.pack(fill="x", pady=(2, 10))

        self.__lbl_registrar = ctk.CTkLabel(frame, text="", font=("Arial", 11))
        self.__lbl_registrar.pack(pady=5)

        ctk.CTkButton(
            frame,
            text="📋 Registrar incidencia",
            font=("Arial", 13, "bold"),
            fg_color="#BA4A00",
            hover_color="#E67E22",
            height=42,
            command=self.__registrar_incidencia
        ).pack(fill="x", pady=10)

    def __registrar_incidencia(self):
        try:
            tipo = self.__sel_tipo.get()
            zona_nombre = self.__sel_zona.get()
            descripcion = self.__entry_desc.get().strip()
            emp_str = self.__entry_emp.get().strip()

            if not descripcion:
                self.__lbl_registrar.configure(
                    text="❌ La descripción es obligatoria",
                    text_color="#E74C3C"
                )
                return

            id_zona = self.__ids_zonas.get(zona_nombre) if zona_nombre != "Global" else None
            id_empleado = int(emp_str) if emp_str else None

            query = """
                INSERT INTO eventos (tipo, descripcion, id_zona, id_empleado, estado, fecha_inicio)
                VALUES (?, ?, ?, ?, 'Activo', datetime('now'))
            """
            self.__db.ejecutar(query, (tipo, descripcion, id_zona, id_empleado))
            Logger.warning(f"Incidencia registrada manualmente: {tipo} — {descripcion}")

            self.__lbl_registrar.configure(
                text=f"✅ Incidencia registrada correctamente",
                text_color="#1E8449"
            )
            self.__entry_desc.delete(0, "end")
            self.__entry_emp.delete(0, "end")
            self.__cargar_activos()
            self.__cargar_historial()

        except Exception as e:
            self.__lbl_registrar.configure(
                text=f"❌ Error: {e}",
                text_color="#E74C3C"
            )
            Logger.error(f"Error al registrar incidencia: {e}")

    def __construir_tab_resolver(self):
        tab = self.__tabs.tab("Resolver evento")

        frame = ctk.CTkFrame(tab, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(
            frame,
            text="Introduce el ID del evento a resolver",
            font=("Arial", 13), text_color="#555555"
        ).pack(pady=(20, 10))

        ctk.CTkLabel(frame, text="ID Evento",
                     font=("Arial", 12), anchor="w").pack(fill="x", pady=(10, 2))
        self.__entry_id_evento = ctk.CTkEntry(
            frame, placeholder_text="Ej: 1",
            font=("Arial", 12), height=38
        )
        self.__entry_id_evento.pack(fill="x", pady=(2, 10))

        ctk.CTkLabel(frame, text="ID Empleado que resuelve (opcional)",
                     font=("Arial", 12), anchor="w").pack(fill="x", pady=(10, 2))
        self.__entry_id_empleado = ctk.CTkEntry(
            frame, placeholder_text="Ej: 3",
            font=("Arial", 12), height=38
        )
        self.__entry_id_empleado.pack(fill="x", pady=(2, 10))

        self.__lbl_resolver = ctk.CTkLabel(frame, text="", font=("Arial", 11))
        self.__lbl_resolver.pack(pady=5)

        ctk.CTkButton(
            frame,
            text="✅ Resolver evento",
            font=("Arial", 13, "bold"),
            fg_color="#1E8449",
            hover_color="#27AE60",
            height=42,
            command=self.__resolver
        ).pack(fill="x", pady=10)

    def __resolver(self):
        try:
            id_evento = int(self.__entry_id_evento.get())
            id_emp_str = self.__entry_id_empleado.get().strip()
            id_empleado = int(id_emp_str) if id_emp_str else None

            self.__controller.resolver_evento(id_evento, id_empleado)
            self.__lbl_resolver.configure(
                text=f"✅ Evento {id_evento} resuelto correctamente",
                text_color="#1E8449"
            )
            self.__cargar_activos()
            self.__cargar_historial()
            self.__entry_id_evento.delete(0, "end")
            self.__entry_id_empleado.delete(0, "end")
        except Exception as e:
            self.__lbl_resolver.configure(
                text=f"❌ Error: {e}",
                text_color="#E74C3C"
            )