---
title: Layouts Overview
category: layouts
related: [Grid, Tabs, Accordion, Alert]
---

# Layout Components

Layout components help organize content and create responsive dashboards.

## Available Layouts

- **Grid** - Multi-column responsive layouts
- **Tabs** - Tabbed content sections
- **Accordion** - Collapsible sections
- **Alert** - Status messages and callouts
- **Modal** - Popup dialogs
- **Details** - Expandable summary/details

## Grid

Create multi-column layouts:

```svelte
<Grid cols=2>
    <BigValue data={kpi1} value=metric1/>
    <BigValue data={kpi2} value=metric2/>
</Grid>
```

Columns collapse to single column on mobile.

## Tabs

Organize content into tabs:

```svelte
<Tabs>
    <Tab label="Overview">
        Overview content...
    </Tab>
    <Tab label="Details">
        Details content...
    </Tab>
</Tabs>
```

## Accordion

Collapsible sections:

```svelte
<Accordion title="More Information">
    Detailed content here...
</Accordion>
```

## Alert

Status messages:

```svelte
<Alert status="info">
    This is an informational message.
</Alert>
```

Status options: `info`, `success`, `warning`, `error`

## Responsive Design

Evidence layouts are mobile-responsive by default:
- Grid columns stack on small screens
- Tables become scrollable
- Charts resize to fit
