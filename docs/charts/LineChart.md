---
title: LineChart
category: charts
related: [AreaChart, BarChart, Sparkline]
---

# LineChart

Display how one or more metrics vary over time. Line charts are suitable for plotting a large number of data points on the same chart.

## Basic Usage

```svelte
<LineChart
    data={orders_by_month}
    x=month
    y=sales_usd0k
    yAxisTitle="Sales per Month"
/>
```

## Required Props

| Prop | Type | Description |
|------|------|-------------|
| `data` | query | Query name, wrapped in curly braces |
| `x` | string | Column to use for the x-axis |
| `y` | string/array | Column(s) to use for the y-axis |

## Optional Props

### Data Handling

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `y2` | string/array | - | Column(s) for secondary y-axis |
| `y2SeriesType` | string | line | Chart type for y2 axis (line, bar, scatter) |
| `series` | string | - | Column for grouping into multi-series chart |
| `sort` | boolean | true | Apply default sorting |
| `handleMissing` | string | gap | Treatment of missing values (gap, connect, zero) |

### Styling

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `step` | boolean | false | Display as step line |
| `lineColor` | string | - | Override series color |
| `lineOpacity` | number | 1 | Color transparency (0-1) |
| `lineType` | string | solid | Line style (solid, dashed, dotted) |
| `lineWidth` | number | 2 | Line thickness in pixels |
| `markers` | boolean | false | Show point markers |
| `markerShape` | string | circle | Marker style (circle, emptyCircle, rect, triangle, diamond) |
| `colorPalette` | array | - | Custom color array |

### Labels

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `labels` | boolean | false | Show value labels |
| `labelPosition` | string | above | Label placement (above, middle, below) |
| `xFmt` | string | - | Format string for x-axis |
| `yFmt` | string | - | Format string for y-axis |
| `y2Fmt` | string | - | Format string for secondary y-axis |

### Axes

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `xAxisTitle` | string | - | X-axis label |
| `yAxisTitle` | string | - | Y-axis label |
| `yLog` | boolean | false | Use logarithmic scale |
| `yMin` / `yMax` | number | - | Y-axis bounds |
| `y2Min` / `y2Max` | number | - | Secondary y-axis bounds |
| `xGridlines` | boolean | false | Show vertical gridlines |
| `yGridlines` | boolean | true | Show horizontal gridlines |

### Chart Properties

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | string | - | Chart title |
| `subtitle` | string | - | Chart subtitle |
| `legend` | boolean | true | Show legend |
| `chartAreaHeight` | number | 180 | Minimum height in pixels |
| `downloadableData` | boolean | false | Enable data export button |
| `downloadableImage` | boolean | false | Enable image export button |

## Examples

### Multi-Series Chart

```svelte
<LineChart
    data={sales_by_category}
    x=month
    y=sales
    series=category
    title="Sales by Category"
/>
```

### Dual Y-Axis

```svelte
<LineChart
    data={orders_by_month}
    x=month
    y=sales_usd0k
    y2=orders
    y2SeriesType=bar
    yAxisTitle="Sales"
    y2AxisTitle="Order Count"
/>
```

### Step Line with Markers

```svelte
<LineChart
    data={inventory_levels}
    x=date
    y=stock_level
    step=true
    markers=true
    markerShape=circle
/>
```

### With Annotations

```svelte
<LineChart data={monthly_data} x=month y=value>
    <ReferenceLine y=100 label="Target"/>
    <ReferenceArea xMin="2023-06" xMax="2023-08" label="Peak Season"/>
</LineChart>
```
