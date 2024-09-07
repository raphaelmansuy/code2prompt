"""
This module contains the GenerateCommand class, which is responsible for generating
markdown content from code files based on the provided configuration.
"""

from typing import List, Dict, Any
from code2prompt.core.process_files import process_files
from code2prompt.core.generate_content import generate_content
from code2prompt.core.write_output import write_output
from code2prompt.utils.count_tokens import count_tokens
from code2prompt.utils.logging_utils import log_token_count
from code2prompt.utils.display_price_table import display_price_table
from code2prompt.commands.base_command import BaseCommand


class GenerateCommand(BaseCommand):
    """Command for generating markdown content from code files."""

    def execute(self) -> None:
        """Execute the generate command."""
        self.logger.info("Generating markdown...")
        file_paths = self._process_files()
        content = self._generate_content(file_paths)
        self._write_output(content)

        if self.config.price:
            self.display_token_count_and_price(content)
        elif self.config.tokens:
            self.display_token_count(content)

        self.logger.info("Generation complete.")

    def _process_files(self) -> List[Dict[str, Any]]:
        """Process files based on the configuration."""
        all_files_data = []
        files_data = process_files(
            file_paths=self.config.path,
            line_number=self.config.line_number,
            no_codeblock=self.config.no_codeblock,
            suppress_comments=self.config.suppress_comments,
        )
        all_files_data.extend(files_data)
        return all_files_data

    def _generate_content(self, files_data: List[Dict[str, Any]]) -> str:
        """Generate content from processed files data."""
        return generate_content(files_data, self.config.dict())

    def _write_output(self, content: str) -> None:
        """Write the generated content to output."""
        write_output(content, self.config.output, copy_to_clipboard=True)

    def display_token_count_and_price(self, content: str) -> None:
        """Handle token counting and price calculation if enabled."""
        token_count = count_tokens(content, self.config.encoding)
        model = self.config.model
        provider = self.config.provider
        display_price_table(token_count, provider, model, self.config.output_tokens)
        log_token_count(token_count)

        
    def display_token_count(self, content: str) -> None:
        """Display the token count if enabled."""
        token_count = count_tokens(content, self.config.encoding)
        log_token_count(token_count)
        
