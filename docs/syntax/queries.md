---
title: SQL Queries
category: syntax
related: [expressions, loops, conditionals]
---

# SQL Queries

Evidence executes SQL queries through markdown code fences using DuckDB dialect.

## Basic Query

Each query requires a name after the opening backticks:

```sql sales_by_category
SELECT
    category,
    SUM(sales) as total_sales
FROM orders
GROUP BY 1
ORDER BY 2 DESC
```

Reference in components using the `data` prop:

```svelte
<BarChart data={sales_by_category} x=category y=total_sales/>
```

## Query Chaining

Reference other queries using `${}` syntax:

```sql base_orders
SELECT * FROM orders WHERE status = 'complete'
```

```sql order_summary
SELECT
    category,
    COUNT(*) as order_count,
    AVG(amount) as avg_amount
FROM ${base_orders}
GROUP BY 1
```

The compiler automatically expands nested queries into subqueries.

## Parameterized Queries

Use input values in queries:

### From Input Components

```sql filtered_sales
SELECT * FROM orders
WHERE category = '${inputs.category_dropdown}'
  AND order_date >= '${inputs.date_range.start}'
  AND order_date <= '${inputs.date_range.end}'
```

### From URL Parameters (Templated Pages)

```sql product_details
SELECT * FROM products
WHERE product_id = '${params.product_id}'
```

## Multi-Select Parameters

For multi-select inputs, use `IN` without quotes:

```sql multi_category_sales
SELECT * FROM orders
WHERE category IN ${inputs.categories.value}
```

## File-Based Queries

Store SQL in separate files and import via frontmatter:

```yaml
---
queries:
  - quarterly_data: queries/quarterly.sql
  - regional_sales: reports/regional.sql
---
```

Then reference like any other query:

```svelte
<DataTable data={quarterly_data}/>
```

## DuckDB Features

Evidence uses DuckDB, which supports:

- **Window Functions**: `ROW_NUMBER()`, `LAG()`, `LEAD()`, `SUM() OVER()`
- **CTEs**: `WITH cte AS (...) SELECT ...`
- **JSON**: `json_extract()`, `->`, `->>`
- **Date Functions**: `date_trunc()`, `date_part()`, `current_date`
- **String Functions**: `concat()`, `lower()`, `regexp_matches()`

## Best Practices

1. **Descriptive Names**: Use `orders_by_month` not `q1`
2. **Format SQL**: Use line breaks and indentation
3. **Use CTEs**: For complex logic, break into readable steps
4. **Unique Names**: Each query name must be unique per page
5. **Sort Explicitly**: Don't rely on implicit ordering
