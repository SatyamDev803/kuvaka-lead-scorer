import pytest
from app.db import models
from app.services.scoring_service import calculate_rule_score

@pytest.fixture
def decision_maker_lead():
    return models.Lead(
        name="Ava Patel", role="Head of Growth", company="FlowMetrics",
        industry="B2B SaaS", location="New York", linkedin_bio="Bio here"
    )

@pytest.fixture
def influencer_lead():
    return models.Lead(
        name="Ben Carter", role="Senior Marketing Manager", company="DataCorp",
        industry="Fintech", location="London", linkedin_bio="Bio here"
    )

@pytest.fixture
def incomplete_lead():
    return models.Lead(
        name="Charlie Day", role="Analyst", company="Incomplete Inc.",
        industry="Retail", location="", linkedin_bio=""
    )

def test_decision_maker_score(decision_maker_lead):
    assert calculate_rule_score(decision_maker_lead) == 50

def test_influencer_score(influencer_lead):
    assert calculate_rule_score(influencer_lead) == 40

def test_incomplete_data_score(incomplete_lead):
    lead_with_complete_data = models.Lead(
        name="Charlie Day", role="Analyst", company="Incomplete Inc.",
        industry="Retail", location="Philly", linkedin_bio="Bio"
    )
    assert calculate_rule_score(incomplete_lead) == 0
    assert calculate_rule_score(lead_with_complete_data) == 10