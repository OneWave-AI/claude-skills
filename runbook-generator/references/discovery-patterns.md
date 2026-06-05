# Discovery Patterns

Use these patterns during the discovery phase to map a system's structure, configuration, and operational behavior before generating a runbook.

## Step 1: Glob patterns for project structure

Run these Glob patterns to identify what kind of system this is:

```
**/*.tf                    # Terraform infrastructure
**/*.yaml, **/*.yml        # Kubernetes manifests, CI/CD configs, docker-compose
**/Dockerfile*             # Container definitions
**/docker-compose*         # Multi-container orchestration
**/*.toml                  # Rust/Python config files
**/package.json            # Node.js projects
**/go.mod                  # Go projects
**/requirements.txt        # Python projects
**/Cargo.toml              # Rust projects
**/pom.xml                 # Java/Maven projects
**/build.gradle*           # Java/Gradle projects
**/Gemfile                 # Ruby projects
**/.github/workflows/*     # GitHub Actions CI/CD
**/.gitlab-ci.yml          # GitLab CI/CD
**/Jenkinsfile             # Jenkins pipelines
**/Makefile                # Build automation
**/Procfile                # Heroku-style process definitions
**/serverless.yml          # Serverless Framework
**/sam-template.yaml       # AWS SAM
**/cdk.json                # AWS CDK
**/pulumi.*                # Pulumi infrastructure
**/ansible/**              # Ansible playbooks
**/helm/**                 # Helm charts
**/.env.example            # Environment variable templates
```

## Step 2: Key configuration files to read

Read and analyze these files when found:

- Infrastructure as Code: all Terraform files, CloudFormation templates, Pulumi programs, CDK constructs
- Container configs: Dockerfiles, docker-compose files, Kubernetes manifests
- CI/CD pipelines: GitHub Actions workflows, GitLab CI, Jenkinsfiles, CircleCI configs
- Application config: environment variable templates, config files, secrets references
- Deployment scripts: any scripts in `scripts/`, `deploy/`, `bin/`, or `ops/` directories
- Monitoring config: Datadog, Prometheus, Grafana, PagerDuty, OpsGenie configurations
- Database migrations: migration files, schema definitions, seed data scripts
- Load balancer config: Nginx, HAProxy, ALB/NLB, Traefik configurations
- README and docs: existing documentation for context

## Step 3: Grep patterns for operational behavior

Search the codebase for these operational patterns:

```
"healthcheck|health_check|health-check"    # Health endpoints
"readiness|liveness|startup"               # Kubernetes probes
"metric|prometheus|statsd|datadog"         # Metrics instrumentation
"sentry|bugsnag|rollbar|error.track"       # Error tracking
"redis|memcache|cache"                     # Caching layers
"queue|worker|job|sidekiq|celery|bull"     # Background job processing
"migrate|migration"                        # Database migrations
"rollback|revert"                          # Rollback mechanisms
"scale|autoscal|replica"                   # Scaling configuration
"backup|snapshot|dump"                     # Backup procedures
"ssl|tls|cert|certificate"                 # TLS/certificate management
"cron|schedule|periodic"                   # Scheduled tasks
"rate.limit|throttle"                      # Rate limiting
"circuit.break|retry|timeout"              # Resilience patterns
"log.level|LOG_LEVEL|debug|verbose"        # Log level configuration
"feature.flag|toggle|flipper|launchdarkly" # Feature flags
"cdn|cloudfront|fastly|cloudflare"         # CDN configuration
"dns|route53|domain"                       # DNS management
"secret|vault|ssm|kms"                     # Secrets management
"alert|alarm|notification|pagerduty"       # Alerting rules
```
