from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLineEdit,QPushButton,QTableWidget,QTableWidgetItem,QMessageBox
from ..database import SessionLocal
from ..models import Category,Unit,Supplier,Customer

class SimpleMaster(QWidget):
    def __init__(self, model, title, fields):
        super().__init__(); self.model=model; self.fields=fields; self.setWindowTitle(title)
        l=QVBoxLayout(self); row=QHBoxLayout(); self.inputs=[]
        for f in fields:
            x=QLineEdit(); x.setPlaceholderText(f); self.inputs.append(x); row.addWidget(x)
        b=QPushButton("Simpan"); b.clicked.connect(self.save); row.addWidget(b); l.addLayout(row)
        self.table=QTableWidget(0,len(fields)+1); self.table.setHorizontalHeaderLabels(fields+["ID"]); l.addWidget(self.table); self.refresh()
    def save(self):
        vals=[x.text().strip() for x in self.inputs]
        if not vals[0]: QMessageBox.warning(self,"Validasi",f"{self.fields[0]} wajib diisi"); return
        try:
            with SessionLocal() as s:
                obj=self.model(**{f.lower():v for f,v in zip(self.fields,vals)})
                s.add(obj); s.commit()
            for x in self.inputs:x.clear()
            self.refresh()
        except Exception as e: QMessageBox.warning(self,"Gagal",str(e))
    def refresh(self):
        with SessionLocal() as s: rows=s.query(self.model).order_by(self.model.id.desc()).all()
        self.table.setRowCount(len(rows))
        for r,o in enumerate(rows):
            for c,f in enumerate(self.fields): self.table.setItem(r,c,QTableWidgetItem(str(getattr(o,f.lower(), ""))))
            self.table.setItem(r,len(self.fields),QTableWidgetItem(str(o.id)))

def category_page(): return SimpleMaster(Category,"Kategori",["Name"])
def unit_page(): return SimpleMaster(Unit,"Satuan",["Name"])
def supplier_page(): return SimpleMaster(Supplier,"Supplier",["Name","Phone","Address"])
def customer_page(): return SimpleMaster(Customer,"Pelanggan",["Name","Phone","Address"])
