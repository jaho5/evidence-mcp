---
title: Components Overview
category: components
related: [Value, BigValue, DataTable, Delta]
---

# Data Display Components

Evidence provides components for displaying data values, metrics, and tables.

## Available Components

- **Value** - Display inline values from queries
- **BigValue** - Large KPI cards with optional comparison and sparkline
- **DataTable** - Rich interactive tables with sorting, search, and formatting
- **Delta** - Show change values with directional indicators

## Basic Patterns

### Displaying a Single Value

```sql total_sales
SELECT SUM(amount) as total FROM orders
```

The total is: <Value data={total_sales} column=total fmt=usd/>

### KPI Card

```svelte
<BigValue
    data={total_sales}
    value=total
    title="Total Sales"
    fmt=usd
/>
```

### Data Table

```svelte
<DataTable data={orders_summary}>
    <Column id=category/>
    <Column id=sales fmt=usd/>
</DataTable>
```

## Format Strings

Common format codes:

| Code | Description | Example |
|------|-------------|---------|
| `usd` | US Currency | $1,234.56 |
| `eur` | Euro | €1,234.56 |
| `pct` | Percentage | 12.34% |
| `pct0` | Percentage (no decimals) | 12% |
| `pct2` | Percentage (2 decimals) | 12.34% |
| `num0` | Number (no decimals) | 1,235 |
| `num2` | Number (2 decimals) | 1,234.56 |
| `date` | Date | 2024-01-15 |

Custom Excel-style formats are also supported:
- `#,##0` - Thousands separator
- `$#,##0.00` - Currency with decimals
- `0.0%` - Percentage with decimal
