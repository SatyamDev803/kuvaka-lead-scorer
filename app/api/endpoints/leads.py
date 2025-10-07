# Endpoints for creating offers, uploading leads via CSV, triggering the scoring process, and retrieving the results

import csv
import io
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import models
from app.db.base import get_db
from app.schemas import offer as offer_schema
from app.schemas import lead as lead_schema
from app.services import scoring_service

router = APIRouter()


# API endpoint for creating a new offer in the database
@router.post("/offer", response_model=offer_schema.Offer, status_code=201)
async def create_offer(
    offer: offer_schema.OfferCreate,
    db: AsyncSession = Depends(get_db)
):
    db_offer = models.Offer(**offer.model_dump())
    db.add(db_offer)
    await db.commit()
    await db.refresh(db_offer)

    # Return created offer object
    return db_offer


# API endppoint for uploading a CSV file of leads and saves them to the database
@router.post("/leads/upload", status_code=200)
async def upload_leads_csv(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")
    
    try:
        # Read and decode the uploaded file asynchronously
        contents = await file.read()
        buffer = io.StringIO(contents.decode('utf-8'))
        csv_reader = csv.DictReader(buffer)

        leads_to_create = []
        for row in csv_reader:
            # Validate each row using the Pydantic schema
            lead_data = lead_schema.LeadCreate(**row)
            leads_to_create.append(models.Lead(**lead_data.model_dump()))

        # Add all new leads to the session and commit in a single transaction
        db.add_all(leads_to_create)
        await db.commit()

        return {"message": f"Successfully uploaded and saved {len(leads_to_create)} leads."}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

# API endpoint for retrieving all the leads from the database
@router.get("/results", response_model=List[lead_schema.Lead])
async def get_results(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Lead))
    leads = result.scalars().all()

    # Returns a list of all lead objects.
    return leads


# API endpoint for triggering the scoring process for all unscored leads
@router.post("/score", status_code=200)
async def score_leads(db: AsyncSession = Depends(get_db)):
    # Fetch the most recent offer to use as context for scoring
    offer_result = await db.execute(select(models.Offer).order_by(models.Offer.created_at.desc()))
    latest_offer = offer_result.scalars().first()
    if not latest_offer:
        raise HTTPException(status_code=404, detail="No offer found. Please create an offer first.")

    # Fetch all leads that have not been scored yet
    leads_result = await db.execute(select(models.Lead).where(models.Lead.is_scored == False))
    unscored_leads = leads_result.scalars().all()

    if not unscored_leads:
        return {"message": "No new leads to score."}

    # Iterate through each unscored lead and apply the scoring logic
    for lead in unscored_leads:
        rule_score = scoring_service.calculate_rule_score(lead)
        ai_result = await scoring_service.get_ai_score_and_reasoning(lead, latest_offer)
        
        # Update the lead object with the results
        lead.score = rule_score + ai_result['score']
        lead.intent = ai_result['intent']
        lead.reasoning = ai_result['reasoning']
        lead.is_scored = True

    # Commit all the updated leads to the database
    await db.commit()
    
    return {"message": f"Successfully scored {len(unscored_leads)} leads."}