from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..config import APP_VERSION
from .branding import LOGO_PATH
from .main_window import MainWindow


class ModernMainWindow(MainWindow):
    """Modern POS 2026 shell around the existing WPOS PRO business pages."""

    NAVIGATION = [
        ("OPERASIONAL", [("▣", "Dashboard", 0), ("＋", "Kasir", 1), ("□", "Produk", 2), ("▤", "Stok & Mutasi", 3), ("↥", "Pembelian", 4)]),
        ("KEUANGAN", [("Rp", "Kas", 5), ("◫", "Laporan", 6)]),
        ("DATA MASTER", [("◎", "Pelanggan", 13), ("◉", "Supplier", 12), ("◇", "Kategori", 10), ("◇", "Satuan", 11)]),
        ("SISTEM", [("⚙", "Pengaturan Toko", 7), ("▣", "Printer", 8), ("↻", "Backup / Restore", 9)]),
    ]

    def __init__(self, user, logout_callback=None):
        super().__init__(user, logout_callback=logout_callback)
        self._build_modern_shell()

    def _build_modern_shell(self):
        old_tabs = self.tabs
        pages = [old_tabs.widget(i) for i in range(old_tabs.count())]
        titles = [old_tabs.tabText(i) for i in range(old_tabs.count())]
        old_tabs.currentChanged.connect(self._legacy_navigation)
        old_tabs.setParent(None)
        for toolbar in self.findChildren(QWidget):
            if toolbar.__class__.__name__ == "QToolBar":
                toolbar.hide()

        shell = QWidget()
        root = QHBoxLayout(shell)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("modernSidebar")
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(14, 16, 14, 14)
        side.setSpacing(6)

        brand = QFrame()
        brand.setObjectName("modernBrand")
        brand_l = QHBoxLayout(brand)
        brand_l.setContentsMargins(10, 10, 10, 10)
        logo = QLabel()
        logo.setObjectName("modernBrandLogo")
        if LOGO_PATH.exists():
            pix = QPixmap(str(LOGO_PATH))
            if not pix.isNull():
                logo.setPixmap(pix.scaled(44, 44, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        brand_l.addWidget(logo)
        brand_text = QVBoxLayout()
        brand_text.setContentsMargins(0, 0, 0, 0)
        brand_text.setSpacing(1)
        name = QLabel("WPOS PRO")
        name.setObjectName("modernBrandName")
        version = QLabel(f"{APP_VERSION} · POS 2026")
        version.setObjectName("modernBrandVersion")
        brand_text.addWidget(name)
        brand_text.addWidget(version)
        brand_l.addLayout(brand_text, 1)
        side.addWidget(brand)
        side.addSpacing(8)

        self.nav_list = QListWidget()
        self.nav_list.setObjectName("modernNav")
        self.nav_list.setSpacing(2)
        self.nav_list.setFrameShape(QFrame.NoFrame)
        self.nav_list.setFocusPolicy(Qt.NoFocus)
        self._nav_indexes = []
        for section, entries in self.NAVIGATION:
            header = QListWidgetItem(section)
            header.setFlags(Qt.NoItemFlags)
            header.setData(Qt.UserRole, -1)
            self.nav_list.addItem(header)
            for icon, title, index in entries:
                item = QListWidgetItem(f"  {icon}   {title}")
                item.setData(Qt.UserRole, index)
                item.setToolTip(title)
                self.nav_list.addItem(item)
                self._nav_indexes.append(index)
        self.nav_list.currentItemChanged.connect(self._navigate)
        side.addWidget(self.nav_list, 1)

        account = QFrame()
        account.setObjectName("modernAccount")
        al = QVBoxLayout(account)
        al.setContentsMargins(10, 9, 10, 9)
        al.setSpacing(3)
        user_label = QLabel(f"{self.user.username}")
        user_label.setObjectName("modernUser")
        role_label = QLabel(f"{self.user.role} · Lokal")
        role_label.setObjectName("modernRole")
        al.addWidget(user_label)
        al.addWidget(role_label)
        logout = QPushButton("Keluar")
        logout.setObjectName("modernLogout")
        logout.clicked.connect(self.logout)
        al.addWidget(logout)
        side.addWidget(account)

        content = QFrame()
        content.setObjectName("modernContent")
        content_l = QVBoxLayout(content)
        content_l.setContentsMargins(22, 18, 22, 12)
        content_l.setSpacing(10)

        topbar = QFrame()
        topbar.setObjectName("modernTopbar")
        top_l = QHBoxLayout(topbar)
        top_l.setContentsMargins(16, 9, 16, 9)
        top_l.setSpacing(10)
        self.modern_context = QLabel("Dashboard")
        self.modern_context.setObjectName("modernContext")
        self.modern_hint = QLabel("Ringkasan bisnis hari ini")
        self.modern_hint.setObjectName("modernHint")
        top_l.addWidget(self.modern_context)
        top_l.addWidget(self.modern_hint)
        top_l.addStretch()
        clock = QLabel("● OFFLINE  ·  DATABASE LOKAL")
        clock.setObjectName("modernStatus")
        top_l.addWidget(clock)
        content_l.addWidget(topbar)

        self.modern_stack = QStackedWidget()
        self.modern_stack.setObjectName("modernStack")
        for page in pages:
            self.modern_stack.addWidget(page)
        content_l.addWidget(self.modern_stack, 1)

        root.addWidget(sidebar, 0)
        root.addWidget(content, 1)
        self.setCentralWidget(shell)
        self.tabs = self._compat_tabs(old_tabs, titles)
        self._select_navigation(0)
        self._apply_modern_style()

    def _compat_tabs(self, old_tabs, titles):
        class CompatTabs:
            def __init__(self, owner, titles):
                self.owner = owner
                self.titles = titles
            def setCurrentIndex(self, index):
                self.owner._select_navigation(index)
            def tabText(self, index):
                return self.titles[index]
        return CompatTabs(self, titles)

    def _legacy_navigation(self, index):
        if index >= 0 and hasattr(self, "modern_stack"):
            self._select_navigation(index)

    def _select_navigation(self, page_index):
        self.modern_stack.setCurrentIndex(page_index)
        title = self.modern_stack.widget(page_index).property("modern_title") or self._title_for(page_index)
        self.modern_context.setText(title)
        self.modern_hint.setText(self._hint_for(page_index))
        for row in range(self.nav_list.count()):
            item = self.nav_list.item(row)
            if item.data(Qt.UserRole) == page_index:
                self.nav_list.blockSignals(True)
                self.nav_list.setCurrentItem(item)
                self.nav_list.blockSignals(False)
                break
        self.on_tab_changed(page_index)

    def _navigate(self, current, _previous):
        if current is None:
            return
        index = current.data(Qt.UserRole)
        if isinstance(index, int) and index >= 0:
            self.modern_stack.setCurrentIndex(index)
            self.modern_context.setText(self._title_for(index))
            self.modern_hint.setText(self._hint_for(index))
            self.on_tab_changed(index)

    @staticmethod
    def _title_for(index):
        return [
            "Dashboard", "Kasir", "Produk", "Stok & Mutasi", "Pembelian", "Kas", "Laporan",
            "Pengaturan Toko", "Printer", "Backup / Restore", "Kategori", "Satuan", "Supplier", "Pelanggan",
        ][index]

    @staticmethod
    def _hint_for(index):
        return [
            "Ringkasan bisnis hari ini", "Transaksi cepat · barcode first", "Master produk & harga",
            "Kontrol persediaan", "Restock & supplier", "Arus kas toko", "Analitik & riwayat",
            "Identitas dan preferensi", "Thermal printer · 58mm", "Keamanan database lokal",
            "Kelompok produk", "Satuan barang", "Data pemasok", "Riwayat pelanggan",
        ][index]

    def _apply_modern_style(self):
        self.setStyleSheet(self.styleSheet() + """
        QFrame#modernSidebar { background: #111827; border: 0; min-width: 230px; max-width: 250px; }
        QFrame#modernBrand { background: #1f2937; border: 1px solid #374151; border-radius: 12px; }
        QLabel#modernBrandLogo { min-width: 44px; max-width: 44px; min-height: 44px; max-height: 44px; }
        QLabel#modernBrandName { color: #ffffff; font-size: 18px; font-weight: 900; }
        QLabel#modernBrandVersion { color: #9ca3af; font-size: 9px; font-weight: 700; }
        QListWidget#modernNav { background: transparent; color: #9ca3af; border: 0; }
        QListWidget#modernNav::item { padding: 9px 8px; border-radius: 8px; margin: 1px 0; font-size: 12px; }
        QListWidget#modernNav::item:hover { background: #1f2937; color: #ffffff; }
        QListWidget#modernNav::item:selected { background: #2563eb; color: #ffffff; font-weight: 800; }
        QListWidget#modernNav::item:disabled { color: #6b7280; padding: 11px 8px 4px; font-size: 9px; font-weight: 900; }
        QFrame#modernAccount { background: #1f2937; border: 1px solid #374151; border-radius: 10px; }
        QLabel#modernUser { color: #ffffff; font-weight: 800; }
        QLabel#modernRole { color: #9ca3af; font-size: 10px; }
        QPushButton#modernLogout { background: #374151; color: #f3f4f6; border-radius: 7px; padding: 7px; margin-top: 5px; }
        QPushButton#modernLogout:hover { background: #4b5563; }
        QFrame#modernContent { background: #f5f7fb; }
        QFrame#modernTopbar { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; }
        QLabel#modernContext { color: #111827; font-size: 15px; font-weight: 900; }
        QLabel#modernHint { color: #6b7280; font-size: 11px; }
        QLabel#modernStatus { color: #15803d; font-size: 9px; font-weight: 800; }
        QStackedWidget#modernStack { background: transparent; border: 0; }
        QGroupBox { border-radius: 12px; border: 1px solid #e2e8f0; background: #ffffff; }
        QLineEdit, QDoubleSpinBox, QComboBox, QTextEdit, QSpinBox { min-height: 32px; border-radius: 8px; border: 1px solid #cbd5e1; }
        QPushButton { border-radius: 8px; padding: 8px 14px; }
        QTableWidget { border-radius: 10px; border: 1px solid #e2e8f0; }
        QHeaderView::section { padding: 9px; border: 0; font-weight: 800; }
        """)
        self.setWindowTitle(f"WPOS PRO {APP_VERSION}")
        self.setMinimumSize(1180, 720)
