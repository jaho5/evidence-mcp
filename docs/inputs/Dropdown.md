---
title: Dropdown
category: inputs
related: [ButtonGroup, TextInput, Slider]
---

# Dropdown

Creates a dropdown menu with a list of options that can be selected. Selected values can filter queries or be used in markdown content.

## Basic Usage

```svelte
<Dropdown
    data={categories}
    name=category_filter
    value=category_name
/>
```

## Required Props

| Prop | Type | Description |
|------|------|-------------|
| `name` | string | Identifies the dropdown; accessed via `{inputs.name.value}` |
| `data` | query | Data source containing available options |
| `value` | string | Column containing selectable values |

## Optional Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `multiple` | boolean | false | Enable multi-select (returns array) |
| `defaultValue` | string/array | - | Initial selection |
| `selectAllByDefault` | boolean | false | Select all values (with `multiple`) |
| `label` | string | - | Column for display text (different from value) |
| `title` | string | - | Header text above dropdown |
| `order` | string | - | Sort column (append `asc`/`desc`) |
| `where` | string | - | SQL clause to filter options |
| `noDefault` | boolean | false | No automatic default selection |
| `disableSelectAll` | boolean | false | Remove select-all button |
| `hideDuringPrint` | boolean | true | Hide in print mode |
| `description` | string | - | Tooltip on info icon |

## Hardcoded Options

Use `DropdownOption` for static options:

```svelte
<Dropdown name=status>
    <DropdownOption valueLabel="Active" value="active"/>
    <DropdownOption valueLabel="Inactive" value="inactive"/>
    <DropdownOption valueLabel="Pending" value="pending"/>
</Dropdown>
```

## Filtering Queries

### Single Select

```sql filtered_orders
SELECT * FROM orders
WHERE category = '${inputs.category_filter}'
```

### Multi-Select

Use the `IN` operator without quotes:

```sql filtered_orders
SELECT * FROM orders
WHERE category IN ${inputs.category_filter.value}
```

## Examples

### With Label Column

```svelte
<Dropdown
    data={countries}
    name=country
    value=country_code
    label=country_name
    title="Select Country"
/>
```

### Sorted Options

```svelte
<Dropdown
    data={products}
    name=product
    value=product_name
    order="product_name asc"
/>
```

### Multi-Select with Default

```svelte
<Dropdown
    data={regions}
    name=regions
    value=region
    multiple=true
    selectAllByDefault=true
    title="Select Regions"
/>
```

### Filtered Options

```svelte
<Dropdown
    data={products}
    name=active_products
    value=product_name
    where="status = 'active'"
/>
```
