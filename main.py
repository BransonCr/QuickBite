from fastapi import FastAPI


from app.routers import Restaurant
app = FastAPI(title="QuickBite", version="0.1.0")


app.include_router(Restuarant.router)

@app.get("/health")
def health():
    return {"status": "ok"}
