from code2prompt.core.template_processor import get_user_inputs, load_template, process_template
from code2prompt.utils.generate_markdown_content import generate_markdown_content


def generate_content(files_data, options):
    """
    Generate content based on the provided files data and options.

    This function either processes a Jinja2 template with the given files data and user inputs
    or generates markdown content directly from the files data, depending on whether a
    template option is provided.

    Args:
        files_data (list): A list of dictionaries containing processed file data.
        options (dict): A dictionary containing options such as template path and whether
                        to wrap code inside markdown code blocks.

    Returns:
        str: The generated content as a string, either from processing a template or
             directly generating markdown content.
    """
    if options['template']:
        template_content = load_template(options['template'])
        user_inputs = get_user_inputs(template_content)
        return process_template(template_content, files_data, user_inputs, options['template'])
    return generate_markdown_content(files_data, options['no_codeblock'])