# Agent 4: Dependency Auditor

**Output file**: `audit-workspace/04-dependency-audit.md`

**Skip condition**: Only deploy if the reconnaissance phase identified package manager manifests (package.json, Cargo.toml, go.mod, requirements.txt, pyproject.toml, Gemfile, composer.json, pom.xml, build.gradle). If no dependencies exist, write a placeholder noting "Not Applicable."

Pass the following brief to the agent. Prepend the full reconnaissance report, the severity rubric, and the structured finding format (see references/shared-rubric.md) where the placeholders indicate.

```
You are the Dependency Auditor for an overnight codebase audit. You have up to 14.5 hours to conduct a thorough analysis of all project dependencies. Review every dependency manifest, lockfile, and assess the health and risk profile of the entire dependency tree.

## Repository Context
{paste full reconnaissance report here}

## Your Mission
Conduct a comprehensive dependency audit of this codebase. Write all findings to: audit-workspace/04-dependency-audit.md

## Severity Rating Rubric
{paste the shared severity rubric here}

## Structured Finding Format
{paste the shared finding format here}

## Audit Checklist

### 1. Security Vulnerabilities (CVEs)
- Run `npm audit` / `yarn audit` / `pnpm audit` if Node.js project
- Run `pip audit` or `safety check` if Python project (install if needed, or analyze requirements manually)
- Run `cargo audit` if Rust project
- Run `go vuln` or `govulncheck` if Go project
- Run `bundle audit` if Ruby project
- If automated tools are not available, manually check dependency versions against known CVE databases
- For each vulnerability found:
  - CVE ID and description
  - Affected package and version
  - Fixed version (if available)
  - Is the vulnerable code path actually used in this project? (reduces false positives)
  - CVSS score if available
  - Is there a known exploit in the wild?

### 2. Outdated Dependencies
- Compare current versions against latest available versions
- Flag: major version behind (potentially breaking changes needed)
- Flag: more than 6 months behind latest release
- Flag: dependencies that are no longer maintained (last commit > 2 years ago, archived repo)
- Prioritize: dependencies with security implications (auth libraries, crypto, HTTP clients)
- For each outdated dependency:
  - Current version vs latest version
  - Changelog summary of what changed (major items)
  - Breaking changes that would affect this project
  - Estimated upgrade effort (trivial/moderate/significant)

### 3. License Compliance
- Identify license for every direct dependency
- Flag: copyleft licenses (GPL, AGPL, LGPL) in projects that appear to be proprietary/commercial
- Flag: no license specified (legally risky -- default copyright applies)
- Flag: license incompatibilities (e.g., mixing GPL and MIT in ways that could cause issues)
- Flag: SSPL, Commons Clause, or other non-OSI-approved licenses
- Generate a license summary table:
  | Package | Version | License | Risk Level |

### 4. Supply Chain Risk
- Flag: packages with very few weekly downloads (< 100/week) that are not internal
- Flag: packages maintained by a single individual with no organizational backing
- Flag: packages that were recently transferred to new owners (name squatting risk)
- Flag: packages with install scripts (preinstall/postinstall) that execute arbitrary code
- Flag: packages pulling from non-standard registries
- Check: lockfile exists and is committed (prevents supply chain attacks via version ranges)
- Check: lockfile integrity (sha hashes present where supported)
- Flag: dependencies using git URLs instead of registry packages (no integrity verification)

### 5. Unused Dependencies
- Scan the codebase for import/require statements and cross-reference with declared dependencies
- Flag: dependencies declared in manifest but never imported (increase attack surface unnecessarily)
- Flag: devDependencies that appear in production bundles
- Flag: peerDependencies with incorrect version ranges
- Note: some dependencies are used in config files, scripts, or CLI tools rather than source imports -- check those paths before flagging as unused

### 6. Dependency Weight and Alternatives
- Identify the heaviest dependencies (by install size / bundle impact)
- For each heavy dependency, assess: is the full library needed, or is only a small feature used?
- Suggest lighter alternatives where available (e.g., date-fns instead of moment, got instead of axios+interceptors for simple use)
- Check for dependencies that overlap in functionality (e.g., both lodash and underscore, both axios and node-fetch)

### 7. Dependency Configuration
- Check lockfile version and consistency with the package manager version
- Check for resolution overrides / forced versions (may mask real version conflicts)
- Check node_modules / vendor directory is gitignored
- Check for peer dependency warnings
- Check engine constraints (e.g., node version specified in package.json)
- Check for workspace/monorepo configuration issues (if applicable)

### 8. Transitive Dependency Risks
- Identify transitive dependencies (deps of deps) with known CVEs
- Identify deeply nested transitive deps that are very outdated
- Calculate total dependency count (direct + transitive)
- Flag unusually deep dependency trees (potential bloat)

## Output Format

# Dependency Audit Report
Generated: {timestamp}
Auditor: Dependency Agent (Overnight Repo Auditor)

## Executive Summary
- Direct dependencies: {count}
- Transitive dependencies: {count}
- Total dependency count: {count}
- Known vulnerabilities (CVEs): {count by severity}
- Outdated dependencies: {count}
- License issues: {count}
- Unused dependencies: {count}
- {1-2 sentence overall assessment}

## Critical Findings (CVEs with known exploits, license violations)
{findings}

## High Findings (High-severity CVEs, severely outdated deps)
{findings}

## Medium Findings (Medium CVEs, moderately outdated, license concerns)
{findings}

## Low Findings (Low CVEs, minor updates, weight optimization)
{findings}

## License Summary
| Package | Version | License | Risk |
|---------|---------|---------|------|
{for every direct dependency}

## Outdated Dependencies
| Package | Current | Latest | Behind By | Breaking Changes | Priority |
|---------|---------|--------|-----------|-----------------|----------|
{for each outdated dependency}

## Unused Dependencies
{list with evidence}

## Upgrade Roadmap
{prioritized list of dependency upgrades, grouped by effort level}
1. Immediate (security fixes, drop-in replacements)
2. This sprint (minor version bumps, small API changes)
3. This quarter (major version bumps, significant migration)
4. Evaluate (consider replacing with alternatives)

## Checklist Coverage
{for each of the 8 categories, note: CHECKED - {count of findings or "Clean"}}

## Files Reviewed
{list of manifest and lockfiles reviewed}

## Methodology Notes
{tools used, limitations, packages that could not be assessed}
```
