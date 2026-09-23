---
name: template-deck-builder
description: Builds and edits PowerPoint decks bound to a company's own .pptx or .potx template, with a consulting-grade storyline and a rendered visual QA pass. Maps the template's masters, layouts, placeholders, theme colors and fonts; drafts a storyboard of action titles (pyramid principle, SCR) for approval; fills the template's own placeholders instead of drawing text boxes; adds native charts in theme colors, tables sized to placeholders, speaker notes and source lines; then renders every slide to PNG and checks text overflow, off-slide and overlapping shapes, off-theme fonts and colors, empty placeholders and weak titles. Use whenever the user says use our template, company deck, brand or corporate template, make slides, build a deck, pptx, potx, consulting-style deck, board or client presentation, action titles, or fix my deck formatting, and whenever an existing deck must be edited without breaking its masters. Complements the generic pptx skill.
---

# Template Deck Builder

Build decks INTO the company template and make them argue something. The three ways decks go wrong are: rebuilding the template from scratch (floating text boxes, hard-coded colors, ignored layouts), having no storyline (topic-label titles, one slide per data dump), and shipping without looking (overflowing text, boxes over charts). This skill has one step for each.

Scripts need `python-pptx` (`pip install python-pptx`), plus LibreOffice (`soffice`) and poppler (`pdftoppm`) for the render. Anthropic's generic `pptx` skill covers raw pptx manipulation from scratch. Use this skill when a template exists or the deck has to read like consulting work.

## Files

- `scripts/inspect_template.py`: template to `layout_map.json` (layouts, placeholders, geometry, theme, recommended layout per slide type).
- `scripts/build_deck.py`: storyboard JSON to deck, filling placeholders. Also edits an existing deck in place (`--edit`).
- `scripts/qa_deck.py`: checks, render, contact sheet, report. Exits 1 on any ERROR.
- `references/storyboard-schema.md`: every storyboard field, with examples.
- `references/storyline.md`: action titles, pyramid, SCR, ghost deck, chart choice.
- `references/python-pptx-notes.md`: placeholder mechanics, autofit limits, EMU, charts, breakages.
- `tests/run_tests.sh OUT_DIR`: builds a sample template, a good 6-slide deck and a bad one, and checks that QA passes the first and catches the second.

## Workflow

### 1. Inspect the template (never skip)

```bash
python3 scripts/inspect_template.py company.potx -o layout_map.json
```

Read the printed layout list and `recommended`. From here on, every slide uses one of these layouts by exact name. Note the theme fonts and colors. They are the only fonts and colors allowed. If the template holds sample slides, the build drops them by default (`keep_template_slides: true` keeps them).

If no layout fits a slide type (for example no two-column layout), say so and pick the closest one. Do not draw your own. A deck that ignores the layouts breaks the moment someone applies a new theme or edits it in PowerPoint.

### 2. Write the storyline before any slide

Read `references/storyline.md`, then give the user:

1. The governing thought: one sentence, the answer to the audience's question.
2. The ghost deck: one action title per slide, numbered, with its layout and a one-line note on the evidence (chart type, table, bullets).

Test it. Read the titles alone, top to bottom. They must make the whole argument in order, and each must be a full sentence with a so-what, around 15 words or fewer. "Q3 revenue" is a label. "Q3 revenue fell 8% because two accounts churned" is a title. Every slide carries one message, and its body only proves that message.

**Stop and get the storyline approved.** Changing a title list costs seconds. Rebuilding 20 slides costs an hour.

### 3. Write the storyboard JSON

Follow `references/storyboard-schema.md`. Each slide gets `layout` (exact name) or `type`, `title`, one content block (`bullets`, `chart`, `table`, `columns`, `quote`), `source`, and `notes`. Rules:

- Charts carry real numbers and a `number_format`. Use `highlight` for the bar that makes the point. The chart type follows from the message (see storyline.md).
- Every chart or table gets a `source`. Every content slide gets `notes`, which hold what the presenter says, not the slide text again.
- Bullets: at most 6, one line each where possible, parallel grammar. Use `**Lead-in:** detail` for scannable bullets.
- Use `free_text` only when the user asks for an annotation the template has no placeholder for. It is flagged in QA on purpose.

### 4. Build into the placeholders

```bash
python3 scripts/build_deck.py storyboard.json --template company.potx -o deck.pptx
```

The build fills title, subtitle, body, chart, table, quote and source placeholders by role. Charts and tables go into the content placeholder itself, so they inherit its position. Charts use theme accent colors (schemeClr), so a theme change recolors them. Speaker notes are written, and unused empty placeholders are removed. Read the build log. Any `ERROR` (unknown layout, content with no placeholder to hold it) means fix the storyboard and rebuild. Never patch the output by hand with text boxes.

### 5. QA: render, look, fix, repeat

```bash
python3 scripts/qa_deck.py deck.pptx --storyboard storyboard.json --out-dir qa/
```

Then open `qa/contact_sheet.png` and look at every slide. The checks estimate text fit from font metrics. The render shows what the checks miss: an unbalanced layout, a chart that says nothing, a label collision.

Fix at the source, in order:
- `text_overflow` / `text_tight`: cut words, split into two slides, or move detail to notes. Do not shrink fonts, and do not rely on "shrink text on overflow". PowerPoint recomputes that on edit, so type sizes drift from slide to slide.
- `overlap`, `off_slide`, `free_text_box`, `template_bypass`: move the content into a layout placeholder, or change the layout.
- `off_theme_font` / `off_theme_color`: remove the hard-coded value so the theme applies.
- `empty_placeholder`: fill it or drop it. Empty ones show "Click to add text" in edit view.
- `action_title`: rewrite as a full-sentence takeaway. Re-read the storyline section of the report.
- `no_source`: add the source line.

Rebuild and rerun QA until it reports 0 ERROR and every WARN is fixed or explained to the user. Only then deliver.

### 6. Deliver

Deliver `deck.pptx`, the contact sheet, and a short note: the governing thought, the slide count, and any WARN you chose to leave with the reason. Offer the ghost deck (the titles) as the executive summary.

## Editing an existing deck

The goal is to change the content and keep the design system.

1. Run `inspect_template.py deck.pptx`. `existing_slides` lists each slide's layout and its placeholder shapes and text.
2. Write an edit storyboard: `{"slides": [{"edit": 4, "title": "...", "bullets": [...]}], "delete": [7], "order": [...]}`. Edits replace text inside the existing placeholders and keep the first run's formatting. New slides without `edit` are appended from the deck's own layouts.
3. `build_deck.py edits.json --edit deck.pptx -o deck_v2.pptx`, then QA with `expected_slide_count`.

Never re-create the deck to change it, and never copy slides into a fresh file. Either one silently drops the masters. For "fix my deck formatting", run QA first and fix what it finds, working from ERRORs down.

## Guardrails

- The template decides fonts, colors, positions and bullet styles. The storyboard decides words and numbers.
- One message per slide. If a title needs "and", it is probably two slides.
- Numbers on slides must come from the user's data. Mark placeholders as `[TBD]` rather than inventing figures, and QA will show them.
- Keep text at 10pt or larger (source lines excepted). QA warns below that.
