from typing import List

from shopline.database.model import CartItem, Product, User
from shopline.database.mysql_client import MysqlClient
from shopline.model import CartItem as CoreCartItem


class Dao():
    def __init__(self):
        self.client = MysqlClient.get_instance()

    def get_user(self, user_id):
        return self.client.get(User, user_id)

    def get_product(self, product_id) -> Product:
        return self.client.get(Product, product_id)

    def get_cart_items(self, user_id) -> List[CoreCartItem]:
        result = self.client.query(CartItem, Product).filter(
            CartItem.cartId == user_id).filter(CartItem.productId == Product.id).all()
        return [CoreCartItem(name=product.name, price=product.price, quantity=item.quantity) for item, product in result]

    def upsert_cart_item(self, user_id, product_id, quantity):
        item = self.client.query(CartItem).filter(CartItem.cartId == user_id).filter(CartItem.productId == product_id).first()
        if item:
            item.quantity = quantity
            self.client.commit()
        else:
            self.client.add(CartItem(cartId=user_id, productId=product_id, quantity=quantity))
