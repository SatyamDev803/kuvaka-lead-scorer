from pydantic import BaseModel
from typing import List
from datetime import datetime

class OfferBase(BaseModel):
    name: str
    value_props: List[str]
    ideal_use_cases: List[str]

class OfferCreate(OfferBase):
    pass

class Offer(OfferBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True