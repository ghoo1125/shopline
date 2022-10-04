from shopline.database.dao import Dao
from shopline.model import Cart

class Processor():
    def __init__(self):
        self.dao = Dao()

    def get_user(self, user_id):
        return self.dao.get_user(user_id)

    def get_cart(self, user_id):
        items = self.dao.get_cart_items(user_id)
        total = sum(map(lambda item: item.quantity*item.price, items))
        return Cart(total_price=total, items=items)

    def add_item(self, user_id, product_id, quantity) -> None:
        product = self.dao.get_product(product_id)
        if not product:
            raise ValueError(f'product {product_id} not exist')
        self.dao.upsert_cart_item(user_id, product_id, quantity)
    
    def checkout(self, user_id):
        pass


proc = Processor()
print(vars(proc.get_user(2)))
print("init:", proc.get_cart(2))
proc.add_item(user_id=1, product_id=111, quantity=3)
print(proc.get_cart(1))
proc.add_item(user_id=1, product_id=111, quantity=4)
print(proc.get_cart(1))
