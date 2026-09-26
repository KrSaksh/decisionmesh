from enum import Enum

from pydantic import BaseModel, Field


class TaskType(str, Enum):
    GENERAL = "general"
    MATH = "math"
    CODE = "code"
    CLASSIFICATION = "classification"
    EXTRACTION = "extraction"

class Task(BaseModel):
    id: str = Field(min_length=1)
    input: str = Field(min_length=1)
    task_type: TaskType = TaskType.GENERAL
    complexity: float = Field(default=0.5, ge=0.0, le=1.0)