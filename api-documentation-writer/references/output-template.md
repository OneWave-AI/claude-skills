# REST API Documentation Template

Use this Markdown structure as the canonical output shape for a REST API. Replace bracketed placeholders with real values and realistic example data.

````markdown
# [API Name] Documentation

## Overview

[Brief description of what the API does]

**Base URL**: `https://api.example.com/v1`

**Authentication**: API Key via `Authorization` header

## Quick Start

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Authentication

All requests require an API key in the `Authorization` header:

```
Authorization: Bearer YOUR_API_KEY
```

Get your API key from [dashboard link].

## Endpoints

### GET /resource

Retrieve a list of resources.

**Parameters**:
- `limit` (optional, integer): Number of results (max 100, default 10)
- `offset` (optional, integer): Pagination offset (default 0)
- `filter` (optional, string): Filter by field

**Request Example**:
```bash
curl -X GET "https://api.example.com/v1/resource?limit=10" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": "123",
      "name": "Example",
      "created_at": "2024-01-15T10:00:00Z"
    }
  ],
  "total": 100,
  "limit": 10,
  "offset": 0
}
```

**Response Codes**:
- `200` - Success
- `400` - Bad request (invalid parameters)
- `401` - Unauthorized (invalid API key)
- `429` - Rate limit exceeded
- `500` - Server error

### POST /resource

Create a new resource.

**Request Body**:
```json
{
  "name": "string (required)",
  "description": "string (optional)",
  "metadata": "object (optional)"
}
```

**Request Example**:
```bash
curl -X POST "https://api.example.com/v1/resource" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Resource",
    "description": "A test resource"
  }'
```

**Response** (201 Created):
```json
{
  "id": "124",
  "name": "My Resource",
  "description": "A test resource",
  "created_at": "2024-01-15T10:30:00Z"
}
```

## Error Handling

All errors follow this format:

```json
{
  "error": {
    "code": "invalid_request",
    "message": "The 'name' field is required",
    "details": {
      "field": "name"
    }
  }
}
```

**Common Error Codes**:
- `invalid_request` - Malformed request
- `authentication_failed` - Invalid API key
- `not_found` - Resource doesn't exist
- `rate_limit_exceeded` - Too many requests
- `internal_error` - Server error

## Rate Limiting

**Limits**: 1000 requests per hour

**Headers**:
- `X-RateLimit-Limit`: Total requests allowed
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Timestamp when limit resets

When rate limited, the API returns a `429` status code.

## Code Examples

### JavaScript (Node.js)
```javascript
const response = await fetch('https://api.example.com/v1/resource', {
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY'
  }
});
const data = await response.json();
```

### Python
```python
import requests

response = requests.get(
  'https://api.example.com/v1/resource',
  headers={'Authorization': 'Bearer YOUR_API_KEY'}
)
data = response.json()
```

## Support

- Documentation: https://docs.example.com
- Support: support@example.com
- Status: https://status.example.com
````
