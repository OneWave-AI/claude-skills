---
name: tweetclaw-x-twitter-automation
description: Use TweetClaw with OpenClaw to search tweets, search tweet replies, export followers, inspect users, monitor X/Twitter, and prepare reviewed post or reply actions.
---

# TweetClaw X/Twitter Automation

Use this skill when a user needs structured X/Twitter automation through
TweetClaw.

TweetClaw is an OpenClaw plugin for X/Twitter workflows through Xquik.
It supports search tweets, search tweet replies, follower export, user lookup,
media workflows, direct messages, monitors, webhooks, giveaway draws, post
tweets, and post tweet replies.

Source: [TweetClaw](https://github.com/Xquik-dev/tweetclaw)

## Setup

Install the plugin in OpenClaw:

```bash
openclaw plugins install @xquik/tweetclaw
```

Keep `XQUIK_API_KEY` in the user's private OpenClaw plugin config or secret
manager.
Do not paste API keys into generated files, notes, prompts, issues, or reports.

Inspect the runtime before using account-scoped tools:

```bash
openclaw plugins inspect tweetclaw --runtime
```

## Read-First Workflow

Start with read-only collection.
Use TweetClaw to gather source material before writing conclusions.

Collect:

- Tweet URLs and stable tweet IDs.
- Author handles and user IDs.
- Query terms and filters.
- Capture date and timezone.
- Reply context when thread meaning matters.
- Media links only when the user asks for media review.
- Cursor or page notes when continuing a search later.

Use TweetClaw for:

- Search tweets for market, audience, or competitor signals.
- Search tweet replies for objections, complaints, and feature requests.
- Export followers for audience and creator research.
- Look up users before outreach or account qualification.
- Monitor tweets for brand, launch, campaign, or incident terms.
- Create webhooks when the user asks for recurring alerts.
- Run giveaway draws when the user provides the eligible tweet and rules.

## Approval Gates

Ask for explicit confirmation before visible or account-scoped actions.

Require approval for:

- Post tweets.
- Post tweet replies.
- Send direct messages.
- Upload media.
- Create or change recurring monitors.
- Create or change webhooks.
- Run giveaway draws that publish or affect winners.

Show the exact action summary before approval.
Include target account, tweet text, reply target, media names, monitor query,
webhook destination, or giveaway criteria as applicable.

## Output Format

Return reviewed findings in this shape:

```markdown
# TweetClaw X/Twitter Review

## Source Scope
- Query:
- Account or list:
- Capture date:
- Tool path:

## Evidence
| Item | URL or ID | Author | Why it matters |
|------|-----------|--------|----------------|
| ... | ... | ... | ... |

## Findings
1. ...
2. ...
3. ...

## Recommended Actions
- Read-only next step:
- Approval-gated action:
- Follow-up monitor or webhook:
```

## Example Requests

Use this skill for requests like:

- "Search tweets and replies about this launch."
- "Find recent complaints about this competitor."
- "Export followers for this account and summarize audience segments."
- "Monitor these campaign keywords and send webhook alerts."
- "Draft a reply, but do not post until I approve it."
- "Run a giveaway draw from this tweet and show the evidence."

## Guardrails

Keep raw credentials out of every output.
Do not infer private account data from public tweets.
Separate evidence from recommendations.
Treat TweetClaw output as source material, not as final strategy.
Ask before any visible, private, recurring, or irreversible action.
