from decisionmesh.models import Decision, Strategy, Task, TaskType


class DeterministicRouter:
    """Route tasks using explicit, deterministic rules."""
    
    def route(self, task: Task) -> Decision:
        if task.task_type == TaskType.MATH:
            return Decision(
                strategy=Strategy.TOOL,
                model=None,
                confidence=0.99,
                estimated_cost=0.0,
                reason="Math tasks are routed to a deterministic tool.",
            )
        
        if task.complexity < 0.4:
            return Decision(
                strategy=Strategy.CHEAP_MODEL,
                model="cheap-model",
                confidence=0.85,
                estimated_cost=0.001,
                reason="Low-complexity task routed to the cheap model.",
            )
        
        return Decision(
            strategy=Strategy.STRONG_MODEL,
            model="strong-model",
            confidence=0.80,
            estimated_cost=0.01,
            reason="Higher-complexity task routed to the strong model.",
        )
        