from datetime import datetime
from decimal import Decimal
from PySide6.QtWidgets import QMainWindow,QTabWidget,QWidget,QVBoxLayout,QHBoxLayout,QLineEdit,QPushButton,QLabel,QDoubleSpinBox,QComboBox,QTableWidget,QTableWidgetItem,QFormLayout,QMessageBox
from ..database import SessionLocal
from ..models import Product,Sale
from ..services.sales import create_sale
from ..services.reports import sales_summary, low_stock_count
from .master_data import category_page,unit_page,supplier_page,customer_page

class MainWindow(QMainWindow):
    def __init__(self,user):
        super().__init__(); self.user=user; self.cart=[]; self.setWindowTitle("WPOS PRO V1.0")
        tabs=QTabWidget(); tabs.addTab(self.dashboard(),"Dashboard"); tabs.addTab(self.cashier(),"Kasir"); tabs.addTab(self.products(),"Produk")
        tabs.addTab(category_page(),"Kategori"); tabs.addTab(unit_page(),"Satuan"); tabs.addTab(supplier_page(),"Supplier"); tabs.addTab(customer_page(),"Pelanggan")
        self.setCentralWidget(tabs); self.resize(1100,700)

    def dashboard(self):
        w=QWidget(); layout=QVBoxLayout(w); layout.addWidget(QLabel(f"<h1>WPOS PRO</h1>Login: {self.user.username} ({self.user.role})"))
        with SessionLocal() as s:
            summary=sales_summary(s); low=low_stock_count(s); products=s.query(Product).count()
        layout.addWidget(QLabel(f"Transaksi: {summary['transactions']}")); layout.addWidget(QLabel(f"Produk: {products}")); layout.addWidget(QLabel(f"Stok menipis/habis: {low}")); layout.addWidget(QLabel(f"Omzet: Rp {summary['omzet']:,.0f}".replace(",",".")))
        return w

    def cashier(self):
        w=QWidget(); layout=QVBoxLayout(w); top=QHBoxLayout()
        self.barcode=QLineEdit(); self.barcode.setPlaceholderText("Scan / ketik barcode + Enter"); self.barcode.returnPressed.connect(self.add_barcode); top.addWidget(self.barcode)
        self.qty=QDoubleSpinBox(); self.qty.setMinimum(0.001); self.qty.setMaximum(999999); self.qty.setDecimals(3); self.qty.setValue(1); top.addWidget(self.qty)
        add=QPushButton("Tambah"); add.clicked.connect(self.add_barcode); top.addWidget(add); layout.addLayout(top)
        self.cart_table=QTableWidget(0,5); self.cart_table.setHorizontalHeaderLabels(["Barcode","Produk","Qty","Harga","Subtotal"]); layout.addWidget(self.cart_table)
        pay=QHBoxLayout(); self.discount=QDoubleSpinBox(); self.discount.setMaximum(999999999); self.discount.valueChanged.connect(self.refresh_cart); self.paid=QDoubleSpinBox(); self.paid.setMaximum(999999999)
        self.method=QComboBox(); self.method.addItems(["CASH","QRIS","TRANSFER","DEBIT"])
        pay.addWidget(QLabel("Diskon")); pay.addWidget(self.discount); pay.addWidget(QLabel("Bayar")); pay.addWidget(self.paid); pay.addWidget(self.method)
        self.total_label=QLabel("TOTAL Rp 0"); pay.addWidget(self.total_label); checkout=QPushButton("BAYAR & SIMPAN"); checkout.clicked.connect(self.checkout); pay.addWidget(checkout)
        clear=QPushButton("CLEAR"); clear.clicked.connect(self.clear_cart); pay.addWidget(clear); layout.addLayout(pay); return w

    def add_barcode(self):
        code=self.barcode.text().strip()
        if not code:return
        with SessionLocal() as s:
            product=s.query(Product).filter_by(barcode=code,active=True).first()
            if not product: QMessageBox.warning(self,"Produk","Barcode tidak ditemukan."); return
            qty=Decimal(str(self.qty.value())); existing=next((x for x in self.cart if x["product_id"]==product.id),None); current=existing["quantity"] if existing else Decimal("0")
            if current+qty>Decimal(str(product.stock)): QMessageBox.warning(self,"Stok","Stok tidak mencukupi."); return
        if existing: existing["quantity"]+=qty
        else: self.cart.append({"product_id":product.id,"quantity":qty})
        self.barcode.clear(); self.refresh_cart()

    def refresh_cart(self):
        self.cart_table.setRowCount(len(self.cart)); subtotal=Decimal("0")
        with SessionLocal() as s:
            for i,item in enumerate(self.cart):
                p=s.get(Product,item["product_id"]); line=Decimal(p.selling_price)*item["quantity"]; subtotal+=line
                for c,v in enumerate([p.barcode,p.name,str(item["quantity"]),str(p.selling_price),str(line)]): self.cart_table.setItem(i,c,QTableWidgetItem(v))
        total=max(Decimal("0"),subtotal-Decimal(str(self.discount.value()))); self.total_label.setText(f"TOTAL Rp {total:,.0f}".replace(",",".")); return total

    def clear_cart(self): self.cart.clear(); self.discount.setValue(0); self.paid.setValue(0); self.refresh_cart()

    def checkout(self):
        try:
            total=self.refresh_cart(); paid=Decimal(str(self.paid.value()))
            if not self.cart: raise ValueError("Keranjang kosong")
            if paid<total: raise ValueError("Pembayaran kurang")
            invoice="INV-"+datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            with SessionLocal() as s: sale=create_sale(s,self.cart,self.discount.value(),paid,self.method.currentText(),invoice)
            QMessageBox.information(self,"Berhasil",f"{sale.invoice_no}\nTotal Rp {sale.total:,.0f}\nKembalian Rp {sale.change:,.0f}".replace(",",".")); self.clear_cart()
        except Exception as exc: QMessageBox.critical(self,"Transaksi gagal",str(exc))

    def products(self):
        w=QWidget(); layout=QVBoxLayout(w); form=QFormLayout(); self.p_barcode=QLineEdit(); self.p_name=QLineEdit(); self.p_buy=QDoubleSpinBox(); self.p_buy.setMaximum(999999999); self.p_sell=QDoubleSpinBox(); self.p_sell.setMaximum(999999999); self.p_stock=QDoubleSpinBox(); self.p_stock.setMaximum(999999999); self.p_stock.setDecimals(3); self.p_min=QDoubleSpinBox(); self.p_min.setMaximum(999999999); self.p_min.setDecimals(3)
        for label,field in [("Barcode",self.p_barcode),("Nama",self.p_name),("Harga Beli",self.p_buy),("Harga Jual",self.p_sell),("Stok",self.p_stock),("Stok Minimum",self.p_min)]: form.addRow(label,field)
        layout.addLayout(form); save=QPushButton("Simpan Produk"); save.clicked.connect(self.save_product); layout.addWidget(save); self.product_table=QTableWidget(0,5); self.product_table.setHorizontalHeaderLabels(["Barcode","Nama","Beli","Jual","Stok"]); layout.addWidget(self.product_table); self.load_products(); return w

    def load_products(self):
        with SessionLocal() as s: rows=s.query(Product).order_by(Product.name).all()
        self.product_table.setRowCount(len(rows))
        for i,p in enumerate(rows):
            for c,v in enumerate([p.barcode,p.name,str(p.purchase_price),str(p.selling_price),str(p.stock)]): self.product_table.setItem(i,c,QTableWidgetItem(v))

    def save_product(self):
        try:
            barcode=self.p_barcode.text().strip(); name=self.p_name.text().strip()
            if not barcode or not name: raise ValueError("Barcode dan nama wajib diisi")
            with SessionLocal() as s:
                if s.query(Product).filter_by(barcode=barcode).first(): raise ValueError("Barcode sudah digunakan")
                s.add(Product(barcode=barcode,name=name,purchase_price=self.p_buy.value(),selling_price=self.p_sell.value(),stock=self.p_stock.value(),minimum_stock=self.p_min.value())); s.commit()
            self.load_products(); self.p_barcode.clear(); self.p_name.clear()
        except Exception as exc: QMessageBox.warning(self,"Produk",str(exc))
