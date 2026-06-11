import enum

from sqlalchemy import BigInteger, Column, Enum, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class OrderStatus(enum.Enum):
    NEW = "NEW"
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=True)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    login_data = Column(String, nullable=True)
    password_data = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    product_name = Column(String)
    amount = Column(Float)
    status = Column(Enum(OrderStatus), default=OrderStatus.NEW)
