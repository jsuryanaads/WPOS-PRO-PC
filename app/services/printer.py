from datetime import datetime
from decimal import Decimal
from html import escape
from math import ceil

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
    return RECEIPT_PROFILES.get(str(paper).lower(), RECEIPT_PROFILES["58mm"])


def available_printers():
    return [info.printerName() for info in QPrinterInfo.availablePrinters()]


def _configure_receipt_page(printer, paper, height_mm):
    """Apply a thermal-friendly physical page size for a continuous roll."""
    profile = _profile(paper)
    width = profile["paper_width_mm"]

    # Use QSizeF directly. The optional match policy is intentionally omitted
    # for compatibility across installed PySide6/Qt 6 versions.
    page_size = QPageSize(
        QSizeF(width, max(1.0, float(height_mm))),
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


def _render_document(html, printable_width_mm):
    """Create a continuously flowing document and measure its required height."""
    document = QTextDocument()
    document.setDocumentMargin(0)
    document.setHtml(html)
    # QTextDocument uses points when laid out for printing; convert mm to points.
    text_width_pt = float(printable_width_mm) * 72.0 / 25.4
    document.setTextWidth(text_width_pt)
    return document


def _document_height_mm(document, minimum_mm=45.0):
    """Return the rendered content height in mm, rounded up for safe feeding."""
    height_pt = max(0.0, float(document.size().height()))
    height_mm = height_pt * 25.4 / 72.0
    return max(float(minimum_mm), ceil(height_mm + 2.0))


def receipt_html(sale, items, settings):
    paper = settings.get("receipt_paper", "58mm")
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


def printer_test_html(settings, paper, printer_name, invoice_no="INV-00001"):
    """Build the fixed sample receipt used by the Print Test page."""
    profile = _profile(paper)
    width = profile["printable_width_mm"]
    store_name = escape(str(settings.get("store_name", "TOKO SEMBAKO")))
    address = escape(str(settings.get("store_address", "Alamat toko"))) or "Alamat toko"
    footer = escape(str(settings.get("receipt_footer", "Terima kasih"))) or "Terima kasih"
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    items = [
        ("Indomie", 2, Decimal("3500")),
        ("Teh", 1, Decimal("5000")),
    ]
    total = sum((qty * price for _, qty, price in items), Decimal("0"))
    paid = Decimal("20000")
    change = paid - total

    item_rows = []
    for name, qty, price in items:
        subtotal = qty * price
        item_rows.append(
            "<tr>"
            f"<td class='name'>{escape(name)}</td>"
            f"<td class='qty'>{qty}</td>"
            f"<td class='price'>x {price:,.0f}</td>"
            f"<td class='amount'>{subtotal:,.0f}</td>"
            "</tr>"
        )

    return f"""
    <html><head><style>
    body {{ width:{width}mm; font-family:'Courier New',monospace; font-size:{profile['font_size_pt']}pt;
           margin:0; padding:0; color:#000; }}
    .center {{ text-align:center; }}
    .line {{ margin:4px 0; border-top:1px dashed #000; height:0; }}
    table {{ width:100%; border-collapse:collapse; table-layout:fixed; }}
    td {{ padding:0; white-space:nowrap; overflow:hidden; }}
    .name {{ width:30%; text-align:left; }}
    .qty {{ width:8%; text-align:right; }}
    .price {{ width:32%; text-align:right; }}
    .amount {{ width:30%; text-align:right; }}
    .label {{ width:60%; text-align:left; }}
    .value {{ width:40%; text-align:right; }}
    p {{ margin:2px 0; }}
    h3 {{ margin:0 0 3px 0; }}
    </style></head><body>
    <div class='center'><h3>{store_name}</h3><p>{address}</p></div>
    <div class='line'></div>
    <p>No: {escape(invoice_no)}</p>
    <p>{now}</p>
    <div class='line'></div>
    <table>{''.join(item_rows)}</table>
    <div class='line'></div>
    <table>
      <tr><td class='label'><b>TOTAL</b></td><td class='value'><b>{total:,.0f}</b></td></tr>
      <tr><td class='label'>Bayar</td><td class='value'>{paid:,.0f}</td></tr>
      <tr><td class='label'>Kembalian</td><td class='value'>{change:,.0f}</td></tr>
    </table>
    <div class='line'></div>
    <p class='center'>{footer}</p>
    </body></html>
    """


def _print_document(printer, document):
    """Print an already-laid-out QTextDocument."""
    document.print_(printer)


def print_receipt(parent, sale, items):
    from ..database import SessionLocal

    with SessionLocal() as session:
        settings = get_settings(session)

    paper = settings.get("receipt_paper", "58mm")
    profile = _profile(paper)
    document = _render_document(receipt_html(sale, items, settings), profile["printable_width_mm"])
    height_mm = _document_height_mm(document)

    printer = QPrinter(QPrinter.HighResolution)
    _configure_receipt_page(printer, paper, height_mm)
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
    _print_document(printer, document)
    return True


def test_print(parent, printer_name="", paper="58mm"):
    """Print the standard WPOS PRO sample receipt for printer verification."""
    from ..database import SessionLocal

    with SessionLocal() as session:
        settings = get_settings(session)

    paper = str(paper).lower() if str(paper).lower() in RECEIPT_PROFILES else "58mm"
    profile = _profile(paper)
    printer = QPrinter(QPrinter.HighResolution)
    if printer_name:
        printer.setPrinterName(printer_name)

    html = printer_test_html(settings, paper, printer_name or printer.printerName())
    document = _render_document(html, profile["printable_width_mm"])
    height_mm = _document_height_mm(document, minimum_mm=45.0)
    _configure_receipt_page(printer, paper, height_mm)

    dialog = QPrintDialog(printer, parent)
    dialog.setWindowTitle("Tes Printer WPOS PRO")
    if dialog.exec() != QPrintDialog.Accepted:
        return False
    _print_document(printer, document)
    return True
