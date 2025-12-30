---
title: Grid
category: layouts
related: [Tabs, Accordion]
---

# Grid

Create multi-column responsive layouts for dashboards and reports.

## Basic Usage

```svelte
<Grid cols=2>
    <BigValue data={kpi1} value=revenue/>
    <BigValue data={kpi2} value=orders/>
</Grid>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `cols` | number | 2 | Number of columns (1-12) |
| `gapSize` | string | md | Gap between items: sm, md, lg |

## Examples

### Three Column Layout

```svelte
<Grid cols=3>
    <BigValue data={metrics} value=revenue fmt=usd title="Revenue"/>
    <BigValue data={metrics} value=orders fmt=num0 title="Orders"/>
    <BigValue data={metrics} value=customers fmt=num0 title="Customers"/>
</Grid>
```

### Mixed Content

```svelte
<Grid cols=2>
    <LineChart data={trend} x=month y=value title="Trend"/>
    <BarChart data={breakdown} x=category y=amount title="Breakdown"/>
</Grid>
```

### Dashboard Layout

```svelte
<Grid cols=4>
    <BigValue data={kpis} value=metric1/>
    <BigValue data={kpis} value=metric2/>
    <BigValue data={kpis} value=metric3/>
    <BigValue data={kpis} value=metric4/>
</Grid>

<Grid cols=2>
    <LineChart data={monthly} x=month y=sales/>
    <DataTable data={top_items}/>
</Grid>
```

## Responsive Behavior

Grid columns automatically collapse on smaller screens:
- Large screens: Full column count
- Medium screens: Max 2 columns
- Small screens: Single column

This ensures content remains readable on mobile devices.
