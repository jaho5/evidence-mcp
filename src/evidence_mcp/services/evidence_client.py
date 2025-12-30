"""Evidence dev server integration client."""

import json
import logging
from pathlib import Path
from typing import Optional

import httpx

logger = logging.getLogger(__name__)


class EvidenceClient:
    """Client for interacting with Evidence dev server and project files."""

    def __init__(
        self,
        base_url: str = "http://localhost:3000",
        evidence_project_path: Optional[Path] = None,
    ):
        """Initialize the Evidence client.

        Args:
            base_url: URL of the Evidence dev server
            evidence_project_path: Optional path to the Evidence project directory
        """
        self.base_url = base_url.rstrip("/")
        self.project_path = evidence_project_path
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=30.0)
        return self._client

    def _parse_evidence_schema_files(self, data_dir: Path) -> dict:
        """Parse Evidence's actual schema structure.

        Evidence stores data as:
        - manifest.json: {"renderedFiles": {"source_name": ["path/to/table.parquet"]}}
        - Per-table schema: static/data/{source}/{table}/{table}.schema.json

        Returns:
            Dictionary in normalized format with sources/tables/columns
        """
        manifest_path = data_dir / "manifest.json"
        if not manifest_path.exists():
            return {"sources": {}}

        manifest = json.loads(manifest_path.read_text())
        rendered_files = manifest.get("renderedFiles", {})

        sources = {}
        for source_name, file_paths in rendered_files.items():
            tables = {}
            for file_path in file_paths:
                # Extract table name from path like "static/data/source/table/table.parquet"
                parts = Path(file_path).parts
                if len(parts) >= 2:
                    table_name = parts[-2]  # e.g., "orders" from ".../orders/orders.parquet"

                    # Look for schema file
                    schema_path = data_dir / source_name / table_name / f"{table_name}.schema.json"
                    if schema_path.exists():
                        schema_data = json.loads(schema_path.read_text())
                        columns = []
                        for col in schema_data:
                            columns.append({
                                "name": col.get("name", ""),
                                "type": self._map_evidence_type(col.get("evidenceType", "unknown")),
                            })
                        tables[table_name] = {"columns": columns}
                    else:
                        logger.warning(f"Schema file not found: {schema_path}")
                        tables[table_name] = {"columns": []}

            if tables:
                sources[source_name] = {"tables": tables}

        return {"sources": sources}

    def _map_evidence_type(self, evidence_type: str) -> str:
        """Map Evidence types to SQL-like types."""
        type_map = {
            "number": "Float64",
            "string": "String",
            "date": "Date",
            "boolean": "Boolean",
        }
        return type_map.get(evidence_type, evidence_type)

    async def get_schema_metadata(self) -> dict:
        """Retrieve schema metadata from Evidence.

        Strategy:
        1. Try HTTP endpoint if dev server is running
        2. Fallback to reading schema files from project directory

        Returns:
            Dictionary containing table and column metadata

        Raises:
            RuntimeError: If unable to retrieve metadata from any source
        """
        # Try live dev server first
        try:
            client = await self._get_client()
            response = await client.get(f"{self.base_url}/_evidence/manifest.json")
            if response.status_code == 200:
                logger.info("Retrieved manifest from Evidence dev server")
                # Dev server returns same format, need to parse schema files
                # Fall through to file-based parsing
        except httpx.RequestError as e:
            logger.debug(f"Could not connect to Evidence dev server: {e}")

        # Parse from file system (works for both dev and built projects)
        if self.project_path:
            data_dirs = [
                self.project_path / ".evidence" / "template" / "static" / "data",
                self.project_path / "static" / "data",
            ]

            for data_dir in data_dirs:
                if data_dir.exists():
                    result = self._parse_evidence_schema_files(data_dir)
                    if result.get("sources"):
                        logger.info(f"Parsed schema from {data_dir}")
                        return result

        raise RuntimeError(
            "Unable to retrieve Evidence schema metadata. "
            "Ensure the Evidence dev server is running or provide a valid project path. "
            f"Checked project path: {self.project_path}"
        )

    async def check_health(self) -> bool:
        """Check if Evidence dev server is running.

        Returns:
            True if the server is accessible, False otherwise
        """
        try:
            client = await self._get_client()
            response = await client.get(self.base_url)
            return response.status_code == 200
        except httpx.RequestError:
            return False

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
