# PhantomOS MCP Server · Query

Exposes `query-context` as an MCP tool for external agents and data pipelines.

## Setup

Add to your `.mcp.json` (workspace root or client config):

```json
{
  "mcpServers": {
    "phantomos-query": {
      "command": "node",
      "args": [".skills/mcp/query-server.js"],
      "env": {
        "WORKSPACE_ROOT": "."
      }
    }
  }
}
```

## Tool: `query_phantomos`

Read-only query against the workspace. Three scopes:

| Scope | Use case | Example |
|-------|----------|---------|
| `kb` | Search shared resources (Ressources/) | "angles for cold traffic" |
| `brand` | Get single brand context | "full context for glowco" |
| `all_brands` | Cross-brand filter, compare, aggregate | "which brands have LTV > 500" |

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | Yes | Natural language query |
| `scope` | enum | No | kb, brand, all_brands, auto (default: auto) |
| `brand_slug` | string | No | Required for brand scope |
| `entity` | enum | No | brand, product, offer, audience, all |
| `product_slug` | string | No | Filter to specific product |
| `audience_slug` | string | No | Filter to specific audience |
| `resource_type` | enum | No | KB type filter |
| `max_results` | int | No | Max results (default: 3, max: 10) |

### Cross-brand query types

- **Filter**: "quelles brands ont des offres actives?" → returns matching brands
- **Compare**: "compare glowco vs nestra" → side-by-side table
- **Aggregate**: "portfolio overview" → totals, revenue range, completeness distribution

## Requirements

- Node.js 18+
- No dependencies (stdlib only)
