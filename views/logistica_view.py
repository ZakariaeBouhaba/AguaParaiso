# ============================================
# AguaParaíso - Vista Logística
# Sistema ERP SmartPark Pro
# ============================================

import customtkinter as ctk
from controllers.logistica_controller import LogisticaController
from views.components.tabla_dinamica import TablaDinamica
from utils.logger import Logger


class LogisticaView(ctk.CTkFrame):
    """Módulo de logística e inventario."""

    def __init__(self, parent, usuario):
        super().__init__(parent, fg_color="transparent")
        self.__usuario = usuario
        self.__controller = LogisticaController()
        self.__construir_ui()
        self.pack(fill="both", expand=True)

    def __construir_ui(self):
        ctk.CTkLabel(
            self, text="📦 Módulo Logística",
            font=("Arial", 22, "bold"), text_color="#1A6B9A"
        ).pack(pady=(20, 10), padx=20, anchor="w")

        self.__tabs = ctk.CTkTabview(self, fg_color="white")
        self.__tabs.pack(fill="both", expand=True, padx=20, pady=10)
        self.__tabs.add("Inventario")
        self.__tabs.add("Alertas Stock")
        self.__tabs.add("Reponer")

        self.__construir_inventario()
        self.__construir_alertas()
        self.__construir_reponer()

    def __construir_inventario(self):
        tab = self.__tabs.tab("Inventario")
        ctk.CTkButton(tab, text="🔄 Actualizar", font=("Arial", 12),
                      fg_color="#1A6B9A", width=120,
                      command=self.__cargar_inventario
                      ).pack(pady=10, anchor="e", padx=10)
        self.__frame_inv = ctk.CTkFrame(tab, fg_color="transparent")
        self.__frame_inv.pack(fill="both", expand=True, padx=10)
        self.__cargar_inventario()

    def __cargar_inventario(self):
        for w in self.__frame_inv.winfo_children():
            w.destroy()
        productos = self.__controller.obtener_inventario()
        columnas = ["ID", "Producto", "Zona", "Stock", "Mínimo", "P.Venta"]
        datos = [[str(p['id_producto']), p['nombre'], p['zona_nombre'],
                  str(p['stock_actual']), str(p['stock_minimo']),
                  f"{p['precio_venta']}€"] for p in productos]
        TablaDinamica(self.__frame_inv, columnas=columnas,
                      datos=datos).pack(fill="both", expand=True)

    def __construir_alertas(self):
        tab = self.__tabs.tab("Alertas Stock")
        ctk.CTkButton(tab, text="🔄 Actualizar", font=("Arial", 12),
                      fg_color="#922B21", width=120,
                      command=self.__cargar_alertas
                      ).pack(pady=10, anchor="e", padx=10)
        self.__frame_alertas = ctk.CTkFrame(tab, fg_color="transparent")
        self.__frame_alertas.pack(fill="both", expand=True, padx=10)
        self.__cargar_alertas()

    def __cargar_alertas(self):
        for w in self.__frame_alertas.winfo_children():
            w.destroy()
        alertas = self.__controller.obtener_alertas_stock()
        if not alertas:
            ctk.CTkLabel(self.__frame_alertas,
                         text="✅ No hay alertas de stock",
                         font=("Arial", 14), text_color="#1E8449"
                         ).pack(pady=30)
            return
        columnas = ["ID", "Producto", "Zona", "Stock actual", "Stock mínimo"]
        datos = [[str(a['id_producto']), a['nombre'], a['zona_nombre'],
                  str(a['stock_actual']), str(a['stock_minimo'])] for a in alertas]
        TablaDinamica(self.__frame_alertas, columnas=columnas,
                      datos=datos).pack(fill="both", expand=True)

    def __construir_reponer(self):
        tab = self.__tabs.tab("Reponer")
        frame = ctk.CTkFrame(tab, fg_color="transparent")
        frame.pack(padx=20, pady=20, fill="x")

        ctk.CTkLabel(frame, text="ID Producto", font=("Arial", 12)).pack(anchor="w")
        self.__entry_prod = ctk.CTkEntry(frame, placeholder_text="Ej: 9",
                                         font=("Arial", 12), height=38)
        self.__entry_prod.pack(fill="x", pady=(2, 10))

        ctk.CTkLabel(frame, text="Cantidad a reponer", font=("Arial", 12)).pack(anchor="w")
        self.__entry_cant = ctk.CTkEntry(frame, placeholder_text="Ej: 50",
                                          font=("Arial", 12), height=38)
        self.__entry_cant.pack(fill="x", pady=(2, 10))

        self.__lbl_rep = ctk.CTkLabel(frame, text="", font=("Arial", 11))
        self.__lbl_rep.pack(pady=5)

        ctk.CTkButton(frame, text="📦 Reponer stock",
                      font=("Arial", 13, "bold"), fg_color="#1E8449",
                      height=42, command=self.__reponer
                      ).pack(fill="x", pady=5)

    def __reponer(self):
        try:
            id_prod = int(self.__entry_prod.get())
            cantidad = int(self.__entry_cant.get())
            self.__controller.reponer_stock(id_prod, cantidad)
            self.__lbl_rep.configure(
                text=f"✅ Stock repuesto correctamente", text_color="#1E8449")
            self.__cargar_inventario()
        except Exception as e:
            self.__lbl_rep.configure(text=f"❌ Error: {e}", text_color="#E74C3C")