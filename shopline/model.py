from decimal import Decimal
from typing import List

from pydantic import BaseModel


class InputItem(BaseModel):
    id: int
    quantity: int


class CartItem(BaseModel):
    name: str
    price: Decimal
    quantity: int


class Cart(BaseModel):
    items: List[CartItem]
    total_price: Decimal
