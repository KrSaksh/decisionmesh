from pydantic import BaseModel, Field


class ExecutionResult(BaseModel):
    success: bool
    output: str | None = None
    latency_ms: float = Field(ge=0.0)
    actual_cost: float = Field(ge=0.0)
    error: str | None = None
