# Async Error Handling and Error Reporting

Error boundaries do not catch errors in event handlers, async callbacks, or promises. Handle those explicitly with the patterns below.

## Async Error Handling Hook

Track loading, data, and error state for async operations so the UI can render a retry path.

```tsx
'use client';

import { useState } from 'react';

interface AsyncState<T> {
  data: T | null;
  error: Error | null;
  isLoading: boolean;
}

function useAsync<T>() {
  const [state, setState] = useState<AsyncState<T>>({
    data: null,
    error: null,
    isLoading: false,
  });

  const execute = async (promise: Promise<T>) => {
    setState({ data: null, error: null, isLoading: true });
    try {
      const data = await promise;
      setState({ data, error: null, isLoading: false });
      return data;
    } catch (error) {
      setState({ data: null, error: error as Error, isLoading: false });
      throw error;
    }
  };

  return { ...state, execute };
}

// Usage
function DataComponent() {
  const { data, error, isLoading, execute } = useAsync<User[]>();

  const loadData = () => execute(fetchUsers());

  if (isLoading) return <Spinner />;
  if (error) return <ErrorMessage error={error} onRetry={loadData} />;
  if (!data) return <button onClick={loadData}>Load</button>;

  return <UserList users={data} />;
}
```

## Error Reporting Integration

Centralize reporting in one module so boundaries and async handlers share a single sink. Swap in the provider (Sentry, LogRocket, custom endpoint) used by the project.

```typescript
// lib/error-reporting.ts
export function reportError(error: Error, context?: Record<string, unknown>) {
  // Sentry
  // Sentry.captureException(error, { extra: context });

  // LogRocket
  // LogRocket.captureException(error);

  // Custom endpoint
  fetch('/api/errors', {
    method: 'POST',
    body: JSON.stringify({
      message: error.message,
      stack: error.stack,
      context,
      timestamp: new Date().toISOString(),
      url: window.location.href,
      userAgent: navigator.userAgent,
    }),
  }).catch(console.error);
}
```
