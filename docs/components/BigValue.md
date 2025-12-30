---
title: BigValue
category: components
related: [Value, Delta, DataTable]
---

# BigValue

Displays a large value standalone with optional comparison and sparkline visualization. Used to highlight key metrics in dashboards and reports.

## Basic Usage

```svelte
<BigValue
    data={orders_summary}
    value=total_orders
/>
```

## Required Props

| Prop | Type | Description |
|------|------|-------------|
| `data` | query | Query name in curly braces |
| `value` | string | Column name for the main metric |

## Optional Props

### Display

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | string | column name | Card header text |
| `fmt` | string | - | Number/date formatting |
| `minWidth` | string | 18% | Minimum component width |
| `maxWidth` | string | - | Maximum component width |
| `link` | string | - | Navigation URL |
| `description` | string | - | Tooltip text on info icon |

### Comparison

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `comparison` | string | - | Column for comparison value |
| `comparisonTitle` | string | - | Label for comparison |
| `comparisonDelta` | boolean | true | Show delta symbol/color |
| `comparisonFmt` | string | - | Format for comparison |
| `downIsGood` | boolean | false | Invert colors (negative=green) |
| `neutralMin` | number | - | Lower bound for neutral coloring |
| `neutralMax` | number | - | Upper bound for neutral coloring |

### Sparkline

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `sparkline` | string | - | Date column for sparkline |
| `sparklineType` | string | line | Chart type: line, area, bar |
| `sparklineColor` | string | - | CSS color for sparkline |
| `sparklineYScale` | boolean | false | Truncate y-axis |
| `sparklineValueFmt` | string | - | Tooltip value format |
| `sparklineDateFmt` | string | YYYY-MM-DD | Tooltip date format |
| `connectGroup` | string | - | Group for synced tooltips |

### Error Handling

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `emptySet` | string | error | Behavior: error, warn, pass |
| `emptyMessage` | string | "No records" | Text for empty data |

## Examples

### With Comparison

```svelte
<BigValue
    data={sales_comparison}
    value=current_sales
    comparison=previous_sales
    comparisonTitle="vs Last Period"
    fmt=usd
/>
```

### With Sparkline

```svelte
<BigValue
    data={daily_orders}
    value=total_orders
    sparkline=order_date
    sparklineType=area
    sparklineColor=#4CAF50
    title="Daily Orders"
/>
```

### Inverted Delta Colors

```svelte
<BigValue
    data={cost_metrics}
    value=current_cost
    comparison=cost_change
    downIsGood=true
    fmt=usd
    title="Operating Cost"
/>
```

### With Link

```svelte
<BigValue
    data={revenue_summary}
    value=total_revenue
    title="Total Revenue"
    fmt=usd
    link="/revenue-details"
/>
```

### Multiple BigValues

```svelte
<Grid cols=3>
    <BigValue data={kpis} value=revenue fmt=usd title="Revenue"/>
    <BigValue data={kpis} value=orders fmt=num0 title="Orders"/>
    <BigValue data={kpis} value=avg_order fmt=usd title="Avg Order"/>
</Grid>
```
