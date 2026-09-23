# Storyboard schema (build_deck.py input)

One JSON file per deck. `build_deck.py` fills the template's placeholders from it. `qa_deck.py --storyboard` uses it to check the slide count and to recognize framing slides (title, section, quote), which are exempt from action-title rules.

## Top level

| Field | Meaning |
|---|---|
| `governing_thought` | The single-sentence answer the deck argues. Not rendered. Keep it here so the storyline stays honest. |
| `template` | Path to the .pptx/.potx. `--template` on the command line overrides it. |
| `slides` | Ordered list of slide specs (below). |
| `keep_template_slides` | Default `false`: sample slides in the template are removed before building. |
| `delete` | Edit mode: 1-based numbers of original slides to remove. |
| `order` | Final order as 1-based positions of the resulting slides, e.g. `[1, 3, 2, 4]`. |
| `expected_slide_count` | For QA in edit mode, where `slides` lists only the changes. |

## Slide spec

| Field | Meaning |
|---|---|
| `layout` | Exact layout name from `layout_map.json` (case-insensitive match allowed). |
| `type` | Used when `layout` is omitted: `title`, `section`, `agenda`, `one_message_chart` (alias `chart`), `two_column`, `table`, `quote`, `title_only`. The inspector's recommended layout is used. |
| `title` | The action title. It goes into the TITLE / CENTER_TITLE placeholder. |
| `subtitle` | Into SUBTITLE, or the first body placeholder (for example on a section divider). |
| `bullets` / `body` | String (`\n` splits paragraphs) or list. A nested list is one level deeper. `{"text": "...", "level": 2}` is also accepted. `**x**` makes a bold run. |
| `chart` | See below. Goes into a CHART or content (OBJECT) placeholder. |
| `table` | See below. Goes into a TABLE or content placeholder. |
| `columns` | List of `{heading?, bullets? / chart? / table?}`, mapped left to right onto the layout's content placeholders. If a column has a separate heading placeholder above its body, the heading goes there. Otherwise it becomes a bold first line. |
| `quote`, `attribution` | Largest body placeholder, then the next one. Curly quotes are added. |
| `source` | Into a placeholder named Source/Footnote, or a small body placeholder near the bottom. With neither, a text box `tdb-source` is added bottom-left and noted in the log. |
| `notes` | Speaker notes. |
| `placeholders` | Explicit fills by idx, e.g. `{"13": "Prepared for the board", "14": {"chart": {...}}}`. Use it for template-specific extras (date line, presenter, kicker). |
| `free_text` | List of `{text, left_in, top_in, width_in, height_in, size_pt?}`. Only when the user asks. QA flags every one. |
| `keep_empty_placeholders` | Default `false`: unused empty placeholders are removed. |
| `edit` | Edit mode: the 1-based number of the existing slide to change in place, instead of adding one. |

## Chart

```json
{"type": "bar", "categories": ["Top 12 lanes", "Next 28", "Remaining 100"],
 "series": [{"name": "Share of loss", "values": [0.80, 0.15, 0.05]}],
 "number_format": "0%", "highlight": 0}
```

- `type`: `column`, `bar`, `stacked_column`, `stacked_column_100`, `stacked_bar`, `line`, `line_plain`, `pie`, `doughnut`, `area`.
- `number_format`: an Excel format (`0%`, `0.0`, `$#,##0`, `#,##0,"K"`). It applies to both the axis and the data labels. `label_format` overrides the labels only.
- `highlight`: an index, a category name, or a list of either. Single-series bar/column only. The highlighted points get accent 1 and the rest a muted theme neutral.
- `data_labels` (default `true`) hides the value axis unless `hide_value_axis: false`. Gridlines are always off.
- Optional: `title` (usually omit it, since the slide title carries the message), `value_axis_title`, `font_size` (default 12), `gap_width` (default 60).
- Series colors are theme accents 1-6 in order, never RGB.
- Bar charts reverse the category axis so the first category reads on top.

## Table

```json
{"columns": ["Wave", "Lanes", "Price change", "Margin impact"],
 "rows": [["Wave 1", "6", "+12%", "+1.8 pts"], ["Total", "12", "+10.5%", "+3.0 pts"]],
 "col_widths": [2, 1, 1.4, 1.6], "highlight_row": 1}
```

- The table fills the placeholder's width. `col_widths` are relative ratios. Without them, widths follow the content length.
- The font size steps down with the row count (14/12/11/10pt) unless `font_size` is set. Numeric-looking cells are right-aligned.
- The header row is styled by the template's table style. `highlight_row` (0-based, data rows) is set in bold.
- If there are more than about 10 rows, the table belongs in the appendix or should be split. QA estimates the grown height and flags a table that runs off the slide.

## Minimal complete example

```json
{
  "governing_thought": "Repricing twelve lanes recovers three margin points without layoffs.",
  "slides": [
    {"type": "title", "title": "Recovering three points of margin", "subtitle": "Board discussion | Sept 2026"},
    {"layout": "Title and Content",
     "title": "Repricing twelve loss-making lanes recovers three margin points without cutting headcount",
     "bullets": ["**Situation:** margin fell from 7.8% to 4.9%", "**Complication:** 12 of 140 lanes drive 80% of the loss",
                 "**Resolution:** reprice them in two waves"],
     "source": "Source: lane P&L FY2024-26", "notes": "The whole deck on one page."}
  ]
}
```

See `tests/storyboard_good.json` for a full six-slide deck and `tests/storyboard_bad.json` for what QA must catch.
