from .mock import MockModel


class StrongModel(MockModel):
    """Development adapter representing a high-capability model."""
    
    def __init__(self):
        super().__init__(model_name="strong-model")