from datetime import datetime
from decimal import Decimal
from PySide6.QtWidgets import (QMainWindow,QTabWidget,QWidget,QVBoxLayout,QHBoxLayout,QLineEdit,QPushButton,QLabel,QDoubleSpinBox,QComboBox,QTableWidget,QTableWidgetItem,QFormLayout,QMessageBox,QTextEdit,QFileDialog)
from ..database import SessionLocal, engine
from ..models import Product, Supplier
from ..services.sales import create_sale
from ..services.products import create_product, update_product, deactivate_product
from ..services.stock import adjust_stock
from ..services.purchases import create_purchase
from ..services.cash import record_cash_movement
from ..services.reports import sales_summary, low_stock_count, cash_summary, stock_summary, recent_sales
from ..services.backup import backup_database, restore_database
from ..services.settings import get_settings, save_settings
from ..services.printer import available_printers, print_receipt, test_print
from .master_data import category_page, unit_page, supplier_page, customer_page

def money(value): return f"Rp {Decimal(str(value)):,.0f}".replace(",", ".")

class MainWindow(QMainWindow):
    def __init__(self,user):
        super().__init__(); self.user=user; self.cart=[]; self.setWindowTitle("WPOS PRO V1.0")
        tabs=QTabWidget(); tabs.addTab(self.dashboard(),"Dashboard"); tabs.addTab(self.cashier(),"Kasir"); tabs.addTab(self.products(),"Produk"); tabs.addTab(self.stock_page(),"Stok & Mutasi"); tabs.addTab(self.purchase_page(),"Pembelian"); tabs.addTab(self.cash_page(),"Kas"); tabs.addTab(self.report_page(),"Laporan"); tabs.addTab(self.settings_page(),"Pengaturan Toko"); tabs.addTab(self.printer_page(),"Printer"); tabs.addTab(self.backup_page(),"Backup / Restore"); tabs.addTab(category_page(),"Kategori"); tabs.addTab(unit_page(),"Satuan"); tabs.addTab(supplier_page(),"Supplier"); tabs.addTab(customer_page(),"Pelanggan"); self.setCentralWidget(tabs); self.resize(1200,760)
    def dashboard(self):
        w=QWidget(); l=QVBoxLayout(w); l.addWidget(QLabel(f"<h1>WPOS PRO</h1>Login: {self.user.username} ({self.user.role})"));
        with SessionLocal() as s: summary=sales_summary(s); low=low_stock_count(s); products=s.query(Product).count(); cash=cash_summary(s)
        for x in [f"Transaksi: {summary['transactions']}",f"Produk: {products}",f"Stok menipis/habis: {low}",f"Omzet: {money(summary['omzet'])}",f"Saldo kas: {money(cash['balance'])}"]: l.addWidget(QLabel(x))
        return w
    def cashier(self):
        w=QWidget(); l=QVBoxLayout(w); top=QHBoxLayout(); self.barcode=QLineEdit(); self.barcode.setPlaceholderText("Scan / ketik barcode + Enter"); self.barcode.returnPressed.connect(self.add_barcode); top.addWidget(self.barcode); self.qty=QDoubleSpinBox(); self.qty.setRange(.001,999999); self.qty.setDecimals(3); self.qty.setValue(1); top.addWidget(self.qty); b=QPushButton("Tambah"); b.clicked.connect(self.add_barcode); top.addWidget(b); l.addLayout(top); self.cart_table=QTableWidget(0,5); self.cart_table.setHorizontalHeaderLabels(["Barcode","Produk","Qty","Harga","Subtotal"]); l.addWidget(self.cart_table); pay=QHBoxLayout(); self.discount=QDoubleSpinBox(); self.discount.setRange(0,999999999); self.discount.valueChanged.connect(self.refresh_cart); self.paid=QDoubleSpinBox(); self.paid.setRange(0,999999999); self.method=QComboBox(); self.method.addItems(["CASH","QRIS","TRANSFER","DEBIT"]); pay.addWidget(QLabel("Diskon")); pay.addWidget(self.discount); pay.addWidget(QLabel("Bayar")); pay.addWidget(self.paid); pay.addWidget(self.method); self.total_label=QLabel("TOTAL Rp 0"); pay.addWidget(self.total_label); b=QPushButton("BAYAR & SIMPAN"); b.clicked.connect(self.checkout); pay.addWidget(b); b=QPushButton("CLEAR"); b.clicked.connect(self.clear_cart); pay.addWidget(b); l.addLayout(pay); return w
    def add_barcode(self):
        code=self.barcode.text().strip()
        if not code:return
        with SessionLocal() as s:
            p=s.query(Product).filter_by(barcode=code,active=True).first()
            if not p: QMessageBox.warning(self,"Produk","Barcode tidak ditemukan."); return
            q=Decimal(str(self.qty.value())); e=next((x for x in self.cart if x["product_id"]==p.id),None); cur=e["quantity"] if e else Decimal(0)
            if cur+q>Decimal(str(p.stock)): QMessageBox.warning(self,"Stok","Stok tidak mencukupi."); return
        if e:e["quantity"]+=q
        else:self.cart.append({"product_id":p.id,"quantity":q})
        self.barcode.clear(); self.refresh_cart()
    def refresh_cart(self):
        self.cart_table.setRowCount(len(self.cart)); sub=Decimal(0)
        with SessionLocal() as s:
            for i,it in enumerate(self.cart):
                p=s.get(Product,it["product_id"])
                if not p:continue
                line=Decimal(str(p.selling_price))*it["quantity"]; sub+=line
                for c,v in enumerate([p.barcode,p.name,str(it["quantity"]),str(p.selling_price),str(line)]):self.cart_table.setItem(i,c,QTableWidgetItem(v))
        total=max(Decimal(0),sub-Decimal(str(self.discount.value()))); self.total_label.setText(f"TOTAL {money(total)}"); return total
    def clear_cart(self): self.cart.clear(); self.discount.setValue(0); self.paid.setValue(0); self.refresh_cart()
    def checkout(self):
        try:
            if not self.cart:raise ValueError("Keranjang kosong")
            total=self.refresh_cart(); paid=Decimal(str(self.paid.value()))
            if paid<total:raise ValueError("Pembayaran kurang")
            invoice="INV-"+datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            with SessionLocal() as s:
                sale=create_sale(s,self.cart,self.discount.value(),paid,self.method.currentText(),invoice); items=[]
                for it in self.cart:
                    p=s.get(Product,it["product_id"])
                    if p:items.append({"name":p.name,"quantity":it["quantity"],"unit_price":p.selling_price,"line_total":p.selling_price*it["quantity"]})
            print_receipt(self,sale,items); QMessageBox.information(self,"Berhasil",f"{sale.invoice_no}\nTotal {money(sale.total)}\nKembalian {money(sale.change)}"); self.clear_cart()
        except Exception as exc:QMessageBox.critical(self,"Transaksi gagal",str(exc))
    def products(self):
        w=QWidget(); l=QVBoxLayout(w); f=QFormLayout(); self.p_barcode=QLineEdit(); self.p_name=QLineEdit(); self.p_buy=QDoubleSpinBox(); self.p_sell=QDoubleSpinBox(); self.p_stock=QDoubleSpinBox(); self.p_min=QDoubleSpinBox();
        for x in (self.p_buy,self.p_sell):x.setRange(0,999999999)
        for x in (self.p_stock,self.p_min):x.setRange(0,999999999);x.setDecimals(3)
        for a,b in [("Barcode",self.p_barcode),("Nama",self.p_name),("Harga Beli",self.p_buy),("Harga Jual",self.p_sell),("Stok Awal",self.p_stock),("Stok Minimum",self.p_min)]:f.addRow(a,b)
        l.addLayout(f); bs=QHBoxLayout(); b=QPushButton("Tambah Produk"); b.clicked.connect(self.save_product); bs.addWidget(b); b=QPushButton("Edit Terpilih"); b.clicked.connect(self.edit_product); bs.addWidget(b); b=QPushButton("Nonaktifkan"); b.clicked.connect(self.deactivate_selected); bs.addWidget(b); l.addLayout(bs); self.product_table=QTableWidget(0,6); self.product_table.setHorizontalHeaderLabels(["ID","Barcode","Nama","Beli","Jual","Stok"]); self.product_table.cellClicked.connect(self.select_product); l.addWidget(self.product_table); self.load_products(); return w
    def load_products(self):
        with SessionLocal() as s:r=s.query(Product).order_by(Product.name).all()
        self.product_table.setRowCount(len(r))
        for i,p in enumerate(r):
            for c,v in enumerate([p.id,p.barcode,p.name,p.purchase_price,p.selling_price,p.stock]):self.product_table.setItem(i,c,QTableWidgetItem(str(v)))
    def select_product(self,row,_):
        self.selected_product_id=int(self.product_table.item(row,0).text())
        with SessionLocal() as s:p=s.get(Product,self.selected_product_id)
        if p:self.p_barcode.setText(p.barcode);self.p_name.setText(p.name);self.p_buy.setValue(float(p.purchase_price));self.p_sell.setValue(float(p.selling_price));self.p_min.setValue(float(p.minimum_stock));self.p_stock.setValue(float(p.stock))
    def save_product(self):
        try:
            with SessionLocal() as s:create_product(s,self.p_barcode.text(),self.p_name.text(),self.p_buy.value(),self.p_sell.value(),self.p_stock.value(),self.p_min.value())
            self.load_products();self.clear_product_form()
        except Exception as e:QMessageBox.warning(self,"Produk",str(e))
    def edit_product(self):
        try:
            pid=getattr(self,"selected_product_id",None)
            if not pid:raise ValueError("Pilih produk terlebih dahulu")
            with SessionLocal() as s:update_product(s,pid,barcode=self.p_barcode.text(),name=self.p_name.text(),purchase_price=self.p_buy.value(),selling_price=self.p_sell.value(),minimum_stock=self.p_min.value())
            self.load_products();QMessageBox.information(self,"Produk","Produk diperbarui.")
        except Exception as e:QMessageBox.warning(self,"Produk",str(e))
    def deactivate_selected(self):
        try:
            pid=getattr(self,"selected_product_id",None)
            if not pid:raise ValueError("Pilih produk terlebih dahulu")
            with SessionLocal() as s:deactivate_product(s,pid)
            self.load_products()
        except Exception as e:QMessageBox.warning(self,"Produk",str(e))
    def clear_product_form(self):self.p_barcode.clear();self.p_name.clear();self.p_buy.setValue(0);self.p_sell.setValue(0);self.p_stock.setValue(0);self.p_min.setValue(0);self.selected_product_id=None
    def stock_page(self):
        w=QWidget();l=QVBoxLayout(w);f=QHBoxLayout();self.stock_product=QComboBox();self.stock_qty=QDoubleSpinBox();self.stock_qty.setRange(-999999,999999);self.stock_qty.setDecimals(3);self.stock_ref=QLineEdit();self.stock_ref.setPlaceholderText("Referensi/opname");self.load_stock_products();f.addWidget(self.stock_product);f.addWidget(self.stock_qty);f.addWidget(self.stock_ref);b=QPushButton("Simpan Mutasi");b.clicked.connect(self.save_stock_adjustment);f.addWidget(b);l.addLayout(f);self.stock_table=QTableWidget(0,5);self.stock_table.setHorizontalHeaderLabels(["Produk","Barcode","Stok","Minimum","Status"]);l.addWidget(self.stock_table);self.load_stock_table();return w
    def load_stock_products(self):
        with SessionLocal() as s:r=s.query(Product).filter_by(active=True).order_by(Product.name).all()
        self.stock_product.clear()
        for p in r:self.stock_product.addItem(f"{p.name} | {p.barcode}",p.id)
    def save_stock_adjustment(self):
        try:
            with SessionLocal() as s:adjust_stock(s,self.stock_product.currentData(),self.stock_qty.value(),"OPNAME",self.stock_ref.text().strip() or None)
            self.load_stock_table();self.load_stock_products()
        except Exception as e:QMessageBox.warning(self,"Stok",str(e))
    def load_stock_table(self):
        with SessionLocal() as s:r=stock_summary(s)
        self.stock_table.setRowCount(len(r))
        for i,x in enumerate(r):
            for c,v in enumerate([x["name"],x["barcode"],x["stock"],x["minimum_stock"],x["status"]]):self.stock_table.setItem(i,c,QTableWidgetItem(str(v)))
    def purchase_page(self):
        w=QWidget();l=QVBoxLayout(w);f=QFormLayout();self.buy_product=QComboBox();self.buy_supplier=QComboBox();self.buy_qty=QDoubleSpinBox();self.buy_qty.setRange(.001,999999);self.buy_qty.setDecimals(3);self.buy_cost=QDoubleSpinBox();self.buy_cost.setRange(0,999999999);self.buy_invoice=QLineEdit();self.load_purchase_options()
        for a,b in [("Produk",self.buy_product),("Supplier",self.buy_supplier),("Qty",self.buy_qty),("Harga Beli",self.buy_cost),("No. Invoice",self.buy_invoice)]:f.addRow(a,b)
        l.addLayout(f);b=QPushButton("Simpan Pembelian & Tambah Stok");b.clicked.connect(self.save_purchase);l.addWidget(b);return w
    def load_purchase_options(self):
        with SessionLocal() as s:p=s.query(Product).filter_by(active=True).order_by(Product.name).all();sup=s.query(Supplier).order_by(Supplier.name).all()
        self.buy_product.clear();self.buy_supplier.clear()
        for x in p:self.buy_product.addItem(f"{x.name} | {x.barcode}",x.id)
        self.buy_supplier.addItem("Tanpa Supplier",None)
        for x in sup:self.buy_supplier.addItem(x.name,x.id)
    def save_purchase(self):
        try:
            inv=self.buy_invoice.text().strip() or "PB-"+datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            with SessionLocal() as s:create_purchase(s,[{"product_id":self.buy_product.currentData(),"quantity":self.buy_qty.value(),"unit_cost":self.buy_cost.value()}],self.buy_supplier.currentData(),inv)
            QMessageBox.information(self,"Pembelian",f"Pembelian {inv} tersimpan.");self.load_stock_table();self.load_stock_products()
        except Exception as e:QMessageBox.warning(self,"Pembelian",str(e))
    def cash_page(self):
        w=QWidget();l=QVBoxLayout(w);f=QHBoxLayout();self.cash_type=QComboBox();self.cash_type.addItems(["IN","OUT"]);self.cash_amount=QDoubleSpinBox();self.cash_amount.setRange(0,999999999);self.cash_note=QLineEdit();self.cash_note.setPlaceholderText("Keterangan");f.addWidget(self.cash_type);f.addWidget(self.cash_amount);f.addWidget(self.cash_note);b=QPushButton("Simpan Kas");b.clicked.connect(self.save_cash);f.addWidget(b);l.addLayout(f);self.cash_label=QLabel();l.addWidget(self.cash_label);self.refresh_cash();return w
    def save_cash(self):
        try:
            with SessionLocal() as s:record_cash_movement(s,self.cash_type.currentText(),self.cash_amount.value(),note=self.cash_note.text())
            self.cash_amount.setValue(0);self.cash_note.clear();self.refresh_cash()
        except Exception as e:QMessageBox.warning(self,"Kas",str(e))
    def refresh_cash(self):
        with SessionLocal() as s:x=cash_summary(s)
        self.cash_label.setText(f"Kas Masuk: {money(x['cash_in'])} | Kas Keluar: {money(x['cash_out'])} | Saldo: {money(x['balance'])}")
    def report_page(self):
        w=QWidget();l=QVBoxLayout(w);self.report_text=QTextEdit();self.report_text.setReadOnly(True);l.addWidget(self.report_text);b=QPushButton("Refresh Laporan");b.clicked.connect(self.refresh_report);l.addWidget(b);self.refresh_report();return w
    def refresh_report(self):
        with SessionLocal() as s:sales=sales_summary(s);cash=cash_summary(s);stock=stock_summary(s);recent=recent_sales(s,20)
        lines=["=== LAPORAN WPOS PRO ===",f"Transaksi: {sales['transactions']}",f"Omzet: {money(sales['omzet'])}",f"Kas masuk: {money(cash['cash_in'])}",f"Kas keluar: {money(cash['cash_out'])}",f"Saldo kas: {money(cash['balance'])}","","=== STOK ==="]
        for r in stock:lines.append(f"{r['name']} | {r['stock']} | {r['status']}")
        lines += ["","=== TRANSAKSI TERBARU ==="]
        for x in recent:lines.append(f"{x.created_at:%Y-%m-%d %H:%M:%S} | {x.invoice_no} | {money(x.total)} | {x.payment_method}")
        self.report_text.setPlainText("\n".join(lines))
    def settings_page(self):
        w=QWidget();l=QVBoxLayout(w);f=QFormLayout();self.store_name=QLineEdit();self.store_address=QLineEdit();self.store_phone=QLineEdit();self.receipt_footer=QLineEdit()
        for a,b in [("Nama Toko",self.store_name),("Alamat",self.store_address),("Telepon",self.store_phone),("Footer Struk",self.receipt_footer)]:f.addRow(a,b)
        l.addLayout(f);b=QPushButton("SIMPAN PENGATURAN TOKO");b.clicked.connect(self.save_store_settings);l.addWidget(b)
        with SessionLocal() as s:x=get_settings(s)
        self.store_name.setText(x["store_name"]);self.store_address.setText(x["store_address"]);self.store_phone.setText(x["store_phone"]);self.receipt_footer.setText(x["receipt_footer"]);return w
    def save_store_settings(self):
        try:
            with SessionLocal() as s:save_settings(s,{"store_name":self.store_name.text().strip() or "TOKO SEMBAKO","store_address":self.store_address.text().strip(),"store_phone":self.store_phone.text().strip(),"receipt_footer":self.receipt_footer.text().strip()})
            QMessageBox.information(self,"Pengaturan","Pengaturan toko berhasil disimpan.")
        except Exception as e:QMessageBox.warning(self,"Pengaturan",str(e))
    def printer_page(self):
        w=QWidget();l=QVBoxLayout(w);f=QFormLayout();self.printer_combo=QComboBox();self.printer_combo.addItem("Gunakan pilihan saat cetak","")
        for n in available_printers():self.printer_combo.addItem(n,n)
        self.paper_combo=QComboBox();self.paper_combo.addItems(["80mm","58mm"]);f.addRow("Printer",self.printer_combo);f.addRow("Ukuran Struk",self.paper_combo);l.addLayout(f);b=QPushButton("SIMPAN PENGATURAN PRINTER");b.clicked.connect(self.save_printer_settings);l.addWidget(b);b=QPushButton("TES CETAK");b.clicked.connect(self.do_test_print);l.addWidget(b)
        with SessionLocal() as s:x=get_settings(s)
        i=self.printer_combo.findData(x["printer_name"]);self.printer_combo.setCurrentIndex(i if i>=0 else 0);i=self.paper_combo.findText(x["receipt_paper"]);self.paper_combo.setCurrentIndex(i if i>=0 else 0);return w
    def save_printer_settings(self):
        try:
            with SessionLocal() as s:save_settings(s,{"printer_name":self.printer_combo.currentData() or "","receipt_paper":self.paper_combo.currentText()})
            QMessageBox.information(self,"Printer","Pengaturan printer berhasil disimpan.")
        except Exception as e:QMessageBox.warning(self,"Printer",str(e))
    def do_test_print(self):
        try:
            if test_print(self,self.printer_combo.currentData() or "",self.paper_combo.currentText()):QMessageBox.information(self,"Printer","Tes cetak selesai.")
        except Exception as e:QMessageBox.warning(self,"Printer",str(e))
    def backup_page(self):
        w=QWidget();l=QVBoxLayout(w);l.addWidget(QLabel("<h2>Backup & Restore Database</h2>"));l.addWidget(QLabel("Backup membuat salinan konsisten SQLite. Restore mengganti database aktif dan membutuhkan restart aplikasi."));b=QPushButton("BUAT BACKUP SEKARANG");b.clicked.connect(self.do_backup);l.addWidget(b);b=QPushButton("RESTORE DARI FILE .DB");b.clicked.connect(self.do_restore);l.addWidget(b);return w
    def do_backup(self):
        try:
            p=backup_database();QMessageBox.information(self,"Backup",f"Backup berhasil dibuat:\n{p}")
        except Exception as e:QMessageBox.critical(self,"Backup gagal",str(e))
    def do_restore(self):
        p,_=QFileDialog.getOpenFileName(self,"Pilih Backup","","Database SQLite (*.db)")
        if not p:return
        if QMessageBox.question(self,"Konfirmasi Restore","Restore akan mengganti database aktif. Lanjutkan?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)!=QMessageBox.Yes:return
        try:
            engine.dispose();restore_database(p);QMessageBox.information(self,"Restore berhasil","Database berhasil dipulihkan. Tutup dan buka kembali WPOS PRO sebelum melanjutkan.")
        except Exception as e:QMessageBox.critical(self,"Restore gagal",str(e))
