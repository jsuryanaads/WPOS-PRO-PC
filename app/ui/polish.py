from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QLabel, QFrame, QHBoxLayout, QStatusBar, QTableWidget

from .branding import LOGO_PATH


MODERN_BLUE = """
QMainWindow { background: #f5f7fb; }
QStatusBar { background: #0f2747; color: #e8f1fb; padding: 5px 12px; }
QTabWidget::pane { border: 0; background: #f5f7fb; }
QTabBar { background: #ffffff; }
QTabBar::tab { background: #eef3f8; color: #526173; padding: 11px 17px; margin: 0 1px 0 0; border: 0; min-height: 18px; font-weight: 600; }
QTabBar::tab:hover { background: #e1ebf7; color: #163b63; }
QTabBar::tab:selected { background: #ffffff; color: #1769aa; border-bottom: 3px solid #1d78c1; font-weight: 800; }
QLabel#pageTitle { font-size: 25px; font-weight: 800; color: #102a43; }
QLabel#pageSubtitle { color: #66788a; font-size: 13px; }
QFrame#card { background: #ffffff; border: 1px solid #dce5ee; border-radius: 12px; }
QLabel#cardTitle { color: #718096; font-size: 11px; font-weight: 700; }
QLabel#cardValue { color: #102a43; font-size: 23px; font-weight: 800; }
QGroupBox { background: #ffffff; border: 1px solid #dce5ee; border-radius: 12px; margin-top: 12px; padding-top: 14px; font-weight: 700; color: #17324d; }
QGroupBox::title { subcontrol-origin: margin; left: 14px; padding: 0 6px; color: #315a7d; }
QLineEdit, QDoubleSpinBox, QComboBox, QTextEdit { background: #ffffff; color: #1f2937; border: 1px solid #cbd7e3; border-radius: 7px; padding: 7px 9px; min-height: 20px; }
QLineEdit:focus, QDoubleSpinBox:focus, QComboBox:focus, QTextEdit:focus { border: 2px solid #4b9bd3; padding: 6px 8px; }
QPushButton { background: #1f5f96; color: #ffffff; border: 0; border-radius: 7px; padding: 9px 15px; font-weight: 700; }
QPushButton:hover { background: #174d7c; }
QPushButton#primary { background: #1677c8; font-size: 14px; padding: 11px 19px; }
QPushButton#primary:hover { background: #125fa0; }
QPushButton#danger { background: #c83c3c; }
QPushButton#danger:hover { background: #a92e2e; }
QLabel#total { background: #0f4c81; color: #ffffff; border-radius: 9px; padding: 11px 15px; font-size: 19px; font-weight: 800; }
QTableWidget { background: #ffffff; color: #1f2937; border: 1px solid #dce5ee; border-radius: 9px; gridline-color: #edf2f7; alternate-background-color: #f8fbfe; }
QTableWidget::item:selected { background: #d8ebfa; color: #102a43; }
QHeaderView::section { background: #eaf1f7; color: #28465f; padding: 8px; border: 0; font-weight: 800; }
QScrollBar:vertical { background: #edf2f7; width: 10px; margin: 0; }
QScrollBar::handle:vertical { background: #b8c9d9; border-radius: 5px; min-height: 30px; }
QToolTip { background: #0f2747; color: #ffffff; border: 0; padding: 6px; }
"""


def apply_ui_polish(window):
    """Apply the Modern Blue visual system without changing POS business logic."""
    window.setStyleSheet(window.styleSheet() + MODERN_BLUE)

    if window.statusBar() is None:
        window.setStatusBar(QStatusBar(window))
    window.statusBar().showMessage(f"WPOS PRO V1.0  |  {window.user.username}  |  {window.user.role}")

    tabs = getattr(window, "tabs", None)
    if tabs:
        bar = tabs.tabBar()
        bar.setExpanding(False)
        bar.setUsesScrollButtons(True)
        bar.setElideMode(Qt.ElideRight)
        bar.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))

    for table in window.findChildren(QTableWidget):
        table.setShowGrid(False)
        table.setWordWrap(False)
        table.setMinimumHeight(180)
        table.verticalHeader().setDefaultSectionSize(32)
        table.setFont(QFont("Segoe UI", 9))

    if tabs and LOGO_PATH.exists() and tabs.count() > 0:
        dashboard = tabs.widget(0)
        layout = dashboard.layout()
        if layout and not dashboard.findChildren(QLabel, "brandStrip"):
            strip = QFrame()
            strip.setObjectName("brandStrip")
            strip.setStyleSheet("QFrame#brandStrip { background: #1769aa; border-radius: 11px; }")
            row = QHBoxLayout(strip)
            row.setContentsMargins(14, 9, 14, 9)
            logo = QLabel()
            logo.setObjectName("brandLogo")
            pix = QPixmap(str(LOGO_PATH))
            if not pix.isNull():
                logo.setPixmap(pix.scaledToHeight(42, Qt.SmoothTransformation))
            name = QLabel("WPOS PRO")
            name.setStyleSheet("color: white; font-size: 18px; font-weight: 800;")
            version = QLabel("V1.0  ·  Point of Sale")
            version.setStyleSheet("color: #dceeff; font-size: 11px;")
            row.addWidget(logo)
            row.addSpacing(10)
            text = QHBoxLayout()
            text.addWidget(name)
            text.addSpacing(8)
            text.addWidget(version)
            text.addStretch()
            row.addLayout(text)
            layout.insertWidget(0, strip)
