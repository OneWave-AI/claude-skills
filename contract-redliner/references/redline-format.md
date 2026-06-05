# Redline Entry Format and Tracked-Changes Conventions

## Per-Issue Redline Entry

For EVERY issue identified, produce a redline entry in this exact format:

```
SECTION [number]: [Section Title]
RISK CATEGORY: [One of the seven categories]
RISK RATING: [CRITICAL / HIGH / MEDIUM / LOW]

CURRENT LANGUAGE:
> "[Exact quote of the problematic clause from the contract]"

PROBLEM:
[2-4 sentence explanation of why this language is problematic, what risk it creates,
and who it disadvantages. Reference specific legal concepts or industry standards.]

SUGGESTED REPLACEMENT:
> "[-Deleted text shown with strikethrough markers-] [+Added text shown with insertion markers+]"

CLEAN VERSION:
> "[The final suggested language as it would read after accepting all changes]"

NEGOTIATION TALKING POINT:
[1-2 sentences framing why this change is reasonable and how to present it
to the other party. Include leverage points and compromise positions.]
```

## Tracked-Changes Formatting Rules

Follow these conventions strictly:

1. **Deletions**: Wrap removed text in `[-` and `-]` markers
   - Example: `[-The Company shall have sole discretion-]`

2. **Insertions**: Wrap added text in `[+` and `+]` markers
   - Example: `[+Both parties shall mutually agree+]`

3. **Combined edits**: Show deletion immediately followed by insertion
   - Example: `[-sole discretion-] [+mutual written agreement+]`

4. **Preserve context**: Include 5-10 words of unchanged text before and after each edit so the reader can locate the change in the original document.

5. **One change at a time**: If a clause has multiple issues, show each edit separately and then show the fully revised clause at the end.

6. **Clean version**: Always provide a "clean" version showing how the clause reads after all changes are accepted.
