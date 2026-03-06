from fastapi import FastAPI


from app.routers import Payment
app = FastAPI(title="QuickBite", version="0.1.0")


app.include_router(Payment.router)

@app.get("/health")
def health():
    return {"status": "ok"}
