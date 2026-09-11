import sys
from PySide6.QtWidgets import QApplication, QListWidgetItem
from PySide6.QtGui import QIcon
from .config import APP_VERSION
from .database import init_db
from .ui.login import LoginWindow
from .ui.modern_main_window import ModernMainWindow
from .ui.user_management import UserManagementPage
from .ui.branding import LOGO_PATH
from .ui.polish import apply_ui_polish
from .ui.ux2026 import apply_ux2026
from .ui.unified_ui import apply_unified_ui
from .ui.dashboard_ux import apply_dashboard_ux
from .ui.purchase_ux import apply_purchase_ux
from .ui.product_stock_ux import apply_product_stock_ux
from .ui.cash_report_ux import apply_cash_report_ux
from .ui.system_ux import apply_system_ux
from .ui.themes import apply_theme, current_theme


def main():
    init_db()
    app = QApplication(sys.argv)
    if LOGO_PATH.exists():
        app.setWindowIcon(QIcon(str(LOGO_PATH)))
    apply_theme(app, current_theme())
    holder = {}

    def refresh_ui(window):
        apply_ui_polish(window)
        window._apply_modern_style()
        apply_ux2026(window)
        apply_unified_ui(window)
        apply_dashboard_ux(window)
        apply_purchase_ux(window)
        apply_product_stock_ux(window)
        apply_cash_report_ux(window)
        apply_system_ux(window)

    def success(user):
        def logout_callback(window):
            holder.pop("main", None)
            window.close()
            login_window = LoginWindow(success)
            apply_unified_ui(login_window)
            holder["login"] = login_window
            login_window.show()

        window = ModernMainWindow(user, logout_callback=logout_callback)
        window.setStyleSheet("")
        apply_theme(app, current_theme())
        refresh_ui(window)
        holder["main"] = window

        # Administration is a normal page in the same QStackedWidget.
        # No secondary dialog/window is opened for user management.
        if str(user.role).upper() == "ADMIN":
            admin_page = UserManagementPage(user, window)
            admin_index = window.modern_stack.addWidget(admin_page)
            window.tabs.titles.append("Manajemen User")
            admin_item = QListWidgetItem("  ⚙   Manajemen User")
            admin_item.setData(256, admin_index)  # Qt.UserRole without importing Qt here.
            admin_item.setToolTip("Kelola akun dan akses pengguna")
            window.nav_list.addItem(admin_item)

        window.show()

    login = LoginWindow(success)
    apply_unified_ui(login)
    holder["login"] = login
    login.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
