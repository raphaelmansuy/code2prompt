# code2prompt/config.py

from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class Configuration(BaseModel):
    """
    Configuration class for code2prompt tool.
    
    This class uses Pydantic for data validation and settings management.
    It defines all the configuration options available for the code2prompt tool.
    """

    path: List[Path] = Field(default_factory=list, description="Path(s) to the directory or file to process.")
    output: Optional[Path] = Field(None, description="Name of the output Markdown file.")
    gitignore: Optional[Path] = Field(None, description="Path to the .gitignore file.")
    filter: Optional[str] = Field(None, description="Comma-separated filter patterns to include files.")
    exclude: Optional[str] = Field(None, description="Comma-separated patterns to exclude files.")
    case_sensitive: bool = Field(False, description="Perform case-sensitive pattern matching.")
    suppress_comments: bool = Field(False, description="Strip comments from the code files.")
    line_number: bool = Field(False, description="Add line numbers to source code blocks.")
    no_codeblock: bool = Field(False, description="Disable wrapping code inside markdown code blocks.")
    template: Optional[Path] = Field(None, description="Path to a Jinja2 template file for custom prompt generation.")
    tokens: bool = Field(False, description="Display the token count of the generated prompt.")
    encoding: str = Field("cl100k_base", description="Specify the tokenizer encoding to use.")
    create_templates: bool = Field(False, description="Create a templates directory with example templates.")
    log_level: str = Field("INFO", description="Set the logging level.")
    price: bool = Field(False, description="Display the estimated price of tokens based on provider and model.")
    provider: Optional[str] = Field(None, description="Specify the provider for price calculation.")
    model: Optional[str] = Field(None, description="Specify the model for price calculation.")
    output_tokens: int = Field(1000, description="Specify the number of output tokens for price calculation.")
    analyze: bool = Field(False, description="Analyze the codebase and provide a summary of file extensions.")
    format: str = Field("flat", description="Format of the analysis output (flat or tree-like).")
    interactive: bool = Field(False, description="Interactive mode to select files.")

    @field_validator('encoding')
    @classmethod
    def validate_encoding(cls, v: str) -> str:
        valid_encodings = ["cl100k_base", "p50k_base", "p50k_edit", "r50k_base"]
        if v not in valid_encodings:
            raise ValueError(f"Invalid encoding. Must be one of: {', '.join(valid_encodings)}")
        return v

    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Invalid log level. Must be one of: {', '.join(valid_levels)}")
        return v.upper()

    @field_validator('format')
    @classmethod
    def validate_format(cls, v: str) -> str:
        valid_formats = ["flat", "tree"]
        if v not in valid_formats:
            raise ValueError(f"Invalid format. Must be one of: {', '.join(valid_formats)}")
        return v

    @classmethod
    def load_from_file(cls, file_path: Path) -> "Configuration":
        """
        Load configuration from a file.

        Args:
            file_path (Path): Path to the configuration file.

        Returns:
            Configuration: Loaded configuration object.

        Raises:
            FileNotFoundError: If the configuration file is not found.
            ValidationError: If the configuration file is invalid.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        try:
            with file_path.open() as f:
                config_data = f.read()
            return cls.model_validate_json(config_data)
        except ValidationError as e:
            raise ValueError(f"Invalid configuration file: {e}")

    def merge(self, cli_options: dict) -> "Configuration":
        """
        Merge CLI options with the current configuration.

        Args:
            cli_options (dict): Dictionary of CLI options.

        Returns:
            Configuration: New configuration object with merged options.
        """
        # Create a new dict with all current config values
        merged_dict = self.model_dump()

        # Update with CLI options, but only if they're different from the default
        for key, value in cli_options.items():
            if value is not None and value != self.model_fields[key].default:
                merged_dict[key] = value

        # Create a new Configuration object with the merged options
        return Configuration.model_validate(merged_dict)