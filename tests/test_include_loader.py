import pytest
from jinja2 import Environment, TemplateNotFound
from code2prompt.utils.include_loader import IncludeLoader

@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory with some template files."""
    main = tmp_path / "main.j2"
    main.write_text("Main: {% include 'sub.j2' %}")
    
    sub = tmp_path / "sub.j2"
    sub.write_text("Sub: {{ variable }}")
    
    nested1 = tmp_path / "nested1.j2"
    nested1.write_text("Nested1: {% include 'nested2.j2' %}")
    
    nested2 = tmp_path / "nested2.j2"
    nested2.write_text("Nested2: {{ deep_variable }}")
    
    circular1 = tmp_path / "circular1.j2"
    circular1.write_text("Circular1: {% include 'circular2.j2' %}")
    
    circular2 = tmp_path / "circular2.j2"
    circular2.write_text("Circular2: {% include 'circular1.j2' %}")
    
    return tmp_path

def test_simple_include(temp_dir):
    loader = IncludeLoader(str(temp_dir))
    env = Environment(loader=loader)
    template = env.get_template("main.j2")
    result = template.render(variable="test")
    assert result == "Main: Sub: test"

def test_nested_include(temp_dir):
    loader = IncludeLoader(str(temp_dir))
    env = Environment(loader=loader)
    template = env.get_template("nested1.j2")
    result = template.render(deep_variable="deep test")
    assert result == "Nested1: Nested2: deep test"

#def test_circular_include(temp_dir):
#    loader = IncludeLoader(str(temp_dir))
#    env = Environment(loader=loader)
#    template = env.get_template("circular1.j2")
#    with pytest.raises(CircularIncludeError):
#        template.render()

def test_missing_template(temp_dir):
    loader = IncludeLoader(str(temp_dir))
    env = Environment(loader=loader)
    with pytest.raises(TemplateNotFound):
        env.get_template("non_existent.j2")

def test_include_stack_reset(temp_dir):
    loader = IncludeLoader(str(temp_dir))
    env = Environment(loader=loader)
    template = env.get_template("main.j2")
    template.render(variable="test")
    assert not hasattr(loader.include_stack, 'stack') or not loader.include_stack.stack

def test_multiple_includes(temp_dir):
    multi = temp_dir / "multi.j2"
    multi.write_text("Multi: {% include 'main.j2' %} and {% include 'nested1.j2' %}")
    
    loader = IncludeLoader(str(temp_dir))
    env = Environment(loader=loader)
    template = env.get_template("multi.j2")
    result = template.render(variable="test1", deep_variable="test2")
    assert result == "Multi: Main: Sub: test1 and Nested1: Nested2: test2"

#def test_recursive_include(temp_dir):
#    recursive = temp_dir / "recursive.j2"
#    recursive.write_text("{% if depth > 0 %}Depth {{ depth }}: {% include 'recursive.j2' %}{% else %}End{% endif %}")
#    
#    loader = IncludeLoader(str(temp_dir))
#    env = Environment(loader=loader)
#    template = env.get_template("recursive.j2")
#    result = template.render(depth=3)
#    assert result == "Depth 3: Depth 2: Depth 1: End"

def test_include_with_different_encoding(temp_dir):
    utf16_file = temp_dir / "utf16.j2"
    utf16_file.write_text("UTF-16: {{ variable }}", encoding='utf-16')
    
    loader = IncludeLoader(str(temp_dir), encoding='utf-16')
    env = Environment(loader=loader)
    template = env.get_template("utf16.j2")
    result = template.render(variable="test")
    assert result == "UTF-16: test"

def test_list_templates(temp_dir):
    loader = IncludeLoader(str(temp_dir))
    templates = loader.list_templates()
    assert templates == []

def test_get_source_not_found(temp_dir):
    loader = IncludeLoader(str(temp_dir))
    env = Environment(loader=loader)
    with pytest.raises(TemplateNotFound):
        loader.get_source(env, "non_existent.j2")

def test_get_source_success(temp_dir):
    loader = IncludeLoader(str(temp_dir))
    env = Environment(loader=loader)
    source, path, uptodate = loader.get_source(env, "main.j2")
    assert source == "Main: {% include 'sub.j2' %}"
    assert path == str(temp_dir / "main.j2")
    assert uptodate() is True