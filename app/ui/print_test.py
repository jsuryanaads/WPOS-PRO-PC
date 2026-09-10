from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGroupBox,
    QComboBox,
    QPushButton,
    QLabel,
    QMessageBox,
)

from ..services.printer import available_printers, test_print
from ..services.settings import get_settings, save_settings
from ..database import SessionLocal


def print_test_page():
    w = QWidget()
    layout = QVBoxLayout(w)
    layout.setContentsMargins(18, 16, 18, 18)
    layout.setSpacing(12)

    title = QLabel("Print Test")
    title.setObjectName("pageTitle")
    subtitle = QLabel("Uji printer thermal WPOS PRO sebelum digunakan untuk transaksi.")
    subtitle.setObjectName("pageSubtitle")
    layout.addWidget(title)
    layout.addWidget(subtitle)

    box = QGroupBox("Konfigurasi Cetak")
    form = QFormLayout(box)

    printer_combo = QComboBox()
    printer_combo.addItem("Printer default / pilih saat cetak", "")
    for name in available_printers():
        printer_combo.addItem(name, name)

    paper_combo = QComboBox()
    paper_combo.addItems(["58mm", "80mm"])

    with SessionLocal() as session:
        settings = get_settings(session)

    current_printer = settings.get("printer_name", "")
    printer_index = printer_combo.findData(current_printer)
    if printer_index >= 0:
        printer_combo.setCurrentIndex(printer_index)

    saved_paper = settings.get("receipt_paper", "58mm")
    paper_combo.setCurrentText(saved_paper if saved_paper in ("58mm", "80mm") else "58mm")

    form.addRow("Printer", printer_combo)
    form.addRow("Ukuran Kertas", paper_combo)
    layout.addWidget(box)

    info = QGroupBox("Yang Diuji")
    info_layout = QVBoxLayout(info)
    info_text = QLabel(
        "• Nama toko dan identitas WPOS PRO\n"
        "• Lebar area cetak dan wrapping teks\n"
        "• Format kertas 58mm / 80mm\n"
        "• Printer Windows yang dipilih\n"
        "• Tinggi struk dinamis tanpa halaman kosong panjang"
    )
    info_text.setWordWrap(True)
    info_layout.addWidget(info_text)
    layout.addWidget(info)

    status = QLabel("Siap melakukan tes cetak.")
    status.setObjectName("pageSubtitle")
    layout.addWidget(status)

    actions = QHBoxLayout()
    save = QPushButton("Simpan Pengaturan")
    save.setObjectName("primary")
    test = QPushButton("PRINT TEST")
    test.setObjectName("primary")
    refresh = QPushButton("Refresh Printer")

    def save_settings_now():
        try:
            with SessionLocal() as session:
                save_settings(
                    session,
                    {
                        "printer_name": printer_combo.currentData() or "",
                        "receipt_paper": paper_combo.currentText(),
                    },
                )
            status.setText("Pengaturan printer berhasil disimpan.")
            QMessageBox.information(w, "Print Test", "Pengaturan printer berhasil disimpan.")
        except Exception as exc:
            status.setText(f"Gagal menyimpan: {exc}")
            QMessageBox.warning(w, "Print Test", str(exc))

    def refresh_printers():
        selected = printer_combo.currentData() or ""
        printer_combo.clear()
        printer_combo.addItem("Printer default / pilih saat cetak", "")
        for name in available_printers():
            printer_combo.addItem(name, name)
        index = printer_combo.findData(selected)
        printer_combo.setCurrentIndex(index if index >= 0 else 0)
        status.setText("Daftar printer Windows diperbarui.")

    def run_test():
        printer_name = printer_combo.currentData() or ""
        paper = paper_combo.currentText()
        status.setText("Mengirim halaman tes ke printer...")
        test.setEnabled(False)
        try:
            test_print(w, printer_name, paper)
            status.setText(f"Perintah tes cetak dikirim · {paper}")
        except Exception as exc:
            status.setText(f"Tes cetak gagal: {exc}")
            QMessageBox.warning(w, "Print Test", str(exc))
        finally:
            test.setEnabled(True)

    save.clicked.connect(save_settings_now)
    refresh.clicked.connect(refresh_printers)
    test.clicked.connect(run_test)

    actions.addWidget(save)
    actions.addWidget(test)
    actions.addWidget(refresh)
    actions.addStretch()
    layout.addLayout(actions)
    layout.addStretch()
    return w
