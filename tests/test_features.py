from decisionmesh.features import FeatureExtractor
from decisionmesh.models import Task, TaskType


def test_extracts_basic_text_features():
    extractor = FeatureExtractor()
    
    task = Task(
        id="task-1",
        input="Hello world",
    )
    
    features = extractor.extract(task)
    
    assert features.input_length == 11
    assert features.word_count == 2
    assert features.has_math_expression is False
    assert features.has_code_indicators is False
    assert features.estimated_complexity == 0.2


def test_detects_math_expression():
    extractor = FeatureExtractor()
    
    task = Task(
        id="task-2",
        input="10 + 20 * 3",
        task_type=TaskType.MATH,
    )
    
    features = extractor.extract(task)
    
    assert features.has_math_expression is True
    assert features.estimated_complexity == 0.1


def test_detects_code_indicators():
    extractor = FeatureExtractor()
    
    task = Task(
        id="task-3",
        input="def calculate_total(items): return sum(items)",
        task_type=TaskType.CODE,
    )
    
    features = extractor.extract(task)
    
    assert features.has_code_indicators is True
    assert features.estimated_complexity == 0.8


def test_detects_longer_general_task():
    extractor = FeatureExtractor()
    
    task = Task(
        id="task-4",
        input=(
            "Explain how distributed systems handle failures, "
            "consensus, replication, and network partitions."
        ),
    )
    
    features = extractor.extract(task)
    
    assert features.word_count > 5
    assert features.input_length > 80
    assert features.estimated_complexity == 0.7


def test_math_task_has_math_feature_even_withour_operator():
    extractor = FeatureExtractor()
    
    task = Task(
        id="task-5",
        input="Calculate the area of a circle",
        task_type=TaskType.MATH,
    )
    
    features = extractor.extract(task)
    
    assert features.has_math_expression is True
    assert features.estimated_complexity == 0.1