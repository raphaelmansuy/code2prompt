import pytest
from unittest.mock import patch
from code2prompt.core.template_processor import get_user_inputs

@pytest.fixture
def mock_prompt():
    with patch('code2prompt.core.template_processor.prompt') as mock:
        yield mock

def test_get_user_inputs_single_variable(mock_prompt):
    mock_prompt.return_value = "test_value"
    template_content = "This is a {{input:variable}} test."
    result = get_user_inputs(template_content)
    assert result == {"variable": "test_value"}
    mock_prompt.assert_called_once_with("Enter value for variable: ")

def test_get_user_inputs_multiple_variables(mock_prompt):
    mock_prompt.side_effect = ["value1", "value2"]
    template_content = "{{input:var1}} and {{input:var2}} are two variables."
    result = get_user_inputs(template_content)
    assert result == {"var1": "value1", "var2": "value2"}
    assert mock_prompt.call_count == 2

def test_get_user_inputs_duplicate_variables(mock_prompt):
    mock_prompt.return_value = "repeated_value"
    template_content = "{{input:var}} appears twice: {{input:var}}"
    result = get_user_inputs(template_content)
    assert result == {"var": "repeated_value"}
    mock_prompt.assert_called_once_with("Enter value for var: ")

def test_get_user_inputs_no_variables(mock_prompt):
    template_content = "This template has no input variables."
    result = get_user_inputs(template_content)
    assert result == {}
    mock_prompt.assert_not_called()

def test_get_user_inputs_whitespace_in_variable_names(mock_prompt):
    mock_prompt.side_effect = ["value1", "value2"]
    template_content = "{{ input:var1 }} and {{  input:var2  }} have whitespace."
    result = get_user_inputs(template_content)
    assert result == {"var1": "value1", "var2": "value2"}
    assert mock_prompt.call_count == 2

def test_get_user_inputs_case_sensitivity(mock_prompt):
    mock_prompt.side_effect = ["value1", "value2"]
    template_content = "{{input:VAR}} and {{input:var}} are different."
    result = get_user_inputs(template_content)
    assert result == {"VAR": "value1", "var": "value2"}
    assert mock_prompt.call_count == 2

def test_get_user_inputs_special_characters(mock_prompt):
    mock_prompt.return_value = "special_value"
    template_content = "This is a {{input:special!@#$%^&*()_+}} variable."
    result = get_user_inputs(template_content)
    assert result == {"special!@#$%^&*()_+": "special_value"}
    mock_prompt.assert_called_once_with("Enter value for special!@#$%^&*()_+: ")

def test_get_user_inputs_empty_variable_name(mock_prompt):
    template_content = "This has an {{input:}} empty variable name."
    result = get_user_inputs(template_content)
    assert result == {}
    mock_prompt.assert_not_called()

def test_get_user_inputs_malformed_variables(mock_prompt):
    template_content = "Malformed {{input:var} and {input:var}} variables."
    result = get_user_inputs(template_content)
    assert result == {}
    mock_prompt.assert_not_called()

def test_get_user_inputs_ignore_jinja_execute_blocks(mock_prompt):
    template_content = """
    {% if condition %}
        {{var}}
    {% endif %}
    {{input:user_var}}
    {% for item in items %}
        {{item}}
    {% endfor %}
    """
    mock_prompt.return_value = "user_value"
    result = get_user_inputs(template_content)
    assert result == {"user_var": "user_value"}
    mock_prompt.assert_called_once_with("Enter value for user_var: ")

def test_get_user_inputs_mixed_variables(mock_prompt):
    template_content = """
    Regular variable: {{var}}
    Input variable: {{input:user_var}}
    {% if condition %}
        Jinja block variable: {{block_var}}
    {% endif %}
    Another input: {{input:another_var}}
    """
    mock_prompt.side_effect = ["user_value", "another_value"]
    result = get_user_inputs(template_content)
    assert result == {"user_var": "user_value", "another_var": "another_value"}
    assert mock_prompt.call_count == 2

def test_get_user_inputs_nested_jinja_blocks(mock_prompt):
    template_content = """
    {% if outer_condition %}
        {% for item in items %}
            {{input:user_var}}
        {% endfor %}
    {% endif %}
    """
    mock_prompt.return_value = "user_value"
    result = get_user_inputs(template_content)
    assert result == {"user_var": "user_value"}
    mock_prompt.assert_called_once_with("Enter value for user_var: ")