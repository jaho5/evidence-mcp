"""Documentation registry service for hierarchical doc lookup."""

import logging
from pathlib import Path
from typing import Optional

import frontmatter

from ..models.schemas import DocResponse, DocType

logger = logging.getLogger(__name__)

# Registry mapping doc_type -> component -> relative file path
DOC_REGISTRY: dict[str, dict[str, str]] = {
    # Charts - data visualization components
    "charts": {
        "_index": "components/charts/index.md",
        "LineChart": "components/charts/line-chart/index.md",
        "BarChart": "components/charts/bar-chart/index.md",
        "AreaChart": "components/charts/area-chart/index.md",
        "ScatterPlot": "components/charts/scatter-plot/index.md",
        "Histogram": "components/charts/histogram/index.md",
        "BoxPlot": "components/charts/box-plot/index.md",
        "BubbleChart": "components/charts/bubble-chart/index.md",
        "Heatmap": "components/charts/heatmap/index.md",
        "CalendarHeatmap": "components/charts/calendar-heatmap/index.md",
        "FunnelChart": "components/charts/funnel-chart/index.md",
        "SankeyDiagram": "components/charts/sankey-diagram/index.md",
        "Sparkline": "components/charts/sparkline/index.md",
        "Annotations": "components/charts/annotations/index.md",
        "ReferenceLine": "components/charts/annotations/index.md",
        "ReferenceArea": "components/charts/annotations/index.md",
        "MixedTypeCharts": "components/charts/mixed-type-charts/index.md",
        "CustomECharts": "components/charts/custom-echarts/index.md",
        "EChartsOptions": "components/charts/echarts-options/index.md",
    },
    # Data display components
    "data": {
        "_index": "components/data/index.md",
        "Value": "components/data/value/index.md",
        "BigValue": "components/data/big-value/index.md",
        "DataTable": "components/data/data-table/index.md",
        "Delta": "components/data/delta/index.md",
    },
    # Input components
    "inputs": {
        "_index": "components/inputs/index.md",
        "Dropdown": "components/inputs/dropdown/index.md",
        "ButtonGroup": "components/inputs/button-group/index.md",
        "TextInput": "components/inputs/text-input/index.md",
        "DateInput": "components/inputs/date-input/index.md",
        "DateRange": "components/inputs/date-range/index.md",
        "Slider": "components/inputs/slider/index.md",
        "Checkbox": "components/inputs/checkbox/index.md",
        "DimensionGrid": "components/inputs/dimension-grid/index.md",
    },
    # UI components (layouts, etc.)
    "ui": {
        "_index": "components/ui/index.md",
        "Grid": "components/ui/grid/index.md",
        "Tabs": "components/ui/tabs/index.md",
        "Accordion": "components/ui/accordion/index.md",
        "Alert": "components/ui/alert/index.md",
        "Modal": "components/ui/modal/index.md",
        "Details": "components/ui/details/index.md",
        "BigLink": "components/ui/big-link/index.md",
        "DownloadData": "components/ui/download-data/index.md",
        "Embed": "components/ui/embed/index.md",
        "Image": "components/ui/image/index.md",
        "Info": "components/ui/info/index.md",
        "LastRefreshed": "components/ui/last-refreshed/index.md",
        "Link": "components/ui/link/index.md",
        "LinkButton": "components/ui/link-button/index.md",
        "Note": "components/ui/note/index.md",
        "PrintFormatComponents": "components/ui/print-format-components/index.md",
    },
    # Map components
    "maps": {
        "_index": "components/maps/index.md",
        "AreaMap": "components/maps/area-map/index.md",
        "BaseMap": "components/maps/base-map/index.md",
        "BubbleMap": "components/maps/bubble-map/index.md",
        "PointMap": "components/maps/point-map/index.md",
        "USMap": "components/maps/us-map/index.md",
    },
    # Custom components
    "custom": {
        "_index": "components/custom/index.md",
        "CustomComponent": "components/custom/custom-component/index.md",
        "ComponentQueries": "components/custom/component-queries/index.md",
    },
    # Core concepts
    "core-concepts": {
        "_index": "core-concepts/index.md",
        "queries": "core-concepts/queries/index.md",
        "syntax": "core-concepts/syntax/index.md",
        "components": "core-concepts/components/index.md",
        "pages": "core-concepts/pages/index.md",
        "templated-pages": "core-concepts/templated-pages/index.md",
        "loops": "core-concepts/loops/index.md",
        "if-else": "core-concepts/if-else/index.md",
        "formatting": "core-concepts/formatting/index.md",
        "filters": "core-concepts/filters/index.md",
        "exports": "core-concepts/exports/index.md",
        "themes": "core-concepts/themes/index.md",
        "query-functions": "core-concepts/query-functions/index.md",
    },
    # Data sources
    "data-sources": {
        "_index": "core-concepts/data-sources/index.md",
        "postgres": "core-concepts/data-sources/postgres/index.md",
        "mysql": "core-concepts/data-sources/mysql/index.md",
        "sqlite": "core-concepts/data-sources/sqlite/index.md",
        "duckdb": "core-concepts/data-sources/duckdb/index.md",
        "bigquery": "core-concepts/data-sources/bigquery/index.md",
        "snowflake": "core-concepts/data-sources/snowflake/index.md",
        "redshift": "core-concepts/data-sources/redshift/index.md",
        "databricks": "core-concepts/data-sources/databricks/index.md",
        "mssql": "core-concepts/data-sources/mssql/index.md",
        "trino": "core-concepts/data-sources/trino/index.md",
        "motherduck": "core-concepts/data-sources/motherduck/index.md",
        "csv": "core-concepts/data-sources/csv/index.md",
        "google-sheets": "core-concepts/data-sources/google-sheets/index.md",
        "javascript": "core-concepts/data-sources/javascript/index.md",
    },
    # Deployment
    "deployment": {
        "_index": "deployment/index.md",
        "overview": "deployment/overview/index.md",
        "configuration": "deployment/configuration/index.md",
        "environments": "deployment/configuration/environments/index.md",
        "rendering-modes": "deployment/configuration/rendering-modes/index.md",
        "base-paths": "deployment/configuration/base-paths/index.md",
        "vercel": "deployment/self-host/vercel/index.md",
        "netlify": "deployment/self-host/netlify/index.md",
        "cloudflare-pages": "deployment/self-host/cloudflare-pages/index.md",
        "github-pages": "deployment/self-host/github-pages/index.md",
        "gitlab-pages": "deployment/self-host/gitlab-pages/index.md",
        "aws-amplify": "deployment/self-host/aws-amplify/index.md",
        "azure-static-apps": "deployment/self-host/azure-static-apps/index.md",
        "firebase": "deployment/self-host/firebase/index.md",
        "hugging-face-spaces": "deployment/self-host/hugging-face-spaces/index.md",
        "windows-iis": "deployment/self-host/windows-iis/index.md",
    },
    # Guides
    "guides": {
        "_index": "guides/index.md",
        "best-practices": "guides/best-practices/index.md",
        "chart-cheat-sheet": "guides/chart-cheat-sheet/index.md",
        "troubleshooting": "guides/troubleshooting/index.md",
        "updating-your-app": "guides/updating-your-app/index.md",
        "system-requirements": "guides/system-requirements/index.md",
    },
    # Reference
    "reference": {
        "_index": "reference/index.md",
        "cli": "reference/cli/index.md",
        "markdown": "reference/markdown/index.md",
        "layouts": "reference/layouts/index.md",
    },
    # Plugins
    "plugins": {
        "_index": "plugins/index.md",
        "source-plugins": "plugins/source-plugins/index.md",
        "component-plugins": "plugins/component-plugins/index.md",
        "create-source-plugin": "plugins/create-source-plugin/index.md",
        "create-component-plugin": "plugins/create-component-plugin/index.md",
    },
    # Getting started
    "getting-started": {
        "_index": "index.md",
        "install-evidence": "install-evidence/index.md",
        "build-your-first-app": "build-your-first-app/index.md",
        "motivation": "motivation/index.md",
    },
    # Legacy aliases for backwards compatibility
    "components": {
        "_index": "components/index.md",
        "all-components": "components/all-components/index.md",
        # Data components aliased here for discoverability
        "Value": "components/data/value/index.md",
        "BigValue": "components/data/big-value/index.md",
        "DataTable": "components/data/data-table/index.md",
        "Delta": "components/data/delta/index.md",
        # Input components
        "Dropdown": "components/inputs/dropdown/index.md",
        "ButtonGroup": "components/inputs/button-group/index.md",
        "TextInput": "components/inputs/text-input/index.md",
        "DateInput": "components/inputs/date-input/index.md",
        "DateRange": "components/inputs/date-range/index.md",
        "Slider": "components/inputs/slider/index.md",
        "Checkbox": "components/inputs/checkbox/index.md",
        # UI components
        "Grid": "components/ui/grid/index.md",
        "Tabs": "components/ui/tabs/index.md",
        "Accordion": "components/ui/accordion/index.md",
        "Alert": "components/ui/alert/index.md",
        "Modal": "components/ui/modal/index.md",
        "Details": "components/ui/details/index.md",
    },
    "layouts": {
        "_index": "components/ui/index.md",
        "Grid": "components/ui/grid/index.md",
        "Tabs": "components/ui/tabs/index.md",
        "Accordion": "components/ui/accordion/index.md",
        "Alert": "components/ui/alert/index.md",
        "Modal": "components/ui/modal/index.md",
        "Details": "components/ui/details/index.md",
        # Map components aliased here
        "USMap": "components/maps/us-map/index.md",
        "AreaMap": "components/maps/area-map/index.md",
        "PointMap": "components/maps/point-map/index.md",
        "BubbleMap": "components/maps/bubble-map/index.md",
        "BaseMap": "components/maps/base-map/index.md",
    },
    "syntax": {
        "_index": "core-concepts/syntax/index.md",
        "queries": "core-concepts/queries/index.md",
        "loops": "core-concepts/loops/index.md",
        "conditionals": "core-concepts/if-else/index.md",
    },
    "queries": {
        "_index": "core-concepts/queries/index.md",
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
