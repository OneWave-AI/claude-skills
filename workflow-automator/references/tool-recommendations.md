# Tool Recommendation Framework

## Decision Matrix

Evaluate each automation platform against these criteria:

| Criteria | Zapier | Make (Integromat) | n8n (Self-Hosted) | Custom Code | Power Automate |
|----------|--------|-------------------|---------------------|-------------|----------------|
| **Ease of Setup** | Very High | High | Medium | Low | High |
| **Cost at Scale** | Expensive | Moderate | Low (hosting only) | Variable | Moderate |
| **Integration Breadth** | 6000+ apps | 1500+ apps | 800+ apps | Unlimited | 1000+ (MS-heavy) |
| **Complex Logic** | Limited | Good | Excellent | Unlimited | Good |
| **Error Handling** | Basic | Good | Excellent | Unlimited | Good |
| **Self-Hosting** | No | No | Yes | Yes | No |
| **API/Webhook Support** | Good | Excellent | Excellent | Unlimited | Good |
| **Team Collaboration** | Good | Good | Good | Requires DevOps | Excellent (MS orgs) |
| **Data Residency** | US/EU | EU | Your servers | Your servers | MS regions |
| **Learning Curve** | Very Low | Low | Medium | High | Low-Medium |

## When to Recommend Each Tool

**Zapier** -- Best for:
- Simple linear workflows (under 10 steps)
- Non-technical teams who need to maintain their own automations
- Workflows connecting popular SaaS tools with well-supported integrations
- Quick wins that need to be live within hours
- Low volume (under 1000 runs/month cost-effectively)

**Make (Integromat)** -- Best for:
- Workflows with branching logic, loops, or data transformation
- Teams that need visual workflow design but more power than Zapier
- Moderate volume (cost-effective up to 10,000+ runs/month)
- Scenarios requiring array/JSON manipulation
- Multi-step workflows with error handling routes

**n8n (Self-Hosted)** -- Best for:
- High-volume workflows where per-execution pricing is prohibitive
- Workflows requiring custom code nodes mixed with no-code steps
- Organizations with data residency or compliance requirements
- Technical teams comfortable with Docker/Kubernetes
- Complex workflows with advanced error handling, sub-workflows, and custom logic

**Custom Code** -- Best for:
- Workflows requiring sub-second latency
- Complex business logic that cannot be expressed in visual builders
- Workflows that are core to the product (not internal operations)
- High-volume, high-reliability requirements
- Workflows requiring database transactions or complex state management

**Power Automate** -- Best for:
- Microsoft-heavy environments (Office 365, Teams, SharePoint, Dynamics)
- Organizations already paying for Microsoft 365 E3/E5 licenses
- Workflows that interact heavily with Microsoft products
- Teams familiar with the Microsoft ecosystem

## Hybrid Architectures

Many workflows benefit from combining tools:

- **Zapier/Make for triggers + n8n for logic**: Use Zapier to catch webhooks from apps with limited n8n integrations, then forward to n8n for complex processing
- **No-code for happy path + custom code for exceptions**: Handle 90% of cases with Make, route exceptions to a custom microservice
- **Multiple platforms for redundancy**: Critical workflows can use a secondary platform as failover
- **Custom code for core + no-code for notifications**: Write the business logic in code, use Zapier/Make to handle Slack/email notifications
