# Writing Style and Output Requirements

Apply these rules strictly when writing the runbook.

## Clarity
- Write for an engineer who has never seen this system before.
- Make every command copy-pasteable -- no placeholder values without clear labels.
- Use `<PLACEHOLDER>` format for values the engineer must fill in.
- Include expected output for diagnostic commands so engineers know what "healthy" looks like.
- Number all steps sequentially -- never use ambiguous ordering.

## Urgency-Appropriate
- Put P1 procedures first in each section.
- Mark time-sensitive steps clearly: "MUST complete within 5 minutes".
- Separate "do this now" from "do this after incident".
- Include estimated time for each major procedure.

## Completeness
- Include the full flags needed on every `kubectl`, `aws`, `gcloud`, `docker`, or CLI command.
- Include both the "happy path" and what to do when a step fails.
- Document prerequisites for each procedure (access, tools, permissions).
- Cross-reference related sections.

## Formatting
- Use tables for structured data (metrics, thresholds, contacts).
- Use code blocks for all commands with language hints for syntax highlighting.
- Use bold for warnings and critical notes.
- Use checklists for multi-step procedures.
- Never use emojis anywhere in the document.
- Keep lines under 120 characters where possible.

## Output Requirements

Generate the runbook as `runbook.md` in the project root directory (or the directory the user specifies). The file MUST:

1. Be 500+ lines.
2. Cover all 9 major sections from the template.
3. Contain actual commands and configuration derived from the codebase (not just generic placeholders).
4. Include at least one ASCII or Mermaid architecture diagram.
5. Have a complete table of contents.
6. Be immediately useful to an on-call engineer.

If the codebase lacks information for certain sections (for example, no monitoring config found), still include the section with a clear note:
`[ACTION REQUIRED]: No monitoring configuration found in codebase. Complete this section with your monitoring setup.`
This ensures the runbook serves as both documentation and a gap analysis.

## Accuracy Rules
- Never fabricate infrastructure details -- only document what is verifiable from the codebase.
- When uncertain about a detail, mark it clearly with `[VERIFY]` so the team can confirm.
- Prefer specificity over generality -- a runbook with real commands is worth ten with generic advice.
- Confirm that referenced file paths and scripts actually exist in the codebase.
- If the system uses multiple environments (dev/staging/prod), document differences between them.
- Include version numbers for all tools and dependencies where visible in config files.
