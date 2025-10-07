import google.generativeai as genai
import json
from typing import Dict, Any

from app.db import models
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')


# Calculate the score based on predefined rule
def calculate_rule_score(lead: models.Lead) -> int:
    score = 0
    
    # Rule 1 Role relevance max 20
    role = lead.role.lower()
    if any(keyword in role for keyword in ['head', 'vp', 'director', 'manager', 'founder', 'c-level', 'cxo']):
        score += 20
    elif any(keyword in role for keyword in ['senior', 'lead', 'principal', 'architect']):
        score += 10
        
    # Rule 2 Industry match max 20
    industry = lead.industry.lower()
    if 'saas' in industry or 'software' in industry:
        score += 20
    elif any(keyword in industry for keyword in ['tech', 'it', 'b2b']):
        score += 10

    # Rule 3 Data completeness max 10
    if all([lead.name, lead.role, lead.company, lead.industry, lead.linkedin_bio]):
        score += 10
        
    return score


# Gets a score, intent, and reasoning from the Gemini AI model
async def get_ai_score_and_reasoning(lead: models.Lead, offer: models.Offer) -> Dict[str, Any]:
    prompt = f"""
    You are an expert B2B sales development representative. Given the product offer and prospect information, classify the prospect's buying intent as High, Medium, or Low. Then, provide a concise, one-sentence explanation for your classification.

    **Product Offer:**
    - Name: {offer.name}
    - Value Propositions: {', '.join(offer.value_props)}
    - Ideal Use Cases: {', '.join(offer.ideal_use_cases)}

    **Prospect Information:**
    - Role: {lead.role} at {lead.company}
    - Industry: {lead.industry}
    - LinkedIn Bio: {lead.linkedin_bio}

    Return your response ONLY in a valid JSON format with the keys "intent" and "reasoning".
    """
    
    try:
        generation_config = genai.types.GenerationConfig(response_mime_type="application/json")
        
        response = await model.generate_content_async(
            prompt,
            generation_config=generation_config
        )
        
        result = json.loads(response.text)
        
        # Map the text-based intent to a numerical score
        intent_map = {"High": 50, "Medium": 30, "Low": 10}
        result['score'] = intent_map.get(result.get('intent'), 0)
        
        return result
    except Exception as e:
        print(f"Error during AI scoring: {e}")
        return {"intent": "Low", "reasoning": "AI analysis failed.", "score": 10}