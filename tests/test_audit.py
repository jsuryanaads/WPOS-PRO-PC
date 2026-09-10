from decimal import Decimal
import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Product, Sale, SaleItem
from app.services.auth import hash_password, verify_password
from app.services.sales import create_sale


def make_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)()


def test_password_hashing():
    h = hash_password("secret")
    assert verify_password("secret", h)
    assert not verify_password("wrong", h)


def test_required_tables_and_constraints():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    tables = set(inspect(engine).get_table_names())
    assert {"users", "products", "sales", "sale_items", "purchases", "purchase_items", "stock_movements", "cash_movements", "settings"}.issubset(tables)
    assert any(c.name == "ck_products_stock_nonnegative" for c in Product.__table__.constraints)
    assert any(c.name == "ck_sale_items_quantity_positive" for c in SaleItem.__table__.constraints)


def test_money_math():
    assert Decimal("10.00") * Decimal("2") == Decimal("20.00")


def test_duplicate_cart_rows_cannot_bypass_stock():
    session = make_session()
    product = Product(barcode="8990001", name="Beras", selling_price=Decimal("10000"), stock=Decimal("5"))
    session.add(product)
    session.commit()
    with pytest.raises(ValueError, match="tidak mencukupi"):
        create_sale(session, [
            {"product_id": product.id, "quantity": "3"},
            {"product_id": product.id, "quantity": "3"},
        ], Decimal("0"), Decimal("20000"), "CASH", "INV-001")
    assert session.query(Sale).count() == 0
    assert session.get(Product, product.id).stock == Decimal("5.000")
