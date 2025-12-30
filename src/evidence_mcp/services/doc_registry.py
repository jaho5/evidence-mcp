"""Documentation registry service for hierarchical doc lookup."""

import logging
from pathlib import Path
from typing import Optional

import frontmatter

from ..models.schemas import DocResponse, DocType

logger = logging.getLogger(__name__)

# Registry mapping doc_type -> component -> relative file path
DOC_REGISTRY: dict[str, dict[str, str]] = {
    "components": {
        "_index": "components/_index.md",
        "Value": "components/Value.md",
        "BigValue": "components/BigValue.md",
        "DataTable": "components/DataTable.md",
        "Delta": "components/Delta.md",
    },
    "charts": {
        "_index": "charts/_index.md",
        "LineChart": "charts/LineChart.md",
        "BarChart": "charts/BarChart.md",
        "AreaChart": "charts/AreaChart.md",
        "ScatterPlot": "charts/ScatterPlot.md",
        "Histogram": "charts/Histogram.md",
        "BoxPlot": "charts/BoxPlot.md",
        "BubbleChart": "charts/BubbleChart.md",
        "Heatmap": "charts/Heatmap.md",
        "CalendarHeatmap": "charts/CalendarHeatmap.md",
        "FunnelChart": "charts/FunnelChart.md",
        "SankeyDiagram": "charts/SankeyDiagram.md",
        "Sparkline": "charts/Sparkline.md",
    },
    "inputs": {
        "_index": "inputs/_index.md",
        "Dropdown": "inputs/Dropdown.md",
        "ButtonGroup": "inputs/ButtonGroup.md",
        "TextInput": "inputs/TextInput.md",
        "DateInput": "inputs/DateInput.md",
        "DateRange": "inputs/DateRange.md",
        "Slider": "inputs/Slider.md",
        "Checkbox": "inputs/Checkbox.md",
        "DimensionGrid": "inputs/DimensionGrid.md",
    },
    "syntax": {
        "_index": "syntax/_index.md",
        "queries": "syntax/queries.md",
        "expressions": "syntax/expressions.md",
        "loops": "syntax/loops.md",
        "conditionals": "syntax/conditionals.md",
        "frontmatter": "syntax/frontmatter.md",
    },
    "queries": {
        "_index": "queries/_index.md",
        "basics": "queries/basics.md",
        "chaining": "queries/chaining.md",
        "parameters": "queries/parameters.md",
    },
    "layouts": {
        "_index": "layouts/_index.md",
        "Grid": "layouts/Grid.md",
        "Tabs": "layouts/Tabs.md",
        "Accordion": "layouts/Accordion.md",
        "Alert": "layouts/Alert.md",
        "Modal": "layouts/Modal.md",
        "Details": "layouts/Details.md",
    },
}


class DocRegistry:
    """Service for looking up Evidence documentation."""

    def __init__(self, docs_path: Path):
        """Initialize the doc registry.

        Args:
            docs_path: Path to the directory containing documentation files
        """
        self.docs_path = docs_path

    def _find_file(self, doc_type: DocType, component: Optional[str]) -> Optional[Path]:
        """Find the documentation file for a given doc_type and component.

        Args:
            doc_type: Category of documentation
            component: Optional specific component name

        Returns:
            Path to the documentation file, or None if not found
        """
        category = DOC_REGISTRY.get(doc_type, {})

        if component:
            # Try exact match
            if component in category:
                file_path = self.docs_path / category[component]
                if file_path.exists():
                    return file_path

            # Try case-insensitive match
            component_lower = component.lower()
            for key, path in category.items():
                if key.lower() == component_lower:
                    file_path = self.docs_path / path
                    if file_path.exists():
                        return file_path

        # Fallback to category index
        if "_index" in category:
            file_path = self.docs_path / category["_index"]
            if file_path.exists():
                return file_path

        return None

    def _get_related_docs(self, doc_type: DocType, component: Optional[str]) -> list[str]:
        """Get related documentation suggestions.

        Args:
            doc_type: Category of documentation
            component: Optional specific component name

        Returns:
            List of related component/topic names
        """
        category = DOC_REGISTRY.get(doc_type, {})
        related = [key for key in category.keys() if key != "_index" and key != component]
        return related[:5]  # Limit to 5 suggestions

    def lookup(self, doc_type: DocType, component: Optional[str] = None) -> DocResponse:
        """Look up documentation for a given doc_type and component.

        Args:
            doc_type: Category of documentation
            component: Optional specific component name

        Returns:
            DocResponse containing the documentation content
        """
        file_path = self._find_file(doc_type, component)

        if file_path is None:
            # Return a helpful message if no docs found
            available = list(DOC_REGISTRY.get(doc_type, {}).keys())
            available = [a for a in available if a != "_index"]

            return DocResponse(
                doc_type=doc_type,
                component=component,
                title="Documentation not found",
                content=f"No documentation found for '{component}' in '{doc_type}'.\n\n"
                f"Available topics: {', '.join(available)}",
                related_docs=available[:5],
            )

        # Parse the markdown file with frontmatter
        try:
            post = frontmatter.load(file_path)
            title = post.get("title", component or doc_type.capitalize())
            content = post.content
            related = post.get("related", self._get_related_docs(doc_type, component))
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {e}")
            # Fallback to raw content
            title = component or doc_type.capitalize()
            content = file_path.read_text()
            related = self._get_related_docs(doc_type, component)

        return DocResponse(
            doc_type=doc_type,
            component=component,
            title=title,
            content=content,
            related_docs=related if isinstance(related, list) else [related],
        )
