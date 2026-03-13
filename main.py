from fastapi import FastAPI

from app.routers import (
    Delivery,
    MenuItem,
    Notfication,
    Order,
    OrderItem,
    Payment,
    Restaurant,
    Review,
    User,
    auth,
)

app = FastAPI(title="QuickBite", version="0.1.0")
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(Review.router)
app.include_router(Notfication.router)
app.include_router(MenuItem.router)
app.include_router(User.router)
app.include_router(Order.router)
app.include_router(OrderItem.router)
app.include_router(Delivery.router)
app.include_router(Delivery.router)
app.include_router(Restaurant.router)
app.include_router(Payment.router)


@app.get("/health")
def health():
    return {"status": "ok"}
