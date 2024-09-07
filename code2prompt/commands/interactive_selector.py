from typing import List, Dict, Set, Tuple
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

    def __init__(self, paths: List[Path], selected_files: List[Path]):
        self.paths: List[Path] = paths.copy()
        self.start_line: int = 0
        self.cursor_position: int = 0
        self.formatted_tree: List[str] = []
        self.tree_paths: List[Path] = []
        self.tree_full_paths: List[str] = []
        self.kb = self._create_key_bindings()
        self.app = self._create_application(self.kb)
        self.selected_files: Set[str] = set(
            [str(Path(file).resolve()) for file in selected_files]
        )

    def _get_terminal_height(self) -> int:
        """Get the height of the terminal."""
        return os.get_terminal_size().lines

    def _get_directory_tree(self) -> Dict[Path, Dict]:
        """Get a combined directory tree for the given paths."""
        tree: Dict[Path, Dict] = {}

        for path in self.paths:
            current = tree  # Start from the root of the tree
            # Iterate through each part of the path
            for part in Path(path).parts:
                if part not in current:  # Check if part is already in the current level
                    current[part] = {}  # Create a new dictionary for the part
                current = current[part]  # Move to the next level in the tree

        return tree
    
    

    def _format_tree(
        self, tree: Dict[Path, Dict], indent: str = "", parent_dir: str = ""
    ) -> Tuple[List[str], List[Path], List[str]]:
        """Format the directory tree into a list of strings."""
        lines: List[str] = []
        tree_paths: List[Path] = []
        tree_full_paths: List[str] = []

        for i, (file_path, subtree) in enumerate(tree.items()):
            is_last = i == len(tree) - 1
            prefix = "└── " if is_last else "├── "
            line = f"{indent}{prefix}{Path(file_path).name}"
            lines.append(line)

            # Resolve and store the full path
            resolved_path = Path(parent_dir, file_path).resolve()
            tree_paths.append(resolved_path)
            tree_full_paths.append(str(resolved_path))  # Store the full path as a string

            if subtree:
                extension = " " if is_last else "│ "
                sub_lines, sub_tree_paths, sub_full_paths = self._format_tree(
                    subtree, indent + extension, str(resolved_path)
                )
                lines.extend(sub_lines)
                tree_paths.extend(sub_tree_paths)
                tree_full_paths.extend(sub_full_paths)  # Merge the full paths from the subtree

        return lines, tree_paths, tree_full_paths

    def _get_visible_lines(self) -> int:
        """Calculate the number of visible lines based on terminal height."""
        terminal_height = self._get_terminal_height()
        return terminal_height - 3  # Subtracting for instructions and padding

    def _get_formatted_text(self) -> List[tuple]:
        """Generate formatted text for display."""
        result = []

        # Ensure that formatted_tree and tree_paths have the same length
        if len(self.formatted_tree) == len(self.tree_paths):
            visible_lines = self._get_visible_lines()

            # Calculate the end line for the loop
            end_line = min(self.start_line + visible_lines, len(self.formatted_tree))

            for i in range(self.start_line, end_line):
                line = self.formatted_tree[i]
                style = "class:cursor" if i == self.cursor_position else ""

                # Ensure cursor_position is valid
                if self.cursor_position >= len(self.formatted_tree):
                    self.cursor_position = len(self.formatted_tree) - 1

                # Get the full path
                file_path = str(self.tree_full_paths[i])

                # Check if the full path is selected
                is_selected = file_path in self.selected_files

                # Update checkbox based on selection
                checkbox = "[X]" if is_selected else "[ ]"

                # Append formatted line to result
                result.append((style, f"{checkbox} {line}\n"))

                # Debugging output
                # print(f"Line: {line}, Full Path: {full_path}, Selected: {is_selected}")

        return result

    def _toggle_file_selection(self, current_item: str) -> None:
        """Toggle the selection of the current item."""
        if current_item in self.selected_files:
            self.selected_files.remove(current_item)
        else:
            self.selected_files.add(current_item)

    def _get_current_item(self) -> str:
        """Get the current item based on cursor position."""
        if 0 <= self.cursor_position < len(self.tree_paths):
            current_item = self.tree_full_paths[self.cursor_position]
            return current_item  # Return the full path
        return None  # Return None if no valid path is found

    def _resize_handler(self, _event) -> None:
        """Handle terminal resize event."""
        self.start_line = max(0, self.cursor_position - self._get_visible_lines() + 1)
        self.app.invalidate()  # Invalidate the application to refresh the layout

    def run(self) -> List[Path]:
        """Run the interactive file selection."""
        self._check_paths()
        tree = self._get_directory_tree()
        self.formatted_tree, self.tree_paths, self.tree_full_paths = self._format_tree(
            tree
        )
        signal.signal(signal.SIGWINCH, self._resize_handler)
        self.app.run()
        return self.selected_files, self.tree_paths, self.tree_full_paths

    def _create_key_bindings(self) -> KeyBindings:
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
            if self.cursor_position < self.start_line:
                self.start_line = (
                    self.cursor_position
                )  # Adjust start_line to keep the cursor in view

        @kb.add("pagedown")
        def page_down(_event):
            self.cursor_position = min(
                len(self.formatted_tree) - 1,
                self.cursor_position + self._get_visible_lines(),
            )
            if self.cursor_position >= self.start_line + self._get_visible_lines():
                self.start_line = (
                    self.cursor_position - self._get_visible_lines() + 1
                )  # Adjust start_line to keep the cursor in view

        @kb.add("space")
        def toggle_selection(_event):
            current_item = self._get_current_item()  # Get the current item as a Path
            if current_item:  # Ensure current_item is not None
                self._toggle_file_selection(
                    current_item
                )  # Pass the Path object directly

        @kb.add("enter")
        def confirm_selection(_event):
            self.app.exit()

        return kb

    def _get_selected_files_text(self) -> str:
        """Get the selected files text."""
        # Create a nicer display for selected files
        if self.selected_files:
            files_list = "\n".join(f"- {file}" for file in self.selected_files)
            return f"Selected: {len(self.selected_files)} file(s):\n{files_list}"
        return "Selected: 0 file(s): None"

    def _create_application(self, kb) -> Application:
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
                                    self._get_selected_files_text
                                ),
                                height=10,
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

    def _check_paths(self) -> None:
        """Check if the provided paths are valid."""
        if not self.paths or any(not path for path in self.paths):
            raise ValueError(
                "A valid list of paths must be provided for interactive mode."
            )
