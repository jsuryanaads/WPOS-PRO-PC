from datetime import datetime
from decimal import Decimal
from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QDoubleSpinBox, QComboBox, QTableWidget,
    QTableWidgetItem, QFormLayout, QMessageBox, QTextEdit
)
from ..database import SessionLocal
from ..models import Product, Sale, Supplier, StockMovement, CashMovement
from ..services.sales import create_sale
from ..services.products import create_product, update_product, deactivate_product
from ..services.stock import adjust_stock
from ..services.purchases import create_purchase
from ..services.cash import record_cash_movement
from ..services.reports import sales_summary, low_stock_count, cash_summary, stock_summary, recent_sales
from .master_data import category_page, unit_page, supplier_page, customer_page


def money(value):
    return f"Rp {Decimal(str(value)):,.0f}".replace(",", ".")


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.cart = []
        self.setWindowTitle("WPOS PRO V1.0")
        tabs = QTabWidget()
        tabs.addTab(self.dashboard(), "Dashboard")
        tabs.addTab(self.cashier(), "Kasir")
        tabs.addTab(self.products(), "Produk")
        tabs.addTab(self.stock_page(), "Stok & Mutasi")
        tabs.addTab(self.purchase_page(), "Pembelian")
        tabs.addTab(self.cash_page(), "Kas")
        tabs.addTab(self.report_page(), "Laporan")
        tabs.addTab(category_page(), "Kategori")
        tabs.addTab(unit_page(), "Satuan")
        tabs.addTab(supplier_page(), "Supplier")
        tabs.addTab(customer_page(), "Pelanggan")
        self.setCentralWidget(tabs)
        self.resize(1200, 760)

    def dashboard(self):
        w = QWidget(); layout = QVBoxLayout(w)
        layout.addWidget(QLabel(f"<h1>WPOS PRO</h1>Login: {self.user.username} ({self.user.role})"))
        with SessionLocal() as s:
            summary = sales_summary(s); low = low_stock_count(s); products = s.query(Product).count(); cash = cash_summary(s)
        for text in [
            f"Transaksi: {summary['transactions']}",
            f"Produk: {products}",
            f"Stok menipis/habis: {low}",
            f"Omzet: {money(summary['omzet'])}",
            f"Saldo kas: {money(cash['balance'])}",
        ]: layout.addWidget(QLabel(text))
        return w

    def cashier(self):
        w = QWidget(); layout = QVBoxLayout(w); top = QHBoxLayout()
        self.barcode = QLineEdit(); self.barcode.setPlaceholderText("Scan / ketik barcode + Enter"); self.barcode.returnPressed.connect(self.add_barcode); top.addWidget(self.barcode)
        self.qty = QDoubleSpinBox(); self.qty.setRange(0.001, 999999); self.qty.setDecimals(3); self.qty.setValue(1); top.addWidget(self.qty)
        add = QPushButton("Tambah"); add.clicked.connect(self.add_barcode); top.addWidget(add); layout.addLayout(top)
        self.cart_table = QTableWidget(0, 5); self.cart_table.setHorizontalHeaderLabels(["Barcode", "Produk", "Qty", "Harga", "Subtotal"]); layout.addWidget(self.cart_table)
        pay = QHBoxLayout(); self.discount = QDoubleSpinBox(); self.discount.setRange(0, 999999999); self.discount.valueChanged.connect(self.refresh_cart)
        self.paid = QDoubleSpinBox(); self.paid.setRange(0, 999999999)
        self.method = QComboBox(); self.method.addItems(["CASH", "QRIS", "TRANSFER", "DEBIT"])
        pay.addWidget(QLabel("Diskon")); pay.addWidget(self.discount); pay.addWidget(QLabel("Bayar")); pay.addWidget(self.paid); pay.addWidget(self.method)
        self.total_label = QLabel("TOTAL Rp 0"); pay.addWidget(self.total_label)
        checkout = QPushButton("BAYAR & SIMPAN"); checkout.clicked.connect(self.checkout); pay.addWidget(checkout)
        clear = QPushButton("CLEAR"); clear.clicked.connect(self.clear_cart); pay.addWidget(clear); layout.addLayout(pay)
        return w

    def add_barcode(self):
        code = self.barcode.text().strip()
        if not code: return
        with SessionLocal() as s:
            product = s.query(Product).filter_by(barcode=code, active=True).first()
            if not product: QMessageBox.warning(self, "Produk", "Barcode tidak ditemukan."); return
            qty = Decimal(str(self.qty.value()))
            existing = next((x for x in self.cart if x["product_id"] == product.id), None)
            current = existing["quantity"] if existing else Decimal("0")
            if current + qty > Decimal(str(product.stock)): QMessageBox.warning(self, "Stok", "Stok tidak mencukupi."); return
        if existing: existing["quantity"] += qty
        else: self.cart.append({"product_id": product.id, "quantity": qty})
        self.barcode.clear(); self.refresh_cart()

    def refresh_cart(self):
        self.cart_table.setRowCount(len(self.cart)); subtotal = Decimal("0")
        with SessionLocal() as s:
            for i, item in enumerate(self.cart):
                p = s.get(Product, item["product_id"])
                if not p: continue
                line = Decimal(str(p.selling_price)) * item["quantity"]; subtotal += line
                for c, v in enumerate([p.barcode, p.name, str(item["quantity"]), str(p.selling_price), str(line)]): self.cart_table.setItem(i, c, QTableWidgetItem(v))
        total = max(Decimal("0"), subtotal - Decimal(str(self.discount.value())))
        self.total_label.setText(f"TOTAL {money(total)}"); return total

    def clear_cart(self):
        self.cart.clear(); self.discount.setValue(0); self.paid.setValue(0); self.refresh_cart()

    def checkout(self):
        try:
            if not self.cart: raise ValueError("Keranjang kosong")
            total = self.refresh_cart(); paid = Decimal(str(self.paid.value()))
            if paid < total: raise ValueError("Pembayaran kurang")
            invoice = "INV-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            with SessionLocal() as s: sale = create_sale(s, self.cart, self.discount.value(), paid, self.method.currentText(), invoice)
            QMessageBox.information(self, "Berhasil", f"{sale.invoice_no}\nTotal {money(sale.total)}\nKembalian {money(sale.change)}")
            self.clear_cart()
        except Exception as exc: QMessageBox.critical(self, "Transaksi gagal", str(exc))

    def products(self):
        w = QWidget(); layout = QVBoxLayout(w); form = QFormLayout()
        self.p_barcode = QLineEdit(); self.p_name = QLineEdit(); self.p_buy = QDoubleSpinBox(); self.p_sell = QDoubleSpinBox(); self.p_stock = QDoubleSpinBox(); self.p_min = QDoubleSpinBox()
        for f in (self.p_buy, self.p_sell): f.setRange(0, 999999999)
        for f in (self.p_stock, self.p_min): f.setRange(0, 999999999); f.setDecimals(3)
        for label, field in [("Barcode", self.p_barcode), ("Nama", self.p_name), ("Harga Beli", self.p_buy), ("Harga Jual", self.p_sell), ("Stok Awal", self.p_stock), ("Stok Minimum", self.p_min)]: form.addRow(label, field)
        layout.addLayout(form)
        buttons = QHBoxLayout(); save = QPushButton("Tambah Produk"); save.clicked.connect(self.save_product); buttons.addWidget(save)
        edit = QPushButton("Edit Terpilih"); edit.clicked.connect(self.edit_product); buttons.addWidget(edit)
        off = QPushButton("Nonaktifkan"); off.clicked.connect(self.deactivate_selected); buttons.addWidget(off); layout.addLayout(buttons)
        self.product_table = QTableWidget(0, 6); self.product_table.setHorizontalHeaderLabels(["ID", "Barcode", "Nama", "Beli", "Jual", "Stok"]); self.product_table.cellClicked.connect(self.select_product); layout.addWidget(self.product_table); self.load_products(); return w

    def load_products(self):
        with SessionLocal() as s: rows = s.query(Product).order_by(Product.name).all()
        self.product_table.setRowCount(len(rows))
        for i, p in enumerate(rows):
            for c, v in enumerate([p.id, p.barcode, p.name, p.purchase_price, p.selling_price, p.stock]): self.product_table.setItem(i, c, QTableWidgetItem(str(v)))

    def select_product(self, row, _column):
        self.selected_product_id = int(self.product_table.item(row, 0).text())
        self.p_barcode.setText(self.product_table.item(row, 1).text()); self.p_name.setText(self.product_table.item(row, 2).text())
        self.p_buy.setValue(float(self.product_table.item(row, 3).text())); self.p_sell.setValue(float(self.product_table.item(row, 4).text())); self.p_min.setValue(0)

    def save_product(self):
        try:
            with SessionLocal() as s:
                create_product(s, self.p_barcode.text(), self.p_name.text(), self.p_buy.value(), self.p_sell.value(), self.p_stock.value(), self.p_min.value())
            self.load_products(); self.clear_product_form()
        except Exception as exc: QMessageBox.warning(self, "Produk", str(exc))

    def edit_product(self):
        try:
            pid = getattr(self, "selected_product_id", None)
            if not pid: raise ValueError("Pilih produk terlebih dahulu")
            with SessionLocal() as s: update_product(s, pid, barcode=self.p_barcode.text(), name=self.p_name.text(), purchase_price=self.p_buy.value(), selling_price=self.p_sell.value(), minimum_stock=self.p_min.value())
            self.load_products(); QMessageBox.information(self, "Produk", "Produk diperbarui.")
        except Exception as exc: QMessageBox.warning(self, "Produk", str(exc))

    def deactivate_selected(self):
        try:
            pid = getattr(self, "selected_product_id", None)
            if not pid: raise ValueError("Pilih produk terlebih dahulu")
            with SessionLocal() as s: deactivate_product(s, pid)
            self.load_products()
        except Exception as exc: QMessageBox.warning(self, "Produk", str(exc))

    def clear_product_form(self):
        self.p_barcode.clear(); self.p_name.clear(); self.p_buy.setValue(0); self.p_sell.setValue(0); self.p_stock.setValue(0); self.p_min.setValue(0)

    def stock_page(self):
        w = QWidget(); layout = QVBoxLayout(w); form = QHBoxLayout()
        self.stock_product = QComboBox(); self.stock_qty = QDoubleSpinBox(); self.stock_qty.setRange(-999999, 999999); self.stock_qty.setDecimals(3); self.stock_ref = QLineEdit(); self.stock_ref.setPlaceholderText("Referensi/opname")
        self.load_stock_products(); form.addWidget(self.stock_product); form.addWidget(self.stock_qty); form.addWidget(self.stock_ref)
        btn = QPushButton("Simpan Mutasi"); btn.clicked.connect(self.save_stock_adjustment); form.addWidget(btn); layout.addLayout(form)
        self.stock_table = QTableWidget(0, 5); self.stock_table.setHorizontalHeaderLabels(["Produk", "Barcode", "Stok", "Minimum", "Status"]); layout.addWidget(self.stock_table); self.load_stock_table(); return w

    def load_stock_products(self):
        with SessionLocal() as s: rows = s.query(Product).filter_by(active=True).order_by(Product.name).all()
        self.stock_product.clear()
        for p in rows: self.stock_product.addItem(f"{p.name} | {p.barcode}", p.id)

    def save_stock_adjustment(self):
        try:
            with SessionLocal() as s: adjust_stock(s, self.stock_product.currentData(), self.stock_qty.value(), "OPNAME", self.stock_ref.text().strip() or None)
            self.load_stock_table(); self.load_stock_products()
        except Exception as exc: QMessageBox.warning(self, "Stok", str(exc))

    def load_stock_table(self):
        with SessionLocal() as s: rows = stock_summary(s)
        self.stock_table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            for c, v in enumerate([r["name"], r["barcode"], r["stock"], r["minimum_stock"], r["status"]]): self.stock_table.setItem(i, c, QTableWidgetItem(str(v)))

    def purchase_page(self):
        w = QWidget(); layout = QVBoxLayout(w); form = QFormLayout()
        self.buy_product = QComboBox(); self.buy_supplier = QComboBox(); self.buy_qty = QDoubleSpinBox(); self.buy_qty.setRange(0.001, 999999); self.buy_qty.setDecimals(3); self.buy_cost = QDoubleSpinBox(); self.buy_cost.setRange(0, 999999999); self.buy_invoice = QLineEdit()
        self.load_purchase_options()
        for label, field in [("Produk", self.buy_product), ("Supplier", self.buy_supplier), ("Qty", self.buy_qty), ("Harga Beli", self.buy_cost), ("No. Invoice", self.buy_invoice)]: form.addRow(label, field)
        layout.addLayout(form); btn = QPushButton("Simpan Pembelian & Tambah Stok"); btn.clicked.connect(self.save_purchase); layout.addWidget(btn)
        return w

    def load_purchase_options(self):
        with SessionLocal() as s:
            products = s.query(Product).filter_by(active=True).order_by(Product.name).all(); suppliers = s.query(Supplier).order_by(Supplier.name).all()
        self.buy_product.clear(); self.buy_supplier.clear()
        for p in products: self.buy_product.addItem(f"{p.name} | {p.barcode}", p.id)
        self.buy_supplier.addItem("Tanpa Supplier", None)
        for x in suppliers: self.buy_supplier.addItem(x.name, x.id)

    def save_purchase(self):
        try:
            invoice = self.buy_invoice.text().strip() or "PB-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            with SessionLocal() as s: create_purchase(s, [{"product_id": self.buy_product.currentData(), "quantity": self.buy_qty.value(), "unit_cost": self.buy_cost.value()}], self.buy_supplier.currentData(), invoice)
            QMessageBox.information(self, "Pembelian", f"Pembelian {invoice} tersimpan."); self.load_stock_table(); self.load_stock_products()
        except Exception as exc: QMessageBox.warning(self, "Pembelian", str(exc))

    def cash_page(self):
        w = QWidget(); layout = QVBoxLayout(w); form = QHBoxLayout(); self.cash_type = QComboBox(); self.cash_type.addItems(["IN", "OUT"]); self.cash_amount = QDoubleSpinBox(); self.cash_amount.setRange(0, 999999999); self.cash_note = QLineEdit(); self.cash_note.setPlaceholderText("Keterangan")
        form.addWidget(self.cash_type); form.addWidget(self.cash_amount); form.addWidget(self.cash_note); btn = QPushButton("Simpan Kas"); btn.clicked.connect(self.save_cash); form.addWidget(btn); layout.addLayout(form); self.cash_label = QLabel(); layout.addWidget(self.cash_label); self.refresh_cash(); return w

    def save_cash(self):
        try:
            with SessionLocal() as s: record_cash_movement(s, self.cash_type.currentText(), self.cash_amount.value(), note=self.cash_note.text())
            self.cash_amount.setValue(0); self.cash_note.clear(); self.refresh_cash()
        except Exception as exc: QMessageBox.warning(self, "Kas", str(exc))

    def refresh_cash(self):
        with SessionLocal() as s: summary = cash_summary(s)
        self.cash_label.setText(f"Kas Masuk: {money(summary['cash_in'])} | Kas Keluar: {money(summary['cash_out'])} | Saldo: {money(summary['balance'])}")

    def report_page(self):
        w = QWidget(); layout = QVBoxLayout(w); self.report_text = QTextEdit(); self.report_text.setReadOnly(True); layout.addWidget(self.report_text); btn = QPushButton("Refresh Laporan"); btn.clicked.connect(self.refresh_report); layout.addWidget(btn); self.refresh_report(); return w

    def refresh_report(self):
        with SessionLocal() as s:
            sales = sales_summary(s); cash = cash_summary(s); stock = stock_summary(s); recent = recent_sales(s, 20)
        lines = ["=== LAPORAN WPOS PRO ===", f"Transaksi: {sales['transactions']}", f"Omzet: {money(sales['omzet'])}", f"Kas masuk: {money(cash['cash_in'])}", f"Kas keluar: {money(cash['cash_out'])}", f"Saldo kas: {money(cash['balance'])}", "", "=== STOK ==="]
        for r in stock: lines.append(f"{r['name']} | {r['stock']} | {r['status']}")
        lines += ["", "=== TRANSAKSI TERBARU ==="]
        for x in recent: lines.append(f"{x.created_at:%Y-%m-%d %H:%M:%S} | {x.invoice_no} | {money(x.total)} | {x.payment_method}")
        self.report_text.setPlainText("\n".join(lines))
