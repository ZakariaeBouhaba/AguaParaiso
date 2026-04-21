# ============================================
# AguaParaíso - Tabla dinámica reutilizable
# Sistema ERP SmartPark Pro
# ============================================

import customtkinter as ctk
import tkinter as tk


class TablaDinamica(ctk.CTkFrame):
    """
    Tabla dinámica con scroll vertical y horizontal.
    Permite ver el contenido completo de todas las columnas.
    """

    def __init__(self, parent, columnas, datos=None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.__columnas = columnas
        self.__datos = datos or []
        self.__construir(self.__datos)

    def __construir(self, datos):
        # Canvas con scrollbars
        canvas = tk.Canvas(self, bg="#F0F8FF", highlightthickness=0)
        scroll_y = ctk.CTkScrollbar(self, orientation="vertical",
                                     command=canvas.yview,
                                     button_color="#1A6B9A",
                                     button_hover_color="#2E86C1")
        scroll_x = ctk.CTkScrollbar(self, orientation="horizontal",
                                     command=canvas.xview,
                                     button_color="#1A6B9A",
                                     button_hover_color="#2E86C1")

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        # Frame interior
        frame_interior = ctk.CTkFrame(canvas, fg_color="transparent")
        canvas_window = canvas.create_window((0, 0), window=frame_interior, anchor="nw")

        COL_W = 180

        # Cabecera
        frame_header = ctk.CTkFrame(frame_interior, fg_color="#1A6B9A", corner_radius=8)
        frame_header.pack(fill="x", pady=(0, 2))

        for i, col in enumerate(self.__columnas):
            ctk.CTkLabel(
                frame_header,
                text=col,
                font=("Arial", 11, "bold"),
                text_color="white",
                width=COL_W,
                anchor="w"
            ).grid(row=0, column=i, padx=8, pady=8, sticky="w")

        # Filas
        if not datos:
            frame_vacio = ctk.CTkFrame(frame_interior, fg_color="#F7FBFE", corner_radius=6)
            frame_vacio.pack(fill="x", pady=1)
            ctk.CTkLabel(
                frame_vacio,
                text="Sin datos disponibles",
                font=("Arial", 11),
                text_color="#AAAAAA"
            ).pack(pady=10)
        else:
            for ri, fila in enumerate(datos):
                color = "#F7FBFE" if ri % 2 == 0 else "white"
                frame_fila = ctk.CTkFrame(
                    frame_interior, fg_color=color,
                    corner_radius=6, cursor="hand2"
                )
                frame_fila.pack(fill="x", pady=1)

                for ci, celda in enumerate(fila):
                    lbl = ctk.CTkLabel(
                        frame_fila,
                        text=str(celda),
                        font=("Arial", 11),
                        text_color="#2C3E50",
                        width=COL_W,
                        anchor="w",
                        wraplength=COL_W - 10
                    )
                    lbl.grid(row=0, column=ci, padx=8, pady=6, sticky="w")

                # Hover
                frame_fila.bind("<Enter>", lambda e, fr=frame_fila: fr.configure(fg_color="#D6EAF8"))
                frame_fila.bind("<Leave>", lambda e, fr=frame_fila, c=color: fr.configure(fg_color=c))
                for widget in frame_fila.winfo_children():
                    widget.bind("<Enter>", lambda e, fr=frame_fila: fr.configure(fg_color="#D6EAF8"))
                    widget.bind("<Leave>", lambda e, fr=frame_fila, c=color: fr.configure(fg_color=c))

        # Actualizar scroll region
        def actualizar_scroll(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width()
                              if canvas.winfo_width() > frame_interior.winfo_reqwidth()
                              else frame_interior.winfo_reqwidth())

        frame_interior.bind("<Configure>", actualizar_scroll)
        canvas.bind("<Configure>", actualizar_scroll)

        # Scroll con rueda del ratón
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    def actualizar(self, datos):
        """Actualiza los datos de la tabla."""
        self.__datos = datos
        for w in self.winfo_children():
            w.destroy()
        self.__construir(datos)