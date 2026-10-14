from decisionmesh.decision import DecisionEngine
from decisionmesh.execution import Executor
from decisionmesh.features import FeatureExtractor
from decisionmesh.integration.result import IntegrationResult
from decisionmesh.models import Task
from decisionmesh.policy import PolicyEngine


class IntegrationRunner:
    """Run tasks through feature extraction, routing, policy, and execution."""

    def __init__(
        self,
        feature_extractor: FeatureExtractor,
        decision_engine: DecisionEngine,
        policy_engine: PolicyEngine,
        executor: Executor,
    ) -> None:
        self.feature_extractor = feature_extractor
        self.decision_engine = decision_engine
        self.policy_engine = policy_engine
        self.executor = executor

    def run(self, task: Task) -> IntegrationResult:
        features = self.feature_extractor.extract(task)

        initial_decision = self.decision_engine.decide(task)
        final_decision = self.policy_engine.apply(initial_decision)

        execution = self.executor.execute(task, final_decision)

        return IntegrationResult(
            task_id=task.id,
            task_type=task.task_type,
            input=task.input,
            features=features,
            initial_strategy=initial_decision.strategy,
            final_strategy=final_decision.strategy,
            confidence=initial_decision.confidence,
            success=execution.success,
            output=execution.output,
            latency_ms=execution.latency_ms,
            estimated_cost=final_decision.estimated_cost,
            actual_cost=execution.actual_cost,
            error=execution.error,
        )