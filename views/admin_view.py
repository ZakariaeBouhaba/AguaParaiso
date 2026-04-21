# ============================================
# AguaParaíso - Vista Administrativo
# Sistema ERP SmartPark Pro
# ============================================

import customtkinter as ctk
from controllers.admin_controller import AdminController
from views.components.tabla_dinamica import TablaDinamica
from utils.logger import Logger


class AdminView(ctk.CTkFrame):
    """Módulo administrativo — RRHH y nóminas."""

    def __init__(self, parent, usuario):
        super().__init__(parent, fg_color="transparent")
        self.__usuario = usuario
        self.__controller = AdminController()
        self.__construir_ui()
        self.pack(fill="both", expand=True)

    def __construir_ui(self):
        ctk.CTkLabel(
            self,
            text="👷 Módulo Administrativo",
            font=("Arial", 22, "bold"),
            text_color="#1A6B9A"
        ).pack(pady=(20, 10), padx=20, anchor="w")

        # Tabs
        self.__tabs = ctk.CTkTabview(self, fg_color="white")
        self.__tabs.pack(fill="both", expand=True, padx=20, pady=10)

        self.__tabs.add("Empleados")
        self.__tabs.add("Alta empleado")
        self.__tabs.add("Nóminas")

        self.__construir_tab_empleados()
        self.__construir_tab_alta()
        self.__construir_tab_nominas()

    def __construir_tab_empleados(self):
        tab = self.__tabs.tab("Empleados")

        ctk.CTkButton(
            tab,
            text="🔄 Actualizar",
            font=("Arial", 12),
            fg_color="#1A6B9A",
            width=120,
            command=self.__cargar_empleados
        ).pack(pady=10, anchor="e", padx=10)

        self.__frame_emp = ctk.CTkFrame(tab, fg_color="transparent")
        self.__frame_emp.pack(fill="both", expand=True, padx=10)
        self.__cargar_empleados()

    def __cargar_empleados(self):
        for w in self.__frame_emp.winfo_children():
            w.destroy()

        empleados = self.__controller.obtener_empleados()
        columnas = ["ID", "Nombre", "Rol", "Categoría", "Turno", "Zona", "Estado"]
        datos = []
        for e in empleados:
            datos.append([
                str(e['id_empleado']),
                e['nombre'],
                e['rol'],
                e['categoria'],
                e['turno'],
                e['zona_nombre'],
                e['estado']
            ])

        TablaDinamica(
            self.__frame_emp,
            columnas=columnas,
            datos=datos
        ).pack(fill="both", expand=True)

    def __construir_tab_alta(self):
        tab = self.__tabs.tab("Alta empleado")

        frame = ctk.CTkFrame(tab, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        campos = [
            ("nombre", "Nombre completo", "Ej: Juan García López"),
            ("sueldo_base", "Sueldo base (€)", "Ej: 1400"),
        ]

        self.__campos_alta = {}
        for key, label, placeholder in campos:
            ctk.CTkLabel(frame, text=label, font=("Arial", 12),
                         anchor="w").pack(fill="x", pady=(10, 2))
            entrada = ctk.CTkEntry(frame, placeholder_text=placeholder,
                                   font=("Arial", 12), height=38)
            entrada.pack(fill="x")
            self.__campos_alta[key] = entrada

        selectores = [
            ("rol", "Rol", ["Socorrista", "Tecnico", "Taquillero", "Camarero",
                            "PersonalVIP", "Vigilante", "Limpiador", "Administrativo", "Enfermero"]),
            ("categoria", "Categoría", ["Junior", "Senior", "Jefe"]),
            ("turno", "Turno", ["Manana", "Tarde", "Mantenimiento"]),
            ("contrato", "Contrato", ["Fijo", "Temporal"]),
            ("id_zona", "Zona", ["1", "2", "3", "4", "5", "6"]),
        ]

        for key, label, opciones in selectores:
            ctk.CTkLabel(frame, text=label, font=("Arial", 12),
                         anchor="w").pack(fill="x", pady=(10, 2))
            selector = ctk.CTkComboBox(frame, values=opciones,
                                       font=("Arial", 12), height=38)
            selector.pack(fill="x")
            self.__campos_alta[key] = selector

        self.__lbl_alta = ctk.CTkLabel(frame, text="", font=("Arial", 11))
        self.__lbl_alta.pack(pady=5)

        ctk.CTkButton(
            frame,
            text="✅ Dar de alta",
            font=("Arial", 13, "bold"),
            fg_color="#1E8449",
            hover_color="#27AE60",
            height=42,
            command=self.__dar_alta
        ).pack(fill="x", pady=10)

    def __dar_alta(self):
        try:
            datos = {k: v.get() for k, v in self.__campos_alta.items()}
            datos['id_zona'] = int(datos['id_zona'])
            datos['sueldo_base'] = float(datos['sueldo_base'])

            id_emp = self.__controller.alta_empleado(datos)
            self.__lbl_alta.configure(
                text=f"✅ Empleado dado de alta (ID: {id_emp})",
                text_color="#1E8449"
            )
            self.__cargar_empleados()
        except Exception as e:
            self.__lbl_alta.configure(
                text=f"❌ Error: {e}",
                text_color="#E74C3C"
            )

    def __construir_tab_nominas(self):
        tab = self.__tabs.tab("Nóminas")

        frame_form = ctk.CTkFrame(tab, fg_color="transparent")
        frame_form.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame_form, text="ID Empleado",
                     font=("Arial", 12)).pack(anchor="w")
        self.__entry_id_emp = ctk.CTkEntry(
            frame_form, placeholder_text="Ej: 1",
            font=("Arial", 12), height=38
        )
        self.__entry_id_emp.pack(fill="x", pady=(2, 10))

        ctk.CTkLabel(frame_form, text="Mes (YYYY-MM)",
                     font=("Arial", 12)).pack(anchor="w")
        self.__entry_mes = ctk.CTkEntry(
            frame_form, placeholder_text="Ej: 2026-07",
            font=("Arial", 12), height=38
        )
        self.__entry_mes.pack(fill="x", pady=(2, 10))

        ctk.CTkLabel(frame_form, text="Horas extra",
                     font=("Arial", 12)).pack(anchor="w")
        self.__entry_horas = ctk.CTkEntry(
            frame_form, placeholder_text="Ej: 5",
            font=("Arial", 12), height=38
        )
        self.__entry_horas.pack(fill="x", pady=(2, 10))

        self.__lbl_nomina = ctk.CTkLabel(frame_form, text="", font=("Arial", 12))
        self.__lbl_nomina.pack(pady=5)

        ctk.CTkButton(
            frame_form,
            text="💰 Calcular nómina",
            font=("Arial", 13, "bold"),
            fg_color="#1A6B9A",
            height=42,
            command=self.__calcular_nomina
        ).pack(fill="x", pady=5)

    def __calcular_nomina(self):
        try:
            id_emp = int(self.__entry_id_emp.get())
            mes = self.__entry_mes.get()
            horas = int(self.__entry_horas.get() or 0)
            neto = self.__controller.calcular_nomina(id_emp, mes, horas)
            self.__lbl_nomina.configure(
                text=f"✅ Nómina calculada: {neto}€ neto",
                text_color="#1E8449"
            )
        except Exception as e:
            self.__lbl_nomina.configure(
                text=f"❌ Error: {e}",
                text_color="#E74C3C"
            )