from decimal import Decimal
from ..models import Sale, Product

def sales_summary(session):
    sales = session.query(Sale).all()
    omzet = sum((Decimal(s.total) for s in sales), Decimal("0"))
    return {"transactions": len(sales), "omzet": omzet}

def low_stock_count(session):
    return session.query(Product).filter(Product.active == True, Product.stock <= Product.minimum_stock).count()
