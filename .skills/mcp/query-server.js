#!/usr/bin/env node

/**
 * PhantomOS Query MCP Server
 *
 * Exposes query-context as an MCP tool for external agents and pipelines.
 * Read-only · never modifies workspace files.
 *
 * Usage:
 *   node .skills/mcp/query-server.js
 *
 * Environment:
 *   WORKSPACE_ROOT · path to workspace root (default: process.cwd())
 *
 * MCP config (.mcp.json):
 *   {
 *     "mcpServers": {
 *       "phantomos-query": {
 *         "command": "node",
 *         "args": [".skills/mcp/query-server.js"],
 *         "env": { "WORKSPACE_ROOT": "." }
 *       }
 *     }
 *   }
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const WORKSPACE_ROOT = path.resolve(process.env.WORKSPACE_ROOT || process.cwd());

// --- File Utilities ---

function readJSON(filePath) {
  try {
    const full = path.resolve(WORKSPACE_ROOT, filePath);
    const content = fs.readFileSync(full, 'utf-8');
    return JSON.parse(content);
  } catch (e) {
    return null;
  }
}

function fileExists(filePath) {
  return fs.existsSync(path.resolve(WORKSPACE_ROOT, filePath));
}

function listBrandSlugs() {
  const brandsDir = path.resolve(WORKSPACE_ROOT, 'brands');
  if (!fs.existsSync(brandsDir)) return [];
  return fs.readdirSync(brandsDir)
    .filter(d => !d.startsWith('_') && !d.startsWith('.'))
    .filter(d => fs.statSync(path.join(brandsDir, d)).isDirectory())
    .filter(d => fileExists(`brands/${d}/brand.json`));
}

function listProducts(brandSlug) {
  const dir = path.resolve(WORKSPACE_ROOT, `brands/${brandSlug}/products`);
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .filter(d => !d.startsWith('_') && !d.startsWith('.'))
    .filter(d => fs.statSync(path.join(dir, d)).isDirectory());
}

function listAudiences(brandSlug) {
  const dir = path.resolve(WORKSPACE_ROOT, `brands/${brandSlug}/audiences`);
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .filter(d => !d.startsWith('_') && !d.startsWith('.'))
    .filter(d => fs.statSync(path.join(dir, d)).isDirectory());
}

// --- Scoring ---

function scoreResource(resource, query, type) {
  let score = 0;
  const q = query.toLowerCase();
  const domain = (resource.domain || '').toLowerCase();
  const tags = (resource.tags || []).map(t => t.toLowerCase());

  if (domain && q.includes(domain)) score += 3;
  for (const tag of tags) {
    if (q.includes(tag)) { score += 1; if (score >= 5) break; }
  }
  if (type && resource.type === type) score += 1;
  return score;
}

// --- Query Handlers ---

function queryKB(params) {
  const index = readJSON('index.json');
  if (!index || !index.resources) {
    return { error: 'index.json not found or empty. Run ingest-resource first.' };
  }

  const results = index.resources
    .map(r => ({ ...r, score: scoreResource(r, params.query, params.resource_type) }))
    .filter(r => r.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, params.max_results || 3);

  return {
    scope: 'kb',
    total_resources: index.resources.length,
    results: results.map(r => {
      const content = readJSON(r.path);
      return {
        type: r.type,
        slug: r.slug,
        domain: r.domain,
        tags: r.tags,
        path: r.path,
        score: r.score,
        content: content
      };
    })
  };
}

function queryBrand(params) {
  const slug = params.brand_slug;
  if (!slug) return { error: 'brand_slug required for brand scope.' };
  if (!fileExists(`brands/${slug}/brand.json`)) {
    return { error: `Brand "${slug}" not found.` };
  }

  const status = readJSON(`brands/${slug}/status.json`);
  const entity = params.entity || 'all';
  const result = { scope: 'brand', brand_slug: slug, status: status, entities: {} };

  if (entity === 'all' || entity === 'brand') {
    result.entities.brand = readJSON(`brands/${slug}/brand.json`);
  }
  if (entity === 'all' || entity === 'product') {
    const pSlug = params.product_slug;
    if (pSlug) {
      result.entities.product = readJSON(`brands/${slug}/products/${pSlug}/spec.json`);
      result.entities.offers = readJSON(`brands/${slug}/products/${pSlug}/offers.json`);
    } else {
      result.entities.products = {};
      for (const p of listProducts(slug)) {
        result.entities.products[p] = readJSON(`brands/${slug}/products/${p}/spec.json`);
      }
    }
  }
  if (entity === 'all' || entity === 'audience') {
    const aSlug = params.audience_slug;
    if (aSlug) {
      result.entities.audience = readJSON(`brands/${slug}/audiences/${aSlug}/profile.json`);
    } else {
      result.entities.audiences = {};
      for (const a of listAudiences(slug)) {
        result.entities.audiences[a] = readJSON(`brands/${slug}/audiences/${a}/profile.json`);
      }
    }
  }
  if (entity === 'all' || entity === 'offer') {
    if (!params.product_slug) {
      result.entities.offers = {};
      for (const p of listProducts(slug)) {
        const offers = readJSON(`brands/${slug}/products/${p}/offers.json`);
        if (offers) result.entities.offers[p] = offers;
      }
    }
  }

  // Always include learnings and strategy
  if (entity === 'all') {
    result.entities.learnings = readJSON(`brands/${slug}/learnings.json`);
    result.entities.strategy = readJSON(`brands/${slug}/strategy.json`);
  }

  return result;
}

function queryAllBrands(params) {
  const slugs = listBrandSlugs();
  if (slugs.length === 0) {
    return { error: 'No brands found. Run setup-brand first.' };
  }
  if (slugs.length > 20) {
    return { error: `${slugs.length} brands found. Max 20 for cross-brand queries. Filter first.` };
  }

  const q = params.query.toLowerCase();

  // Detect query type: compare vs filter vs aggregate
  const compareMatch = q.match(/compare?\s+(\S+)\s+(?:vs?|versus|et|and)\s+(\S+)/i);
  if (compareMatch || (params.brand_slugs && params.brand_slugs.length >= 2)) {
    // Compare mode
    const compareSlugs = params.brand_slugs || [compareMatch[1], compareMatch[2]];
    const brands = compareSlugs
      .filter(s => fileExists(`brands/${s}/brand.json`))
      .map(s => {
        const brand = readJSON(`brands/${s}/brand.json`);
        const status = readJSON(`brands/${s}/status.json`);
        return {
          slug: s,
          vertical: brand?.meta?.vertical,
          stage: brand?.meta?.stage,
          aov: brand?.financials?.aov,
          monthly_revenue: brand?.financials?.monthly_revenue,
          roas_breakeven: brand?.financials?.roas_breakeven,
          positioning: brand?.positioning?.value_proposition,
          products: listProducts(s).length,
          audiences: listAudiences(s).length,
          wedge_complete: status?.wedge_complete,
        };
      });
    return { scope: 'all_brands', type: 'compare', brands };
  }

  if (q.includes('overview') || q.includes('portfolio') || q.includes('résumé') || q.includes('summary')) {
    // Aggregate mode
    const summary = { total: slugs.length, by_stage: {}, by_vertical: {}, revenues: [], wedge_complete: 0, stale: 0 };
    for (const s of slugs) {
      const brand = readJSON(`brands/${s}/brand.json`);
      const status = readJSON(`brands/${s}/status.json`);
      const stage = brand?.meta?.stage || 'unknown';
      const vert = brand?.meta?.vertical || 'unknown';
      summary.by_stage[stage] = (summary.by_stage[stage] || 0) + 1;
      summary.by_vertical[vert] = (summary.by_vertical[vert] || 0) + 1;
      if (brand?.financials?.monthly_revenue) summary.revenues.push(brand.financials.monthly_revenue);
      if (status?.wedge_complete) summary.wedge_complete++;
    }
    summary.revenue_range = summary.revenues.length > 0
      ? { min: Math.min(...summary.revenues), max: Math.max(...summary.revenues), avg: Math.round(summary.revenues.reduce((a, b) => a + b, 0) / summary.revenues.length) }
      : null;
    delete summary.revenues;
    return { scope: 'all_brands', type: 'aggregate', summary };
  }

  // Filter mode (default)
  const results = [];
  for (const s of slugs) {
    const brand = readJSON(`brands/${s}/brand.json`);
    const status = readJSON(`brands/${s}/status.json`);
    const learnings = readJSON(`brands/${s}/learnings.json`);
    const strategy = readJSON(`brands/${s}/strategy.json`);

    // Build searchable text blob for fuzzy matching
    const blob = JSON.stringify({ brand, status, learnings, strategy }).toLowerCase();
    if (blob.includes(q) || q.split(' ').some(w => w.length > 2 && blob.includes(w))) {
      results.push({
        slug: s,
        name: brand?.meta?.name,
        vertical: brand?.meta?.vertical,
        wedge_complete: status?.wedge_complete,
        match_context: 'fuzzy keyword match'
      });
    }
  }

  return {
    scope: 'all_brands',
    type: 'filter',
    query: params.query,
    total_brands: slugs.length,
    matches: results.length,
    results: results.slice(0, params.max_results || 10)
  };
}

// --- MCP Protocol (stdio JSON-RPC) ---

const TOOL_DEFINITION = {
  name: 'query_phantomos',
  description: 'Query a PhantomOS workspace for brand context, shared KB resources, or cross-brand data. Read-only.',
  inputSchema: {
    type: 'object',
    properties: {
      scope: {
        type: 'string',
        enum: ['kb', 'brand', 'all_brands', 'auto'],
        description: 'Search shared KB, single brand, all brands (cross-brand), or auto-detect. Default: auto.'
      },
      brand_slug: {
        type: 'string',
        description: "Brand slug (required if scope=brand). Example: 'lumya'."
      },
      entity: {
        type: 'string',
        enum: ['brand', 'product', 'offer', 'audience', 'all'],
        description: 'Entity type to query (brand scope only). Default: all.'
      },
      product_slug: { type: 'string', description: 'Product slug for product/offer queries.' },
      audience_slug: { type: 'string', description: 'Audience slug for audience queries.' },
      resource_type: {
        type: 'string',
        enum: ['catalogue', 'routing', 'framework', 'sop', 'quality-spec', 'convention', 'template'],
        description: 'KB resource type filter (kb scope only).'
      },
      query: {
        type: 'string',
        description: "Natural language query. Example: 'angles for cold traffic problem-unaware audience'."
      },
      max_results: { type: 'integer', default: 3, maximum: 10, description: 'Max results to return.' }
    },
    required: ['query']
  }
};

function handleToolCall(params) {
  // Auto-detect scope
  let scope = params.scope || 'auto';
  if (scope === 'auto') {
    const q = params.query.toLowerCase();
    if (params.brand_slug) scope = 'brand';
    else if (q.includes('cross-brand') || q.includes('all brands') || q.includes('toutes les brands') || q.includes('compare') || q.includes('portfolio') || q.includes('overview') || q.match(/quelles?\s+brands?/)) scope = 'all_brands';
    else if (q.includes('angle') || q.includes('framework') || q.includes('routing') || q.includes('sop') || q.includes('convention') || q.includes('template') || q.includes('catalogue')) scope = 'kb';
    else scope = 'kb'; // default
  }

  switch (scope) {
    case 'kb': return queryKB(params);
    case 'brand': return queryBrand(params);
    case 'all_brands': return queryAllBrands(params);
    default: return { error: `Unknown scope: ${scope}` };
  }
}

// --- MCP stdio transport ---

const rl = readline.createInterface({ input: process.stdin });
let buffer = '';

rl.on('line', (line) => {
  try {
    const msg = JSON.parse(line);
    let response;

    if (msg.method === 'initialize') {
      response = {
        jsonrpc: '2.0', id: msg.id,
        result: {
          protocolVersion: '2024-11-05',
          serverInfo: { name: 'phantomos-query', version: '1.1.0' },
          capabilities: { tools: {} }
        }
      };
    } else if (msg.method === 'notifications/initialized') {
      return; // no response needed
    } else if (msg.method === 'tools/list') {
      response = {
        jsonrpc: '2.0', id: msg.id,
        result: { tools: [TOOL_DEFINITION] }
      };
    } else if (msg.method === 'tools/call') {
      const toolName = msg.params?.name;
      if (toolName !== 'query_phantomos') {
        response = {
          jsonrpc: '2.0', id: msg.id,
          result: { content: [{ type: 'text', text: JSON.stringify({ error: `Unknown tool: ${toolName}` }) }] }
        };
      } else {
        const result = handleToolCall(msg.params?.arguments || {});
        response = {
          jsonrpc: '2.0', id: msg.id,
          result: { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] }
        };
      }
    } else {
      response = {
        jsonrpc: '2.0', id: msg.id,
        error: { code: -32601, message: `Method not found: ${msg.method}` }
      };
    }

    if (response) {
      process.stdout.write(JSON.stringify(response) + '\n');
    }
  } catch (e) {
    const errResponse = {
      jsonrpc: '2.0', id: null,
      error: { code: -32700, message: `Parse error: ${e.message}` }
    };
    process.stdout.write(JSON.stringify(errResponse) + '\n');
  }
});

process.stderr.write('PhantomOS Query MCP Server started\n');
process.stderr.write(`Workspace root: ${WORKSPACE_ROOT}\n`);
