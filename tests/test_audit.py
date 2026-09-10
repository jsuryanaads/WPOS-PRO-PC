from decimal import Decimal
from app.models import Product, Sale
from app.services.auth import hash_password, verify_password

def test_password_hashing():
    h = hash_password("secret")
    assert verify_password("secret", h)
    assert not verify_password("wrong", h)

def test_models():
    assert Product.__tablename__ == "products"
    assert Sale.__tablename__ == "sales"

def test_money_math():
    assert Decimal("10.00") * Decimal("2") == Decimal("20.00")
