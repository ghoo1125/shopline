from typing import List

from src.database.model import CartItem, LineItem, Order, Product, User
from src.database.mysql_client import MysqlClient
from src.model import CartItem as CoreCartItem
from src.model import Product as CoreProduct
from src.model import User as CoreUser


class Dao():
    def __init__(self):
        self.client = MysqlClient.get_instance()

    def get_user(self, user_id):
        user = self.client.get(User, user_id)
        return CoreUser(id=user.id, name=user.name, email=user.email, address=user.address) if user else None

    def get_product(self, product_id) -> CoreProduct:
        product = self.client.get(Product, product_id)
        return CoreProduct(id=product.id, name=product.name, price=product.price, inventory=product.inventory) if product else None

    def get_products(self, product_ids) -> List[Product]:
        return [CoreProduct(id=p.id, name=p.name, price=p.price, inventory=p.inventory) for p in self.client.query(Product).filter(Product.id.in_(product_ids)).all()]

    def update_products(self, products):
        id_to_product = {p.id: p for p in products}
        existing_products = self.client.query(Product).filter(
            Product.id.in_(id_to_product.keys())).all()
        for p in existing_products:
            p.inventory = id_to_product[p.id].inventory
        self.client.commit()

    def get_cart_items(self, user_id) -> List[CoreCartItem]:
        result = self.client.query(CartItem, Product).filter(
            CartItem.cartId == user_id).filter(CartItem.productId == Product.id).all()
        return [CoreCartItem(id=product.id, name=product.name, price=product.price, quantity=item.quantity) for item, product in result]

    def upsert_cart_item(self, user_id, product_id, quantity):
        item = self.client.query(CartItem).filter(CartItem.cartId == user_id).filter(
            CartItem.productId == product_id).first()
        if item:
            item.quantity = quantity
            self.client.commit()
        else:
            self.client.add(
                CartItem(cartId=user_id, productId=product_id, quantity=quantity))

    def delete_cart(self, user_id):
        self.client.query(CartItem).filter(CartItem.cartId == user_id).delete()
        self.client.commit()

    def get_order(self, user_id):
        self.client.query(Order)

    def create_order(self, user_id, items) -> int:
        # TODO should apply transaction to prevent race condition
        order = Order(userId=user_id)
        self.client.add(order)
        self.client.commit()
        line_items = [LineItem(
            orderId=order.id, productId=item.id, quantity=item.quantity) for item in items]
        self.client.add_all(line_items)
        return order.id
