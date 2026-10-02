import time

from decisionmesh.models import Decision, ExecutionResult, Strategy, Task
from decisionmesh.models.llm import ModelRunner
from decisionmesh.tools import Calculator


class Executor:
    """Execute decisions using injected models and tools."""
    
    def __init__(
        self,
        cheap_model: ModelRunner,
        strong_model: ModelRunner,
        calculator: Calculator,
    ):
        self.cheap_model = cheap_model
        self.strong_model = strong_model
        self.calculator = calculator
    
    def execute(self, task: Task, decision: Decision) -> ExecutionResult:
        """Execute a decision and return a normalized result."""
        start = time.perf_counter()
        
        try:
            if decision.strategy == Strategy.CHEAP_MODEL:
                output = self.cheap_model.generate(task.input)
                
            elif decision.strategy == Strategy.STRONG_MODEL:
                output = self.strong_model.generate(task.input)
            
            elif decision.strategy == Strategy.TOOL:
                output = str(self.calculator.calculate(task.input))
            
            else:
                raise ValueError(
                    f"Unsupported execution strategy: {decision.strategy}"
                )
            
            latency_ms = (time.perf_counter() - start) * 1000
            
            return ExecutionResult(
                success=True,
                output=output,
                latency_ms=latency_ms,
                actual_cost=decision.estimated_cost,
            )
        
        except (ValueError, ArithmeticError) as exc:
            latency_ms = (time.perf_counter() - start) * 1000
            
            return ExecutionResult(
                success=False,
                output=None,
                latency_ms=latency_ms,
                actual_cost=0.0,
                error=str(exc),
            )