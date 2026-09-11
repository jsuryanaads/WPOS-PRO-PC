from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QBrush
from PySide6.QtWidgets import QApplication, QAbstractItemView, QTableWidget, QLabel, QDialog, QMessageBox, QPushButton


# Single source of truth for the WPOS PRO visual color system.
WPOS_COLORS = {
    "primary": "#2563EB",
    "primary_dark": "#1D4ED8",
    "success": "#16A34A",
    "success_soft": "#F0FDF4",
    "warning": "#D97706",
    "warning_soft": "#FFF7ED",
    "danger": "#DC2626",
    "danger_soft": "#FFF1F2",
    "info": "#0891B2",
    "info_soft": "#ECFEFF",
    "background": "#F8FAFC",
    "surface": "#FFFFFF",
    "border": "#E2E8F0",
    "text": "#0F172A",
    "muted": "#64748B",
    "sidebar": "#0B1220",
}

WPOS_UNIFIED_QSS = """
/* WPOS PRO 2026 — unified visual language */
QMainWindow, QDialog { background: #f8fafc; color: #0f172a; }
QWidget { font-family: "Segoe UI"; font-size: 11px; color: #0f172a; }
QMenuBar { background: #ffffff; color: #334155; border-bottom: 1px solid #e2e8f0; padding: 2px 6px; }
QMenuBar::item { padding: 6px 10px; border-radius: 6px; }
QMenuBar::item:selected { background: #eff6ff; color: #1d4ed8; }
QMenu { background: #ffffff; color: #0f172a; border: 1px solid #dbe3ec; padding: 5px; }
QMenu::item { padding: 7px 22px 7px 10px; border-radius: 5px; }
QMenu::item:selected { background: #eff6ff; color: #1d4ed8; }
QStatusBar { background: #ffffff; color: #64748b; border-top: 1px solid #e2e8f0; min-height: 25px; }
QStatusBar::item { border: 0; }
QGroupBox { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; margin-top: 12px; padding: 18px 12px 12px; font-weight: 800; }
QGroupBox::title { subcontrol-origin: margin; left: 13px; top: 1px; padding: 0 7px; background: #ffffff; color: #334155; }
QFrame#card, QFrame#premiumScanCard, QFrame#premiumCartCard, QFrame#premiumPayCard { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }
QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox, QTextEdit { background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; border-radius: 8px; padding: 5px 9px; min-height: 34px; selection-background-color: #bfdbfe; }
QLineEdit:hover, QComboBox:hover, QDoubleSpinBox:hover, QSpinBox:hover, QTextEdit:hover { border-color: #94a3b8; }
QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus, QSpinBox:focus, QTextEdit:focus { border: 2px solid #2563eb; padding: 4px 8px; }
QLineEdit:disabled, QComboBox:disabled, QDoubleSpinBox:disabled, QSpinBox:disabled { background: #f1f5f9; color: #94a3b8; }
QAbstractItemView { background: #ffffff; color: #0f172a; border: 1px solid #dbe3ec; selection-background-color: #dbeafe; selection-color: #0f172a; outline: none; }
QComboBox::drop-down { border: 0; width: 26px; }
QPushButton { background: #ffffff; color: #334155; border: 1px solid #cbd5e1; border-radius: 8px; padding: 7px 14px; min-height: 34px; font-weight: 700; }
QPushButton:hover { background: #eff6ff; border-color: #93c5fd; color: #1d4ed8; }
QPushButton:pressed { background: #dbeafe; }
QPushButton:disabled { background: #f1f5f9; color: #94a3b8; border-color: #e2e8f0; }
QPushButton#primary, QPushButton#dashboardPrimary, QPushButton[variant="primary"] { background: #2563eb; color: #ffffff; border: 0; font-weight: 800; }
QPushButton#primary:hover, QPushButton#dashboardPrimary:hover, QPushButton[variant="primary"]:hover { background: #1d4ed8; color: #ffffff; }
QPushButton[variant="success"] { background: #16a34a; color: #ffffff; border: 0; font-weight: 800; }
QPushButton[variant="success"]:hover { background: #15803d; color: #ffffff; }
QPushButton[variant="info"] { background: #0891b2; color: #ffffff; border: 0; font-weight: 800; }
QPushButton[variant="info"]:hover { background: #0e7490; color: #ffffff; }
QPushButton#dashboardSecondary { background: #0f766e; color: #ffffff; border: 0; font-weight: 800; }
QPushButton#dashboardSecondary:hover { background: #0d9488; color: #ffffff; }
QPushButton#danger, QPushButton#premiumClear, QPushButton[variant="danger"] { background: #fff1f2; color: #be123c; border: 1px solid #fecdd3; }
QPushButton#danger:hover, QPushButton#premiumClear:hover, QPushButton[variant="danger"]:hover { background: #ffe4e6; border-color: #fda4af; color: #9f1239; }
QTableWidget { background: #ffffff; alternate-background-color: #f8fafc; color: #0f172a; border: 1px solid #e2e8f0; border-radius: 10px; gridline-color: #eef2f7; selection-background-color: #dbeafe; selection-color: #0f172a; }
QTableWidget::item { padding: 7px 8px; border-bottom: 1px solid #f1f5f9; }
QTableWidget::item:hover { background: #f8fafc; }
QHeaderView::section { background: #f8fafc; color: #475569; border: 0; border-bottom: 1px solid #e2e8f0; padding: 9px 8px; min-height: 30px; font-weight: 800; }
QScrollBar:vertical { width: 9px; background: transparent; margin: 2px; }
QScrollBar::handle:vertical { background: #cbd5e1; border-radius: 4px; min-height: 32px; }
QScrollBar::handle:vertical:hover { background: #94a3b8; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { height: 9px; background: transparent; margin: 2px; }
QScrollBar::handle:horizontal { background: #cbd5e1; border-radius: 4px; min-width: 32px; }
QTabWidget::pane { border: 0; background: #f8fafc; }
QTabBar::tab { background: #f1f5f9; color: #64748b; border: 0; border-radius: 7px; padding: 8px 13px; margin-right: 3px; }
QTabBar::tab:hover { background: #e2e8f0; color: #334155; }
QTabBar::tab:selected { background: #2563eb; color: #ffffff; font-weight: 800; }
QToolTip { background: #0f172a; color: #ffffff; border: 0; padding: 6px 8px; border-radius: 5px; }
QLabel#pageTitle { color: #0f172a; font-size: 23px; font-weight: 900; }
QLabel#pageSubtitle { color: #64748b; font-size: 11px; }
QLabel#cardTitle { color: #64748b; font-size: 10px; font-weight: 800; }
QLabel#cardValue { color: #0f172a; font-size: 23px; font-weight: 900; }
QLabel#total, QLabel#premiumTotal { color: #1d4ed8; font-size: 23px; font-weight: 900; }
QLabel#premiumPageTitle { color: #0f172a; font-size: 22px; font-weight: 900; }
QLabel#premiumPageSubtitle, QLabel#premiumMuted { color: #64748b; font-size: 10px; }
QLabel#premiumFieldCaption, QLabel#premiumPayLabel { color: #475569; font-size: 10px; font-weight: 800; }
QLabel#premiumSectionTitle { color: #0f172a; font-size: 13px; font-weight: 900; }
QLabel#premiumShortcut { color: #64748b; font-size: 10px; }
QFrame#premiumTotalBox { background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 10px; }
QLabel#premiumTotalCaption, QLabel#premiumChangeCaption { color: #64748b; font-size: 9px; font-weight: 900; }
QFrame#premiumChangeBox { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 9px; }
QLabel#premiumChange { color: #0f766e; font-size: 18px; font-weight: 900; }
QPushButton#premiumAdd, QPushButton#premiumCheckout { background: #2563eb; color: #ffffff; border: 0; font-weight: 900; }
QPushButton#premiumAdd:hover, QPushButton#premiumCheckout:hover { background: #1d4ed8; color: #ffffff; }
QLineEdit#premiumBarcode { min-height: 42px; font-size: 14px; font-weight: 700; }
QDoubleSpinBox#premiumQty { min-height: 42px; min-width: 85px; }
QDoubleSpinBox#premiumMoneyInput { min-height: 38px; font-size: 12px; font-weight: 700; }
QDialog#loginWindow { background: #0b1220; }
QFrame#loginCard { background: #ffffff; border: 1px solid #dbe3ec; border-radius: 18px; }
QLabel#loginTitle { color: #0f172a; font-size: 24px; font-weight: 900; }
QLabel#loginVersion { color: #2563eb; font-size: 10px; font-weight: 800; }
QLabel#loginWelcome { color: #64748b; font-size: 11px; }
QLabel#loginFieldLabel { color: #334155; font-size: 10px; font-weight: 900; }
QLineEdit#loginInput { min-height: 44px; border-radius: 9px; font-size: 12px; }
QPushButton#loginPrimaryButton { min-height: 46px; background: #2563eb; color: #ffffff; border: 0; border-radius: 9px; font-size: 12px; font-weight: 900; }
QPushButton#loginPrimaryButton:hover { background: #1d4ed8; }
QPushButton#loginSecondaryButton { min-height: 44px; background: #f1f5f9; color: #334155; border: 1px solid #cbd5e1; }
QLabel#loginFooter { color: #94a3b8; font-size: 9px; }
QFrame#modernSidebar { background: #0b1220; }
QFrame#modernBrand, QFrame#modernAccount { background: #151f32; border: 1px solid #263550; border-radius: 12px; }
QListWidget#modernNav::item { padding: 9px 8px; border-radius: 8px; color: #94a3b8; }
QListWidget#modernNav::item:hover { background: #151f32; color: #ffffff; }
QListWidget#modernNav::item:selected { background: #2563eb; color: #ffffff; font-weight: 800; }
QFrame#modernTopbar { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }
QLabel#modernContext { color: #0f172a; font-size: 17px; font-weight: 900; }
QLabel#modernHint { color: #64748b; font-size: 10px; }
QLabel#modernStatusOffline { background: #fff1f2; color: #be123c; border: 1px solid #fecdd3; border-radius: 999px; padding: 5px 9px; font-size: 9px; font-weight: 900; }
QLabel#modernStatusLocal { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; border-radius: 999px; padding: 5px 9px; font-size: 9px; font-weight: 900; }

/* UX 9/10 completion layer */
QMessageBox { background: #ffffff; }
QMessageBox QLabel { color: #0f172a; font-size: 11px; }
QMessageBox QPushButton { min-width: 82px; }
QDialog QLabel { color: #0f172a; }
QToolBar { background: #ffffff; border: 0; spacing: 6px; padding: 4px 8px; }
QCheckBox, QRadioButton { spacing: 7px; color: #334155; min-height: 28px; }
QCheckBox:disabled, QRadioButton:disabled { color: #94a3b8; }
QToolButton { background: transparent; border: 0; border-radius: 7px; padding: 6px 9px; }
QToolButton:hover { background: #eff6ff; color: #1d4ed8; }
QListWidget, QTreeWidget { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 4px; outline: none; }
QListWidget::item, QTreeWidget::item { padding: 7px 8px; border-radius: 6px; }
QListWidget::item:hover, QTreeWidget::item:hover { background: #f8fafc; }
QListWidget::item:selected, QTreeWidget::item:selected { background: #dbeafe; color: #1e3a8a; }
QProgressBar { background: #f1f5f9; border: 0; border-radius: 6px; text-align: center; min-height: 12px; color: #334155; }
QProgressBar::chunk { background: #2563eb; border-radius: 6px; }

/* Semantic status colors shared by every data table. */
QTableWidget::item[status="success"] { color: #15803d; font-weight: 800; }
QTableWidget::item[status="warning"] { color: #b45309; font-weight: 800; }
QTableWidget::item[status="danger"] { color: #be123c; font-weight: 800; }
"""


def _button_variant(button):
    """Return a consistent semantic variant without changing page business logic."""
    name = button.objectName().lower()
    text = button.text().strip().lower()
    if name in {"danger", "premiumclear"} or any(word in text for word in ("hapus", "nonaktif", "restore", "batalkan")):
        return "danger"
    if name in {"primary", "dashboardprimary", "premiumadd", "premiumcheckout", "loginprimarybutton"}:
        return "primary"
    if any(word in text for word in ("simpan", "tambah", "buat", "checkout", "bayar", "cetak", "test print", "backup")):
        return "primary"
    if any(word in text for word in ("aktif", "aktifkan", "terapkan")):
        return "success"
    if any(word in text for word in ("info", "detail")):
        return "info"
    return "secondary"


def _apply_status_colors(table):
    """Color common status cells consistently across all pages."""
    success = {"aman", "aktif", "lunas", "berhasil", "tersedia", "normal"}
    warning = {"menipis", "peringatan", "pending", "sebagian"}
    danger = {"habis", "nonaktif", "gagal", "kurang", "error"}
    for row in range(table.rowCount()):
        for col in range(table.columnCount()):
            item = table.item(row, col)
            if item is None:
                continue
            value = item.text().strip().lower()
            if value in success:
                item.setForeground(QBrush(QColor(WPOS_COLORS["success"])))
                item.setData(Qt.UserRole + 10, "success")
            elif value in warning:
                item.setForeground(QBrush(QColor(WPOS_COLORS["warning"])))
                item.setData(Qt.UserRole + 10, "warning")
            elif value in danger:
                item.setForeground(QBrush(QColor(WPOS_COLORS["danger"])))
                item.setData(Qt.UserRole + 10, "danger")


def apply_unified_ui(window):
    """Apply the final WPOS visual system without changing business logic."""
    app = QApplication.instance()
    if app:
        app.setFont(QFont("Segoe UI", 10))

    existing = window.styleSheet()
    window.setStyleSheet(existing + WPOS_UNIFIED_QSS)
    window.setAttribute(Qt.WA_StyledBackground, True)

    # Tables: predictable density, selection and scanning behavior.
    for table in window.findChildren(QTableWidget):
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setShowGrid(False)
        table.setWordWrap(False)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(32)
        table.setFocusPolicy(Qt.StrongFocus)
        _apply_status_colors(table)

    # Central semantic button coloring: every page gets the same action hierarchy.
    for button in window.findChildren(QPushButton):
        button.setFocusPolicy(Qt.StrongFocus)
        variant = _button_variant(button)
        if button.property("variant") != variant:
            button.setProperty("variant", variant)
            button.style().unpolish(button)
            button.style().polish(button)

    # Modern shell already supplies the page title. Hide duplicated legacy
    # page headers so every page has one clear title/hint hierarchy.
    for title in window.findChildren(QLabel, "pageTitle"):
        parent = title.parentWidget()
        if parent is not None:
            parent.hide()
    for subtitle in window.findChildren(QLabel, "pageSubtitle"):
        subtitle.hide()

    # Give dialogs the same visual language while retaining their existing
    # dimensions and behavior.
    if isinstance(window, QDialog):
        window.setAttribute(Qt.WA_StyledBackground, True)
