from decisionmesh.models import Strategy, Task, TaskType
from decisionmesh.router import DeterministicRouter


def test_math_task_routes_to_tool():
    router = DeterministicRouter()
    
    task = Task(
        id="math-001",
        input="Calculate 17 * 24",
        task_type=TaskType.MATH,
        complexity=0.9,
    )
    
    decision = router.route(task)
    
    assert decision.strategy == Strategy.TOOL
    assert decision.model is None

def test_low_complexity_task_routes_to_cheap_model():
    router = DeterministicRouter()
    
    task = Task(
        id="cheap-001",
        input="What is the capital of France?",
        complexity=0.2,
    )
    
    decision = router.route(task)
    
    assert decision.strategy == Strategy.CHEAP_MODEL
    assert decision.model == "cheap-model"
    
def test_high_complexity_task_routes_to_strong_model():
    router = DeterministicRouter()
    
    task = Task(
        id="strong-001",
        input="Analyze the tradeoffs between microservices and a monolith.",
        complexity=0.8,
    )
    
    decision = router.route(task)
    
    assert decision.strategy == Strategy.STRONG_MODEL
    assert decision.model == "strong-model"

def test_complexity_boundary():
    router = DeterministicRouter()
    
    low = router.route(
        Task(
            id="boundary-low",
            input="Boundary test",
            complexity=0.39,
        )
    )
    
    high = router.route(
        Task(
            id="boundary-high",
            input="Boundary test",
            complexity=0.40,
        )
    )
    
    assert low.strategy == Strategy.CHEAP_MODEL
    assert high.strategy == Strategy.STRONG_MODEL
