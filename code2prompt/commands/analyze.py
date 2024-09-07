# code2prompt/commands/analyze.py

from pathlib import Path
from typing import Dict

from code2prompt.commands.base_command import BaseCommand
from code2prompt.utils.analyzer import (
    analyze_codebase,
    format_flat_output,
    format_tree_output,
    get_extension_list,
)


class AnalyzeCommand(BaseCommand):
    """Command for analyzing the codebase structure."""

    def execute(self) -> None:
        """Execute the analyze command."""
        self.logger.info("Analyzing codebase...")

        for path in self.config.path:
            self._analyze_path(Path(path))

        self.logger.info("Analysis complete.")

    def _analyze_path(self, path: Path) -> None:
        """
        Analyze a single path and output the results.

        Args:
            path (Path): The path to analyze.
        """
        extension_counts, extension_dirs = analyze_codebase(path)

        if not extension_counts:
            self.logger.warning(f"No files found in {path}")
            return

        if self.config.format == "flat":
            output = format_flat_output(extension_counts)
        else:
            output = format_tree_output(extension_dirs)

        print(output)

        print("\nComma-separated list of extensions:")
        print(get_extension_list(extension_counts))

        if self.config.tokens:
            total_tokens = self._count_tokens(extension_counts)
            self.logger.info(f"Total tokens in codebase: {total_tokens}")

    def _count_tokens(self, extension_counts: Dict[str, int]) -> int:
        """
        Count the total number of tokens in the codebase.

        Args:
            extension_counts (Dict[str, int]): A dictionary of file extensions and their counts.

        Returns:
            int: The total number of tokens.
        """
        total_tokens = 0
        for _ext, count in extension_counts.items():
            # This is a simplified token count. You might want to implement a more
            # sophisticated counting method based on the file type.
            total_tokens += count * 100  # Assuming an average of 100 tokens per file

        return total_tokens
