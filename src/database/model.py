from sqlalchemy import FLOAT, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False)
    address = Column(String(64), nullable=False)


class Product(Base):
    __tablename__ = "Product"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    price = Column(FLOAT(precision=2), nullable=False)
    inventory = Column(Integer, nullable=False)


class CartItem(Base):
    __tablename__ = "CartItem"
    id = Column(Integer, primary_key=True)
    cartId = Column(Integer, ForeignKey("User.id"))
    productId = Column(Integer, ForeignKey("Product.id"))
    quantity = Column(Integer, nullable=False)


class Order(Base):
    __tablename__ = "Order"
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey("User.id"))


class LineItem(Base):
    __tablename__ = "LineItem"
    id = Column(Integer, primary_key=True)
    orderId = Column(Integer, ForeignKey("Order.id"))
    productId = Column(Integer, ForeignKey("Product.id"))
    quantity = Column(Integer, nullable=False)
