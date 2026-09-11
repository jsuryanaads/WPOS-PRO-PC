from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QAbstractItemView, QCheckBox, QComboBox, QFormLayout,
    QFrame, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QMessageBox,
    QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
)

from ..database import SessionLocal
from ..services.users import ROLES, list_users, create_user, set_user_active, reset_password


class UserManagementPage(QWidget):
    """Unified administration page rendered inside the main WPOS window."""

    def __init__(self, actor, parent=None):
        super().__init__(parent)
        self.actor = actor
        self.selected_user_id = None
        self.setObjectName("userManagementPage")

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 16, 18, 18)
        root.setSpacing(14)

        title = QLabel("Manajemen User")
        title.setObjectName("pageTitle")
        root.addWidget(title)
        subtitle = QLabel("Kelola akun, role, status akses, dan reset password pengguna WPOS PRO.")
        subtitle.setObjectName("pageSubtitle")
        root.addWidget(subtitle)

        form_card = QFrame()
        form_card.setObjectName("card")
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(16, 16, 16, 16)
        form_layout.setSpacing(10)

        section = QLabel("Data Akun")
        section.setObjectName("premiumSectionTitle")
        form_layout.addWidget(section)

        form = QFormLayout()
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(10)

        self.username = QLineEdit()
        self.username.setObjectName("userUsername")
        self.username.setPlaceholderText("Masukkan username")
        self.username.setClearButtonEnabled(True)

        self.password = QLineEdit()
        self.password.setObjectName("userPassword")
        self.password.setPlaceholderText("Password / password baru")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setClearButtonEnabled(True)

        self.role = QComboBox()
        self.role.setObjectName("userRole")
        self.role.addItems(ROLES)

        self.active = QCheckBox("Akun aktif")
        self.active.setObjectName("userActive")
        self.active.setChecked(True)

        form.addRow("Username", self.username)
        form.addRow("Password", self.password)
        form.addRow("Role", self.role)
        form.addRow("Status", self.active)
        form_layout.addLayout(form)
        root.addWidget(form_card)

        actions = QHBoxLayout()
        actions.setSpacing(8)
        self.add_button = QPushButton("Tambah User")
        self.add_button.setObjectName("primary")
        self.add_button.setToolTip("Buat akun pengguna baru")
        self.add_button.clicked.connect(self.add_user)

        self.reset_button = QPushButton("Reset Password")
        self.reset_button.setToolTip("Reset password user yang dipilih")
        self.reset_button.clicked.connect(self.do_reset_password)

        self.toggle_button = QPushButton("Aktif / Nonaktif")
        self.toggle_button.setToolTip("Ubah status akses user yang dipilih")
        self.toggle_button.clicked.connect(self.toggle_active)

        self.clear_button = QPushButton("Bersihkan")
        self.clear_button.setObjectName("danger")
        self.clear_button.setToolTip("Kosongkan form dan batalkan pilihan")
        self.clear_button.clicked.connect(self.clear_form)

        for button in (self.add_button, self.reset_button, self.toggle_button, self.clear_button):
            button.setMinimumHeight(38)
            actions.addWidget(button)
        actions.addStretch(1)
        root.addLayout(actions)

        table_card = QFrame()
        table_card.setObjectName("card")
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(12, 12, 12, 12)
        table_layout.setSpacing(8)

        table_header = QHBoxLayout()
        table_title = QLabel("Daftar Pengguna")
        table_title.setObjectName("premiumSectionTitle")
        self.count_label = QLabel("0 user")
        self.count_label.setObjectName("premiumMuted")
        table_header.addWidget(table_title)
        table_header.addStretch(1)
        table_header.addWidget(self.count_label)
        table_layout.addLayout(table_header)

        self.table = QTableWidget(0, 4)
        self.table.setObjectName("userManagementTable")
        self.table.setHorizontalHeaderLabels(["ID", "Username", "Role", "Status"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(34)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.cellClicked.connect(self.select_user)
        self.table.itemSelectionChanged.connect(self._sync_selected_state)
        table_layout.addWidget(self.table)
        root.addWidget(table_card, 1)

        hint = QLabel("Klik baris user untuk memilih akun. Password tidak pernah ditampilkan kembali.")
        hint.setObjectName("premiumMuted")
        root.addWidget(hint)

        self.refresh()

    def refresh(self):
        with SessionLocal() as s:
            rows = list_users(s)
            data = [(u.id, u.username, u.role, "AKTIF" if u.active else "NONAKTIF") for u in rows]

        self.table.setRowCount(len(data))
        for r, row in enumerate(data):
            for c, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignVCenter | (Qt.AlignCenter if c in (0, 3) else Qt.AlignLeft))
                self.table.setItem(r, c, item)
            status_item = self.table.item(r, 3)
            status_item.setForeground(QColor("#15803D" if row[3] == "AKTIF" else "#BE123C"))

        self.count_label.setText(f"{len(data)} user")
        self._sync_selected_state()

    def select_user(self, row, _column):
        item = self.table.item(row, 0)
        if item is None:
            return
        self.selected_user_id = int(item.text())
        self.username.setText(self.table.item(row, 1).text())
        self.role.setCurrentText(self.table.item(row, 2).text())
        self.active.setChecked(self.table.item(row, 3).text() == "AKTIF")
        self.password.clear()
        self._sync_selected_state()

    def _sync_selected_state(self):
        selected = bool(self.selected_user_id)
        self.reset_button.setEnabled(selected)
        self.toggle_button.setEnabled(selected)
        self.reset_button.setToolTip("Reset password user yang dipilih" if selected else "Pilih user terlebih dahulu")
        self.toggle_button.setToolTip("Ubah status akses user yang dipilih" if selected else "Pilih user terlebih dahulu")

    def add_user(self):
        username = self.username.text().strip()
        password = self.password.text()
        if not username or not password:
            QMessageBox.warning(self, "Data belum lengkap", "Username dan password wajib diisi.")
            return
        try:
            with SessionLocal() as s:
                create_user(s, username, password, self.role.currentText())
            self.clear_form()
            self.refresh()
            QMessageBox.information(self, "User", "User berhasil ditambahkan.")
        except Exception as exc:
            QMessageBox.warning(self, "User", str(exc))

    def do_reset_password(self):
        if not self.selected_user_id:
            QMessageBox.warning(self, "User", "Pilih user terlebih dahulu.")
            return
        if not self.password.text():
            QMessageBox.warning(self, "Password", "Masukkan password baru terlebih dahulu.")
            self.password.setFocus()
            return
        try:
            with SessionLocal() as s:
                reset_password(s, self.selected_user_id, self.password.text())
            self.password.clear()
            QMessageBox.information(self, "User", "Password berhasil direset.")
        except Exception as exc:
            QMessageBox.warning(self, "User", str(exc))

    def toggle_active(self):
        if not self.selected_user_id:
            QMessageBox.warning(self, "User", "Pilih user terlebih dahulu.")
            return
        try:
            with SessionLocal() as s:
                set_user_active(s, self.selected_user_id, self.active.isChecked(), self.actor.id)
            self.refresh()
            QMessageBox.information(self, "User", "Status akun berhasil diperbarui.")
        except Exception as exc:
            QMessageBox.warning(self, "User", str(exc))

    def clear_form(self):
        self.selected_user_id = None
        self.username.clear()
        self.password.clear()
        self.role.setCurrentText("TEKNISI" if "TEKNISI" in ROLES else ROLES[0])
        self.active.setChecked(True)
        self.table.clearSelection()
        self._sync_selected_state()
        self.username.setFocus()


# Backward-compatible name for any external imports; it is now a normal page.
UserManagementDialog = UserManagementPage
