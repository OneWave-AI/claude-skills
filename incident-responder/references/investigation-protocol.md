# Investigation and Root Cause Analysis Protocol

Follow this systematic approach. Do not skip steps.

## Step 1: Identify Relevant Log Sources

Search the codebase and infrastructure for log files, log aggregation configs, and monitoring setup.

Common log locations to check:
- Application logs: /var/log/*, ./logs/*, stdout/stderr captures
- Web server logs: nginx/apache access and error logs
- Container logs: docker logs, kubernetes pod logs
- Database logs: slow query logs, error logs, connection logs
- Load balancer logs: request logs, health check logs
- Cloud provider logs: CloudWatch, Stackdriver, Azure Monitor configs
- Application-specific: Sentry configs, DataDog configs, custom logging setup

For each log source, extract entries from the incident time window. Look for:
- Error messages and stack traces
- Unusual patterns in request rates, response times, or error rates
- Connection failures or timeouts
- Resource exhaustion warnings (memory, CPU, disk, file descriptors, connection pools)
- Authentication or authorization failures
- Configuration loading errors

## Step 2: Check Recent Deployments

The most common root cause of production incidents is a recent change. Correlate deployment timestamps with incident start time.

Deployment artifacts to examine:
- Git log: recent commits, merges to main/production branches
- CI/CD configs: .github/workflows/*, .gitlab-ci.yml, Jenkinsfile
- Deployment manifests: kubernetes manifests, terraform files, CloudFormation templates
- Package changes: package.json, requirements.txt, Gemfile.lock diffs
- Database migrations: migration files, schema changes
- Feature flags: feature flag configuration changes
- Environment variables: .env changes, secret rotations
- Infrastructure changes: scaling events, instance type changes, network configuration

## Step 3: Dependency Analysis

Check for issues with external dependencies:
- Third-party API status pages
- Database connection health
- Cache layer (Redis, Memcached) connectivity
- Message queue (Kafka, RabbitMQ, SQS) health
- CDN and DNS status
- Certificate expiration
- Rate limiting from external providers

## Step 4: Resource Analysis

Check system resource utilization:
- CPU utilization and saturation
- Memory usage and OOM events
- Disk space and I/O throughput
- Network throughput and packet loss
- Connection pool utilization
- Thread pool exhaustion
- File descriptor limits

## Step 5: Establish Root Cause Chain

Build a causal chain from the triggering event to the user-visible impact:

```
Triggering Event
  -> First Failure
    -> Cascading Effect(s)
      -> Detection Point
        -> User-Visible Impact
```

Example:

```
Deployment v2.4.1 with updated ORM library
  -> ORM generates N+1 queries for user profile endpoint
    -> Database connection pool exhausted within 8 minutes
      -> Health checks start failing at 14:23 UTC
        -> 503 errors for all authenticated requests
```

Every link in the chain must be supported by evidence from logs, metrics, code, or configuration.

## Common Root Cause Categories

Most incidents fall into one of these:

1. Deployment-related: bad code deploy, configuration change, feature flag change, database migration issue
2. Capacity-related: traffic spike, resource exhaustion, connection pool saturation, storage full
3. Dependency-related: third-party outage, API rate limiting, DNS failure, certificate expiration
4. Data-related: data corruption, schema mismatch, migration failure, replication lag
5. Infrastructure-related: hardware failure, network partition, cloud provider issue, auto-scaling failure
6. Security-related: DDoS attack, credential compromise, vulnerability exploitation
7. Configuration-related: wrong environment variable, expired secret, misconfigured service discovery

## Codebase Investigation Patterns

When investigating through the codebase without direct infrastructure access:

1. Search for error messages reported by users or found in logs. Use Grep to find where the error is thrown, then trace backward to the triggering conditions.
2. Search for recent changes to the affected service. Use `git log` to find recent modifications and review diffs for race conditions, missing null checks, or incorrect queries.
3. Search for configuration related to the affected component: environment variable usage, feature flags, connection strings and pool sizes, timeout values, rate limits.
4. Search for dependencies of the affected component: import statements, API client configurations, database queries, external service calls.
5. Search for monitoring and alerting configuration: health check endpoints, alert rules, dashboard definitions, SLO/SLI definitions.
