# ============================================
# AguaParaíso - Vista Login
# Sistema ERP SmartPark Pro
# ============================================

import customtkinter as ctk
from PIL import Image
import os
from utils.logger import Logger
from utils.security import Security
from database.connection import Database
from exceptions.exceptions import CredencialesInvalidasError, UsuarioBloqueadoError


class LoginView(ctk.CTk):
    """Ventana de login del sistema."""

    def __init__(self, callback_login):
        super().__init__()
        self.__callback_login = callback_login
        self.__db = Database.obtener_instancia()
        self.__intentos = 0

        self.__configurar_ventana()
        self.__construir_ui()

    def __configurar_ventana(self):
        self.title("AguaParaíso — SmartPark Pro")
        self.geometry("500x650")
        self.resizable(False, False)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color="#F0F8FF")

    def __construir_ui(self):
        # Logo
        try:
            logo_img = Image.open("assets/images/logo.png").resize((80, 80))
            logo_ctk = ctk.CTkImage(logo_img, size=(80, 80))
            ctk.CTkLabel(self, image=logo_ctk, text="").pack(pady=(30, 5))
        except Exception:
            pass

        # Título
        ctk.CTkLabel(
            self,
            text="AguaParaíso",
            font=("Arial", 32, "bold"),
            text_color="#1A6B9A"
        ).pack(pady=(5, 2))

        ctk.CTkLabel(
            self,
            text="SmartPark Pro — Sistema ERP",
            font=("Arial", 14),
            text_color="#555555"
        ).pack(pady=(0, 25))

        # Frame login
        frame = ctk.CTkFrame(self, corner_radius=15, fg_color="white",
                              border_width=1, border_color="#D6EAF8")
        frame.pack(padx=60, fill="x")

        ctk.CTkLabel(
            frame,
            text="Iniciar Sesión",
            font=("Arial", 18, "bold"),
            text_color="#1A6B9A"
        ).pack(pady=(25, 20))

        # Usuario
        ctk.CTkLabel(frame, text="Usuario", font=("Arial", 12),
                     anchor="w").pack(padx=30, fill="x")
        self.__entry_user = ctk.CTkEntry(
            frame, placeholder_text="Introduce tu usuario",
            height=40, font=("Arial", 13), corner_radius=8
        )
        self.__entry_user.pack(padx=30, pady=(5, 15), fill="x")

        # Contraseña
        ctk.CTkLabel(frame, text="Contraseña", font=("Arial", 12),
                     anchor="w").pack(padx=30, fill="x")
        self.__entry_pass = ctk.CTkEntry(
            frame, placeholder_text="Introduce tu contraseña",
            show="*", height=40, font=("Arial", 13), corner_radius=8
        )
        self.__entry_pass.pack(padx=30, pady=(5, 20), fill="x")

        # Mensaje error
        self.__lbl_error = ctk.CTkLabel(
            frame, text="", font=("Arial", 11),
            text_color="#E74C3C"
        )
        self.__lbl_error.pack()

        # Botón login
        ctk.CTkButton(
            frame,
            text="Entrar",
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#1A6B9A",
            hover_color="#2E86C1",
            corner_radius=8,
            command=self.__login
        ).pack(padx=30, pady=(10, 25), fill="x")

        # Bind Enter
        self.bind("<Return>", lambda e: self.__login())

        # Footer
        ctk.CTkLabel(
            self,
            text="Instituto Tecnológico Granada · 2026",
            font=("Arial", 10),
            text_color="#AAAAAA"
        ).pack(pady=(20, 0))

    def __login(self):
        username = self.__entry_user.get().strip()
        password = self.__entry_pass.get().strip()

        if not username or not password:
            self.__mostrar_error("Introduce usuario y contraseña")
            return

        try:
            usuario = self.__db.consultar_uno(
                "SELECT * FROM usuarios WHERE username = ?",
                (username,)
            )

            if not usuario:
                self.__intentos += 1
                self.__mostrar_error(f"Usuario no encontrado ({self.__intentos}/3)")
                return

            if usuario['bloqueado'] == 1:
                if Security.usuario_bloqueado(usuario['fecha_bloqueo']):
                    mins = Security.tiempo_restante_bloqueo(usuario['fecha_bloqueo'])
                    self.__mostrar_error(f"Usuario bloqueado. Espera {mins} min")
                    return
                else:
                    self.__db.ejecutar(
                        "UPDATE usuarios SET bloqueado=0, intentos_fallidos=0 WHERE username=?",
                        (username,)
                    )

            if not Security.verificar_password(password, usuario['password_hash']):
                self.__intentos += 1
                nuevos_intentos = usuario['intentos_fallidos'] + 1
                if nuevos_intentos >= 3:
                    self.__db.ejecutar(
                        "UPDATE usuarios SET intentos_fallidos=?, bloqueado=1, fecha_bloqueo=datetime('now') WHERE username=?",
                        (nuevos_intentos, username)
                    )
                    self.__mostrar_error("Usuario bloqueado 15 minutos")
                else:
                    self.__db.ejecutar(
                        "UPDATE usuarios SET intentos_fallidos=? WHERE username=?",
                        (nuevos_intentos, username)
                    )
                    self.__mostrar_error(f"Contraseña incorrecta ({nuevos_intentos}/3)")
                return

            # Login correcto
            self.__db.ejecutar(
                "UPDATE usuarios SET intentos_fallidos=0, ultimo_acceso=datetime('now') WHERE username=?",
                (username,)
            )
            Logger.info(f"Login correcto: {username}")
            self.destroy()
            self.__callback_login(dict(usuario))

        except Exception as e:
            Logger.error(f"Error en login: {e}")
            self.__mostrar_error("Error del sistema")

    def __mostrar_error(self, mensaje):
        self.__lbl_error.configure(text=mensaje)