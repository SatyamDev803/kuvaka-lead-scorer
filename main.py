from fastapi import FastAPI
from app.api import routes

app = FastAPI(title="Kuvaka Lead Scoring API")

app.include_router(routes.api_router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Lead Scoring API"}