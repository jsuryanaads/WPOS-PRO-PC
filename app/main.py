import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from .config import APP_VERSION
from .database import init_db
from .ui.login import LoginWindow
from .ui.modern_main_window import ModernMainWindow
from .ui.user_management import UserManagementDialog
from .ui.branding import LOGO_PATH
from .ui.polish import apply_ui_polish
from .ui.ux2026 import apply_ux2026
from .ui.themes import apply_theme, current_theme


def main():
    init_db()
    app = QApplication(sys.argv)
    if LOGO_PATH.exists():
        app.setWindowIcon(QIcon(str(LOGO_PATH)))
    # Keep the existing theme infrastructure for compatibility, but do not
    # expose theme switching in the application menu for V1.1.5.
    apply_theme(app, current_theme())
    holder = {}

    def refresh_ui(window):
        apply_ui_polish(window)
        window._apply_modern_style()
        apply_ux2026(window)

    def success(user):
        def logout_callback(window):
            holder.pop("main", None)
            window.close()
            login_window = LoginWindow(success)
            holder["login"] = login_window
            login_window.show()

        window = ModernMainWindow(user, logout_callback=logout_callback)
        window.setStyleSheet("")
        apply_theme(app, current_theme())
        refresh_ui(window)
        holder["main"] = window

        # V1.1.5: theme switching is intentionally hidden for now.
        # The underlying theme service remains intact to avoid unnecessary
        # changes to the existing styling pipeline.
        if str(user.role).upper() == "ADMIN":
            menu = window.menuBar().addMenu("Administrasi")
            action = menu.addAction("Manajemen User")
            action.triggered.connect(lambda: UserManagementDialog(user, window).exec())

        window.show()

    login = LoginWindow(success)
    holder["login"] = login
    login.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
