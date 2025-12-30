"""Pydantic models for Evidence MCP server responses."""

from typing import Literal, Optional

from pydantic import BaseModel, Field


# Metadata models
class Column(BaseModel):
    """Represents a database column."""

    name: str
    type: str  # String|Int64|Float64|Date32|Decimal(p,s)


class Table(BaseModel):
    """Represents a database table with its columns."""

    name: str  # format: source_name.table_name
    columns: list[Column]


class MetadataResponse(BaseModel):
    """Response from get_metadata tool."""

    tables: list[Table]

    @classmethod
    def from_manifest(cls, manifest: dict) -> "MetadataResponse":
        """Create MetadataResponse from Evidence manifest.json structure."""
        tables = []

        # Evidence manifest structure may vary, handle common formats
        if "sources" in manifest:
            for source_name, source_data in manifest.get("sources", {}).items():
                for table_name, table_data in source_data.get("tables", {}).items():
                    columns = []
                    for col in table_data.get("columns", []):
                        columns.append(
                            Column(
                                name=col.get("name", col.get("column_name", "")),
                                type=col.get("type", col.get("data_type", "unknown")),
                            )
                        )
                    tables.append(Table(name=f"{source_name}.{table_name}", columns=columns))
        elif "tables" in manifest:
            # Alternative flat structure
            for table_data in manifest.get("tables", []):
                columns = [
                    Column(
                        name=col.get("name", ""),
                        type=col.get("type", "unknown"),
                    )
                    for col in table_data.get("columns", [])
                ]
                tables.append(Table(name=table_data.get("name", ""), columns=columns))

        return cls(tables=tables)


# Documentation models
DocType = Literal[
    "charts",
    "data",
    "inputs",
    "ui",
    "maps",
    "custom",
    "core-concepts",
    "data-sources",
    "deployment",
    "guides",
    "reference",
    "plugins",
    "getting-started",
    # Legacy aliases
    "components",
    "layouts",
    "syntax",
    "queries",
]


class DocResponse(BaseModel):
    """Response from read_docs tool."""

    doc_type: DocType
    component: Optional[str] = None
    title: str
    content: str
    related_docs: list[str] = Field(default_factory=list)


# Edit page models
class EditPageResponse(BaseModel):
    """Response from edit_page tool."""

    success: bool
    description: str
    content: str
    warnings: list[str] = Field(default_factory=list)


# Debug models
class FixSuggestion(BaseModel):
    """A suggested fix for a validation error."""

    error_index: int
    description: str
    suggested_fix: str
    line_range: Optional[tuple[int, int]] = None


class DebugResponse(BaseModel):
    """Response from debug_code tool."""

    analysis: str
    suggestions: list[FixSuggestion] = Field(default_factory=list)
    fixed_content: Optional[str] = None
