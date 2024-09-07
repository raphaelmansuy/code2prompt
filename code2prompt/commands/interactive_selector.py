"""
This module contains the InteractiveFileSelector class, which allows for interactive file selection.
"""

from typing import List, Dict  # Import necessary types
import os
import signal
from pathlib import Path
from prompt_toolkit import Application
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.scrollable_pane import ScrollablePane
from prompt_toolkit.widgets import Frame
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style


class InteractiveFileSelector:
    """Interactive file selector."""

    def __init__(self, paths: List[str]):  # Specify type for paths
        self.paths: List[str] = paths  # Store the list of paths
        self.start_line: int = 0
        self.cursor_position: int = 0
        self.selected_files: List[str] = []
        self.formatted_tree: List[str] = []
        self.kb = self._create_key_bindings()  # Call the new method
        self.app = self._create_application(self.kb)  # Use the private property

    def _get_terminal_height(self) -> int:  # Add return type
        """Get the height of the terminal."""
        return os.get_terminal_size().lines

    def _get_directory_tree(self) -> Dict[str, Dict]:  # Add return type
        """Get a combined directory tree for the given paths."""
        tree: Dict[str, Dict] = {}
        for path in self.paths:  # Iterate over each resolved path
            parts = Path(path).parts  # Get parts of the resolved path
            current = tree
            for part in parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
        return tree

    def _format_tree(self, tree, indent=""):
        """Format the directory tree into a list of strings."""
        lines = []
        for i, (name, subtree) in enumerate(tree.items()):
            is_last = i == len(tree) - 1
            prefix = "└── " if is_last else "├── "
            lines.append(f"{indent}{prefix}{name}")
            if subtree:
                extension = " " if is_last else "│ "
                lines.extend(self._format_tree(subtree, indent + extension))
        return lines

    def _get_visible_lines(self):
        """Calculate the number of visible lines based on terminal height."""
        terminal_height = self._get_terminal_height()
        return terminal_height - 3  # Subtracting for instructions and padding

    def _get_formatted_text(self):
        """Generate formatted text for display."""
        result = []
        visible_lines = self._get_visible_lines()
        for i in range(
            self.start_line,
            min(self.start_line + visible_lines, len(self.formatted_tree)),
        ):
            line = self.formatted_tree[i]
            style = "class:cursor" if i == self.cursor_position else ""
            checkbox = (
                "[X]"
                if any(
                    str(Path(path) / line.split("── ")[-1].strip())
                    in self.selected_files
                    for path in self.paths
                )  # Check against all paths
                else "[ ]"
            )
            result.append((style, f"{checkbox} {line}\n"))
        return result

    def _toggle_file_selection(
        self, current_item: str
    ) -> None:  # Add parameter type and return type
        """Toggle the selection of the current item."""
        full_paths: List[str] = [
            str(Path(path) / current_item) for path in self.paths
        ]  # Create full paths for all paths
        for full_path in full_paths:
            if full_path in self.selected_files:
                self.selected_files.remove(full_path)
            else:
                self.selected_files.append(full_path)

    def _get_current_item(self) -> str:  # Add return type
        """Get the current item based on cursor position."""
        return self.formatted_tree[self.cursor_position].split("── ")[-1].strip()

    def _resize_handler(self, _event):
        """Handle terminal resize event."""
        # Ensure cursor is in view
        self.start_line = max(0, self.cursor_position - self._get_visible_lines() + 1)
        self.app.invalidate()  # Invalidate the application to refresh the layout

    def run(self):
        """Run the interactive file selection."""
        self._check_paths()  # Update method name to check multiple paths
        tree = self._get_directory_tree()
        self.formatted_tree = self._format_tree(tree)

        signal.signal(signal.SIGWINCH, self._resize_handler)

        self.app.run()

        print(
            "Selected files:",
            self.selected_files if self.selected_files else "No files selected.",
        )
        return self.selected_files

    def _create_key_bindings(self) -> KeyBindings:  # New private method
        """Create and return key bindings for the application."""
        kb = KeyBindings()

        @kb.add("q")
        def quit_application(event):
            event.app.exit()

        @kb.add("up")
        def move_cursor_up(_event):
            if self.cursor_position > 0:
                self.cursor_position -= 1
                if self.cursor_position < self.start_line:
                    self.start_line = self.cursor_position  # Scroll up

        @kb.add("down")
        def move_cursor_down(_event):
            if self.cursor_position < len(self.formatted_tree) - 1:
                self.cursor_position += 1
                if self.cursor_position >= self.start_line + self._get_visible_lines():
                    self.start_line = (
                        self.cursor_position - self._get_visible_lines() + 1
                    )  # Scroll down

        @kb.add("pageup")
        def page_up(_event):
            self.cursor_position = max(
                0, self.cursor_position - self._get_visible_lines()
            )
            # Adjust start_line to keep the cursor in view
            if self.cursor_position < self.start_line:
                self.start_line = self.cursor_position

        @kb.add("pagedown")
        def page_down(_event):
            self.cursor_position = min(
                len(self.formatted_tree) - 1,
                self.cursor_position + self._get_visible_lines(),
            )
            # Adjust start_line to keep the cursor in view
            if self.cursor_position >= self.start_line + self._get_visible_lines():
                self.start_line = self.cursor_position - self._get_visible_lines() + 1

        @kb.add("space")
        def toggle_selection(_event):
            current_item = self._get_current_item()
            self._toggle_file_selection(current_item)

        @kb.add("enter")
        def confirm_selection(_event):
            self.app.exit()

        return kb  # Return the created key bindings

    def _create_application(self, kb) -> Application:  # New private method
        """Create and return the application instance."""
        tree_window = Window(
            content=FormattedTextControl(self._get_formatted_text, focusable=True),
            width=60,
            dont_extend_width=True,
            wrap_lines=False,
        )

        scrollable_tree = ScrollablePane(tree_window)

        instructions = (
            "Instructions:\n"
            "-------------\n"
            "1. Use ↑ and ↓ to navigate\n"
            "2. Press Space to select/deselect an item\n"
            "3. Press Enter to confirm your selection\n"
            "4. Press q to quit the selection process\n"
        )

        layout = Layout(
            VSplit(
                [
                    Frame(scrollable_tree, title="File Tree"),
                    Window(width=1, char="│"),
                    HSplit(
                        [
                            Window(
                                content=FormattedTextControl(instructions), height=5
                            ),
                            Window(height=1),
                            Window(
                                content=FormattedTextControl(
                                    lambda: f"Selected: {len(self.selected_files)} file(s): {', '.join(self.selected_files) if self.selected_files else 'None'}"
                                ),
                                height=1,
                            ),
                        ]
                    ),
                ],
                padding=1,
            )
        )

        style = Style.from_dict(
            {
                "cursor": "bg:#00ff00 #000000",
                "frame.border": "#888888",
            }
        )

        return Application(
            layout=layout,
            key_bindings=kb,
            full_screen=True,
            style=style,
            mouse_support=True,
        )

    def _check_paths(self) -> None:  # Add return type
        """Check if the provided paths are valid."""
        if not self.paths or any(not path for path in self.paths):
            raise ValueError(
                "A valid list of paths must be provided for interactive mode."
            )
