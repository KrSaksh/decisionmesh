import pytest

from decisionmesh.models import Decision, Strategy
from decisionmesh.policy import ConfidencePolicy


def make_decision(confidence: float) -> Decision:
    return Decision(
        strategy=Strategy.CHEAP_MODEL,
        model="cheap-model",
        confidence=confidence,
        estimated_cost=0.001,
        reason="Test decision.",
    )


def test_accepts_decision_above_threshold():
    policy = ConfidencePolicy(threshold=0.75)
    
    decision = make_decision(0.85)
    
    assert policy.accepts(decision) is True


def test_accepts_decision_at_threshold():
    policy = ConfidencePolicy(threshold=0.75)
    
    decision = make_decision(0.75)
    
    assert policy.accepts(decision) is True


def test_rejects_decision_below_threshold():
    policy = ConfidencePolicy(threshold=0.75)
    
    decision = make_decision(0.70)
    
    assert policy.accepts(decision) is False


def test_rejects_decision_invalid_threshold_above_one():
    with pytest.raises(ValueError):
        ConfidencePolicy(threshold=1.1)


def test_rejects_decision_invalid_threshold_below_zero():
    with pytest.raises(ValueError):
        ConfidencePolicy(threshold=-0.1)