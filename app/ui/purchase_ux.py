from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QTabWidget,
)


PURCHASE_ACCENT = "#2563EB"
PURCHASE_TEXT = "#0F172A"
PURCHASE_MUTED = "#64748B"
PURCHASE_BORDER = "#E2E8F0"
PURCHASE_SURFACE = "#FFFFFF"
PURCHASE_BG = "#F8FAFC"


def apply_purchase_ux(window):
    """Polish the Pembelian tab without changing business logic or data flow."""
    tabs = window.findChild(QTabWidget)
    if tabs is None:
        return

    purchase_page = None
    for index in range(tabs.count()):
        if tabs.tabText(index).strip().lower() == "pembelian":
            purchase_page = tabs.widget(index)
            break
    if purchase_page is None:
        return

    purchase_page.setObjectName("purchasePage")
    purchase_page.setStyleSheet(
        "QWidget#purchasePage { background: %s; }" % PURCHASE_BG
    )

    card = None
    for group in purchase_page.findChildren(QGroupBox):
        if group.title().strip().lower() == "pembelian barang":
            card = group
            break
    if card is None:
        return

    card.setObjectName("purchaseCard")
    card.setStyleSheet(
        "QGroupBox#purchaseCard {"
        " background: %s; border: 1px solid %s; border-radius: 12px;"
        " margin-top: 12px; padding: 18px 16px 16px 16px; color: %s;"
        " font-weight: 700; }"
        "QGroupBox#purchaseCard::title { subcontrol-origin: margin;"
        " left: 14px; padding: 0 7px; background: %s; color: %s; }"
        % (PURCHASE_SURFACE, PURCHASE_BORDER, PURCHASE_TEXT, PURCHASE_BG, PURCHASE_TEXT)
    )

    form = card.layout()
    if isinstance(form, QFormLayout):
        form.setContentsMargins(12, 14, 12, 10)
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(12)

    fields = card.findChildren((QComboBox, QDoubleSpinBox, QLineEdit))
    for field in fields:
        field.setMinimumHeight(38)
        field.setStyleSheet(
            "background: white; border: 1px solid %s; border-radius: 8px;"
            " padding: 7px 10px; color: %s;"
            " selection-background-color: %s;"
            % (PURCHASE_BORDER, PURCHASE_TEXT, PURCHASE_ACCENT)
        )

    save_button = None
    for button in purchase_page.findChildren(QPushButton):
        if "Simpan Pembelian" in button.text():
            save_button = button
            break
    if save_button:
        save_button.setObjectName("purchasePrimary")
        save_button.setMinimumHeight(44)
        save_button.setMinimumWidth(250)
        save_button.setToolTip("Simpan pembelian dan tambahkan jumlah stok secara otomatis")
        save_button.setStyleSheet(
            "QPushButton#purchasePrimary { background: %s; color: white;"
            " border: 0; border-radius: 9px; padding: 10px 18px; font-weight: 800; }"
            "QPushButton#purchasePrimary:hover { background: #1D4ED8; }"
            "QPushButton#purchasePrimary:pressed { background: #1E40AF; }"
            % PURCHASE_ACCENT
        )

    for label in purchase_page.findChildren(QLabel):
        if label.text().startswith("Catatan:"):
            label.setObjectName("purchaseNote")
            label.setWordWrap(True)
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            label.setStyleSheet(
                "QLabel#purchaseNote { background: #EFF6FF; border: 1px solid #DBEAFE;"
                " border-radius: 8px; padding: 10px 12px; color: %s; font-size: 12px; }"
                % PURCHASE_MUTED
            )
            break
