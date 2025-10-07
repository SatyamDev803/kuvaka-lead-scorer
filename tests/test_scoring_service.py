import pytest
from app.db import models
from app.services.scoring_service import calculate_rule_score

# Provides a mock Lead object representing a perfect decision-maker
@pytest.fixture
def decision_maker_lead():
    return models.Lead(
        name="Ava Patel", role="Head of Growth", company="FlowMetrics",
        industry="B2B SaaS", location="New York", linkedin_bio="Bio here"
    )

# Provides a mock Lead object representing an influencer role
@pytest.fixture
def influencer_lead():
    return models.Lead(
        name="Ben Carter", role="Senior Marketing Manager", company="DataCorp",
        industry="Fintech", location="London", linkedin_bio="Bio here"
    )

# Provides a mock Lead object with missing data
@pytest.fixture
def incomplete_lead():
    return models.Lead(
        name="Charlie Day", role="Analyst", company="Incomplete Inc.",
        industry="Retail", location="", linkedin_bio=""
    )

# Tests a perfect lead: decision maker, exact industry, complete data
def test_decision_maker_score(decision_maker_lead):
    assert calculate_rule_score(decision_maker_lead) == 50

# Tests a lead whose role matches a decision-maker keyword ('manager')
def test_influencer_score(influencer_lead):
    assert calculate_rule_score(influencer_lead) == 40

# Tests leads with incomplete vs. complete data to verify the completeness rule
def test_incomplete_data_score(incomplete_lead):
    # Create a version of the lead with complete data for comparison
    lead_with_complete_data = models.Lead(
        name="Charlie Day", role="Analyst", company="Incomplete Inc.",
        industry="Retail", location="Philly", linkedin_bio="Bio"
    )

    # The incomplete lead should score 0 for completeness
    assert calculate_rule_score(incomplete_lead) == 0
    # The complete lead should score 10 for completeness
    assert calculate_rule_score(lead_with_complete_data) == 10