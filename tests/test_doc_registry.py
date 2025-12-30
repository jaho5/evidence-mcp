"""Tests for the DocRegistry service."""

import pytest

from evidence_mcp.services.doc_registry import DocRegistry


@pytest.fixture
def temp_docs(tmp_path):
    """Create temporary documentation files for testing."""
    # Create directory structure
    charts_dir = tmp_path / "charts"
    charts_dir.mkdir()
    components_dir = tmp_path / "components"
    components_dir.mkdir()

    # Create index file
    (charts_dir / "_index.md").write_text(
        """---
title: Charts Overview
category: charts
---

# Charts

Overview of chart components.
"""
    )

    # Create component file
    (charts_dir / "LineChart.md").write_text(
        """---
title: LineChart
category: charts
related: [BarChart, AreaChart]
---

# LineChart

Display data over time.

## Basic Usage

```svelte
<LineChart data={query} x=date y=value/>
```
"""
    )

    return tmp_path


@pytest.fixture
def registry(temp_docs):
    """Create a DocRegistry with temporary docs."""
    return DocRegistry(docs_path=temp_docs)


def test_lookup_specific_component(registry):
    """Test looking up a specific component."""
    result = registry.lookup("charts", "LineChart")

    assert result.doc_type == "charts"
    assert result.component == "LineChart"
    assert result.title == "LineChart"
    assert "Display data over time" in result.content
    assert "BarChart" in result.related_docs


def test_lookup_case_insensitive(registry):
    """Test case-insensitive component lookup."""
    result = registry.lookup("charts", "linechart")

    assert result.title == "LineChart"
    assert "LineChart" in result.content


def test_lookup_fallback_to_index(registry):
    """Test fallback to category index for unknown component."""
    result = registry.lookup("charts", "NonExistentChart")

    assert result.doc_type == "charts"
    assert "Overview" in result.title
    assert "Overview of chart components" in result.content


def test_lookup_category_index(registry):
    """Test looking up category index directly."""
    result = registry.lookup("charts", None)

    assert result.doc_type == "charts"
    assert "Overview" in result.title


def test_lookup_missing_component_in_valid_category(registry):
    """Test looking up a missing component in a valid but empty category."""
    # components category exists in registry but has no files in our temp fixture
    result = registry.lookup("components", "MissingComponent")

    # Should fall back to index or show not found message
    assert result.doc_type == "components"


def test_related_docs_extraction(registry):
    """Test that related docs are extracted from frontmatter."""
    result = registry.lookup("charts", "LineChart")

    assert isinstance(result.related_docs, list)
    assert "BarChart" in result.related_docs
    assert "AreaChart" in result.related_docs
