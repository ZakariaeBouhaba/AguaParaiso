# ============================================
# AguaParaíso - Tabla dinámica reutilizable
# Sistema ERP SmartPark Pro
# ============================================

import customtkinter as ctk


class TablaDinamica(ctk.CTkFrame):
    """Tabla dinámica sin CTkTable — compatible con Python 3.14."""

    def __init__(self, parent, columnas, datos=None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.__columnas = columnas
        self.__construir(datos or [])

    def __construir(self, datos):
        # Cabecera
        frame_header = ctk.CTkFrame(self, fg_color="#1A6B9A", corner_radius=8)
        frame_header.pack(fill="x", pady=(0, 2))

        for i, col in enumerate(self.__columnas):
            ctk.CTkLabel(
                frame_header,
                text=col,
                font=("Arial", 11, "bold"),
                text_color="white",
                width=120
            ).grid(row=0, column=i, padx=5, pady=8, sticky="w")

        # Filas
        if not datos:
            frame_vacio = ctk.CTkFrame(self, fg_color="#F7FBFE", corner_radius=6)
            frame_vacio.pack(fill="x", pady=1)
            ctk.CTkLabel(
                frame_vacio,
                text="Sin datos disponibles",
                font=("Arial", 11),
                text_color="#AAAAAA"
            ).pack(pady=10)
            return

        for ri, fila in enumerate(datos):
            color = "#F7FBFE" if ri % 2 == 0 else "white"
            frame_fila = ctk.CTkFrame(self, fg_color=color, corner_radius=6)
            frame_fila.pack(fill="x", pady=1)

            for ci, celda in enumerate(fila):
                ctk.CTkLabel(
                    frame_fila,
                    text=str(celda),
                    font=("Arial", 11),
                    text_color="#2C3E50",
                    width=120,
                    anchor="w"
                ).grid(row=0, column=ci, padx=5, pady=6, sticky="w")

    def actualizar(self, datos):
        for w in self.winfo_children():
            w.destroy()
        self.__construir(datos)