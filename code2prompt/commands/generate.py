# code2prompt/commands/generate.py

from pathlib import Path
from typing import List, Dict, Any

from code2prompt.commands.base_command import BaseCommand
from code2prompt.core.process_files import process_files
from code2prompt.core.generate_content import generate_content
from code2prompt.core.write_output import write_output
from code2prompt.utils.count_tokens import count_tokens
from code2prompt.utils.logging_utils import log_token_count
from code2prompt.utils.price_calculator import load_token_prices, calculate_prices

class GenerateCommand(BaseCommand):
    """Command for generating markdown content from code files."""

    def execute(self) -> None:
        """Execute the generate command."""
        self.logger.info("Generating markdown...")
        
        files_data = self._process_files()
        content = self._generate_content(files_data)
        self._write_output(content)
        
        if self.config.tokens or self.config.price:
            self._handle_token_count_and_price(content)
        
        self.logger.info("Generation complete.")

    def _process_files(self) -> List[Dict[str, Any]]:
        """Process files based on the configuration."""
        all_files_data = []
        for path in self.config.path:
            files_data = process_files({**self.config.dict(), "path": path})
            all_files_data.extend(files_data)
        return all_files_data

    def _generate_content(self, files_data: List[Dict[str, Any]]) -> str:
        """Generate content from processed files data."""
        return generate_content(files_data, self.config.dict())

    def _write_output(self, content: str) -> None:
        """Write the generated content to output."""
        write_output(content, self.config.output, copy_to_clipboard=True)

    def _handle_token_count_and_price(self, content: str) -> None:
        """Handle token counting and price calculation if enabled."""
        token_count = count_tokens(content, self.config.encoding)
        log_token_count(token_count)

        if self.config.price:
            self._display_price_table(token_count)

    def _display_price_table(self, token_count: int) -> None:
        """Display a table with price estimates for the given token count."""
        token_prices = load_token_prices()
        if not token_prices:
            return

        output_token_count = self.config.output_tokens
        table_data = calculate_prices(
            token_prices,
            token_count,
            output_token_count,
            self.config.provider,
            self.config.model
        )

        if not table_data:
            self.logger.error("Error: No matching provider or model found")
            return

        headers = ["Provider", "Model", "Price for 1K Input Tokens", "Number of Input Tokens", "Total Price"]
        table = self._format_table(table_data, headers)
        
        self.logger.info("\n✨ Estimated Token Prices: (All prices are in USD, it is an estimate as the current token implementation is based on OpenAI's Tokenizer)")
        self.logger.info("\n")
        self.logger.info(table)
        self.logger.info("\n📝 Note: The prices are based on the token count and the provider's pricing model.")

    def _format_table(self, table_data: List[List[str]], headers: List[str]) -> str:
        """Format the price table for display."""
        from tabulate import tabulate
        return tabulate(table_data, headers=headers, tablefmt="grid")