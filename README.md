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

## Programmatic Usage (MCP Client)

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

asyncio.run(main())
```

### With OpenAI Agents SDK

First, run the server in SSE mode:

```bash
EVIDENCE_MCP_TRANSPORT=sse \
EVIDENCE_MCP_EVIDENCE_PROJECT_PATH=/path/to/your/evidence/project \
uv run evidence-mcp
```

Then use `HostedMCPTool` to connect:

```python
from agents import Agent, HostedMCPTool

agent = Agent(
    name="Evidence Assistant",
    instructions="Help users create Evidence reports and dashboards.",
    tools=[
        HostedMCPTool(
            tool_config={
                "type": "mcp",
                "server_label": "evidence",
                "server_url": "http://localhost:8000/sse",
                "require_approval": "never",
            }
        )
    ],
)
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

