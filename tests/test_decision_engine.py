from decisionmesh.decision import DecisionEngine
from decisionmesh.models import Strategy, Task, TaskType
from decisionmesh.router import DeterministicRouter


def test_decision_engine_routes_math_task():
    engine = DecisionEngine(router=DeterministicRouter())
    
    task = Task(
        id="task-1",
        input="10 + 5",
        task_type=TaskType.MATH,
        complexity=0.1,
    )
    
    decision = engine.decide(task)
    
    assert decision.strategy == Strategy.TOOL
    assert decision.confidence == 0.99
    assert decision.estimated_cost == 0.0
    

def test_decision_engine_routes_low_complexity_task():
    engine = DecisionEngine(router=DeterministicRouter())
    
    task = Task(
        id="task-2",
        input="Hello",
        task_type=TaskType.GENERAL,
        complexity=0.2,
    )
    
    decision = engine.decide(task)
    
    assert decision.strategy == Strategy.CHEAP_MODEL
    assert decision.model == "cheap-model"
    

def test_decision_engine_routes_high_complexity_task():
    engine = DecisionEngine(router=DeterministicRouter())
    
    task = Task(
        id="task-3",
        input="Explain distributed systems",
        task_type=TaskType.GENERAL,
        complexity=0.8,
    )
    
    decision = engine.decide(task)
    
    assert decision.strategy == Strategy.STRONG_MODEL
    assert decision.model == "strong-model"