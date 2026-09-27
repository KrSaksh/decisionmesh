from .base import ModelRunner


class MockModel(ModelRunner):
    """Deterministic model implementation for development and testing."""
    
    def __init__(self, model_name: str = "mock-model"):
        self._name = model_name
        
    @property
    def name(self) -> str:
        return self._name
    
    def generate(self, prompt: str) -> str:
        return f"Mock response to: {prompt}"