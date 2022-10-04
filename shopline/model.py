from decimal import Decimal
from typing import List

from pydantic import BaseModel


class InputItem(BaseModel):
    id: int
    quantity: int


class User(BaseModel):
    id: int
    name: str
    email: str
    address: str


class CartItem(BaseModel):
    id: int
    name: str
    price: Decimal
    quantity: int


class Cart(BaseModel):
    items: List[CartItem]
    total_price: Decimal


class Product(BaseModel):
    id: int
    name: str
    price: Decimal
    inventory: int
