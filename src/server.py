from fastapi import FastAPI, HTTPException, Path, Response

from src.model import Cart, InputItem
from src.processor import Processor

app = FastAPI()


@app.get('/api/v1/users/{user_id}/carts', response_model=Cart)
def get_shopping_cart(user_id: int = Path(None, title="User ID", gt=0)):
    try:
        return Processor().get_cart(user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="get cart failed")


@app.put('/api/v1/users/{user_id}/carts')
def put_shopping_cart(item: InputItem, user_id: int = Path(None, title="User ID", gt=0)):
    try:
        Processor().add_item(user_id, item.id, item.quantity)
        return Response(status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="put cart failed")


@app.post('/api/v1/users/{user_id}/cart/checkout', status_code=201)
def checkout_cart(user_id: int = Path(None, title="User ID", gt=0)):
    try:
        return {"orderId": Processor().checkout(user_id)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="create order failed")
