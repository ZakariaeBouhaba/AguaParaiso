# ============================================
# AguaParaíso - Vista Perfil
# Sistema ERP SmartPark Pro
# ============================================

import customtkinter as ctk
from database.connection import Database
from utils.security import Security
from utils.logger import Logger


class PerfilView(ctk.CTkFrame):
    """Vista de perfil de usuario."""

    def __init__(self, parent, usuario):
        super().__init__(parent, fg_color="transparent")
        self.__usuario = usuario
        self.__db = Database.obtener_instancia()
        self.__construir_ui()
        self.pack(fill="both", expand=True)

    def __construir_ui(self):
        ctk.CTkLabel(
            self, text="👤 Mi Perfil",
            font=("Arial", 22, "bold"), text_color="#1A6B9A"
        ).pack(pady=(20, 10), padx=20, anchor="w")

        frame = ctk.CTkFrame(self, fg_color="white", corner_radius=12,
                              border_width=1, border_color="#D6EAF8",
                              width=400)
        frame.pack(padx=20, pady=10, anchor="w")

        info = [
            ("Usuario", self.__usuario['username']),
            ("Rol", self.__usuario['rol']),
            ("Último acceso", self.__usuario.get('ultimo_acceso') or "—"),
        ]

        for label, valor in info:
            f = ctk.CTkFrame(frame, fg_color="transparent")
            f.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(f, text=f"{label}:", font=("Arial", 12, "bold"),
                         width=130, anchor="w").pack(side="left")
            ctk.CTkLabel(f, text=valor, font=("Arial", 12),
                         anchor="w").pack(side="left")

        ctk.CTkLabel(frame, text="Cambiar contraseña",
                     font=("Arial", 14, "bold"), text_color="#1A6B9A"
                     ).pack(pady=(20, 5), padx=20, anchor="w")

        ctk.CTkLabel(frame, text="Nueva contraseña",
                     font=("Arial", 12), anchor="w").pack(padx=20, fill="x")
        self.__entry_pass = ctk.CTkEntry(
            frame, show="*", font=("Arial", 12), height=38)
        self.__entry_pass.pack(padx=20, pady=(5, 10), fill="x")

        ctk.CTkLabel(frame, text="Confirmar contraseña",
                     font=("Arial", 12), anchor="w").pack(padx=20, fill="x")
        self.__entry_confirm = ctk.CTkEntry(
            frame, show="*", font=("Arial", 12), height=38)
        self.__entry_confirm.pack(padx=20, pady=(5, 10), fill="x")

        self.__lbl_msg = ctk.CTkLabel(frame, text="", font=("Arial", 11))
        self.__lbl_msg.pack()

        ctk.CTkButton(
            frame, text="🔒 Cambiar contraseña",
            font=("Arial", 13, "bold"), fg_color="#1A6B9A",
            height=42, command=self.__cambiar_password
        ).pack(padx=20, pady=(5, 20), fill="x")

    def __cambiar_password(self):
        try:
            nueva = self.__entry_pass.get()
            confirmar = self.__entry_confirm.get()

            if not nueva or len(nueva) < 6:
                self.__lbl_msg.configure(
                    text="❌ La contraseña debe tener al menos 6 caracteres",
                    text_color="#E74C3C")
                return

            if nueva != confirmar:
                self.__lbl_msg.configure(
                    text="❌ Las contraseñas no coinciden",
                    text_color="#E74C3C")
                return

            nuevo_hash = Security.hashear_password(nueva)
            self.__db.ejecutar(
                "UPDATE usuarios SET password_hash = ? WHERE id_usuario = ?",
                (nuevo_hash, self.__usuario['id_usuario'])
            )
            Logger.info(f"Contraseña cambiada: {self.__usuario['username']}")
            self.__lbl_msg.configure(
                text="✅ Contraseña cambiada correctamente",
                text_color="#1E8449")
            self.__entry_pass.delete(0, "end")
            self.__entry_confirm.delete(0, "end")

        except Exception as e:
            self.__lbl_msg.configure(text=f"❌ Error: {e}", text_color="#E74C3C")