from fastapi import FastAPI
from app.api import routes

# Initialize the main FastAPI application instance
app = FastAPI(title="Kuvaka Lead Scoring API")

# Include all the API routes defined in the routes module
app.include_router(routes.api_router)

@app.get("/", tags=["Root"])
async def read_root():
    # Root endpoint for the API
    return {"message": "Welcome to the Lead Scoring API"}