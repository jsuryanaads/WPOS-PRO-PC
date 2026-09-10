from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QLabel, QFrame, QHBoxLayout, QStatusBar, QTableWidget

from .branding import LOGO_PATH


FOOTER_TEXT = f"WPOS PRO V1.0 · © {datetime.now().year} Jsuryana · Created by Jsuryana"


def apply_ui_polish(window):
    """Apply theme-neutral presentation refinements without overriding the selected theme."""
    if window.statusBar() is None:
        window.setStatusBar(QStatusBar(window))
    # Keep the bottom status/footer identity synchronized with the Dashboard footer.
    window.statusBar().showMessage(FOOTER_TEXT)

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

    # Theme switching can call this function repeatedly. Reuse the existing strip
    # instead of inserting another copy on every theme change.
    if tabs and LOGO_PATH.exists() and tabs.count() > 0:
        dashboard = tabs.widget(0)
        layout = dashboard.layout()
        existing = dashboard.findChildren(QFrame, "brandStrip")
        if existing:
            return
        if layout:
            strip = QFrame()
            strip.setObjectName("brandStrip")
            row = QHBoxLayout(strip)
            row.setContentsMargins(14, 9, 14, 9)
            logo = QLabel()
            logo.setObjectName("brandLogo")
            pix = QPixmap(str(LOGO_PATH))
            if not pix.isNull():
                logo.setPixmap(pix.scaledToHeight(42, Qt.SmoothTransformation))
            name = QLabel("WPOS PRO")
            name.setObjectName("brandName")
            version = QLabel("V1.0  ·  Point of Sale")
            version.setObjectName("brandVersion")
            row.addWidget(logo)
            row.addSpacing(10)
            text = QHBoxLayout()
            text.setContentsMargins(0, 0, 0, 0)
            text.addWidget(name)
            text.addSpacing(8)
            text.addWidget(version)
            text.addStretch()
            row.addLayout(text)
            layout.insertWidget(0, strip)
