"""Tests for Pydantic models."""


from evidence_mcp.models.schemas import (
    Column,
    Table,
    MetadataResponse,
    DocResponse,
    EditPageResponse,
    FixSuggestion,
    DebugResponse,
)


class TestMetadataModels:
    """Tests for metadata-related models."""

    def test_column_creation(self):
        """Test Column model creation."""
        col = Column(name="id", type="Int64")
        assert col.name == "id"
        assert col.type == "Int64"

    def test_table_creation(self):
        """Test Table model creation."""
        table = Table(
            name="source.orders",
            columns=[
                Column(name="id", type="Int64"),
                Column(name="amount", type="Float64"),
            ],
        )
        assert table.name == "source.orders"
        assert len(table.columns) == 2

    def test_metadata_from_manifest_sources_format(self):
        """Test MetadataResponse.from_manifest with sources format."""
        manifest = {
            "sources": {
                "mydb": {
                    "tables": {
                        "orders": {
                            "columns": [
                                {"name": "id", "type": "Int64"},
                                {"name": "total", "type": "Float64"},
                            ]
                        }
                    }
                }
            }
        }

        response = MetadataResponse.from_manifest(manifest)

        assert len(response.tables) == 1
        assert response.tables[0].name == "mydb.orders"
        assert len(response.tables[0].columns) == 2

    def test_metadata_from_manifest_tables_format(self):
        """Test MetadataResponse.from_manifest with flat tables format."""
        manifest = {
            "tables": [
                {
                    "name": "orders",
                    "columns": [
                        {"name": "id", "type": "Int64"},
                    ]
                }
            ]
        }

        response = MetadataResponse.from_manifest(manifest)

        assert len(response.tables) == 1
        assert response.tables[0].name == "orders"

    def test_metadata_empty_manifest(self):
        """Test MetadataResponse with empty manifest."""
        response = MetadataResponse.from_manifest({})
        assert response.tables == []


class TestDocResponse:
    """Tests for DocResponse model."""

    def test_doc_response_creation(self):
        """Test DocResponse creation."""
        response = DocResponse(
            doc_type="charts",
            component="LineChart",
            title="LineChart",
            content="# LineChart\n\nContent here.",
            related_docs=["BarChart", "AreaChart"],
        )

        assert response.doc_type == "charts"
        assert response.component == "LineChart"
        assert len(response.related_docs) == 2

    def test_doc_response_optional_fields(self):
        """Test DocResponse with optional fields."""
        response = DocResponse(
            doc_type="syntax",
            component=None,
            title="Syntax Overview",
            content="Content",
        )

        assert response.component is None
        assert response.related_docs == []


class TestEditPageResponse:
    """Tests for EditPageResponse model."""

    def test_edit_page_response(self):
        """Test EditPageResponse creation."""
        response = EditPageResponse(
            success=True,
            description="Added a new chart",
            content="# Page\n\nContent here.",
            warnings=["Unclosed tag detected"],
        )

        assert response.success is True
        assert len(response.warnings) == 1

    def test_edit_page_response_no_warnings(self):
        """Test EditPageResponse with no warnings."""
        response = EditPageResponse(
            success=True,
            description="Minor edit",
            content="Content",
        )

        assert response.warnings == []


class TestDebugResponse:
    """Tests for debug-related models."""

    def test_fix_suggestion(self):
        """Test FixSuggestion model."""
        suggestion = FixSuggestion(
            error_index=0,
            description="Query not found",
            suggested_fix="Define the query before using it",
            line_range=(10, 10),
        )

        assert suggestion.error_index == 0
        assert suggestion.line_range == (10, 10)

    def test_debug_response(self):
        """Test DebugResponse creation."""
        response = DebugResponse(
            analysis="Found 2 errors",
            suggestions=[
                FixSuggestion(
                    error_index=0,
                    description="Error 1",
                    suggested_fix="Fix 1",
                )
            ],
            fixed_content=None,
        )

        assert "2 errors" in response.analysis
        assert len(response.suggestions) == 1
