from decisionmesh.models import Decision, Strategy
from decisionmesh.policy import FallbackPolicy


def make_decision(strategy: Strategy) -> Decision:
    return Decision(
        strategy=strategy,
        model="cheap-model" if strategy == Strategy.CHEAP_MODEL else None,
        confidence=0.60,
        estimated_cost=0.001,
        reason="Low-confidence test decision.",
    )


def test_escalates_cheap_model_to_strong_model():
    policy = FallbackPolicy()
    
    decision = make_decision(Strategy.CHEAP_MODEL)
    
    fallback = policy.apply(decision)
    
    assert fallback.strategy == Strategy.STRONG_MODEL
    assert fallback.model == "strong-model"
    assert fallback.estimated_cost == 0.01


def test_keeps_strong_model_decision_unchanged():
    policy = FallbackPolicy()
    
    decision = make_decision(Strategy.STRONG_MODEL)
    
    fallback = policy.apply(decision)
    
    assert fallback == decision