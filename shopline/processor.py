from shopline.database.dao import Dao
from shopline.model import Cart


class Processor():
    def __init__(self):
        self.dao = Dao()

    def get_cart(self, user_id):
        items = self.dao.get_cart_items(user_id)
        total = sum(map(lambda item: item.quantity*item.price, items))
        return Cart(total_price=total, items=items)

    def add_item(self, user_id, product_id, quantity) -> None:
        self.check_user_exist(user_id)
        product = self.dao.get_product(product_id)
        if not product:
            raise ValueError(f'product {product_id} not exist')
        self.dao.upsert_cart_item(user_id, product_id, quantity)

    def get_order(self, user_id):
        pass

    def checkout(self, user_id):
        self.check_user_exist(user_id)
        items = self.dao.get_cart_items(user_id)
        product_ids = list(map(lambda item: item.id, items))
        if not product_ids:
            raise ValueError('no items to checkout')
        id_to_product = {p.id: p for p in self.dao.get_products(product_ids)}
        for item in items:
            if item.id not in id_to_product or item.quantity > id_to_product[item.id].inventory:
                raise ValueError(f'product {item.name} is out of stock')
            else:
                id_to_product[item.id].inventory -= item.quantity
        order_id = self.dao.create_order(user_id, items)
        self.dao.delete_cart(user_id)
        self.dao.update_products(id_to_product.values())
        return order_id

    def check_user_exist(self, user_id):
        user = self.dao.get_user(user_id)
        if not user:
            raise ValueError(f'user {user_id} not found')
