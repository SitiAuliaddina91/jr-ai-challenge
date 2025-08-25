from app.db_setup import SessionMaker, init_db
from app.models import UserData, Produk, OrderData

init_db()
db = SessionMaker()

if not db.query(UserData).first():
    db.add(UserData(id=1, name="Budi", email="budi@example.com"))

if not db.query(Produk).first():
    db.add(Produk(id=1, sku="SKU-001", nama="Kopi Arabika", deskripsi="Biji kopi 250g, medium roast"))

if not db.query(OrderData).filter_by(order_number="ORD001").first():
    db.add(OrderData(order_number="ORD001", user_id=1, produk_id=1, status="Diproses"))

db.commit()
print("seed ok")