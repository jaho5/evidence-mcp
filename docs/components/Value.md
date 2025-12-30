---
title: Value
category: components
related: [BigValue, Delta, DataTable]
---

# Value

Display inline values from query results within text or other components.

## Basic Usage

```svelte
The total sales amount is <Value data={sales_total} column=total fmt=usd/>.
```

## Required Props

| Prop | Type | Description |
|------|------|-------------|
| `data` | query | Query name in curly braces |
| `column` | string | Column name to display |

## Optional Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `row` | number | 0 | Row index (0-based) |
| `fmt` | string | - | Format string |
| `placeholder` | string | - | Text when value is null |
| `agg` | string | - | Aggregation: sum, avg, min, max, count |

## Examples

### Simple Value

```sql total_orders
SELECT COUNT(*) as count FROM orders
```

We have <Value data={total_orders} column=count/> orders.

### Formatted Currency

```svelte
Revenue: <Value data={revenue} column=total fmt=usd/>
```

### Specific Row

```svelte
Top product: <Value data={top_products} column=name row=0/>
Second: <Value data={top_products} column=name row=1/>
```

### With Aggregation

```svelte
Average order: <Value data={orders} column=amount agg=avg fmt=usd/>
```

### With Placeholder

```svelte
Discount: <Value data={order} column=discount fmt=pct placeholder="None"/>
```
