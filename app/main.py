import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon
from .database import init_db
from .ui.login import LoginWindow
from .ui.main_window import MainWindow
from .ui.user_management import UserManagementDialog
from .ui.branding import LOGO_PATH


def main():
    init_db()
    app = QApplication(sys.argv)
    if LOGO_PATH.exists():
        app.setWindowIcon(QIcon(str(LOGO_PATH)))
    holder = {}

    def success(user):
        window = MainWindow(user)
        holder["main"] = window

        # User administration is intentionally available only to ADMIN.
        # It is kept as a separate dialog so the existing POS tab layout is not disturbed.
        if str(user.role).upper() == "ADMIN":
            menu = window.menuBar().addMenu("Administrasi")
            action = menu.addAction("Manajemen User")
            action.triggered.connect(lambda: UserManagementDialog(user, window).exec())

        window.show()

    login = LoginWindow(success)
    login.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
