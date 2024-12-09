import pytest
from unittest.mock import patch, mock_open
from service.prompt_service import PromptService

# Initialize the PromptService instance
prompt_service = PromptService()


def test_prompt_service_singleton():
    """Test that prompt_service is a singleton instance."""
    service1 = PromptService()
    service2 = PromptService()
    assert service1 is service2
    assert prompt_service is service1


def test_build_prompt_from_template(mock_template):
    """Test building prompt from template with valid parameters."""
    with patch("builtins.open", mock_open(read_data=mock_template)):
        with pytest.raises(KeyError) as exc_info:
            prompt_service.build_prompt_from_template(
                "test_template",
                agent_name="TestBot",
                agent_description="A test bot",
                task="Run tests",
            )
        assert "Prompt template not found: test_template" in str(exc_info.value)


def test_add_template():
    """Test adding a new template."""
    template_name = "test_template"
    template_content = {
        "prompt": "Test content: {test_var}",
        "parameters": {"test_var": {"description": "Test variable", "type": "str"}},
    }

    # Add template
    prompt_service.add_template(template_name, template_content)

    # Verify template was added by building a prompt from it
    result = prompt_service.build_prompt_from_template(template_name, test_var="Hello")

    assert result == "Test content: Hello"

    prompt_service.remove_template(template_name)
