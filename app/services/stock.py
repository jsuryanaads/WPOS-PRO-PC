from decimal import Decimal
from ..models import Product, StockMovement

def adjust_stock(session, product_id, quantity, movement_type="ADJUSTMENT", reference=None):
    product = session.get(Product, product_id)
    qty = Decimal(str(quantity))
    if not product or qty == 0:
        raise ValueError("Produk/jumlah tidak valid")
    if product.stock + qty < 0:
        raise ValueError("Stok tidak boleh negatif")
    product.stock += qty
    session.add(StockMovement(product_id=product.id, movement_type=movement_type,
                              quantity=qty, reference=reference))
    session.commit()
    return product
