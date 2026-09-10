from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QAbstractItemView, QLineEdit, QTableWidget, QWidget


def apply_ux2026(window):
    """Small, safe UX layer for the POS 2026 shell.

    Keeps business widgets intact while improving keyboard navigation,
    tables, focus visibility, and the visual rhythm of existing pages.
    """
    window.setAttribute(Qt.WA_StyledBackground, True)

    # Consistent table behavior for mouse + barcode/POS workflows.
    for table in window.findChildren(QTableWidget):
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        table.setSortingEnabled(True)
        table.setFocusPolicy(Qt.StrongFocus)
        table.setToolTip("Klik untuk memilih · Enter untuk membuka/edit · ↑ ↓ untuk berpindah")

    # Make text-entry controls feel like POS controls and expose shortcuts.
    edits = window.findChildren(QLineEdit)
    for edit in edits:
        edit.setClearButtonEnabled(True)
        edit.setFocusPolicy(Qt.StrongFocus)

    # Ctrl+K is a universal quick-focus gesture: first visible text field.
    shortcut = QShortcut(QKeySequence("Ctrl+K"), window)
    shortcut.setContext(Qt.WindowShortcut)

    def focus_search():
        for edit in window.findChildren(QLineEdit):
            if edit.isVisible() and edit.isEnabled():
                edit.setFocus(Qt.ShortcutFocusReason)
                edit.selectAll()
                break

    shortcut.activated.connect(focus_search)

    # Keyboard page navigation. Existing CompatTabs keeps this backward-compatible.
    for key, index in enumerate(range(10), start=1):
        if index >= 10:
            break
        nav = QShortcut(QKeySequence(f"Alt+{key}"), window)
        nav.setContext(Qt.WindowShortcut)
        nav.activated.connect(lambda i=index: window.tabs.setCurrentIndex(i))

    window.setStyleSheet(window.styleSheet() + """
        QWidget { outline: none; }
        QToolTip {
            padding: 6px 8px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            background: #ffffff;
            color: #0f172a;
        }
        QTableWidget::item:selected {
            font-weight: 700;
        }
        QPushButton:focus, QLineEdit:focus, QComboBox:focus,
        QDoubleSpinBox:focus, QSpinBox:focus, QTextEdit:focus {
            outline: 2px solid rgba(37, 99, 235, 0.20);
        }
        QStatusBar {
            min-height: 26px;
            padding-left: 8px;
            padding-right: 8px;
        }
    """)
