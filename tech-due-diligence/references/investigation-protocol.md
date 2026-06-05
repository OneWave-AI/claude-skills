# Investigation Protocol

Execute these phases in order. Be thorough. Read actual files, not just directory listings. Sample deeply -- read at least 3-5 representative files in each major area. Spend more time on areas that show risk signals and less on areas that appear well-maintained.

## Phase 1: Repository Reconnaissance

Establish the scope and shape of the system under evaluation.

Actions:
- List all top-level directories and files to understand project structure.
- Identify the primary programming languages by file extension counts.
- Determine monorepo vs polyrepo structure.
- Find and read README.md, CONTRIBUTING.md, ARCHITECTURE.md, or any onboarding docs.
- Identify total line count by language (use `find` and `wc` or similar).
- Check repository age from git log (earliest commit date).
- Check total number of contributors from git shortlog.
- Identify the most recent commit date to assess whether the codebase is actively maintained.
- Look for .github/, .gitlab-ci/, .circleci/, Jenkinsfile, or other CI/CD indicators.
- Identify all package managers in use (package.json, requirements.txt, go.mod, Cargo.toml, pom.xml, build.gradle, Gemfile, etc.).

Record:
- Total files and lines of code by language.
- Repository age (first commit to last commit).
- Number of unique contributors.
- Primary tech stack identification.
- Monorepo vs polyrepo determination.

## Phase 2: Architecture Assessment

Evaluate the structural quality and design decisions of the system.

Actions:
- Map the high-level architecture by examining directory structure, import patterns, and entry points.
- Identify the architectural style: monolith, microservices, serverless, event-driven, layered, hexagonal, etc.
- Check for clear separation of concerns (controllers/routes, services/business logic, data access, models).
- Look for API definitions: OpenAPI/Swagger specs, GraphQL schemas, gRPC proto files, REST route definitions.
- Identify the database layer: ORMs, raw queries, migration files, schema definitions.
- Check for message queues, event buses, caching layers (Redis, Memcached), search engines (Elasticsearch).
- Evaluate the dependency graph -- check for circular dependencies and clean dependency direction.
- Look for shared libraries, internal packages, or common utilities.
- Check configuration management: environment variables, config files, secrets management.
- Identify external service integrations (payment processors, auth providers, email services, etc.).

Assess:
- Architectural coherence (does the codebase follow its stated or implied architecture consistently?).
- Coupling analysis (how tightly are components bound together?).
- Domain modeling quality (are business concepts clearly represented in code?).
- API design quality (consistency, versioning, error handling patterns).

## Phase 3: Code Quality and Tech Debt Quantification

Measure internal quality and estimate accumulated technical debt.

Actions:
- Sample 5-10 files from different parts of the codebase and evaluate naming conventions and consistency, function/method length (flag functions over 50 lines), file length (flag files over 500 lines), comment quality and density, error handling patterns (swallowed, propagated, logged), and code duplication.
- Check for linting configuration (.eslintrc, .pylintrc, .rubocop.yml, rustfmt.toml, etc.).
- Check for formatting configuration (Prettier, Black, gofmt, etc.).
- Count TODO/FIXME/HACK/XXX comments.
- Identify dead code: unused imports, commented-out blocks, unreachable code paths.
- Check for hardcoded values that should be configurable (URLs, API keys, magic numbers).
- Look for any checked-in credentials, API keys, or secrets (CRITICAL finding if present).
- Evaluate type safety: TypeScript strict mode, Python type hints, Go interface usage.
- Check for consistent error handling and logging patterns.
- Look for anti-patterns specific to the tech stack.

Quantify:
- Estimated lines of dead code.
- Count of TODO/FIXME/HACK comments.
- Number of files exceeding complexity thresholds.
- Percentage of codebase with type coverage (where applicable).
- Estimated engineer-weeks to remediate each category of tech debt.

## Phase 4: Security Posture Analysis

Evaluate security maturity from a static analysis perspective.

Actions:
- Check authentication implementation: JWT handling, session management, OAuth flows.
- Look for authorization patterns: RBAC, ABAC, middleware guards, policy engines.
- Examine input validation: sanitization, parameterized queries, XSS prevention.
- Check for SQL injection vulnerabilities: raw string concatenation in queries.
- Look for secrets management: .env files in .gitignore, vault integrations, KMS usage.
- Check whether .env, .env.local, or credential files are committed to the repository.
- Examine CORS configuration for overly permissive settings.
- Check for rate limiting on API endpoints.
- Look for CSP (Content Security Policy) headers in web applications.
- Examine dependency versions for known CVEs (check package-lock.json, yarn.lock, etc.).
- Look for security headers: HSTS, X-Frame-Options, X-Content-Type-Options.
- Check cryptographic practices: hashing algorithms, key management, TLS configuration.
- Examine file upload handling for path traversal and unrestricted upload vulnerabilities.
- Check for logging of sensitive data (passwords, tokens, PII in log statements).
- Look for OWASP Top 10 vulnerability patterns throughout the codebase.

Rate each finding:
- CRITICAL: Exploitable vulnerability with potential for data breach or system compromise.
- HIGH: Significant security gap that should be remediated before or immediately after close.
- MEDIUM: Security weakness that increases attack surface but is not immediately exploitable.
- LOW: Best practice deviation that marginally increases risk.
- NEGLIGIBLE: Cosmetic or theoretical concern.

## Phase 5: Scalability and Performance Analysis

Assess the system's ability to handle growth in users, data, and traffic.

Actions:
- Identify database query patterns: N+1 queries, missing indexes, full table scans.
- Check caching strategy: application-level caching, CDN configuration, database query caching.
- Look for pagination on list endpoints.
- Examine connection pooling configuration for databases and external services.
- Check for async/concurrent processing: background jobs, worker queues, async patterns.
- Look for horizontal scaling indicators: stateless services, shared-nothing architecture, session externalization.
- Check for database sharding or partitioning strategies.
- Examine file storage patterns: local filesystem vs object storage (S3, GCS).
- Look for monitoring and observability: APM integration, custom metrics, distributed tracing.
- Check for load testing artifacts: k6 scripts, JMeter configs, Artillery configs.
- Examine memory management patterns: large object allocation, stream processing vs buffering.
- Look for WebSocket or real-time communication patterns and their scaling implications.

Assess:
- Current estimated capacity (users, requests/second, data volume) based on architecture.
- Horizontal scaling readiness (1-5 scale).
- Database scaling strategy and headroom.
- Identified bottlenecks and their remediation complexity.

## Phase 6: Test Coverage and Quality Assurance

Evaluate the testing strategy and its effectiveness.

Actions:
- Identify test directories and testing frameworks in use.
- Count test files vs source files to establish a test-to-source ratio.
- Check for test types present: unit, integration, end-to-end (Cypress, Playwright, Selenium), API/contract, performance/load, snapshot.
- Read 3-5 representative test files to evaluate quality: behavior vs implementation testing, proper assertions vs no-error checks, meaningful descriptions, edge case and error path coverage, and test data management (factories, fixtures, seeds).
- Check test configuration: jest.config, pytest.ini, .mocharc, etc.
- Look for code coverage configuration and any existing coverage reports.
- Check test mocking patterns and their appropriateness.
- Check for CI integration of tests (are tests run on every PR?).
- Check for flaky test indicators: retry logic, skipped tests, conditional test execution.

Quantify:
- Test-to-source file ratio.
- Estimated code coverage percentage (from config or inference).
- Number of skipped/disabled tests.
- Test type distribution (unit vs integration vs e2e).

## Phase 7: Build System and Deployment Maturity

Assess engineering operations maturity.

Actions:
- Examine CI/CD pipeline configuration in detail: build steps and purpose, test execution, linting and static analysis, security scanning (SAST, DAST, dependency scanning), deployment stages (dev, staging, production), approval gates and manual intervention points.
- Check for Infrastructure as Code: Terraform, Pulumi, CloudFormation, CDK, Ansible.
- Look for containerization: Dockerfile quality, docker-compose for local dev.
- Check for orchestration: Kubernetes manifests, Helm charts, ECS task definitions.
- Examine environment parity across dev, staging, and production.
- Look for database migration strategy and tools (Flyway, Alembic, Knex, Prisma Migrate).
- Check for feature flags implementation (LaunchDarkly, custom implementation).
- Look for rollback strategy indicators.
- Check for monitoring and alerting configuration.
- Examine logging infrastructure setup.
- Look for runbooks, playbooks, or incident response documentation.
- Check for blue/green or canary deployment patterns.

Rate deployment maturity on a 1-5 scale:
- 1: Manual deployments, no CI/CD, no IaC.
- 2: Basic CI/CD (build + test), some automation, manual deployment triggers.
- 3: Full CI/CD with staging, automated deployments, basic monitoring.
- 4: Advanced CI/CD with security scanning, IaC, feature flags, automated rollbacks.
- 5: Best-in-class DevOps with full observability, chaos engineering, progressive delivery.

## Phase 8: Team Capability Inference from Git History

Use version control history as a proxy for team dynamics, expertise distribution, and bus factor risk.

Actions:
- Run git shortlog to identify all contributors and their commit counts.
- Analyze commit frequency over time (monthly or quarterly) to identify trends.
- Identify the top 5 contributors by commit volume and assess their areas of ownership.
- Calculate the bus factor -- how many people would need to leave before critical knowledge is lost.
- Inspect commit messages for quality and convention (conventional commits, descriptive messages, ticket references).
- Check for code review indicators: merge commits, PR references in commit messages.
- Analyze contribution distribution: dominated by 1-2 individuals or distributed.
- Compare recent vs historical contributors to detect team turnover.
- Separate automated commits (bots, CI, dependency updates) from human commits.
- Identify areas with single-contributor ownership (knowledge silos).
- Inspect commit timing patterns to infer team location/timezone distribution.
- Check for pair programming or co-authoring indicators in commit messages.

Assess:
- Team size and trajectory (growing, stable, shrinking).
- Knowledge distribution risk (concentrated vs distributed).
- Bus factor for critical components.
- Code review culture maturity.
- Commit hygiene and development workflow quality.

## Phase 9: Dependency and Open Source License Risk

Evaluate third-party dependency health and legal compliance risk.

Actions:
- List all direct dependencies from package manifests.
- Count total dependencies (direct + transitive where visible from lock files).
- Identify the top 20 most critical dependencies (by centrality to the application).
- For critical dependencies, check last published version date, community size (GitHub stars), known vulnerabilities (CVE databases), and license type.
- Categorize all licenses found: permissive (MIT, Apache 2.0, BSD) is LOW risk; weak copyleft (LGPL, MPL) is MEDIUM risk requiring legal review; strong copyleft (GPL, AGPL) is HIGH risk for proprietary software requiring immediate legal review; no license / custom license is CRITICAL risk and may not be legally usable; commercial/proprietary requires transfer or relicensing in M&A.
- Check for license compliance tooling (FOSSA, Snyk, WhiteSource/Mend).
- Look for NOTICE files, LICENSE files, and attribution requirements.
- Check for vendored/copied code that may carry its own license.
- Identify dependencies that are deprecated or archived.
- Flag dependencies with under 100 GitHub stars or single-maintainer projects (supply chain risk).

Quantify:
- Total direct dependency count.
- Total transitive dependency count (if determinable).
- License distribution breakdown.
- Number of dependencies with known vulnerabilities.
- Number of unmaintained dependencies (no update in 12+ months).

## Phase 10: Documentation and Knowledge Management

Assess how well the codebase communicates its own design and operation.

Actions:
- Evaluate README quality, API documentation, and architecture decision records (ADRs).
- Inspect inline documentation quality in complex business logic.
- Check for onboarding documentation or setup guides.
- Look for runbooks, incident response docs, or operational guides.
- Check for changelog maintenance (CHANGELOG.md, release notes).
- Evaluate JSDoc/docstring coverage on public APIs and interfaces.
- Look for wiki, Notion, Confluence links or references in the codebase.
