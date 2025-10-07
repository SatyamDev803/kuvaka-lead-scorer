from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LeadBase(BaseModel):
    name: str
    role: str
    company: str
    industry: str
    location: str
    linkedin_bio: str

class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    intent: Optional[str] = None
    score: Optional[int] = None
    reasoning: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True