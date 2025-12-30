---
title: Syntax Overview
category: syntax
related: [queries, loops, conditionals, expressions]
---

# Evidence Syntax

Evidence uses a combination of Markdown, SQL, and Svelte-like syntax to create data-driven reports.

## Core Concepts

### SQL Queries

Define queries in fenced code blocks with a name:

```sql orders_by_month
SELECT
    date_trunc('month', order_date) as month,
    SUM(amount) as total
FROM orders
GROUP BY 1
ORDER BY 1
```

### Component Syntax

Evidence supports two syntaxes for components:

**JSX-style (recommended for simple components):**
```svelte
<LineChart data={orders_by_month} x=month y=total/>
```

**Markdoc-style (for complex nesting):**
```markdown
{% line_chart data="orders_by_month" x="month" y="total" /%}
```

### JavaScript Expressions

Use curly braces for JavaScript:

```svelte
{query_name.length}           // Row count
{query_name[0].column}        // First row value
{2 + 2}                       // Arithmetic
{value.toFixed(2)}            // Methods
```

## Loops

Iterate over query results:

```svelte
{#each orders_by_category as row}
    <Value data={row} column=sales/>
{/each}
```

## Conditionals

```svelte
{#if total_sales[0].amount > 1000}
    Sales target met!
{:else}
    Below target
{/if}
```

## Frontmatter

Page metadata at the top of the file:

```yaml
---
title: Monthly Report
queries:
  - external_data: queries/external.sql
---
```

## Best Practices

1. **Name queries descriptively** - Use meaningful names like `orders_by_month` not `q1`
2. **Keep SQL readable** - Use formatting and CTEs for complex queries
3. **Reference data correctly** - Use `data={query_name}` not `data="query_name"`
4. **Avoid markdown tables** - Use `<DataTable>` component instead
