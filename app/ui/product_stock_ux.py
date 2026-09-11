from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFormLayout,
    QGroupBox,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTabWidget,
    QLineEdit,
    QComboBox,
    QDoubleSpinBox,
    QSpinBox,
    QTextEdit,
)


def _style_field(widget):
    widget.setMinimumHeight(38)
    if isinstance(widget, QLineEdit):
        widget.setClearButtonEnabled(True)
    elif isinstance(widget, (QComboBox, QDoubleSpinBox, QSpinBox)):
        widget.setMinimumWidth(150)


def _style_table(table):
    table.setMinimumHeight(280)
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setSelectionMode(QAbstractItemView.SingleSelection)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.setFocusPolicy(Qt.StrongFocus)
    table.verticalHeader().setVisible(False)
    header = table.horizontalHeader()
    header.setHighlightSections(False)
    header.setStretchLastSection(True)
    header.setSectionResizeMode(QHeaderView.Stretch)


def _style_page(page, section_title):
    page.setObjectName(section_title.lower().replace(" ", "_") + "Page")
    layout = page.layout()
    if layout:
        layout.setContentsMargins(20, 18, 20, 20)
        layout.setSpacing(12)

    for group in page.findChildren(QGroupBox):
        group.setObjectName("uxCard")
        group.setStyleSheet(
            "QGroupBox#uxCard { margin-top: 12px; padding-top: 18px; }"
            "QGroupBox#uxCard::title { left: 14px; padding: 0 6px; }"
        )
        group_layout = group.layout()
        if isinstance(group_layout, QFormLayout):
            group_layout.setHorizontalSpacing(18)
            group_layout.setVerticalSpacing(10)
        elif group_layout:
            group_layout.setSpacing(10)

    for widget in page.findChildren((QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox, QTextEdit)):
        _style_field(widget)

    for table in page.findChildren(QTableWidget):
        _style_table(table)

    buttons = page.findChildren(QPushButton)
    for button in buttons:
        button.setMinimumHeight(40)
        button.setCursor(Qt.PointingHandCursor)
        if not button.objectName():
            button.setObjectName("secondaryAction")

    if buttons:
        # Keep action labels visually grouped without touching their signals.
        for button in buttons:
            button.setProperty("uxPage", section_title)


def apply_product_stock_ux(window):
    """Apply presentation-only polish to Produk and Stok & Mutasi."""
    tabs = window.findChild(QTabWidget)
    if not tabs:
        return

    for index in range(tabs.count()):
        title = tabs.tabText(index).strip()
        if title not in {"Produk", "Stok & Mutasi"}:
            continue
        page = tabs.widget(index)
        if page:
            _style_page(page, title)

    # Make the two operational tabs easier to scan without changing behavior.
    tabs.setTabBarAutoHide(False)
