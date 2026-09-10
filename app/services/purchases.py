from decimal import Decimal
from ..models import Purchase, PurchaseItem, Product, StockMovement, CashMovement

def create_purchase(session, items, supplier_id, invoice_no):
    if not items:
        raise ValueError("Item pembelian kosong")
    total = Decimal("0")
    products = {}
    for row in items:
        product = session.get(Product, row["product_id"])
        qty = Decimal(str(row["quantity"]))
        cost = Decimal(str(row["unit_cost"]))
        if not product or not product.active:
            raise ValueError("Produk tidak ditemukan/tidak aktif")
        if qty <= 0 or cost < 0:
            raise ValueError("Jumlah/harga pembelian tidak valid")
        products[product.id] = product
        total += qty * cost

    if session.query(Purchase).filter_by(invoice_no=invoice_no).first():
        raise ValueError("Nomor pembelian sudah digunakan")

    purchase = Purchase(invoice_no=invoice_no, supplier_id=supplier_id, total=total)
    session.add(purchase)
    session.flush()
    for row in items:
        product = products[row["product_id"]]
        qty = Decimal(str(row["quantity"]))
        cost = Decimal(str(row["unit_cost"]))
        purchase.items.append(PurchaseItem(product_id=product.id, quantity=qty,
                                           unit_cost=cost, line_total=qty*cost))
        product.stock += qty
        product.purchase_price = cost
        session.add(StockMovement(product_id=product.id, movement_type="PURCHASE",
                                  quantity=qty, reference=invoice_no))
    session.commit()
    return purchase
