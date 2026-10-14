
from decisionmesh.decision import DecisionEngine
from decisionmesh.execution import Executor
from decisionmesh.features import FeatureExtractor
from decisionmesh.integration import IntegrationRunner
from decisionmesh.models import Decision, Strategy, Task, TaskType
from decisionmesh.models.llm import CheapModel, StrongModel
from decisionmesh.policy import ConfidencePolicy, FallbackPolicy, PolicyEngine
from decisionmesh.router import DeterministicRouter
from decisionmesh.tools import Calculator


def make_runner(decision_engine=None) -> IntegrationRunner:
    if decision_engine is None:
        decision_engine = DecisionEngine(DeterministicRouter())

    return IntegrationRunner(
        feature_extractor=FeatureExtractor(),
        decision_engine=decision_engine,
        policy_engine=PolicyEngine(
            confidence_policy=ConfidencePolicy(threshold=0.75),
            fallback_policy=FallbackPolicy(),
        ),
        executor=Executor(
            cheap_model=CheapModel(),
            strong_model=StrongModel(),
            calculator=Calculator(),
        ),
    )


def test_math_task_runs_through_complete_pipeline():
    runner = make_runner()
    task = Task(
        id="integration-math",
        input="2 + 3 * 4",
        task_type=TaskType.MATH,
    )

    result = runner.run(task)

    assert result.task_id == "integration-math"
    assert result.features.has_math_expression is True
    assert result.initial_strategy == Strategy.TOOL
    assert result.final_strategy == Strategy.TOOL
    assert result.success is True
    assert result.output == "14.0"
    assert result.error is None


def test_easy_task_uses_cheap_model():
    runner = make_runner()
    task = Task(
        id="integration-easy",
        input="Hello",
        task_type=TaskType.GENERAL,
        complexity=0.2,
    )

    result = runner.run(task)

    assert result.initial_strategy == Strategy.CHEAP_MODEL
    assert result.final_strategy == Strategy.CHEAP_MODEL
    assert result.success is True
    assert result.output == "Mock response to: Hello"


def test_low_confidence_decision_falls_back_to_strong_model():
    class LowConfidenceDecisionEngine:
        def decide(self, task: Task) -> Decision:
            return Decision(
                strategy=Strategy.CHEAP_MODEL,
                model="cheap-model",
                confidence=0.60,
                estimated_cost=0.001,
                reason="Test decision deliberately below threshold.",
            )

    runner = make_runner(LowConfidenceDecisionEngine())
    task = Task(
        id="integration-fallback",
        input="Explain a distributed system.",
        task_type=TaskType.GENERAL,
        complexity=0.2,
    )

    result = runner.run(task)

    assert result.initial_strategy == Strategy.CHEAP_MODEL
    assert result.final_strategy == Strategy.STRONG_MODEL
    assert result.confidence == 0.60
    assert result.success is True
    assert result.output == (
        "Mock response to: Explain a distributed system."
    )
    assert result.estimated_cost == 0.01


def test_failed_calculation_is_recorded():
    runner = make_runner()
    task = Task(
        id="integration-math-failure",
        input="10 / 0",
        task_type=TaskType.MATH,
    )

    result = runner.run(task)

    assert result.final_strategy == Strategy.TOOL
    assert result.success is False
    assert result.output is None
    assert result.error == "Cannot divide by zero."
    assert result.latency_ms >= 0
