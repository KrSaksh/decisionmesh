from decisionmesh.models.llm import CheapModel, ModelRunner, StrongModel


def test_cheap_model_has_expected_name():
    model = CheapModel()
    
    assert model.name == "cheap-model"


def test_strong_model_has_expected_name():
    model = StrongModel()
    
    assert model.name == "strong-model"


def test_cheap_model_implements_model_runner():
    model = CheapModel()
    
    assert isinstance(model, ModelRunner)


def test_strong_model_implements_model_runner():
    model = StrongModel()
    
    assert isinstance(model, ModelRunner)


def test_cheap_model_can_generate():
    model = CheapModel()
    
    result = model.generate("Hello")
    
    assert result == "Mock response to: Hello"


def test_strong_model_can_generate():
    model = StrongModel()
    
    result = model.generate("Hello")
    
    assert result == "Mock response to: Hello"
