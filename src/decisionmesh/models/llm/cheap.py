from .mock import MockModel


class CheapModel(MockModel):
    """Development adapter representing a low-cost model."""
    
    def __init__(self):
        super().__init__(model_name="cheap-model")