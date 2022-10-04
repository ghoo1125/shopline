from fastapi import FastAPI, HTTPException, Path

from shopline.model import Cart, InputItem
from shopline.processor import Processor

app = FastAPI()


@app.get('/api/v1/users/{user_id}/carts', response_model=Cart)
def get_shopping_cart(user_id: int = Path(None, title="User ID", gt=0)):
    try:
        return Processor().get_cart(user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="get cart failed")


@app.post('/api/v1/users/{user_id}/carts', status_code=204)
def put_shopping_cart(item: InputItem, user_id: int = Path(None, title="User ID", gt=0)):
    try:
        Processor().add_item(user_id, item.id, item.quantity)
    except ValueError:
        raise HTTPException(status_code=400, detail="product not found")
    except Exception:
        raise HTTPException(status_code=500, detail="put cart failed")


@app.get('api/v1/users/{user_id}/orders')
def checkout_cart(user_id: int = Path(None, title="User ID", gt=0)):
    return "get orders"


@app.post('api/v1/users/{user_id}/cart/checkout')
def checkout_cart(user_id: int = Path(None, title="User ID", gt=0)):
    return "checkout and create order"
