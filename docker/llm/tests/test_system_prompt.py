import pytest
from llm.sysprompt.system_prompt_pipeline import PromptPipeline

@pytest.fixture
def generate_system_prompt():
    prompt_pipeline = PromptPipeline()
    system_prompt = prompt_pipeline.yaml_to_prompt()
    return system_prompt

def test_prompt_is_string(generate_system_prompt):
    assert isinstance(generate_system_prompt, str)

def test_prompt_not_empty(generate_system_prompt):
    assert generate_system_prompt.strip() != ""

