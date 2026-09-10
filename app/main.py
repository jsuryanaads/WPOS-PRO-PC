import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from .database import init_db
from .ui.login import LoginWindow
from .ui.main_window import MainWindow
from .ui.branding import LOGO_PATH


def main():
    init_db()
    app = QApplication(sys.argv)
    if LOGO_PATH.exists():
        app.setWindowIcon(QIcon(str(LOGO_PATH)))
    holder = {}

    def success(user):
        holder["main"] = MainWindow(user)
        holder["main"].show()

    login = LoginWindow(success)
    login.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
