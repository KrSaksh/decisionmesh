from decisionmesh.models import Decision, Strategy


class FallbackPolicy:
    """Escalate uncertain decisions to a safer execution strategy."""
    
    def apply(self, decision: Decision) -> Decision:
        """Return a safer decision when the original decision is uncertain."""
        if decision.strategy == Strategy.CHEAP_MODEL:
            return Decision(
                strategy=Strategy.STRONG_MODEL,
                model="strong-model",
                confidence=decision.confidence,
                estimated_cost=0.01,
                reason=f"Fallback from cheap model: {decision.reason}",
            )
        
        return decision
    