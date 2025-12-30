"""Main MCP server for Evidence AI Assistant."""

import logging
import re
import sys
from typing import Annotated, Literal, Optional

from mcp.server.fastmcp import FastMCP

from .config import settings
from .models.schemas import (
    DebugResponse,
    EditPageResponse,
    FixSuggestion,
    MetadataResponse,
)
from .services.doc_registry import DocRegistry
from .services.evidence_client import EvidenceClient

# Configure logging to stderr (important for STDIO transport)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP(name=settings.server_name)

# Initialize services (lazy initialization)
_evidence_client: Optional[EvidenceClient] = None
_doc_registry: Optional[DocRegistry] = None


def get_evidence_client() -> EvidenceClient:
    """Get or create the Evidence client."""
    global _evidence_client
    if _evidence_client is None:
        _evidence_client = EvidenceClient(
            base_url=settings.evidence_dev_url,
            evidence_project_path=settings.evidence_project_path,
        )
    return _evidence_client


def get_doc_registry() -> DocRegistry:
    """Get or create the doc registry."""
    global _doc_registry
    if _doc_registry is None:
        _doc_registry = DocRegistry(docs_path=settings.get_docs_path())
    return _doc_registry


# Type alias for doc_type parameter
DocType = Literal["components", "charts", "inputs", "syntax", "queries", "layouts"]


@mcp.tool()
async def get_metadata() -> dict:
    """Returns database schema from Evidence's DuckDB connection.

    Returns a JSON object with tables and their columns, including data types.
    Use this to understand what data is available for queries.

    Returns:
        Dictionary with 'tables' array, each containing 'name' and 'columns'
    """
    client = get_evidence_client()
    try:
        manifest = await client.get_schema_metadata()
        response = MetadataResponse.from_manifest(manifest)
        return response.model_dump()
    except RuntimeError as e:
        return {"error": str(e), "tables": []}


@mcp.tool()
async def read_docs(
    doc_type: Annotated[
        DocType,
        "Category of documentation: components, charts, inputs, syntax, queries, or layouts",
    ],
    component: Annotated[
        Optional[str],
        "Specific component name (e.g., 'LineChart', 'Dropdown'). If not provided, returns category overview.",
    ] = None,
) -> dict:
    """Retrieves Evidence documentation using hierarchical lookup.

    Looks up documentation for Evidence components, charts, inputs, syntax features,
    queries, or layout components. If a specific component is not found, returns
    the category overview with suggestions for available topics.

    Returns:
        Dictionary with 'title', 'content', and 'related_docs' for further exploration
    """
    registry = get_doc_registry()
    response = registry.lookup(doc_type, component)
    return response.model_dump()


@mcp.tool()
async def edit_page(
    description: Annotated[str, "Brief description of the changes being made"],
    edit: Annotated[str, "Complete modified page content (full file replacement)"],
) -> dict:
    """Proposes changes to the current Evidence markdown page.

    Validates the proposed content for common Evidence syntax issues and returns
    the content with any warnings detected.

    Returns:
        Dictionary with 'success', 'description', 'content', and 'warnings' list
    """
    warnings = validate_evidence_content(edit)

    return EditPageResponse(
        success=True,
        description=description,
        content=edit,
        warnings=warnings,
    ).model_dump()


@mcp.tool()
async def debug_code(
    errors: Annotated[
        list[dict],
        "Array of error objects with 'message', 'line' (optional), 'column' (optional), 'type' (optional)",
    ],
    page_content: Annotated[str, "Current page content containing errors"],
) -> dict:
    """Analyzes validation errors and suggests fixes.

    Examines the provided errors and page content to identify issues and
    generate actionable fix suggestions.

    Returns:
        Dictionary with 'analysis', 'suggestions' list, and optionally 'fixed_content'
    """
    suggestions = []
    analysis_parts = []

    for i, error in enumerate(errors):
        message = error.get("message", "Unknown error")
        line = error.get("line")

        analysis_parts.append(f"Error {i + 1}: {message}")
        if line:
            analysis_parts.append(f"  Location: line {line}")

        # Generate suggestions based on error patterns
        suggestion = analyze_error(error, page_content, i)
        if suggestion:
            suggestions.append(suggestion)

    analysis = "\n".join(analysis_parts) if analysis_parts else "No errors to analyze."

    return DebugResponse(
        analysis=analysis,
        suggestions=suggestions,
        fixed_content=None,  # Let the LLM decide on fixes
    ).model_dump()


def validate_evidence_content(content: str) -> list[str]:
    """Validate Evidence markdown content for common issues.

    Args:
        content: The Evidence markdown content to validate

    Returns:
        List of warning messages
    """
    warnings = []

    # Check for balanced code fences
    fence_count = content.count("```")
    if fence_count % 2 != 0:
        warnings.append("Unbalanced code fences detected (odd number of ```)")

    # Check for SQL queries without names
    # Count all SQL blocks
    all_sql_pattern = r"```sql\b"
    sql_blocks = re.findall(all_sql_pattern, content)
    # Count named SQL blocks (sql followed by space/tab and a name, not newline)
    named_sql_pattern = r"```sql[ \t]+\w+"
    named_sql_blocks = re.findall(named_sql_pattern, content)
    if len(sql_blocks) > len(named_sql_blocks):
        warnings.append(
            "Some SQL code blocks may be missing query names. "
            "Use format: ```sql query_name"
        )

    # Check for markdown tables (should use DataTable instead)
    if re.search(r"^\|.*\|.*\|$", content, re.MULTILINE):
        warnings.append(
            "Markdown table detected. Consider using <DataTable data={query} /> instead."
        )

    # Check for unclosed component tags
    open_tags = re.findall(r"<(\w+)[^/>]*>", content)
    close_tags = re.findall(r"</(\w+)>", content)
    self_closing = re.findall(r"<\w+[^>]*/\s*>", content)

    for tag in open_tags:
        if tag not in close_tags and not any(tag in sc for sc in self_closing):
            # Check if it's a known self-closing component
            known_self_closing = {"Value", "BigValue", "Delta", "Sparkline"}
            if tag not in known_self_closing:
                warnings.append(f"Potentially unclosed <{tag}> tag")

    # Check for common prop issues
    if "data={" in content:
        # Check for quoted query references
        if re.search(r'data=\{["\']', content):
            warnings.append(
                "Query references in data prop should not be quoted. "
                "Use data={query_name} not data={'query_name'}"
            )

    return warnings


def analyze_error(error: dict, content: str, index: int) -> Optional[FixSuggestion]:
    """Analyze a single error and suggest a fix.

    Args:
        error: Error object with message, line, etc.
        content: Page content
        index: Error index

    Returns:
        FixSuggestion if a fix can be suggested, None otherwise
    """
    message = error.get("message", "").lower()
    line = error.get("line")

    # Query reference errors
    if "undefined" in message and "query" in message:
        return FixSuggestion(
            error_index=index,
            description="Query reference error - the referenced query may not exist",
            suggested_fix="Ensure the query is defined in a ```sql query_name code block above the component",
            line_range=(line, line) if line else None,
        )

    # Missing required prop
    if "required" in message and "prop" in message:
        return FixSuggestion(
            error_index=index,
            description="Missing required prop",
            suggested_fix="Add the required prop to the component. Check documentation for required props.",
            line_range=(line, line) if line else None,
        )

    # Syntax errors
    if "syntax" in message or "unexpected" in message:
        return FixSuggestion(
            error_index=index,
            description="Syntax error in component or expression",
            suggested_fix="Check for typos, unclosed brackets, or invalid JavaScript expressions",
            line_range=(line, line) if line else None,
        )

    # Generic suggestion
    if message:
        return FixSuggestion(
            error_index=index,
            description=f"Error: {error.get('message', 'Unknown error')}",
            suggested_fix="Review the error message and check Evidence documentation for correct syntax",
            line_range=(line, line) if line else None,
        )

    return None


def main():
    """Entry point for the MCP server."""
    logger.info(f"Starting {settings.server_name}")
    mcp.run(transport=settings.transport)


if __name__ == "__main__":
    main()
