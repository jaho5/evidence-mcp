"""Tests for the main server module."""


from evidence_mcp.server import validate_evidence_content, analyze_error


class TestValidateEvidenceContent:
    """Tests for the validate_evidence_content function."""

    def test_valid_content_no_warnings(self):
        """Test valid content produces no warnings."""
        content = """
# My Page

```sql orders
SELECT * FROM orders
```

<LineChart data={orders} x=date y=amount/>
"""
        warnings = validate_evidence_content(content)
        assert len(warnings) == 0

    def test_unbalanced_code_fences(self):
        """Test detection of unbalanced code fences."""
        content = """
```sql query
SELECT * FROM table
"""
        warnings = validate_evidence_content(content)
        assert any("Unbalanced" in w for w in warnings)

    def test_sql_without_query_name(self):
        """Test detection of SQL blocks without names."""
        content = """
```sql
SELECT * FROM orders
```

```sql named_query
SELECT * FROM products
```
"""
        warnings = validate_evidence_content(content)
        assert any("missing query names" in w for w in warnings)

    def test_markdown_table_warning(self):
        """Test detection of markdown tables."""
        content = """
| Column 1 | Column 2 |
|----------|----------|
| Value 1  | Value 2  |
"""
        warnings = validate_evidence_content(content)
        assert any("Markdown table" in w for w in warnings)
        assert any("DataTable" in w for w in warnings)

    def test_quoted_query_reference(self):
        """Test detection of quoted query references."""
        content = """
<LineChart data={'my_query'} x=date y=value/>
"""
        warnings = validate_evidence_content(content)
        assert any("should not be quoted" in w for w in warnings)

    def test_unclosed_component_tag(self):
        """Test detection of potentially unclosed tags."""
        content = """
<Grid cols=2>
    <LineChart data={query} x=date y=value/>
"""
        warnings = validate_evidence_content(content)
        assert any("unclosed" in w.lower() for w in warnings)


class TestAnalyzeError:
    """Tests for the analyze_error function."""

    def test_query_reference_error(self):
        """Test analysis of query reference errors."""
        error = {
            "message": "Undefined query 'my_query' referenced",
            "line": 10,
            "type": "reference",
        }
        content = "<LineChart data={my_query}/>"

        suggestion = analyze_error(error, content, 0)

        assert suggestion is not None
        assert suggestion.error_index == 0
        assert "query" in suggestion.description.lower()

    def test_missing_prop_error(self):
        """Test analysis of missing required prop errors."""
        error = {
            "message": "Required prop 'data' is missing",
            "line": 5,
            "type": "component",
        }
        content = "<LineChart x=date y=value/>"

        suggestion = analyze_error(error, content, 0)

        assert suggestion is not None
        assert "required prop" in suggestion.description.lower()

    def test_syntax_error(self):
        """Test analysis of syntax errors."""
        error = {
            "message": "Unexpected token in expression",
            "line": 3,
            "type": "syntax",
        }
        content = "{unclosed expression"

        suggestion = analyze_error(error, content, 0)

        assert suggestion is not None
        assert "syntax" in suggestion.description.lower()

    def test_generic_error(self):
        """Test analysis of generic errors."""
        error = {
            "message": "Some unknown error occurred",
            "line": 1,
        }
        content = "Some content"

        suggestion = analyze_error(error, content, 0)

        assert suggestion is not None
        assert suggestion.error_index == 0
