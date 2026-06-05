---
name: api-documentation-writer
description: Generate comprehensive API documentation including endpoint descriptions, request/response examples, authentication guides, error codes, and SDKs. Creates OpenAPI/Swagger specs, REST API docs, and developer-friendly reference materials. Use when users need to document APIs, create technical references, or write developer documentation.
---

# API Documentation Writer

Generate comprehensive, developer-friendly API documentation.

## Contents
- `references/documentation-structure.md` — every section to cover (overview, auth, endpoints, errors, rate limits, SDKs, webhooks, GraphQL)
- `references/output-template.md` — canonical REST Markdown template with worked examples
- `references/best-practices.md` — best practices, developer-experience tips, and the output quality checklist

## Workflow

1. Gather API information. Determine the API type (REST, GraphQL, WebSocket, gRPC), authentication method (API key, OAuth, JWT), base URL and versioning strategy, available endpoints and their purposes, request/response formats, and any rate limiting or usage restrictions.

2. Build the documentation structure. Cover every section in `references/documentation-structure.md`, ordering the most common operations first.

3. Generate the output. Follow `references/output-template.md` for REST APIs; adapt to schema, query, mutation, and subscription examples for GraphQL. Replace all placeholders with realistic example data and show both request and response.

4. Document errors and rate limits. Include the standard error response format, common error codes, troubleshooting guidance, limits, headers to check, and how to handle `429` responses.

5. Provide code samples in multiple languages (curl, JavaScript, Python) and link SDKs, Postman collections, or OpenAPI specs where available.

6. Verify quality against the checklist in `references/best-practices.md` before delivering.

## Example Triggers
- "Write API documentation for my REST endpoints"
- "Create OpenAPI spec for my API"
- "Document this GraphQL schema"
- "Generate developer docs for my webhook API"
- "Write authentication guide for API"
