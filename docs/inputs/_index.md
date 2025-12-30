---
title: Inputs Overview
category: inputs
related: [Dropdown, ButtonGroup, TextInput, DateRange, Slider]
---

# Inputs

Input components allow users to interact with reports by filtering data, selecting options, and providing values. Selected values can be used in SQL queries and markdown content.

## Available Inputs

- **Dropdown** - Select from a list of options
- **ButtonGroup** - Toggle between options with buttons
- **TextInput** - Free-form text entry
- **DateInput** - Single date selection
- **DateRange** - Date range selection
- **Slider** - Numeric range selection
- **Checkbox** - Boolean toggle

## Accessing Input Values

All inputs are accessed via the `inputs` object:

```svelte
{inputs.input_name.value}
```

For multi-select inputs, the value is an array.

## Using in SQL Queries

Reference input values in SQL queries using template syntax:

```sql filtered_data
SELECT * FROM orders
WHERE category = '${inputs.category_dropdown}'
```

For multi-select inputs, use the `IN` operator:

```sql multi_filtered
SELECT * FROM orders
WHERE category IN ${inputs.categories.value}
```

## Common Props

All input components support these common props:

| Prop | Type | Description |
|------|------|-------------|
| `name` | string | Required. Identifier for accessing value |
| `title` | string | Header text above the input |
| `description` | string | Tooltip text on info icon |
| `hideDuringPrint` | boolean | Hide in print mode (default: true) |

## Example: Filtered Dashboard

```sql categories
SELECT DISTINCT category FROM orders
```

```svelte
<Dropdown
    data={categories}
    name=selected_category
    value=category
    title="Select Category"
/>
```

```sql filtered_orders
SELECT * FROM orders
WHERE category = '${inputs.selected_category}'
```

```svelte
<DataTable data={filtered_orders}/>
```
