from fastapi import FastAPI
from app.routers import Order
from app.routers import OrderItem
from app.routers import Delivery

from app.routers import MenuItem

app = FastAPI(title="QuickBite", version="0.1.0")

app.include_router(MenuItem.router)

app.include_router(OrderItem.router)
app.include_router(Delivery.router)
app.include_router(Delivery.router)

@app.get("/health")
def health():
    return {"status": "ok"}
