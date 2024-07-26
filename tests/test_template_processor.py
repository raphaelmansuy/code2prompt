import pytest
from unittest.mock import patch
from code2prompt.core.template_processor import get_user_inputs

@pytest.fixture
def mock_prompt():
    with patch('code2prompt.core.template_processor.prompt') as mock:
        yield mock

def test_get_user_inputs_single_variable(mock_prompt):
    mock_prompt.return_value = "test_value"
    template_content = "This is a {{variable}} test."
    result = get_user_inputs(template_content)
    assert result == {"variable": "test_value"}
    mock_prompt.assert_called_once_with("Enter value for variable: ")

def test_get_user_inputs_multiple_variables(mock_prompt):
    mock_prompt.side_effect = ["value1", "value2"]
    template_content = "{{var1}} and {{var2}} are two variables."
    result = get_user_inputs(template_content)
    assert result == {"var1": "value1", "var2": "value2"}
    assert mock_prompt.call_count == 2

def test_get_user_inputs_duplicate_variables(mock_prompt):
    mock_prompt.return_value = "repeated_value"
    template_content = "{{var}} appears twice: {{var}}"
    result = get_user_inputs(template_content)
    assert result == {"var": "repeated_value"}
    mock_prompt.assert_called_once_with("Enter value for var: ")

def test_get_user_inputs_no_variables(mock_prompt):
    template_content = "This template has no variables."
    result = get_user_inputs(template_content)
    assert result == {}
    mock_prompt.assert_not_called()

def test_get_user_inputs_whitespace_in_variable_names(mock_prompt):
    mock_prompt.side_effect = ["value1", "value2"]
    template_content = "{{ var1 }} and {{  var2  }} have whitespace."
    result = get_user_inputs(template_content)
    assert result == {"var1": "value1", "var2": "value2"}
    assert mock_prompt.call_count == 2

def test_get_user_inputs_case_sensitivity(mock_prompt):
    mock_prompt.side_effect = ["value1", "value2"]
    template_content = "{{VAR}} and {{var}} are different."
    result = get_user_inputs(template_content)
    assert result == {"VAR": "value1", "var": "value2"}
    assert mock_prompt.call_count == 2

def test_get_user_inputs_special_characters(mock_prompt):
    mock_prompt.return_value = "special_value"
    template_content = "This is a {{special!@#$%^&*()_+}} variable."
    result = get_user_inputs(template_content)
    assert result == {"special!@#$%^&*()_+": "special_value"}
    mock_prompt.assert_called_once_with("Enter value for special!@#$%^&*()_+: ")

def test_get_user_inputs_empty_variable_name(mock_prompt):
    template_content = "This has an {{}} empty variable name."
    result = get_user_inputs(template_content)
    assert result == {}
    mock_prompt.assert_not_called()

#def test_get_user_inputs_nested_variables(mock_prompt):
#    mock_prompt.side_effect = ["outer", "inner"]
#    template_content = "Nested {{outer{{inner}}}} variables."
#    result = get_user_inputs(template_content)
#    assert result == {"outer": "outer", "inner": "inner"}
#    assert mock_prompt.call_count == 2

def test_get_user_inputs_malformed_variables(mock_prompt):
    template_content = "Malformed {{var} and {var}} variables."
    result = get_user_inputs(template_content)
    assert result == {}
    mock_prompt.assert_not_called()