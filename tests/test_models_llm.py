import pytest

from decisionmesh.models.llm import MockModel, ModelRunner


def test_mock_model_name():
    model = MockModel()
    
    assert model.name == "mock-model"
    

def test_mock_model_generates_response():
    model = MockModel()
    
    response = model.generate("Hello")
    
    assert response == "Mock response to: Hello"


def test_mock_model_custom_name():
    model = MockModel(model_name="cheap-model")
    
    assert model.name == "cheap-model"


def test_mock_model_runner_is_abstract():
    with pytest.raises(TypeError):
        ModelRunner()
