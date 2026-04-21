# ============================================
# AguaParaíso - Punto de entrada
# Sistema ERP SmartPark Pro
# ============================================

import customtkinter as ctk
from views.login_view import LoginView
from views.dashboard_view import DashboardView
from utils.logger import Logger


def main():
    """Punto de entrada del sistema."""
    Logger.info("Sistema AguaParaíso iniciado")
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    def on_login(usuario):
        dashboard = DashboardView(usuario)
        dashboard.mainloop()

    login = LoginView(on_login)
    login.mainloop()


if __name__ == "__main__":
    main()