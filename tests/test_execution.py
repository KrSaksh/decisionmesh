import pytest

from decisionmesh.execution import Executor
from decisionmesh.models import Decision, Strategy, Task, TaskType
from decisionmesh.models.llm import CheapModel, ModelRunner, StrongModel
from decisionmesh.tools import Calculator


class FailingModel(ModelRunner):
    @property
    def name(self) -> str:
        return "failing-model"
    
    def generate(self, prompt: str) -> str:
        raise RuntimeError("Model execution failed.")
    
@pytest.fixture
def executor() -> Executor:
    return Executor(
        cheap_model=CheapModel(),
        strong_model=StrongModel(),
        calculator=Calculator(),
    )


def test_execute_cheap_model(executor: Executor):
    task = Task(
        id="task-1",
        input="Hello",
        task_type=TaskType.GENERAL,
        complexity=0.2,
    )
    decision = Decision(
        strategy=Strategy.CHEAP_MODEL,
        model="cheap-model",
        confidence=0.9,
        estimated_cost=0.001,
        reason="Low complexity.",
    )
    
    result = executor.execute(task, decision)
    
    assert result.success is True
    assert result.output == "Mock response to: Hello"
    assert result.latency_ms >= 0
    assert result.actual_cost == pytest.approx(0.001)
    assert result.error is None


def test_execute_strong_model(executor: Executor):
    task = Task(
        id="task-2",
        input="Solve this problem",
        task_type=TaskType.GENERAL,
        complexity=0.8,
    )
    decision = Decision(
        strategy=Strategy.STRONG_MODEL,
        model="strong-model",
        confidence=0.8,
        estimated_cost=0.01,
        reason="Higher complexity.",
    )
    
    result = executor.execute(task, decision)
    
    assert result.success is True
    assert result.output == "Mock response to: Solve this problem"
    assert result.latency_ms >= 0
    assert result.actual_cost == pytest.approx(0.01)
    assert result.error is None
    
def test_execute_calculator(executor: Executor):
    task = Task(
        id="task-3",
        input="10 + 5 * 2",
        task_type=TaskType.MATH,
        complexity=0.1,
    )
    decision = Decision(
        strategy=Strategy.TOOL,
        model=None,
        confidence=0.99,
        estimated_cost=0.0,
        reason="Math task.",
    )
    
    result = executor.execute(task, decision)
    
    assert result.success is True
    assert result.output == "20.0"
    assert result.latency_ms >= 0
    assert result.actual_cost == pytest.approx(0.0)
    assert result.error is None
    

def test_execute_calculator_failure(executor: Executor):
    task = Task(
        id="task-4",
        input="10 / 0",
        task_type=TaskType.MATH,
        complexity=0.1,
    )
    decision = Decision(
        strategy=Strategy.TOOL,
        model=None,
        confidence=0.99,
        estimated_cost=0.0,
        reason="Math task.",
    )
    
    result = executor.execute(task, decision)
    
    assert result.success is False
    assert result.output is None
    assert result.latency_ms >= 0
    assert result.actual_cost == pytest.approx(0.0)
    assert result.error == "Cannot divide by zero."


def test_execute_unsupported_strategy(executor: Executor):
    task = Task(
        id="task-5",
        input="test",
    )
    decision = Decision(
        strategy=Strategy.ESCALATE,
        model=None,
        confidence=0.5,
        estimated_cost=0.0,
        reason="Requires escalation.",
    )
    
    result = executor.execute(task, decision)
    
    assert result.success is False
    assert result.output is None
    assert result.latency_ms >= 0
    assert result.actual_cost == pytest.approx(0.0)
    assert "Unsupported execution strategy" in result.error

def test_model_failure_returns_failed_execution_result():
    executor = Executor(
        cheap_model=FailingModel(),
        strong_model=StrongModel(),
        calculator=Calculator(),
    )
    
    task = Task(
        id="failure-test",
        input="Hello",
    )
    
    decision = Decision(
        strategy=Strategy.CHEAP_MODEL,
        model="failing-model",
        confidence=0.85,
        estimated_cost=0.001,
        reason="Test failure.",
    )
    
    result = executor.execute(task, decision)
    
    assert result.success is False
    assert result.output is None
    assert result.error == "Model execution failed."
    assert result.latency_ms >= 0
    
def test_unsupported_strategy_returns_failed_execution_result():
    executor = Executor(
        cheap_model=CheapModel(),
        strong_model=StrongModel(),
        calculator=Calculator(),
    )

    task = Task(
        id="unsupported-test",
        input="Hello",
    )

    decision = Decision(
        strategy=Strategy.ESCALATE,
        model=None,
        confidence=0.5,
        estimated_cost=0.0,
        reason="Unsupported execution strategy test.",
    )

    result = executor.execute(task, decision)

    assert result.success is False
    assert result.output is None
    assert result.error is not None