# ============================================
# AguaParaíso - Vista Reporting
# Sistema ERP SmartPark Pro
# ============================================

import customtkinter as ctk
from controllers.reporting_controller import ReportingController
from views.components.tabla_dinamica import TablaDinamica


class ReportingView(ctk.CTkFrame):
    """Módulo de reporting y estadísticas."""

    def __init__(self, parent, usuario):
        super().__init__(parent, fg_color="transparent")
        self.__usuario = usuario
        self.__controller = ReportingController()
        self.__construir_ui()
        self.pack(fill="both", expand=True)

    def __construir_ui(self):
        ctk.CTkLabel(
            self, text="📊 Módulo Reporting",
            font=("Arial", 22, "bold"), text_color="#1A6B9A"
        ).pack(pady=(20, 10), padx=20, anchor="w")

        self.__tabs = ctk.CTkTabview(self, fg_color="white")
        self.__tabs.pack(fill="both", expand=True, padx=20, pady=10)
        self.__tabs.add("Ganancias")
        self.__tabs.add("Ocupación")
        self.__tabs.add("Empleados")
        self.__tabs.add("Visitantes")
        self.__tabs.add("Histórico")

        self.__construir_ganancias()
        self.__construir_ocupacion()
        self.__construir_empleados()
        self.__construir_visitantes()
        self.__construir_historico()

    def __construir_ganancias(self):
        tab = self.__tabs.tab("Ganancias")
        ctk.CTkButton(tab, text="🔄 Actualizar", font=("Arial", 12),
                      fg_color="#1A6B9A", width=130,
                      command=self.__cargar_ganancias
                      ).pack(pady=10, anchor="e", padx=10)
        self.__frame_gan = ctk.CTkFrame(tab, fg_color="transparent")
        self.__frame_gan.pack(fill="both", expand=True, padx=10)
        self.__cargar_ganancias()

    def __cargar_ganancias(self):
        for w in self.__frame_gan.winfo_children():
            w.destroy()
        datos_bd = self.__controller.ganancias_por_tipo()
        columnas = ["Tipo ticket", "Cantidad", "Total EUR", "Media EUR"]
        datos = [[d['tipo'], str(d['cantidad']),
                  f"{d['total']:.2f}", f"{d['media']:.2f}"] for d in datos_bd]
        TablaDinamica(self.__frame_gan, columnas=columnas,
                      datos=datos).pack(fill="both", expand=True)

    def __construir_ocupacion(self):
        tab = self.__tabs.tab("Ocupación")
        ctk.CTkButton(tab, text="🔄 Actualizar", font=("Arial", 12),
                      fg_color="#1A6B9A", width=130,
                      command=self.__cargar_ocupacion
                      ).pack(pady=10, anchor="e", padx=10)
        self.__frame_ocup = ctk.CTkFrame(tab, fg_color="transparent")
        self.__frame_ocup.pack(fill="both", expand=True, padx=10)
        self.__cargar_ocupacion()

    def __cargar_ocupacion(self):
        for w in self.__frame_ocup.winfo_children():
            w.destroy()
        datos_bd = self.__controller.ocupacion_por_zona()
        columnas = ["Zona", "Aforo actual", "Aforo max", "Estado", "Ocupacion %"]
        datos = [[d['nombre'], str(d['aforo_actual']), str(d['aforo_maximo']),
                  d['estado'], f"{d['porcentaje']}%"] for d in datos_bd]
        TablaDinamica(self.__frame_ocup, columnas=columnas,
                      datos=datos).pack(fill="both", expand=True)

    def __construir_empleados(self):
        tab = self.__tabs.tab("Empleados")
        ctk.CTkButton(tab, text="🔄 Actualizar", font=("Arial", 12),
                      fg_color="#1A6B9A", width=130,
                      command=self.__cargar_empleados
                      ).pack(pady=10, anchor="e", padx=10)
        self.__frame_empl = ctk.CTkFrame(tab, fg_color="transparent")
        self.__frame_empl.pack(fill="both", expand=True, padx=10)
        self.__cargar_empleados()

    def __cargar_empleados(self):
        for w in self.__frame_empl.winfo_children():
            w.destroy()
        datos_bd = self.__controller.empleados_activos_por_turno()
        columnas = ["Zona", "Turno", "Num. empleados"]
        datos = [[d['zona'], d['turno'], str(d['num_empleados'])] for d in datos_bd]
        TablaDinamica(self.__frame_empl, columnas=columnas,
                      datos=datos).pack(fill="both", expand=True)

    def __construir_visitantes(self):
        tab = self.__tabs.tab("Visitantes")
        ctk.CTkButton(tab, text="🔄 Actualizar", font=("Arial", 12),
                      fg_color="#1A6B9A", width=130,
                      command=self.__cargar_visitantes
                      ).pack(pady=10, anchor="e", padx=10)
        self.__frame_vis = ctk.CTkFrame(tab, fg_color="transparent")
        self.__frame_vis.pack(fill="both", expand=True, padx=10)
        self.__cargar_visitantes()

    def __cargar_visitantes(self):
        for w in self.__frame_vis.winfo_children():
            w.destroy()
        datos_bd = self.__controller.visitantes_por_tipo()
        columnas = ["Tipo visitante", "Cantidad", "Total EUR", "Media EUR"]
        datos = [[d['tipo_visitante'], str(d['cantidad']),
                  f"{d['total']:.2f}", f"{d['media']:.2f}"] for d in datos_bd]
        TablaDinamica(self.__frame_vis, columnas=columnas,
                      datos=datos).pack(fill="both", expand=True)

    def __construir_historico(self):
        tab = self.__tabs.tab("Histórico")
        ctk.CTkButton(tab, text="🔄 Actualizar", font=("Arial", 12),
                      fg_color="#1A6B9A", width=130,
                      command=self.__cargar_historico
                      ).pack(pady=10, anchor="e", padx=10)
        self.__frame_hist = ctk.CTkFrame(tab, fg_color="transparent")
        self.__frame_hist.pack(fill="both", expand=True, padx=10)
        self.__cargar_historico()

    def __cargar_historico(self):
        for w in self.__frame_hist.winfo_children():
            w.destroy()
        datos_bd = self.__controller.historico_ingresos_por_dia()
        columnas = ["Fecha", "Tickets vendidos", "Total EUR"]
        datos = [[d['fecha'], str(d['cantidad']),
                  f"{d['total']:.2f}"] for d in datos_bd]
        TablaDinamica(self.__frame_hist, columnas=columnas,
                      datos=datos).pack(fill="both", expand=True)