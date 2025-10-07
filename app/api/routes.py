from fastapi import APIRouter

from app.api.endpoints import leads

# Create the main router instance
api_router = APIRouter()

# Include the router from the leads endpoint module
api_router.include_router(leads.router, tags=["Leads & Offers"])