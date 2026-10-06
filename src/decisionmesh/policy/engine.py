from decisionmesh.models import Decision
from decisionmesh.policy.confidence import ConfidencePolicy
from decisionmesh.policy.fallback import FallbackPolicy


class PolicyEngine:
    """Coordinate confidence checking and fallback decisions."""
    
    def __init__(
        self,
        confidence_policy: ConfidencePolicy,
        fallback_policy: FallbackPolicy,
    ) -> None:
        self.confidence_policy = confidence_policy
        self.fallback_policy = fallback_policy
    
    def apply(self, decision: Decision) -> Decision:
        """Return the decision that should ultimately be executed."""
        if self.confidence_policy.accepts(decision):
            return decision
        
        return self.fallback_policy.apply(decision)