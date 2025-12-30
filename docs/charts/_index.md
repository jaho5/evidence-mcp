---
title: Charts Overview
category: charts
related: [LineChart, BarChart, AreaChart, ScatterPlot, Heatmap]
---

# Charts

Evidence provides a variety of chart components for data visualization. All charts share common props for styling, formatting, and interactivity.

## Available Charts

- **LineChart** - Display how metrics vary over time
- **BarChart** - Compare metrics across categories
- **AreaChart** - Show cumulative values over time
- **ScatterPlot** - Visualize relationships between variables
- **Histogram** - Display distribution of values
- **BoxPlot** - Show statistical distributions
- **Heatmap** - Display values in a matrix format
- **FunnelChart** - Visualize conversion funnels
- **SankeyDiagram** - Show flow between categories
- **Sparkline** - Compact inline charts

## Common Props

All charts support these common props:

| Prop | Type | Description |
|------|------|-------------|
| `data` | query | Query name, wrapped in curly braces |
| `x` | string | Column for x-axis |
| `y` | string/array | Column(s) for y-axis |
| `title` | string | Chart title |
| `subtitle` | string | Chart subtitle |
| `xFmt` / `yFmt` | string | Format strings for axes |
| `legend` | boolean | Show/hide legend |
| `chartAreaHeight` | number | Minimum height in pixels |

## Format Strings

Common format codes:
- `usd` - Currency ($1,234.56)
- `pct` / `pct0` / `pct2` - Percentages
- `num0` / `num2` - Numbers with decimals
- `date` - Date formatting

## Basic Example

```sql orders_by_month
SELECT
    date_trunc('month', order_date) as month,
    SUM(amount) as total_sales
FROM orders
GROUP BY 1
ORDER BY 1
```

```svelte
<LineChart
    data={orders_by_month}
    x=month
    y=total_sales
    yFmt=usd
    title="Monthly Sales"
/>
```
