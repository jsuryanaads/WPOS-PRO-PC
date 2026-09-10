from decimal import Decimal
from ..models import Sale, SaleItem, Product, StockMovement, CashMovement

def create_sale(session, items, discount, paid, payment_method, invoice_no):
    if not items:
        raise ValueError("Keranjang kosong")
    discount = Decimal(str(discount))
    paid = Decimal(str(paid))
    if discount < 0 or paid < 0:
        raise ValueError("Diskon/pembayaran tidak valid")
    if session.query(Sale).filter_by(invoice_no=invoice_no).first():
        raise ValueError("Nomor invoice sudah digunakan")

    total = Decimal("0")
    products = {}
    for row in items:
        product = session.get(Product, row["product_id"])
        qty = Decimal(str(row["quantity"]))
        if not product or not product.active:
            raise ValueError("Produk tidak ditemukan/tidak aktif")
        if qty <= 0:
            raise ValueError("Jumlah tidak valid")
        if Decimal(str(product.stock)) < qty:
            raise ValueError(f"Stok {product.name} tidak mencukupi")
        products[product.id] = product
        total += Decimal(str(product.selling_price)) * qty

    if discount > total:
        discount = total
    total -= discount
    if paid < total:
        raise ValueError("Pembayaran kurang")
    change = paid - total

    sale = Sale(invoice_no=invoice_no, subtotal=total + discount, discount=discount,
                total=total, paid=paid, change=change, payment_method=payment_method)
    session.add(sale)
    session.flush()
    for row in items:
        product = products[row["product_id"]]
        qty = Decimal(str(row["quantity"]))
        line = Decimal(str(product.selling_price)) * qty
        sale.items.append(SaleItem(product_id=product.id, quantity=qty,
                                   unit_price=product.selling_price, line_total=line))
        product.stock -= qty
        session.add(StockMovement(product_id=product.id, movement_type="SALE",
                                  quantity=-qty, reference=invoice_no))
    if payment_method == "CASH":
        session.add(CashMovement(movement_type="SALE", amount=total, reference=invoice_no))
    session.commit()
    return sale
