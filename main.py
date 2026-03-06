from fastapi import FastAPI

from app.routers import Review

app = FastAPI(title="QuickBite", version="0.1.0")
app.include_router(Review.router)


@app.get("/health")
def health():
    return {"status": "ok"}
