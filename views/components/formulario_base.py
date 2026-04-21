# ============================================
# AguaParaíso - Formulario base reutilizable
# Sistema ERP SmartPark Pro
# ============================================

import customtkinter as ctk


class FormularioBase(ctk.CTkFrame):
    """Formulario base reutilizable para el sistema."""

    def __init__(self, parent, titulo, **kwargs):
        super().__init__(parent, **kwargs)
        self.__campos = {}
        self.__titulo = titulo
        self.__construir()

    def __construir(self):
        ctk.CTkLabel(
            self,
            text=self.__titulo,
            font=("Arial", 16, "bold"),
            text_color="#1A6B9A"
        ).pack(pady=10)

    def agregar_campo(self, nombre, etiqueta, placeholder=""):
        """Añade un campo de texto al formulario."""
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(
            frame,
            text=etiqueta,
            font=("Arial", 12),
            width=150,
            anchor="w"
        ).pack(side="left")

        entrada = ctk.CTkEntry(
            frame,
            placeholder_text=placeholder,
            width=250,
            font=("Arial", 12)
        )
        entrada.pack(side="left", padx=10)
        self.__campos[nombre] = entrada

    def agregar_selector(self, nombre, etiqueta, opciones):
        """Añade un selector desplegable al formulario."""
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(
            frame,
            text=etiqueta,
            font=("Arial", 12),
            width=150,
            anchor="w"
        ).pack(side="left")

        selector = ctk.CTkComboBox(
            frame,
            values=opciones,
            width=250,
            font=("Arial", 12)
        )
        selector.pack(side="left", padx=10)
        self.__campos[nombre] = selector

    def obtener_valores(self):
        """Devuelve los valores del formulario."""
        return {nombre: campo.get() for nombre, campo in self.__campos.items()}

    def limpiar(self):
        """Limpia todos los campos."""
        for campo in self.__campos.values():
            if isinstance(campo, ctk.CTkEntry):
                campo.delete(0, "end")