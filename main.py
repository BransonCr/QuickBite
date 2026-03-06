from fastapi import FastAPI
from app.routers import Order
app = FastAPI(title="QuickBite", version="0.1.0")

app.include_router(Order.router)

@app.get("/health")
def health():
    return {"status": "ok"}
