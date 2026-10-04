from decisionmesh.models import Decision


class ConfidencePolicy:
    """Accept decisions that meet the configured confidence threshold."""
    
    def __init__(self, threshold: float = 0.75):
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("Confidence threshold must be between 0.0 and 1.0")
        
        self.threshold = threshold
        
    def accepts(self, decision: Decision) -> bool:
        """Return whether a decision meets the confidence threshold."""
        return decision.confidence >= self.threshold