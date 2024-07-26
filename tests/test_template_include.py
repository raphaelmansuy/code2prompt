import pytest
from code2prompt.core.template_processor import process_template
import os

def test_include_feature(tmp_path):
    # Create a main template
    main_template = tmp_path / "main.j2"
    main_template.write_text("Main: {% include 'sub.j2' %}")

    # Create a sub-template
    sub_template = tmp_path / "sub.j2"
    sub_template.write_text("Sub: {{ variable }}")

    template_content = main_template.read_text()
    files_data = []
    user_inputs = {"variable": "test"}

    result = process_template(template_content, files_data, user_inputs, str(main_template))
    assert result == "Main: Sub: test"

def test_nested_include(tmp_path):
    # Create a main template
    main_template = tmp_path / "main.j2"
    main_template.write_text("Main: {% include 'sub1.j2' %}")

    # Create sub-templates
    sub1_template = tmp_path / "sub1.j2"
    sub1_template.write_text("Sub1: {% include 'sub2.j2' %}")

    sub2_template = tmp_path / "sub2.j2"
    sub2_template.write_text("Sub2: {{ variable }}")

    template_content = main_template.read_text()
    files_data = []
    user_inputs = {"variable": "nested"}

    result = process_template(template_content, files_data, user_inputs, str(main_template))
    assert result == "Main: Sub1: Sub2: nested"

def test_multiple_includes(tmp_path):
    # Create a main template
    main_template = tmp_path / "main.j2"
    main_template.write_text("Main: {% include 'sub1.j2' %} and {% include 'sub2.j2' %}")

    # Create sub-templates
    sub1_template = tmp_path / "sub1.j2"
    sub1_template.write_text("Sub1: {{ var1 }}")

    sub2_template = tmp_path / "sub2.j2"
    sub2_template.write_text("Sub2: {{ var2 }}")

    template_content = main_template.read_text()
    files_data = []
    user_inputs = {"var1": "first", "var2": "second"}

    result = process_template(template_content, files_data, user_inputs, str(main_template))
    assert result == "Main: Sub1: first and Sub2: second"

def test_include_with_context(tmp_path):
    # Create a main template
    main_template = tmp_path / "main.j2"
    main_template.write_text("Main: {% include 'sub.j2' %}")

    # Create a sub-template
    sub_template = tmp_path / "sub.j2"
    sub_template.write_text("Sub: {{ main_var }} and {{ sub_var }}")

    template_content = main_template.read_text()
    files_data = []
    user_inputs = {"main_var": "from main", "sub_var": "from sub"}

    result = process_template(template_content, files_data, user_inputs, str(main_template))
    assert result == "Main: Sub: from main and from sub"



def test_include_with_files_data(tmp_path):
    # Create a main template
    main_template = tmp_path / "main.j2"
    main_template.write_text("Main: {% include 'sub.j2' %}")

    # Create a sub-template
    sub_template = tmp_path / "sub.j2"
    sub_template.write_text("Sub: {{ files[0].name }}")

    template_content = main_template.read_text()
    files_data = [{"name": "test_file.py", "content": "print('Hello')"}]
    user_inputs = {}

    result = process_template(template_content, files_data, user_inputs, str(main_template))
    assert result == "Main: Sub: test_file.py"

#def test_circular_include(tmp_path):
    # Create templates with circular inclusion
#    template1 = tmp_path / "template1.j2"
#    template1.write_text("T1: {% include 'template2.j2' %}")

#    template2 = tmp_path / "template2.j2"
#    template2.write_text("T2: {% include 'template1.j2' %}")

#    template_content = template1.read_text()
#    files_data = []
#    user_inputs = {}

#    with pytest.raises(ValueError, match="Circular include detected"):
#        process_template(template_content, files_data, user_inputs, str(template1))