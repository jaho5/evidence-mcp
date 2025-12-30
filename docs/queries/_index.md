---
title: Queries Overview
category: queries
related: [basics, chaining, parameters]
---

# Queries

Evidence uses SQL queries to fetch and transform data. Queries are written in DuckDB SQL dialect.

## Query Basics

Define queries in fenced code blocks:

```sql my_query
SELECT * FROM table_name
```

## Topics

- **basics** - Writing and referencing queries
- **chaining** - Building queries from other queries
- **parameters** - Using inputs and URL parameters in queries

## Quick Reference

### Define a Query

```sql orders_summary
SELECT
    category,
    COUNT(*) as order_count,
    SUM(amount) as total_amount
FROM orders
GROUP BY 1
```

### Use in Components

```svelte
<DataTable data={orders_summary}/>
<BarChart data={orders_summary} x=category y=total_amount/>
```

### Access Values

```svelte
{orders_summary.length} orders found
{orders_summary[0].total_amount}
```
