from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QLabel, QFrame, QHBoxLayout, QStatusBar, QTableWidget

from .branding import LOGO_PATH


def apply_ui_polish(window):
    """Apply presentation-only refinements without changing POS business logic."""
    window.setStyleSheet(window.styleSheet() + """
        QToolTip { background: #111827; color: white; border: 0; padding: 6px; }
        QStatusBar { background: #111827; color: #e5e7eb; padding: 4px 10px; }
        QStatusBar::item { border: 0; }
        QGroupBox { color: #17202a; }
        QLineEdit:focus, QDoubleSpinBox:focus, QComboBox:focus, QTextEdit:focus { border: 2px solid #64748b; padding: 5px; }
        QTableWidget::item:selected { background: #dbeafe; color: #111827; }
    """)

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
        bar.setStyleSheet("""
            QTabBar { background: #e9edf2; }
            QTabBar::tab { background: #e9edf2; color: #475467; padding: 10px 16px; margin: 0 1px 0 0; border: 0; min-height: 18px; }
            QTabBar::tab:hover { background: #f8fafc; color: #111827; }
            QTabBar::tab:selected { background: #ffffff; color: #111827; border-bottom: 3px solid #1f2937; }
        """)

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
            strip.setStyleSheet("QFrame#brandStrip { background: #111827; border-radius: 10px; }")
            row = QHBoxLayout(strip)
            row.setContentsMargins(14, 9, 14, 9)
            logo = QLabel()
            logo.setObjectName("brandLogo")
            pix = QPixmap(str(LOGO_PATH))
            if not pix.isNull():
                logo.setPixmap(pix.scaledToHeight(42, Qt.SmoothTransformation))
            name = QLabel("WPOS PRO")
            name.setStyleSheet("color: white; font-size: 17px; font-weight: 800;")
            version = QLabel("V1.0  ·  Point of Sale")
            version.setStyleSheet("color: #cbd5e1; font-size: 11px;")
            row.addWidget(logo)
            row.addSpacing(10)
            text = QHBoxLayout()
            text.addWidget(name)
            text.addSpacing(8)
            text.addWidget(version)
            text.addStretch()
            row.addLayout(text)
            layout.insertWidget(0, strip)
