from pydantic import BaseModel, Field

from decisionmesh.features import TaskFeatures
from decisionmesh.models import Strategy, TaskType


class IntegrationResult(BaseModel):
    """Capture routing, extracted features, and execution for one task."""

    task_id: str = Field(min_length=1)
    task_type: TaskType
    input: str = Field(min_length=1)

    features: TaskFeatures

    initial_strategy: Strategy
    final_strategy: Strategy
    confidence: float = Field(ge=0.0, le=1.0)

    success: bool
    output: str | None = None
    latency_ms: float = Field(ge=0.0)
    estimated_cost: float = Field(ge=0.0)
    actual_cost: float = Field(ge=0.0)
    error: str | None = None