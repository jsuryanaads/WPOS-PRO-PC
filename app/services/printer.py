from decimal import Decimal
from html import escape

from PySide6.QtCore import QMarginsF, QSizeF
from PySide6.QtGui import QPageLayout, QPageSize, QTextDocument
from PySide6.QtPrintSupport import QPrinter, QPrinterInfo, QPrintDialog

from .settings import get_settings


# Thermal receipt profiles used by WPOS PRO.
# 58 mm printers commonly expose about 48 mm / 384 dots of printable area;
# the exact dot width is driver-dependent, so WPOS uses physical page width
# plus safe margins instead of hard-coding a dot count for every printer.
RECEIPT_PROFILES = {
    "58mm": {
        "paper_width_mm": 58.0,
        "printable_width_mm": 48.0,
        "margin_mm": 5.0,
        "font_size_pt": 9,
        "cpl_hint": 32,
    },
    "80mm": {
        "paper_width_mm": 80.0,
        "printable_width_mm": 70.0,
        "margin_mm": 5.0,
        "font_size_pt": 9,
        "cpl_hint": 42,
    },
}


def _profile(paper):
    return RECEIPT_PROFILES.get(str(paper).lower(), RECEIPT_PROFILES["80mm"])


def available_printers():
    return [info.printerName() for info in QPrinterInfo.availablePrinters()]


def _configure_receipt_page(printer, paper, height_mm=200.0):
    """Apply a thermal-friendly physical page size and safe print margins."""
    profile = _profile(paper)
    width = profile["paper_width_mm"]

    # Use QSizeF directly. The optional match policy is intentionally omitted
    # for compatibility across installed PySide6/Qt 6 versions.
    page_size = QPageSize(
        QSizeF(width, height_mm),
        QPageSize.Millimeter,
        f"WPOS {paper} Receipt",
    )
    layout = QPageLayout(
        page_size,
        QPageLayout.Portrait,
        QMarginsF(
            profile["margin_mm"],
            profile["margin_mm"],
            profile["margin_mm"],
            profile["margin_mm"],
        ),
        QPageLayout.Millimeter,
    )
    printer.setPageLayout(layout)
    printer.setResolution(203)
    printer.setFullPage(False)
    printer.setCopyCount(1)


def receipt_html(sale, items, settings):
    paper = settings.get("receipt_paper", "80mm")
    profile = _profile(paper)
    width = profile["printable_width_mm"]
    rows = []
    for item in items:
        name = escape(str(item["name"]))
        qty = item["quantity"]
        price = Decimal(str(item["unit_price"]))
        line = Decimal(str(item["line_total"]))
        rows.append(
            f"<tr><td colspan='2'>{name}</td></tr>"
            f"<tr><td>{qty} x {price:,.0f}</td><td align='right'>{line:,.0f}</td></tr>"
        )
    address = escape(str(settings.get("store_address", "")))
    phone = escape(str(settings.get("store_phone", "")))
    store_name = escape(str(settings.get("store_name", "TOKO SEMBAKO")))
    footer = escape(str(settings.get("receipt_footer", "Terima kasih")))
    return f"""
    <html><head><style>
    body {{ width:{width}mm; font-family:'Courier New',monospace; font-size:{profile['font_size_pt']}pt;
           margin:0; padding:0; }}
    h3 {{ text-align:center; margin:0 0 4px 0; }}
    p {{ margin:2px 0; }} table {{ width:100%; border-collapse:collapse; }}
    td {{ padding:0; }}
    .line {{ border-top:1px dashed #000; margin:5px 0; }}
    </style></head><body>
    <h3>{store_name}</h3>
    <p align='center'>{address}</p><p align='center'>{phone}</p>
    <div class='line'></div>
    <p>No: {escape(str(sale.invoice_no))}</p><p>{sale.created_at:%Y-%m-%d %H:%M:%S}</p>
    <div class='line'></div><table>{''.join(rows)}</table><div class='line'></div>
    <table><tr><td>Subtotal</td><td align='right'>{Decimal(str(sale.subtotal)):,.0f}</td></tr>
    <tr><td>Diskon</td><td align='right'>{Decimal(str(sale.discount)):,.0f}</td></tr>
    <tr><td><b>TOTAL</b></td><td align='right'><b>{Decimal(str(sale.total)):,.0f}</b></td></tr>
    <tr><td>Bayar ({escape(str(sale.payment_method))})</td><td align='right'>{Decimal(str(sale.paid)):,.0f}</td></tr>
    <tr><td>Kembalian</td><td align='right'>{Decimal(str(sale.change)):,.0f}</td></tr></table>
    <div class='line'></div><p align='center'>{footer}</p>
    </body></html>
    """


def _print_document(printer, html):
    """Render and print a QTextDocument using the Qt 6 Python binding."""
    document = QTextDocument()
    document.setHtml(html)
    # QTextDocument.print is exposed as print_ in PySide6 because print is a Python keyword.
    document.print_(printer)


def print_receipt(parent, sale, items):
    from ..database import SessionLocal

    with SessionLocal() as session:
        settings = get_settings(session)

    printer = QPrinter(QPrinter.HighResolution)
    _configure_receipt_page(printer, settings.get("receipt_paper", "80mm"))
    configured = settings.get("printer_name", "")
    if configured:
        for info in QPrinterInfo.availablePrinters():
            if info.printerName() == configured:
                printer.setPrinterName(configured)
                break
    dialog = QPrintDialog(printer, parent)
    dialog.setWindowTitle("Cetak Struk WPOS PRO")
    if dialog.exec() != QPrintDialog.Accepted:
        return False
    _print_document(printer, receipt_html(sale, items, settings))
    return True


def test_print(parent, printer_name="", paper="80mm"):
    printer = QPrinter(QPrinter.HighResolution)
    # A printer test should produce a short physical slip, not a full 200 mm page.
    _configure_receipt_page(printer, paper, height_mm=60.0)
    if printer_name:
        printer.setPrinterName(printer_name)
    dialog = QPrintDialog(printer, parent)
    dialog.setWindowTitle("Tes Printer WPOS PRO")
    if dialog.exec() != QPrintDialog.Accepted:
        return False
    profile = _profile(paper)
    html = (
        "<html><head><style>"
        f"body{{width:{profile['printable_width_mm']}mm;"
        f"font-family:'Courier New',monospace;font-size:{profile['font_size_pt']}pt;"
        "margin:0;padding:0;text-align:center;}}"
        "</style></head><body>"
        "<h3>WPOS PRO</h3>"
        "<p>TES CETAK BERHASIL</p>"
        f"<p>Kertas: {escape(str(paper))}</p>"
        f"<p>Area cetak: {profile['printable_width_mm']:.0f} mm</p>"
        f"<p>Target: ~{profile['cpl_hint']} CPL</p>"
        f"<p>Printer: {escape(str(printer.printerName()))}</p>"
        "</body></html>"
    )
    _print_document(printer, html)
    return True
