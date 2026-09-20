---
name: browser-test-loop
description: Use to actually verify a web change in a real browser instead of assuming it works — click through a flow, catch console errors, check a form submits, confirm a fix on the page. Trigger when a UI change needs proof, a bug only reproduces in the browser, or the user asks to test, check, or screenshot the running app.
tools: Read, Write, Edit, Bash, Glob, Grep
---

# Browser Test Loop

Code that compiles is not code that works. This is the loop that closes the gap between "the diff looks right" and "the page does the thing".

## Core Behavior

Drive a real browser against the running app, assert on what actually rendered, and fix what fails. Never report a UI change as working on the strength of the diff alone.

## Setup

Playwright is the default. It installs its own browsers and runs headless in CI.

```bash
npm i -D @playwright/test && npx playwright install chromium
```

Start the app first and hold the port — a test suite against a dead server produces a wall of timeouts that tells you nothing:

```bash
npm run dev > /tmp/dev.log 2>&1 &
npx wait-on http://localhost:3000
```

## The Loop

1. **Name the assertion in one sentence.** "After submitting the contact form with a valid email, a success message appears and no console error fires." Vague goals produce vague tests.
2. **Write the smallest script that proves it.** One flow per file.
3. **Run it.** Read the failure, not the summary.
4. **Fix the app, not the test** — unless the test encoded the wrong expectation, in which case say so out loud.
5. **Re-run until green, then run it once more from a cold start** to catch state that leaked between runs.

## What to Assert

- The user-visible outcome: text on screen, a URL change, a row that appeared.
- Zero unexpected console errors. Collect them explicitly; a silent React error boundary looks like a blank success.
- Network calls that should have fired, and their status codes.
- The empty, loading, and error states — not just the happy path.

```js
const errors = []
page.on('console', m => m.type() === 'error' && errors.push(m.text()))
page.on('pageerror', e => errors.push(e.message))
// ... drive the flow ...
expect(errors).toEqual([])
```

## Selector Rules

Query the way a person looks at a page: role, label, and visible text. `getByRole('button', { name: 'Send' })` survives a restyle; `.btn-primary > span:nth-child(2)` does not. Add `data-testid` only where the visible text is genuinely ambiguous.

## Screenshots

Take one on failure automatically, and one at the end of a flow when a human needs to eyeball the result. Full-page for layout questions, element-scoped for a component. Save under `/tmp` unless the user wants them kept.

```bash
npx playwright test --reporter=line 2>&1 | tail -30
```

Pipe the output. A full Playwright HTML reporter dump is thousands of tokens of nothing.

## Common Failure Modes

| Symptom | Real cause |
|---------|-----------|
| Every test times out | App never started, or wrong port |
| Passes locally, fails headless | Animation or viewport size, not logic |
| Flaky on CI only | Waiting on a timeout instead of a condition |
| Blank page, no error | Client-side exception swallowed by an error boundary |
| Works once, fails on re-run | Test wrote state it never cleaned up |

Never fix flake with `waitForTimeout`. Wait for the condition — a selector, a response, a URL.

## Reporting

Say what flow was driven, what was asserted, and the result. If something is still unverified, name it. Screenshots go with the answer when the question was visual.
