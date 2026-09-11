from PySide6.QtCore import QObject, QEvent, Qt
from PySide6.QtWidgets import QLabel, QTableWidget


DASHBOARD_UX_QSS = """
/* Dashboard refinement — visual hierarchy and empty states */
QFrame#card {
    min-height: 72px;
    padding: 0;
}
QLabel#cardTitle, QLabel#cardValue,
QLabel#modernContext, QLabel#modernHint,
QLabel#pageTitle, QLabel#pageSubtitle {
    background: transparent;
}
QLabel#cardTitle {
    padding: 0;
}
QLabel#cardValue {
    padding: 0;
}
QGroupBox {
    background: #ffffff;
}
QGroupBox::title {
    background: #ffffff;
}
QTableWidget {
    background: #ffffff;
}
QTableWidget#dashboard_sales, QTableWidget#dashboard_low {
    min-height: 260px;
}
"""


class _EmptyTableOverlay(QObject):
    def __init__(self, table):
        super().__init__(table)
        self.table = table
        self.label = QLabel(table)
        self.label.setObjectName("dashboardEmptyState")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Belum ada data\nData akan tampil setelah ada aktivitas.")
        self.label.setStyleSheet(
            "QLabel#dashboardEmptyState {"
            "background: transparent; color: #94a3b8; font-size: 11px;"
            "font-weight: 600; padding: 20px; }"
        )
        self.label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.label.show()
        table.installEventFilter(self)
        model = table.model()
        if model is not None:
            model.rowsInserted.connect(self.refresh)
            model.rowsRemoved.connect(self.refresh)
            model.modelReset.connect(self.refresh)
        self.refresh()

    def refresh(self, *args):
        empty = self.table.rowCount() == 0
        self.label.setVisible(empty)
        if empty:
            margin = 12
            self.label.setGeometry(
                margin,
                self.table.horizontalHeader().height() + margin,
                max(0, self.table.viewport().width() - margin * 2),
                max(42, self.table.viewport().height() - self.table.horizontalHeader().height() - margin * 2),
            )

    def eventFilter(self, obj, event):
        if obj is self.table and event.type() in (QEvent.Resize, QEvent.Show):
            self.refresh()
        return False


def apply_dashboard_ux(window):
    """Refine dashboard presentation without changing business logic."""
    window.setStyleSheet(window.styleSheet() + DASHBOARD_UX_QSS)
    for table in window.findChildren(QTableWidget):
        if table.objectName() in ("dashboard_sales", "dashboard_low"):
            if not table.property("wpos_empty_overlay"):
                overlay = _EmptyTableOverlay(table)
                table.setProperty("wpos_empty_overlay", True)
                table.setProperty("wpos_empty_overlay_obj", overlay)
