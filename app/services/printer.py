from decimal import Decimal
from PySide6.QtGui import QTextDocument
from PySide6.QtPrintSupport import QPrinter, QPrinterInfo, QPrintDialog
from .settings import get_settings


def available_printers():
    return [info.printerName() for info in QPrinterInfo.availablePrinters()]


def receipt_html(sale, items, settings):
    width = "58mm" if settings.get("receipt_paper") == "58mm" else "80mm"
    rows = []
    for item in items:
        name = item["name"]
        qty = item["quantity"]
        price = Decimal(str(item["unit_price"]))
        line = Decimal(str(item["line_total"]))
        rows.append(f"<tr><td colspan='2'>{name}</td></tr><tr><td>{qty} x {price:,.0f}</td><td align='right'>{line:,.0f}</td></tr>")
    address = settings.get("store_address", "")
    phone = settings.get("store_phone", "")
    return f"""
    <html><head><style>
    body {{ width:{width}; font-family:Arial; font-size:9pt; margin:0; }}
    h3 {{ text-align:center; margin:0 0 4px 0; }}
    p {{ margin:2px 0; }} table {{ width:100%; border-collapse:collapse; }}
    .line {{ border-top:1px dashed #000; margin:5px 0; }}
    </style></head><body>
    <h3>{settings.get('store_name','TOKO SEMBAKO')}</h3>
    <p align='center'>{address}</p><p align='center'>{phone}</p>
    <div class='line'></div>
    <p>No: {sale.invoice_no}</p><p>{sale.created_at:%Y-%m-%d %H:%M:%S}</p>
    <div class='line'></div><table>{''.join(rows)}</table><div class='line'></div>
    <table><tr><td>Subtotal</td><td align='right'>{Decimal(str(sale.subtotal)):,.0f}</td></tr>
    <tr><td>Diskon</td><td align='right'>{Decimal(str(sale.discount)):,.0f}</td></tr>
    <tr><td><b>TOTAL</b></td><td align='right'><b>{Decimal(str(sale.total)):,.0f}</b></td></tr>
    <tr><td>Bayar ({sale.payment_method})</td><td align='right'>{Decimal(str(sale.paid)):,.0f}</td></tr>
    <tr><td>Kembalian</td><td align='right'>{Decimal(str(sale.change)):,.0f}</td></tr></table>
    <div class='line'></div><p align='center'>{settings.get('receipt_footer','Terima kasih')}</p>
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
    if printer_name:
        printer.setPrinterName(printer_name)
    dialog = QPrintDialog(printer, parent)
    dialog.setWindowTitle("Tes Printer WPOS PRO")
    if dialog.exec() != QPrintDialog.Accepted:
        return False
    html = (
        "<html><body>"
        "<h3>WPOS PRO</h3>"
        "<p>TES CETAK BERHASIL</p>"
        f"<p>Kertas: {paper}</p>"
        f"<p>Printer: {printer.printerName()}</p>"
        "</body></html>"
    )
    _print_document(printer, html)
    return True
