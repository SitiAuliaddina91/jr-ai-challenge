from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db_setup import Base

class UserData(Base):
    __tablename__ = "user_data"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

class Produk(Base):
    __tablename__ = "produk"
    id = Column(Integer, primary_key=True)
    sku = Column(String, unique=True)
    nama = Column(String)
    deskripsi = Column(Text)

class OrderData(Base):
    __tablename__ = "order_data"
    id = Column(Integer, primary_key=True)
    order_number = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("user_data.id"))
    produk_id = Column(Integer, ForeignKey("produk.id"))
    status = Column(String)
    created_at = Column(DateTime, default=func.now())

class SessionChat(Base):
    __tablename__ = "session_chat"
    id = Column(Integer, primary_key=True)
    session_id = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("user_data.id"))
    created_at = Column(DateTime, default=func.now())
    pesan = relationship("MsgLog", back_populates="session", cascade="all, delete")

class MsgLog(Base):
    __tablename__ = "msg_log"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("session_chat.id"))
    role = Column(String)   # 'user' | 'assistant'
    content = Column(Text)
    created_at = Column(DateTime, default=func.now())
    session = relationship("SessionChat", back_populates="pesan")