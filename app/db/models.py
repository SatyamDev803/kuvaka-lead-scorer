from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
from .base import Base

class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    value_props = Column(ARRAY(String))
    ideal_use_cases = Column(ARRAY(String))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Lead(Base):
    __tablename__ = "Leads"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)
    company = Column(String)
    industry = Column(String)
    location = Column(String)
    linkedin_bio = Column(String)

    is_scored = Column(Boolean, default=False)
    score = Column(Integer, nullable=True)
    intent = Column(String, nullable=True)
    reasoning = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())