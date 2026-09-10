from decimal import Decimal
import pytest
from sqlalchemy import create_engine, inspect, event
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Product, Sale, SaleItem, StockMovement
from app.services.auth import hash_password, verify_password
from app.services.sales import create_sale
from app.services.stock import adjust_stock


def make_session():
    engine = create_engine("sqlite:///:memory:")
    @event.listens_for(engine, "connect")
    def enable_fk(dbapi_connection, connection_record):
        dbapi_connection.execute("PRAGMA foreign_keys=ON")
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


def test_sale_is_atomic_on_failure():
    session = make_session()
    product = Product(barcode="8990002", name="Gula", selling_price=Decimal("15000"), stock=Decimal("2"))
    session.add(product)
    session.commit()
    with pytest.raises(ValueError, match="Pembayaran kurang"):
        create_sale(session, [{"product_id": product.id, "quantity": "1"}], Decimal("0"), Decimal("1"), "CASH", "INV-002")
    assert session.query(Sale).count() == 0
    assert session.query(StockMovement).count() == 0
    assert session.get(Product, product.id).stock == Decimal("2.000")


def test_stock_adjustment_records_movement():
    session = make_session()
    product = Product(barcode="8990003", name="Minyak", selling_price=Decimal("18000"), stock=Decimal("10"))
    session.add(product)
    session.commit()
    adjust_stock(session, product.id, Decimal("-2"), "OPNAME", "SO-001")
    assert session.get(Product, product.id).stock == Decimal("8.000")
    movement = session.query(StockMovement).one()
    assert movement.quantity == Decimal("-2.000")
    assert movement.reference == "SO-001"
