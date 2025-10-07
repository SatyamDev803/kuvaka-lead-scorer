from fastapi import APIRouter

from app.api.endpoints import leads

api_router = APIRouter()

api_router.include_router(leads.router, tags=["Leads & Offers"])