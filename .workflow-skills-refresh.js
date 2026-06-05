export const meta = {
  name: 'skills-2026-refresh',
  description: 'Refresh 82 Claude skills to 2026 standards: de-bloat via progressive disclosure, strip emojis, fix second-person voice',
  phases: [
    { title: 'Pilot', detail: '5 worst offenders first' },
    { title: 'Refresh', detail: 'remaining 77 skills' },
  ],
}

const REPO = '/tmp/cs-work'
const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    skill: { type: 'string' },
    actionsTaken: { type: 'array', items: { type: 'string' } },
    refsCreated: { type: 'array', items: { type: 'string' } },
    coreLinesBefore: { type: 'number' },
    coreLinesAfter: { type: 'number' },
    emojiRemaining: { type: 'number' },
    notes: { type: 'string' },
  },
  required: ['skill', 'actionsTaken', 'coreLinesAfter', 'emojiRemaining'],
}

function brief(item) {
  const path = `${REPO}/${item.skill}/SKILL.md`
  const refdir = `${REPO}/${item.skill}/references`
  return `You are refactoring ONE Claude Code skill to 2026 standards. Work only on this skill's files.

File: ${path}  (currently ~${item.lines} lines)
Issues flagged: ${item.issues.join(', ')}

Read the file first, then apply ONLY the fixes for the flagged issues, following these rules:

PRESERVE: Keep the YAML frontmatter \`name\` and \`description\` (only edit them to strip emoji if present). Keep every real capability and instruction — when de-bloating you RELOCATE detail, you never delete substance.

If "bloat" is flagged — apply progressive disclosure:
- Move long inline output/report templates, large ASCII blocks, exhaustive example dumps, and long lookup tables out of SKILL.md into ${refdir}/<topic>.md (create the dir; use clear kebab-case filenames like output-template.md, examples.md, patterns.md).
- Leave a LEAN core SKILL.md: the H1, a one-line purpose, the workflow as imperative numbered steps, and pointers such as "See references/<file>.md for ...". Add a short "## Contents" list only if it aids navigation.
- Target the core well under ~150 lines without losing capability.

If "emoji" is flagged — remove ALL emoji characters everywhere, including decorative section headers (convert a header like "chart-emoji RESULTS" to "## Results"). The brand rule is zero emojis. This applies to reference files you create too.

If "voice" is flagged — rewrite second-person ("When a user...", "you should") into imperative mood ("Determine...", "Generate...", "Inspect...").

GLOBAL: imperative voice throughout, production quality, no placeholders, no invented features, no purple references. Do NOT run git. Only use Read/Write/Edit (and Bash only for wc -l / mkdir if needed).

After finishing, verify with \`grep\` that no emoji remain if emoji was flagged, and \`wc -l\` the final SKILL.md. Report your results.`
}

const all = typeof args === 'string' ? JSON.parse(args) : args
const pilot = all.slice(0, 5)
const rest = all.slice(5)

log(`Refreshing ${all.length} skills — pilot ${pilot.length}, then ${rest.length}`)

phase('Pilot')
const pilotResults = await parallel(pilot.map(item => () =>
  agent(brief(item), { label: `pilot:${item.skill}`, phase: 'Pilot', schema: SCHEMA })
))

phase('Refresh')
const restResults = await parallel(rest.map(item => () =>
  agent(brief(item), { label: item.skill, phase: 'Refresh', schema: SCHEMA })
))

const results = [...pilotResults, ...restResults].filter(Boolean)
const totalBefore = all.reduce((s, x) => s + x.lines, 0)
const totalAfter = results.reduce((s, r) => s + (r.coreLinesAfter || 0), 0)
const emojiLeft = results.filter(r => (r.emojiRemaining || 0) > 0).map(r => r.skill)
const refsTotal = results.reduce((s, r) => s + (r.refsCreated ? r.refsCreated.length : 0), 0)

return {
  refreshed: results.length,
  ofTotal: all.length,
  coreLinesBefore: totalBefore,
  coreLinesAfter: totalAfter,
  referenceFilesCreated: refsTotal,
  skillsWithEmojiRemaining: emojiLeft,
  perSkill: results.map(r => ({ skill: r.skill, after: r.coreLinesAfter, refs: (r.refsCreated || []).length, actions: r.actionsTaken })),
}
