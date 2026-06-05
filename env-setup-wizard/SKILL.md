---
name: env-setup-wizard
description: Set up environment variables, .env files, and configuration management. Use when configuring environment variables, creating .env files, or managing app configuration.
---

# Environment Setup Wizard

## Instructions

When setting up environment configuration:

1. **Identify required variables** for the project
2. **Create .env structure** with proper organization
3. **Set up type-safe access** to env vars
4. **Add validation** on startup
5. **Document all variables**

## File Structure

```
project/
├── .env                  # Local development (git-ignored)
├── .env.example          # Template (committed to git)
├── .env.local            # Local overrides (git-ignored)
├── .env.development      # Development defaults
├── .env.production       # Production defaults
└── src/
    └── lib/
        └── env.ts        # Type-safe env access
```

## .env.example Template

```bash
# ===================
# Application
# ===================
NODE_ENV=development
APP_URL=http://localhost:3000
PORT=3000

# ===================
# Database
# ===================
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# ===================
# Authentication
# ===================
# Generate with: openssl rand -base64 32
JWT_SECRET=
NEXTAUTH_SECRET=
NEXTAUTH_URL=http://localhost:3000

# ===================
# Third-party APIs
# ===================
# Get from: https://stripe.com/dashboard
STRIPE_SECRET_KEY=
STRIPE_PUBLISHABLE_KEY=
STRIPE_WEBHOOK_SECRET=

# Get from: https://resend.com
RESEND_API_KEY=

# ===================
# Storage
# ===================
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
S3_BUCKET_NAME=
```

## Type-Safe Environment (Zod)

```typescript
// src/lib/env.ts
import { z } from 'zod';

const envSchema = z.object({
  // App
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  APP_URL: z.string().url(),
  PORT: z.coerce.number().default(3000),

  // Database
  DATABASE_URL: z.string().min(1),

  // Auth
  JWT_SECRET: z.string().min(32),
  NEXTAUTH_SECRET: z.string().min(32),
  NEXTAUTH_URL: z.string().url(),

  // APIs (optional in dev)
  STRIPE_SECRET_KEY: z.string().optional(),
  RESEND_API_KEY: z.string().optional(),
});

// Validate on import
const parsed = envSchema.safeParse(process.env);

if (!parsed.success) {
  console.error('Invalid environment variables:');
  console.error(parsed.error.flatten().fieldErrors);
  process.exit(1);
}

export const env = parsed.data;

// Type export for use elsewhere
export type Env = z.infer<typeof envSchema>;
```

## Next.js Specific

```typescript
// src/lib/env.ts for Next.js
import { z } from 'zod';

// Server-side variables
const serverSchema = z.object({
  DATABASE_URL: z.string(),
  JWT_SECRET: z.string(),
});

// Client-side variables (must start with NEXT_PUBLIC_)
const clientSchema = z.object({
  NEXT_PUBLIC_APP_URL: z.string().url(),
  NEXT_PUBLIC_STRIPE_KEY: z.string(),
});

export const serverEnv = serverSchema.parse(process.env);
export const clientEnv = clientSchema.parse({
  NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
  NEXT_PUBLIC_STRIPE_KEY: process.env.NEXT_PUBLIC_STRIPE_KEY,
});
```

## T3 Env (Recommended for Next.js)

```typescript
// src/env.mjs
import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

export const env = createEnv({
  server: {
    DATABASE_URL: z.string().url(),
    NODE_ENV: z.enum(["development", "test", "production"]),
  },
  client: {
    NEXT_PUBLIC_APP_URL: z.string().url(),
  },
  runtimeEnv: {
    DATABASE_URL: process.env.DATABASE_URL,
    NODE_ENV: process.env.NODE_ENV,
    NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
  },
});
```

## .gitignore

```gitignore
# Environment files
.env
.env.local
.env.*.local

# Keep example
!.env.example
```

## Security Best Practices

1. **Never commit secrets** to git
2. **Use different values** per environment
3. **Rotate secrets regularly**
4. **Use secret managers** in production (Vault, AWS Secrets Manager)
5. **Validate on startup** to fail fast
6. **Prefix client vars** (NEXT_PUBLIC_, VITE_, REACT_APP_)
