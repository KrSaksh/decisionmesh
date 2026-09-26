import pytest
from pydantic import ValidationError

from decisionmesh.models import (
    Decision,
    ExecutionResult,
    Strategy,
    Task,
    TaskType,
)


def test_task_defaults():
    task = Task(
        id="task-001",
        input="Calculate 2 + 2",
    )
    
    assert task.task_type == TaskType.GENERAL
    assert task.complexity == 0.5
    

def test_task_accepts_valid_values():
    task = Task(
        id="task-002",
        input="Classify this text",
        task_type=TaskType.CLASSIFICATION,
        complexity=0.8,
    )
    
    assert task.task_type == TaskType.CLASSIFICATION
    assert task.complexity == 0.8


def test_task_rejects_invalid_complexity():
    with pytest.raises(ValidationError):
        Task(
            id="task-003",
            input="Invalid task",
            complexity=1.5,
        )


def test_decision():
    decision = Decision(
        strategy=Strategy.CHEAP_MODEL,
        model="cheap-model",
        confidence=0.92,
        estimated_cost=0.001,
        reason="Low complexity task",
    )
    
    assert decision.strategy == Strategy.CHEAP_MODEL
    assert decision.model == "cheap-model"
    assert decision.confidence == 0.92


def test_execution_result_success():
    result = ExecutionResult(
        success=True,
        output="42",
        latency_ms=35.5,
        actual_cost=0.0005,
    )
    
    assert result.success is True
    assert result.output == "42"
    assert result.error is None


def test_execution_result_failure():
    result = ExecutionResult(
        success=False,
        latency_ms=100.0,
        actual_cost=0.0,
        error="Execution failed",
    )
    
    assert result.success is False
    assert result.output is None
    assert result.error == "Execution failed"
