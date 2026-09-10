from datetime import datetime
from decimal import Decimal
from html import escape
from math import ceil

from PySide6.QtCore import QMarginsF, QSizeF
from PySide6.QtGui import QPageLayout, QPageSize, QTextDocument
from PySide6.QtPrintSupport import QPrinter, QPrinterInfo, QPrintDialog

from .settings import get_settings


# WPOS PRO is standardized for 58 mm thermal receipt printers.
RECEIPT_PROFILE = {
    "paper_width_mm": 58.0,
    "printable_width_mm": 48.0,
    "margin_mm": 5.0,
    "font_size_pt": 9,
    "cpl_hint": 32,
}


def available_printers():
    return [info.printerName() for info in QPrinterInfo.availablePrinters()]


def _configure_receipt_page(printer, height_mm):
    profile = RECEIPT_PROFILE
    page_size = QPageSize(QSizeF(profile["paper_width_mm"], max(1.0, float(height_mm))), QPageSize.Millimeter, "WPOS 58mm Receipt")
    layout = QPageLayout(page_size, QPageLayout.Portrait, QMarginsF(profile["margin_mm"], profile["margin_mm"], profile["margin_mm"], profile["margin_mm"]), QPageLayout.Millimeter)
    printer.setPageLayout(layout)
    printer.setResolution(203)
    printer.setFullPage(False)
    printer.setCopyCount(1)


def _render_document(html):
    document = QTextDocument()
    document.setDocumentMargin(0)
    document.setHtml(html)
    document.setTextWidth(RECEIPT_PROFILE["printable_width_mm"] * 72.0 / 25.4)
    return document


def _document_height_mm(document, minimum_mm=45.0):
    height_pt = max(0.0, float(document.size().height()))
    return max(float(minimum_mm), ceil(height_pt * 25.4 / 72.0 + 2.0))


def receipt_html(sale, items, settings):
    rows = []
    for item in items:
        name = escape(str(item["name"]))
        qty = item["quantity"]
        price = Decimal(str(item["unit_price"]))
        line = Decimal(str(item["line_total"]))
        rows.append(f"<tr><td colspan='2'>{name}</td></tr><tr><td>{qty} x {price:,.0f}</td><td align='right'>{line:,.0f}</td></tr>")
    address = escape(str(settings.get("store_address", "")))
    phone = escape(str(settings.get("store_phone", "")))
    store_name = escape(str(settings.get("store_name", "TOKO SEMBAKO")))
    footer = escape(str(settings.get("receipt_footer", "Terima kasih")))
    return f"""
    <html><head><style>
    body {{ width:48mm; font-family:'Courier New',monospace; font-size:9pt; margin:0; padding:0; }}
    h3 {{ text-align:center; margin:0 0 4px 0; }} p {{ margin:2px 0; }}
    table {{ width:100%; border-collapse:collapse; }} td {{ padding:0; }}
    .line {{ border-top:1px dashed #000; margin:5px 0; }}
    </style></head><body>
    <h3>{store_name}</h3><p align='center'>{address}</p><p align='center'>{phone}</p>
    <div class='line'></div><p>No: {escape(str(sale.invoice_no))}</p><p>{sale.created_at:%Y-%m-%d %H:%M:%S}</p>
    <div class='line'></div><table>{''.join(rows)}</table><div class='line'></div>
    <table><tr><td>Subtotal</td><td align='right'>{Decimal(str(sale.subtotal)):,.0f}</td></tr>
    <tr><td>Diskon</td><td align='right'>{Decimal(str(sale.discount)):,.0f}</td></tr>
    <tr><td><b>TOTAL</b></td><td align='right'><b>{Decimal(str(sale.total)):,.0f}</b></td></tr>
    <tr><td>Bayar ({escape(str(sale.payment_method))})</td><td align='right'>{Decimal(str(sale.paid)):,.0f}</td></tr>
    <tr><td>Kembalian</td><td align='right'>{Decimal(str(sale.change)):,.0f}</td></tr></table>
    <div class='line'></div><p align='center'>{footer}</p></body></html>
    """


def printer_test_html(settings, invoice_no="INV-00001"):
    store_name = escape(str(settings.get("store_name", "TOKO SEMBAKO")))
    address = escape(str(settings.get("store_address", "Alamat toko"))) or "Alamat toko"
    footer = escape(str(settings.get("receipt_footer", "Terima kasih"))) or "Terima kasih"
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    items = [("Indomie", 2, Decimal("3500")), ("Teh", 1, Decimal("5000"))]
    total = sum((qty * price for _, qty, price in items), Decimal("0"))
    paid = Decimal("20000")
    change = paid - total
    rows = []
    for name, qty, price in items:
        subtotal = qty * price
        rows.append(f"<tr><td class='name'>{escape(name)}</td><td class='qty'>{qty}</td><td class='price'>x {price:,.0f}</td><td class='amount'>{subtotal:,.0f}</td></tr>")
    return f"""
    <html><head><style>
    body {{ width:48mm; font-family:'Courier New',monospace; font-size:9pt; margin:0; padding:0; color:#000; }}
    .center {{ text-align:center; }} .line {{ margin:4px 0; border-top:1px dashed #000; height:0; }}
    table {{ width:100%; border-collapse:collapse; table-layout:fixed; }} td {{ padding:0; white-space:nowrap; overflow:hidden; }}
    .name {{ width:30%; text-align:left; }} .qty {{ width:8%; text-align:right; }} .price {{ width:32%; text-align:right; }} .amount {{ width:30%; text-align:right; }}
    .label {{ width:60%; text-align:left; }} .value {{ width:40%; text-align:right; }} p {{ margin:2px 0; }} h3 {{ margin:0 0 3px 0; }}
    </style></head><body><div class='center'><h3>{store_name}</h3><p>{address}</p></div>
    <div class='line'></div><p>No: {escape(invoice_no)}</p><p>{now}</p><div class='line'></div><table>{''.join(rows)}</table><div class='line'></div>
    <table><tr><td class='label'><b>TOTAL</b></td><td class='value'><b>{total:,.0f}</b></td></tr><tr><td class='label'>Bayar</td><td class='value'>{paid:,.0f}</td></tr><tr><td class='label'>Kembalian</td><td class='value'>{change:,.0f}</td></tr></table>
    <div class='line'></div><p class='center'>{footer}</p></body></html>
    """


def _print_document(printer, document):
    document.print_(printer)


def print_receipt(parent, sale, items):
    from ..database import SessionLocal
    with SessionLocal() as session:
        settings = get_settings(session)
    document = _render_document(receipt_html(sale, items, settings))
    printer = QPrinter(QPrinter.HighResolution)
    _configure_receipt_page(printer, _document_height_mm(document))
    configured = settings.get("printer_name", "")
    if configured and any(info.printerName() == configured for info in QPrinterInfo.availablePrinters()):
        printer.setPrinterName(configured)
    dialog = QPrintDialog(printer, parent)
    dialog.setWindowTitle("Cetak Struk WPOS PRO · 58mm")
    if dialog.exec() != QPrintDialog.Accepted:
        return False
    _print_document(printer, document)
    return True


def test_print(parent, printer_name="", paper="58mm"):
    from ..database import SessionLocal
    with SessionLocal() as session:
        settings = get_settings(session)
    printer = QPrinter(QPrinter.HighResolution)
    if printer_name:
        printer.setPrinterName(printer_name)
    document = _render_document(printer_test_html(settings))
    _configure_receipt_page(printer, _document_height_mm(document))
    dialog = QPrintDialog(printer, parent)
    dialog.setWindowTitle("Tes Printer WPOS PRO · 58mm")
    if dialog.exec() != QPrintDialog.Accepted:
        return False
    _print_document(printer, document)
    return True
