from pathlib import Path
from prompt_toolkit import Application
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.scrollable_pane import ScrollablePane
from prompt_toolkit.widgets import Frame
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.application import get_app

import prompt_toolkit

print(prompt_toolkit.__version__)

def get_directory_tree(path):
    """Get a directory tree for the given path."""
    tree = {}
    for p in Path(path).rglob('*'):
        parts = p.relative_to(path).parts
        current = tree
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]
    return tree

def format_tree(tree, indent=''):
    """Format the directory tree into a list of strings."""
    lines = []
    for i, (name, subtree) in enumerate(tree.items()):
        is_last = i == len(tree) - 1
        prefix = '└── ' if is_last else '├── '
        lines.append(f"{indent}{prefix}{name}")
        if subtree:
            extension = ' ' if is_last else '│ '
            lines.extend(format_tree(subtree, indent + extension))
    return lines

def interactive_command(ctx, path):
    """Interactive file selection."""
    tree = get_directory_tree(path)
    formatted_tree = format_tree(tree)
    selected_files = []
    cursor_position = 0
    start_line = 0

    kb = KeyBindings()

    # Key bindings for quitting the application
    @kb.add('q')
    def quit_application(event):
        event.app.exit()

    # Navigation keys
    @kb.add('up')
    def move_cursor_up(event):
        nonlocal cursor_position, start_line
        if cursor_position > 0:
            cursor_position -= 1
            # Adjust start_line to keep the cursor in view
            if cursor_position < start_line:
                start_line = cursor_position

    @kb.add('down')
    def move_cursor_down(event):
        nonlocal cursor_position, start_line
        if cursor_position < len(formatted_tree) - 1:
            cursor_position += 1
            # Adjust start_line to keep the cursor in view
            if cursor_position >= start_line + get_visible_lines():
                start_line += 1

    @kb.add('pageup')
    def page_up(event):
        nonlocal cursor_position, start_line
        cursor_position = max(0, cursor_position - get_visible_lines())
        start_line = max(0, start_line - get_visible_lines())

    @kb.add('pagedown')
    def page_down(event):
        nonlocal cursor_position, start_line
        cursor_position = min(len(formatted_tree) - 1, cursor_position + get_visible_lines())
        start_line = min(len(formatted_tree) - get_visible_lines(), start_line + get_visible_lines())

    @kb.add('space')
    def toggle_selection(event):
        current_item = get_current_item()
        toggle_file_selection(current_item)

    @kb.add('enter')
    def confirm_selection(event):
        event.app.exit()

    def get_current_item():
        """Get the current item based on cursor position."""
        return formatted_tree[cursor_position].split('── ')[-1].strip()

    def toggle_file_selection(current_item):
        """Toggle the selection of the current item."""
        full_path = str(Path(path) / current_item)
        if full_path in selected_files:
            selected_files.remove(full_path)
        else:
            selected_files.append(full_path)

    def get_visible_lines():
        """Calculate the number of visible lines based on terminal height."""
        terminal_height = 60
        return terminal_height - 3  # Subtracting for instructions and padding

    def get_formatted_text():
        """Generate formatted text for display."""
        result = []
        visible_lines = get_visible_lines()
        for i in range(start_line, min(start_line + visible_lines, len(formatted_tree))):
            line = formatted_tree[i]
            style = 'class:cursor' if i == cursor_position else ''
            checkbox = '[X]' if str(Path(path) / line.split('── ')[-1].strip()) in selected_files else '[ ]'
            result.append((style, f"{checkbox} {line}\n"))
        return result

    # Create a scrollable window
    tree_window = Window(
        content=FormattedTextControl(get_formatted_text, focusable=True),
        width=60,
        dont_extend_width=True,
        wrap_lines=False,
    )

    # Wrap the tree window in a ScrollablePane
    scrollable_tree = ScrollablePane(tree_window)

    instructions = HTML('Use arrow keys to navigate, space to select, enter to confirm, q to quit')
    layout = Layout(
        VSplit([
            Frame(
                scrollable_tree,
                title="File Tree"
            ),
            Window(width=1, char='│'),
            HSplit([
                Window(content=FormattedTextControl(instructions)),
                Window(height=1),
                Window(content=FormattedTextControl(lambda: f"Selected: {len(selected_files)} file(s)")),
            ])
        ])
    )

    style = Style.from_dict({
        'cursor': 'bg:#00ff00 #000000',  # Green background for the cursor line
        'frame.border': '#888888',
    })

    app = Application(
        layout=layout,
        key_bindings=kb,
        full_screen=True,
        style=style,
        mouse_support=True,
    )

    app.run()

    # Output selected files
    print("Selected files:", selected_files if selected_files else "No files selected.")