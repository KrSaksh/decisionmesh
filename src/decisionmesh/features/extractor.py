from pydantic import BaseModel, Field

from decisionmesh.models import Task, TaskType


class TaskFeatures(BaseModel):
    """Deterministic features extracted from a task."""
    
    input_length: int = Field(ge=1)
    word_count: int = Field(ge=1)
    has_math_expression: bool
    has_code_indicators: bool
    estimated_complexity: float = Field(ge=0.0, le=1.0)


class FeatureExtractor:
    """Extract deterministic routing features from a task."""
    
    def extract(self, task: Task) -> TaskFeatures:
        """Convert task information into routing features."""
        text = task.input.strip()
        words = text.split()
        lower_text = text.lower()
        
        has_math_expression = (
            task.task_type == TaskType.MATH
            or any(operator in text for operator in ("+", "-", "*", "/", "%", "^"))
        )
        
        code_indicators = (
            "def" in lower_text
            or "class" in lower_text
            or "import" in lower_text
            or"```" in text
            or "function" in lower_text
        )
        
        estimated_complexity = self._estimate_complexity(
            task=task,
            input_length=len(text),
            word_count=len(words),
            has_code_indicators=code_indicators,
        )
        
        return TaskFeatures(
            input_length=len(text),
            word_count=len(words),
            has_math_expression=has_math_expression,
            has_code_indicators=code_indicators,
            estimated_complexity=estimated_complexity,
        )
    
    def _estimate_complexity(
        self,
        task: Task,
        input_length: int,
        word_count: int,
        has_code_indicators: bool,
    ) -> float:
        """Estimate complexity using explicit deterministic signals."""
        if task.task_type == TaskType.MATH:
            return 0.1
        
        if has_code_indicators:
            return 0.8
        
        if word_count <= 5:
            return 0.2
        
        if input_length <= 80:
            return 0.4
        
        return 0.7
        