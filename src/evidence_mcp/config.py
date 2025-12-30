"""Configuration management for Evidence MCP server."""

from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the Evidence MCP server."""

    model_config = SettingsConfigDict(
        env_prefix="EVIDENCE_MCP_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Evidence dev server settings
    evidence_dev_url: str = "http://localhost:3000"
    evidence_project_path: Optional[Path] = None

    # MCP server settings
    server_name: str = "Evidence AI Assistant"
    transport: str = "stdio"  # stdio, sse, or streamable-http

    # Documentation settings
    docs_path: Path = Path(__file__).parent.parent.parent / "docs"

    def get_docs_path(self) -> Path:
        """Get the absolute path to the docs directory."""
        if self.docs_path.is_absolute():
            return self.docs_path
        return Path(__file__).parent.parent.parent / self.docs_path


settings = Settings()
