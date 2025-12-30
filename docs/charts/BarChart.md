---
title: BarChart
category: charts
related: [LineChart, AreaChart, Histogram]
---

# BarChart

Use bar or column charts to compare a metric across categories.

## Basic Usage

```svelte
<BarChart
    data={orders_by_category}
    x=category
    y=sales
    title="Sales by Category"
/>
```

## Required Props

| Prop | Type | Description |
|------|------|-------------|
| `data` | query | Query name, wrapped in curly braces |
| `x` | string | Column for x-axis (defaults to first column) |
| `y` | string/array | Column(s) for y-axis |

## Optional Props

### Data Configuration

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `y2` | string/array | - | Column(s) for secondary y-axis |
| `series` | string | - | Column for grouping into multi-series |
| `type` | string | stacked | Grouping method: stacked, grouped, stacked100 |
| `sort` | boolean | true | Apply default sorting |
| `swapXY` | boolean | false | Create horizontal bars |
| `stackName` | string | - | Name for individual stacks |

### Formatting

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `xFmt` | string | - | Format for x-axis |
| `yFmt` | string | - | Format for y-axis |
| `y2Fmt` | string | - | Format for secondary y-axis |
| `colorPalette` | array | - | Array of custom colors |
| `seriesColors` | object | - | Map specific colors to series |
| `seriesOrder` | array | - | Define series display order |

### Labels

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `labels` | boolean | false | Show value labels |
| `stackTotalLabel` | boolean | true | Show stack totals |
| `labelPosition` | string | outside | Label position: outside, inside |

### Axes

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `xAxisTitle` | string | - | X-axis label |
| `yAxisTitle` | string | - | Y-axis label |
| `yMin` / `yMax` | number | - | Y-axis range |
| `yLog` | boolean | false | Logarithmic scale |
| `yGridlines` | boolean | true | Show horizontal gridlines |

### Chart Properties

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | string | - | Chart title |
| `subtitle` | string | - | Chart subtitle |
| `legend` | boolean | auto | Show legend (auto for multi-series) |
| `chartAreaHeight` | number | 180 | Minimum height in pixels |

## Examples

### Stacked Bar Chart

```svelte
<BarChart
    data={orders_by_category}
    x=month
    y=sales
    series=category
    type=stacked
    title="Sales by Category"
/>
```

### Horizontal Bar Chart

```svelte
<BarChart
    data={top_products}
    x=product_name
    y=revenue
    swapXY=true
    title="Top Products by Revenue"
/>
```

### 100% Stacked

```svelte
<BarChart
    data={category_mix}
    x=month
    y=sales
    series=category
    type=stacked100
    yFmt=pct0
    title="Category Mix Over Time"
/>
```

### Grouped Bars

```svelte
<BarChart
    data={quarterly_comparison}
    x=quarter
    y=value
    series=year
    type=grouped
    title="Year over Year Comparison"
/>
```

### Dual Axis

```svelte
<BarChart
    data={orders_by_month}
    x=month
    y=sales_usd0k
    y2=num_orders
    yAxisTitle="Sales ($K)"
    y2AxisTitle="Order Count"
/>
```
