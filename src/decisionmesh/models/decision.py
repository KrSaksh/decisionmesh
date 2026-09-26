from enum import Enum

from pydantic import BaseModel, Field


class Strategy(str, Enum):
    CHEAP_MODEL = "cheap_model"
    STRONG_MODEL = "strong_model"
    TOOL = "tool"
    ESCALATE = "escalate"

class Decision(BaseModel):
    strategy: Strategy
    model: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    estimated_cost: float = Field(ge=0.0)
    reason: str = Field(min_length=1)
