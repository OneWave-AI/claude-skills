export const meta = {
  name: 'skills-refresh-batch2',
  description: 'Refresh the remaining 63 skills to 2026 standards (no-schema): de-bloat via progressive disclosure, strip emojis, fix second-person voice',
  phases: [{ title: 'Refresh' }],
}

const REPO = '/tmp/cs-work'

function brief(item) {
  const path = `${REPO}/${item.skill}/SKILL.md`
  const refdir = `${REPO}/${item.skill}/references`
  return `You are refactoring ONE Claude Code skill to 2026 standards. Work only on this skill's files.

File: ${path}  (currently ~${item.lines} lines)
Issues flagged: ${item.issues.join(', ')}

Read the file first, then apply ONLY the fixes for the flagged issues:

PRESERVE: Keep the YAML frontmatter \`name\` and \`description\` (only edit them to strip emoji if present). Keep every real capability — when de-bloating you RELOCATE detail, never delete substance.

If "bloat": apply progressive disclosure. Move long inline output/report templates, large ASCII blocks, exhaustive example dumps, and long lookup tables out of SKILL.md into ${refdir}/<topic>.md (create the dir; kebab-case names like output-template.md, examples.md, patterns.md). Leave a LEAN core SKILL.md: H1, one-line purpose, imperative numbered workflow, and "See references/<file>.md for ..." pointers. Add a short "## Contents" list if it aids navigation. Target the core well under ~150 lines without losing capability.

If "emoji": remove ALL emoji characters everywhere including decorative section headers (a header like "chart-emoji RESULTS" becomes "## Results"). Zero emojis. Applies to any reference files you create too.

If "voice": rewrite second-person ("When a user...", "you should") into imperative mood ("Determine...", "Generate...", "Inspect...").

GLOBAL: imperative voice throughout, production quality, no placeholders, no invented features, no purple references. Do NOT run git. Use Read/Write/Edit (and Bash only for wc -l / mkdir).

After finishing, end your reply with one line: "DONE: ${item.skill} | core lines: <N> | refs: <count>".`
}

const all = typeof args === 'string' ? JSON.parse(args) : args
log(`Refresh batch 2 (no-schema): ${all.length} skills`)

phase('Refresh')
const results = await parallel(all.map(item => () =>
  agent(brief(item), { label: item.skill, phase: 'Refresh' })
))

return { dispatched: all.length, returned: results.filter(Boolean).length, note: 'Verify on disk with git status.' }
