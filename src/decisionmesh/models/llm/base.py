from abc import ABC, abstractmethod


class ModelRunner(ABC):
    """Interface for models that can execute an AI task."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the model identifier."""
        raise NotImplementedError
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response for the given prompt."""
        raise NotImplementedError