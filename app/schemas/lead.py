from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base schema with common lead attributes
class LeadBase(BaseModel):
    name: str
    role: str
    company: str
    industry: str
    location: str
    linkedin_bio: str

# Schema used for creating a new lead
class LeadCreate(LeadBase):
    pass

# Schema for returning a lead in API responses
class Lead(LeadBase):
    id: int
    intent: Optional[str] = None
    score: Optional[int] = None
    reasoning: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True