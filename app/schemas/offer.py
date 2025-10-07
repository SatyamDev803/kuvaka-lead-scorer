from pydantic import BaseModel
from typing import List
from datetime import datetime

# Base schema with common offer attributes
class OfferBase(BaseModel):
    name: str
    value_props: List[str]
    ideal_use_cases: List[str]

# Schema used for creating a new offer via the API
class OfferCreate(OfferBase):
    pass

# Schema for returning an offer in API responses
class Offer(OfferBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True