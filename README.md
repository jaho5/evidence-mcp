# Evidence MCP Server

An MCP (Model Context Protocol) server that provides tools for AI assistants to help users create Evidence reports and dashboards.

## Installation

```bash
# Clone and install
git clone https://github.com/jaho5/evidence-mcp.git
cd evidence-mcp
uv sync
```

## Usage

```bash
# Run the MCP server
uv run evidence-mcp

# With custom Evidence project path
EVIDENCE_MCP_EVIDENCE_PROJECT_PATH=/path/to/project uv run evidence-mcp
```

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `EVIDENCE_MCP_EVIDENCE_DEV_URL` | `http://localhost:3000` | Evidence dev server URL |
| `EVIDENCE_MCP_EVIDENCE_PROJECT_PATH` | - | Path to Evidence project |
| `EVIDENCE_MCP_TRANSPORT` | `stdio` | Transport mode: stdio, sse |

## Tools

### get_metadata
Returns database schema from Evidence's DuckDB connection.

### read_docs
Retrieves Evidence documentation using hierarchical lookup.

### edit_page
Proposes changes to the current Evidence markdown page.

### debug_code
Analyzes validation errors and suggests fixes.

---

## Claude Code Setup

Add to your Claude Code MCP settings (`~/.claude.json`):

```json
{
  "mcpServers": {
    "evidence-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/evidence-mcp", "evidence-mcp"],
      "env": {
        "EVIDENCE_MCP_EVIDENCE_PROJECT_PATH": "/path/to/your/evidence/project"
      }
    }
  }
}
```

Or add via CLI:

```bash
claude mcp add evidence-mcp -- uv run --directory /path/to/evidence-mcp evidence-mcp
```

To verify installation:

```bash
claude mcp list
```

---

## Claude Desktop Setup

Add to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "evidence-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/evidence-mcp", "evidence-mcp"],
      "env": {
        "EVIDENCE_MCP_EVIDENCE_PROJECT_PATH": "/path/to/your/evidence/project"
      }
    }
  }
}
```

---

## Programmatic Usage

### Using the MCP Python SDK

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "--directory", "/path/to/evidence-mcp", "evidence-mcp"],
        env={
            "EVIDENCE_MCP_EVIDENCE_PROJECT_PATH": "/path/to/your/evidence/project"
        }
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("Available tools:", [t.name for t in tools.tools])

            # Call get_metadata
            result = await session.call_tool("get_metadata", arguments={})
            print("Metadata:", result.content)

            # Call read_docs
            result = await session.call_tool("read_docs", arguments={
                "doc_type": "charts",
                "component": "LineChart"
            })
            print("Docs:", result.content)

            # Call edit_page
            result = await session.call_tool("edit_page", arguments={
                "description": "Add a sales chart",
                "edit": "# Sales Report\n\n```sql sales\nSELECT * FROM orders\n```\n\n<LineChart data={sales} x=date y=amount/>"
            })
            print("Edit result:", result.content)

            # Call debug_code
            result = await session.call_tool("debug_code", arguments={
                "errors": [{"message": "Unknown query 'sales'", "line": 5}],
                "page_content": "<LineChart data={sales}/>"
            })
            print("Debug result:", result.content)

asyncio.run(main())
```

### Direct Import (for embedding)

```python
import asyncio
from evidence_mcp.server import get_metadata, read_docs, edit_page, debug_code
from evidence_mcp.services.doc_registry import DocRegistry
from evidence_mcp.services.evidence_client import EvidenceClient
from evidence_mcp.config import settings

async def example():
    # Use the tools directly

    # Get documentation
    registry = DocRegistry(docs_path=settings.get_docs_path())
    doc = registry.lookup("charts", "LineChart")
    print(f"Title: {doc.title}")
    print(f"Content: {doc.content[:200]}...")

    # Validate content
    from evidence_mcp.server import validate_evidence_content
    warnings = validate_evidence_content("""
    ```sql
    SELECT * FROM orders
    ```
    <LineChart data={query}/>
    """)
    print(f"Warnings: {warnings}")

asyncio.run(example())
```

### Using with LangChain

```python
from langchain_core.tools import tool
from evidence_mcp.server import validate_evidence_content
from evidence_mcp.services.doc_registry import DocRegistry
from evidence_mcp.config import settings

registry = DocRegistry(docs_path=settings.get_docs_path())

@tool
def evidence_read_docs(doc_type: str, component: str = None) -> dict:
    """Look up Evidence documentation for a component."""
    return registry.lookup(doc_type, component).model_dump()

@tool
def evidence_validate(content: str) -> list[str]:
    """Validate Evidence markdown content."""
    return validate_evidence_content(content)

# Use with your LangChain agent
tools = [evidence_read_docs, evidence_validate]
```

### Using with OpenAI Function Calling

```python
import json
from openai import OpenAI
from evidence_mcp.services.doc_registry import DocRegistry
from evidence_mcp.server import validate_evidence_content
from evidence_mcp.config import settings

client = OpenAI()
registry = DocRegistry(docs_path=settings.get_docs_path())

# Define tools in OpenAI format
tools = [
    {
        "type": "function",
        "function": {
            "name": "read_docs",
            "description": "Look up Evidence documentation",
            "parameters": {
                "type": "object",
                "properties": {
                    "doc_type": {
                        "type": "string",
                        "enum": ["components", "charts", "inputs", "syntax", "queries", "layouts"]
                    },
                    "component": {"type": "string"}
                },
                "required": ["doc_type"]
            }
        }
    }
]

def handle_tool_call(name: str, args: dict) -> str:
    if name == "read_docs":
        result = registry.lookup(args["doc_type"], args.get("component"))
        return json.dumps(result.model_dump())
    return json.dumps({"error": "Unknown tool"})

# Use in chat completion
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "How do I create a line chart in Evidence?"}],
    tools=tools
)

if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        result = handle_tool_call(
            tool_call.function.name,
            json.loads(tool_call.function.arguments)
        )
        print(result)
```

---

## Development

```bash
# Install with dev dependencies
uv sync --extra dev

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=evidence_mcp

# Lint
uv run ruff check

# Format
uv run ruff format
```

