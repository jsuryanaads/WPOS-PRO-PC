from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QGroupBox


def _card(parent=None):
    frame = QFrame(parent)
    frame.setObjectName("uxCard")
    return frame


def _style_cash(window):
    page = window.tabs.widget(5)
    if page is None:
        return
    page.setObjectName("cashPage")
    page.setStyleSheet("""
        QWidget#cashPage QGroupBox { margin-top: 12px; padding-top: 18px; font-weight: 700; }
        QWidget#cashPage QLabel#cardValue { font-size: 20px; font-weight: 800; padding: 16px 18px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; }
        QWidget#cashPage QLineEdit, QWidget#cashPage QComboBox, QWidget#cashPage QDoubleSpinBox { min-height: 36px; }
    """)
    if not hasattr(window, "cash_label"):
        return
    window.cash_label.setToolTip("Ringkasan kas masuk, kas keluar, dan saldo saat ini")


def _style_report(window):
    page = window.tabs.widget(6)
    if page is None:
        return
    page.setObjectName("reportPage")
    page.setStyleSheet("""
        QWidget#reportPage QTextEdit { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px; }
        QWidget#reportPage QTableWidget { min-height: 240px; }
    """)
    if hasattr(window, "report_text"):
        window.report_text.setToolTip("Ringkasan performa penjualan dan kas")
    if hasattr(window, "report_table"):
        window.report_table.setToolTip("Daftar transaksi penjualan terbaru")


def apply_cash_report_ux(window):
    if not hasattr(window, "tabs"):
        return
    _style_cash(window)
    _style_report(window)
