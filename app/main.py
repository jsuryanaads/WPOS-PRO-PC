import sys
from PySide6.QtWidgets import QApplication
from .database import init_db
from .ui.login import LoginWindow
from .ui.main_window import MainWindow

def main():
    init_db()
    app = QApplication(sys.argv)
    holder = {}
    def success(user):
        holder["main"] = MainWindow(user)
        holder["main"].show()
    login = LoginWindow(success)
    login.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
