# Style Guide

Apply to every document.

## Sentences
- Short sentences, one idea each. Split anything over about 25 words.
- Active voice and imperative mood for steps: "Run `npm install`", not "The dependencies should be installed".
- Be specific: "Set `TIMEOUT_MS` to `30000`", not "set a reasonable timeout".
- Define a term the first time it appears, then use that exact term every time. Do not alternate "workspace", "project", and "space" for one thing.
- Cut filler: "simply", "just", "easily", "please note that", "it is important to".

## Structure
- Headings describe the content ("Configure SSO"), not the category ("Overview 2").
- Numbered lists for sequences, bullets for unordered items, tables for comparisons and reference values.
- One action per numbered step. Put the result of the step right after it.
- Add a table of contents to anything longer than about three screens.
- Put warnings before the step they apply to, not after.

## Code and commands
- Every code block has a language tag (`bash`, `ts`, `yaml`).
- Commands are copy-pasteable: no leading `$`, no placeholder the reader has to spot. Mark placeholders clearly, for example `<your-project-id>`, and say where to get the value.
- Show expected output after commands that produce it.
- Examples must run. Prefer a small real example over a large invented one.
- Show file paths relative to the repo root.

## Audience fit
- Beginner: explain each step's purpose in one clause, link out for concepts.
- Experienced: lead with the commands, keep explanation brief, link to depth.
- Mixed: write for the less experienced reader and put advanced material in a clearly labeled section.

## Visuals
- Use a diagram (Mermaid or ASCII) when a flow has more than three moving parts.
- Use screenshots only for UI that is hard to describe, and annotate what to look at.

## Final checklist
- Title says what the doc helps you do
- Reader and prerequisites stated before step 1
- Every command, path, flag, and env var verified or marked `[VERIFY]`
- Expected results shown for key steps
- Troubleshooting covers the likely failures
- Links to related docs work
- No step depends on knowledge the doc does not give or list as a prerequisite
