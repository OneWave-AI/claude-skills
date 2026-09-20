---
name: mcp-server-builder
description: Use to build, wire up, or debug an MCP (Model Context Protocol) server that gives Claude access to an internal API, database, or SaaS tool. Trigger when the user wants Claude to connect to their own system, asks for an MCP server, needs custom tools for Claude Code or the Claude app, or an existing server's tools are not showing up.
tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
---

# MCP Server Builder

An MCP server is how Claude reaches a system it does not otherwise know about — your database, your internal API, your ops tooling. The protocol is small. Almost every real problem is a design problem: which tools to expose and what they return.

## Decide the Shape First

**Local (stdio)** — runs on the user's machine, launched by the client, credentials from the local environment. Right for developer tooling and anything touching localhost or a local database. Only that machine gets it.

**Remote (HTTP)** — deployed once, reached by URL, OAuth for identity. Right when a team needs it, or when the data lives in a service rather than on a laptop. Everyone gets updates the moment you deploy.

Build remote when more than one person will use it. Retrofitting local-only to multi-user later means redoing auth from scratch.

## Tool Design — the part that matters

Tools are an interface for a model, not a REST API. The common failure is exposing twenty thin endpoint wrappers and watching the model chain them badly.

- **Name the job, not the endpoint.** `get_pipeline_board` beats `query_deals` plus `query_stages` plus `query_owners`.
- **One call should answer a real question.** If using your server always takes three calls in the same order, that sequence should have been one tool.
- **Descriptions are prompts.** Say what the tool is for, when to reach for it, and what it does not do. This text is the only instruction the model gets.
- **Return prose-shaped, compact results.** Trim nulls and internal ids nobody will use. A 40KB JSON blob buries the answer and eats the window.
- **Paginate and cap.** Always a default limit. Say in the response when results were truncated, and how to get the rest.
- **Separate reads from writes.** Writes get explicit, narrow tools with clear names — never a generic `execute` that takes arbitrary input.
- **Errors are instructions.** "No company matched 'acme' — try search_companies first" gets recovered from; "500 Internal Server Error" does not.

Ten well-shaped tools beat fifty thin ones.

## Minimum Viable Server

```ts
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { z } from 'zod'

const server = new McpServer({ name: 'acme-crm', version: '1.0.0' })

server.tool(
  'get_deal',
  'Fetch one deal with its owner, stage, and recent activity. Use when the user names a specific deal or company.',
  { id: z.string().describe('Deal id or display id like D-1042') },
  async ({ id }) => ({ content: [{ type: 'text', text: await renderDeal(id) }] }),
)

await server.connect(new StdioServerTransport())
```

Check the SDK's current API before writing more than this — the interface has changed across releases, and code written from memory tends to target an older one.

## Security

- Least privilege on the credential. A read-only token for a read-only server.
- Never take a raw query string from the model into a database. Parameterize, allow-list tables, scope by tenant on the server side.
- Scope every request to the authenticated user. A remote server that trusts a user id in the arguments is an authorization hole.
- Never log or return secrets. Redact tokens in error paths.
- Rate-limit writes.

## Debugging

```bash
npx @modelcontextprotocol/inspector node build/index.js   # exercise tools directly
claude mcp list                                           # is it registered
claude mcp get <name>                                     # config and status
```

Tools missing in the client is nearly always one of: the server crashed on startup (run it by hand and read stderr), a stdio server wrote a stray `console.log` to stdout and corrupted the protocol stream, the config points at a stale build, or the client was not restarted. For stdio servers, all logging goes to stderr — stdout belongs to the protocol.

## Ship Checklist

- Every tool description says when to use it and when not to.
- Every tool tested through the inspector, not only through the client.
- Results capped and truncation stated.
- Errors say what to try next.
- Credentials from the environment, never in the repo.
- README: install, config snippet, and one example prompt per tool.
