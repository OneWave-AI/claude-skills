# Scout

Not sure which skill, subagent or command fits what you are doing? Ask Scout.

Scout reads the current conversation, works out what you are trying to get done, and recommends the skills (`/skill-name`) and subagents that fit best. For each one it explains why, and for bigger jobs it lays out the order to run them in.

## Use it

```
/plugin marketplace add OneWave-AI/claude-skills
/plugin install scout@onewave-skills
```

Then ask: "scout, what should I use for this?" It works best mid-task, once the conversation shows what you are building.

## Privacy and data

Scout is instructions only. It reads the conversation it is invoked in, ships no code, makes no network requests of its own, and stores nothing.

Want recommendations that learn from your history? See [Scout Pro](../scout-pro).

## Support

- Questions: [onewave-ai.com/contact](https://www.onewave-ai.com/contact)
- Bugs: [GitHub issues](https://github.com/OneWave-AI/claude-skills/issues)

Built by [OneWave AI](https://www.onewave-ai.com). MIT licensed.
