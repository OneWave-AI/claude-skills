# Phase 1: Reconnaissance Detail

Run sequentially in the Commander context before deploying any audit agents. Build a complete picture of the repository.

## Step 1.1: Repository Structure Scan

Scan the top-level directory structure and build a manifest.

1. Run `ls -la` at the repo root to get top-level contents
2. Run `find . -type f | head -5000` to get a file listing (cap at 5000 for initial scan)
3. Run `find . -type f | wc -l` to get total file count
4. Run `find . -type d | wc -l` to get total directory count
5. Run `wc -l $(find . -type f -name "*.{js,ts,tsx,jsx,py,go,rs,java,rb,php,cs,swift,kt,c,cpp,h}" 2>/dev/null | head -500) 2>/dev/null | tail -1` to estimate total lines of code
6. Use Glob to find all config files: package.json, Cargo.toml, go.mod, pyproject.toml, Gemfile, composer.json, pom.xml, build.gradle, Makefile, Dockerfile, docker-compose.yml, .github/workflows/*, tsconfig.json, webpack.config.*, vite.config.*, next.config.*, .eslintrc*, .prettierrc*, tailwind.config.*

## Step 1.2: Technology Stack Identification

From the config files and file extensions found, determine:

1. **Primary languages** -- Ranked by line count (e.g., TypeScript 45K lines, Python 12K lines)
2. **Frameworks** -- React, Next.js, Django, Rails, Express, FastAPI, Spring, etc.
3. **Package managers** -- npm, yarn, pnpm, pip, cargo, go modules, bundler, composer
4. **Build tools** -- webpack, vite, esbuild, turbopack, make, gradle, maven
5. **CI/CD** -- GitHub Actions, GitLab CI, CircleCI, Jenkins, etc.
6. **Infrastructure** -- Docker, Kubernetes, Terraform, CloudFormation, serverless configs
7. **Database** -- Prisma schema, migrations folders, SQL files, ORM configs
8. **Testing** -- Jest, Pytest, Go test, RSpec, PHPUnit, test directories

Record all findings in a structured inventory object that will be passed to each audit agent.

## Step 1.3: Audit Module Relevance Check

Not every audit applies to every repo. Determine which modules are relevant:

| Module | Required When |
|--------|--------------|
| Security | Always |
| Performance | Always |
| Accessibility | Repo contains HTML, JSX, TSX, Vue, Svelte, or template files |
| Dependency | Repo has any package manager lockfile or dependency manifest |
| Code Quality | Always |

If accessibility is not relevant (e.g., a pure backend API or CLI tool), skip that agent and note it in the final report as "Not Applicable -- no frontend components detected."

## Step 1.4: Write Reconnaissance Report

Write `audit-workspace/00-reconnaissance.md` in the repo root. This file serves as the shared context document for all audit agents.

```markdown
# Reconnaissance Report
Generated: {timestamp}

## Repository Overview
- Total files: {count}
- Total directories: {count}
- Estimated lines of code: {count}
- Primary languages: {list with line counts}
- Frameworks: {list}
- Package managers: {list}

## Technology Stack
{detailed breakdown}

## Audit Plan
- Security: ACTIVE
- Performance: ACTIVE
- Accessibility: ACTIVE / NOT APPLICABLE (reason)
- Dependency: ACTIVE / NOT APPLICABLE (reason)
- Code Quality: ACTIVE

## File Inventory
{top-level directory tree}
```
