from fastapi import FastAPI

from app.database import Base, engine
from app.routers import expenses, finances

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Tracker API")

app.include_router(expenses.router)
app.include_router(finances.router)


@app.get("/")
def root():
    return {"message": "Finance Tracker API", "docs": "/docs"}
