from PySide6.QtWidgets import QDialog,QVBoxLayout,QLineEdit,QPushButton,QLabel,QMessageBox
from ..database import SessionLocal
from ..services.auth import login

class LoginWindow(QDialog):
    def __init__(self, on_success):
        super().__init__(); self.on_success=on_success; self.setWindowTitle("WPOS PRO - Login")
        layout=QVBoxLayout(self); layout.addWidget(QLabel("WPOS PRO"))
        self.username=QLineEdit(); self.username.setPlaceholderText("Username"); layout.addWidget(self.username)
        self.password=QLineEdit(); self.password.setPlaceholderText("Password"); self.password.setEchoMode(QLineEdit.Password); layout.addWidget(self.password)
        b=QPushButton("LOGIN"); b.clicked.connect(self.handle_login); layout.addWidget(b)
    def handle_login(self):
        with SessionLocal() as s: user=login(s,self.username.text().strip(),self.password.text())
        if user: self.on_success(user); self.close()
        else: QMessageBox.warning(self,"Login","Username atau password salah")
