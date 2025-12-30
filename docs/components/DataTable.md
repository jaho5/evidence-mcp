---
title: DataTable
category: components
related: [Value, BigValue, Delta]
---

# DataTable

Display richly formatted data from queries in a dense, readable table format. Supports sorting, searching, pagination, and conditional formatting.

## Basic Usage

```svelte
<DataTable data={orders_summary}/>
```

## Core Props

### Data & Display

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data` | query | required | Query name in curly braces |
| `rows` | number/string | 10 | Rows before pagination (use `rows=all` for all) |
| `title` | string | - | Table title |
| `subtitle` | string | - | Subtitle under title |
| `sortable` | boolean | true | Enable column sorting |
| `sort` | string | - | Initial sort column (e.g., "sales desc") |
| `search` | boolean | false | Add search bar |
| `downloadable` | boolean | true | Enable download button |

### Styling

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `headerColor` | string | - | Header background color |
| `headerFontColor` | string | - | Header text color |
| `backgroundColor` | string | - | Table background color |
| `rowShading` | boolean | false | Alternate row shading |
| `rowLines` | boolean | true | Show row borders |
| `rowNumbers` | boolean | false | Display row index |
| `compact` | boolean | false | More compact layout |
| `wrapTitles` | boolean | false | Wrap column titles |

### Totals

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `totalRow` | boolean | false | Display total row |
| `totalRowColor` | string | - | Total row background |
| `totalFontColor` | string | - | Total row text color |

### Grouping

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `groupBy` | string | - | Column for creating groups |
| `groupType` | string | accordion | Type: accordion or section |
| `subtotals` | boolean | false | Show group subtotals |
| `groupsOpen` | boolean | true | Accordion open by default |

### Navigation

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `link` | string | - | Column containing URLs for row clicks |
| `showLinkCol` | boolean | false | Display link column |

## Column Configuration

Customize columns using nested `<Column>` components:

```svelte
<DataTable data={orders}>
    <Column id=state title="Sales State"/>
    <Column id=sales fmt=usd/>
</DataTable>
```

### Column Props

| Prop | Type | Description |
|------|------|-------------|
| `id` | string | Column identifier from query (required) |
| `title` | string | Override column title |
| `align` | string | Alignment: left, center, right |
| `fmt` | string | Format code (e.g., usd, pct2, #,##0) |
| `wrap` | boolean | Wrap text |
| `totalAgg` | string | Aggregation for totals: sum, mean, median, min, max, count |
| `contentType` | string | Special content: link, image, delta, colorscale, bar, sparkline |

### Content Types

#### Delta

```svelte
<Column id=growth contentType=delta fmt=pct deltaSymbol=true/>
```

#### Colorscale

```svelte
<Column id=value contentType=colorscale colorScale=#a85ab8/>
```

#### Bar

```svelte
<Column id=sales contentType=bar barColor=#53768a/>
```

#### Sparkline

```svelte
<Column id=sales_trend contentType=sparkline sparkX=date sparkY=sales/>
```

## Examples

### With Search and Sorting

```svelte
<DataTable data={orders} search=true sort="sales desc">
    <Column id=category/>
    <Column id=sales fmt=usd/>
</DataTable>
```

### With Totals

```svelte
<DataTable data={countries} totalRow=true rows=5>
    <Column id=country/>
    <Column id=gdp_usd totalAgg=sum fmt='$#,##0"B"'/>
</DataTable>
```

### Grouped with Subtotals

```svelte
<DataTable data={sales} groupBy=region subtotals=true>
    <Column id=region/>
    <Column id=store/>
    <Column id=sales fmt=usd totalAgg=sum/>
</DataTable>
```

### Conditional Formatting

```svelte
<DataTable data={performance}>
    <Column id=name/>
    <Column id=change contentType=delta fmt=pct/>
    <Column id=score contentType=colorscale colorScale=green/>
</DataTable>
```
