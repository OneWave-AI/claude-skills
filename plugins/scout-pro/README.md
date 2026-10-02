# Scout Pro

A deeper version of [Scout](../scout). Scout Pro reads the whole conversation, checks which skills you actually have installed, and recommends multi-skill chains where each step feeds the next. It keeps a local log of what it recommended and how it went, so its suggestions improve the more you use it.

## What it does

- **Deep context scan.** Goal, sub-goals, blockers and what you already tried.
- **Verified inventory.** It scans your installed skills before recommending any, so it never suggests one you do not have.
- **Chains, not lists.** Multi-step tasks get an ordered workflow. A one-skill job gets one skill.
- **Learns from outcomes.** Tell it what worked and it factors that into next time.

## Use it

```
/plugin marketplace add OneWave-AI/claude-skills
/plugin install scout-pro@onewave-skills
```

## Privacy and data

Scout Pro is instructions only and ships no code. To personalize its recommendations it reads, on your machine only:

- your installed skills: `~/.claude/skills/`, the project's `.claude/skills/` and plugin skill folders
- your Claude Code memory and session context: `~/.claude/projects/` and `~/.claude/rules/session-context.md`, when present

It writes one file, a usage log at `~/.claude/scout-pro-usage-log.json`. Delete that file at any time to reset what it has learned. Nothing is sent anywhere except to the Claude model your session already uses. It can use web search when a recommendation needs current information.

## Support

- Questions: [onewave-ai.com/contact](https://www.onewave-ai.com/contact)
- Bugs: [GitHub issues](https://github.com/OneWave-AI/claude-skills/issues)

Built by [OneWave AI](https://www.onewave-ai.com). MIT licensed.
