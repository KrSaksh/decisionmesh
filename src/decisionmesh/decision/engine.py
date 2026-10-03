from decisionmesh.models import Decision, Task
from decisionmesh.router import DeterministicRouter


class DecisionEngine:
    """Coordinate task routing and produce execution decisions."""
    
    def __init__(self, router: DeterministicRouter):
        self.router = router
        
    def decide(self, task: Task) -> Decision:
        """Produce an execution decision for a task."""
        return self.router.route(task)