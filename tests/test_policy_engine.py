from decisionmesh.models import Decision, Strategy
from decisionmesh.policy import ConfidencePolicy, FallbackPolicy, PolicyEngine


def make_decision(
    strategy: Strategy,
    confidence: float,
) -> Decision:
    model = None
    
    if strategy == Strategy.CHEAP_MODEL:
        model = "cheap-model"
    elif strategy == Strategy.STRONG_MODEL:
        model = "strong-model"
    
    return Decision(
        strategy=strategy,
        model=model,
        confidence=confidence,
        estimated_cost=0.001,
        reason="Policy engine test.",
    )


def test_accepts_high_confidence_decision():
    engine = PolicyEngine(
        confidence_policy=ConfidencePolicy(threshold=0.75),
        fallback_policy=FallbackPolicy(),
    )
    
    decision = make_decision(
        Strategy.CHEAP_MODEL,
        confidence=0.85,
    )
    
    result = engine.apply(decision)
    
    assert result == decision


def test_falls_back_when_confidence_is_low():
    engine = PolicyEngine(
        confidence_policy=ConfidencePolicy(threshold=0.75),
        fallback_policy=FallbackPolicy(),
    )
    
    decision = make_decision(
        Strategy.CHEAP_MODEL,
        confidence=0.60,
    )
    
    result = engine.apply(decision)
    
    assert result.strategy == Strategy.STRONG_MODEL
    assert result.model == "strong-model"


def test_tool_decision_is_preserced_when_confident():
    engine = PolicyEngine(
        confidence_policy=ConfidencePolicy(threshold=0.75),
        fallback_policy=FallbackPolicy(),
    )
    
    decision = make_decision(
        Strategy.TOOL,
        confidence=0.99,
    )
    
    result = engine.apply(decision)
    
    assert result == decision