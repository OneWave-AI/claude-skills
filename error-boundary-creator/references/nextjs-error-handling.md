# Next.js App Router Error Handling

The App Router uses file conventions to catch errors per route segment. Each file must be placed inside the relevant `app/` segment.

## Route Segment Error (app/error.tsx)

Catches errors thrown in the route segment and its children. Must be a Client Component.

```tsx
// app/error.tsx (or any route segment)
'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log error to reporting service
    console.error(error);
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center min-h-[400px]">
      <h2 className="text-2xl font-bold">Something went wrong!</h2>
      <button
        onClick={reset}
        className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg"
      >
        Try again
      </button>
    </div>
  );
}
```

## Global Error (app/global-error.tsx)

Catches errors in the root layout. Must render its own `<html>` and `<body>` because it replaces the root layout when active.

```tsx
'use client';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body>
        <div className="flex flex-col items-center justify-center min-h-screen">
          <h2 className="text-2xl font-bold">Something went wrong!</h2>
          <button onClick={reset} className="mt-4 btn-primary">
            Try again
          </button>
        </div>
      </body>
    </html>
  );
}
```

## Not Found (app/not-found.tsx)

Rendered when `notFound()` is called or for unmatched routes.

```tsx
import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[400px]">
      <h2 className="text-4xl font-bold">404</h2>
      <p className="text-gray-600 mt-2">Page not found</p>
      <Link href="/" className="mt-4 text-blue-600 hover:underline">
        Go home
      </Link>
    </div>
  );
}
```
