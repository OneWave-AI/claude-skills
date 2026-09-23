# Storyline: making a deck argue something

A consulting deck is an argument, and each slide is one step in it. The failure to avoid is a deck that reads as a sequence of topics ("Market overview", "Financials", "Next steps") with no claim. The reader then has to work out the point, and usually works out a different one.

## 1. Start from the governing thought

Write one sentence that answers the audience's question before writing any slide. It should be specific, arguable and actionable.

- Weak: "An overview of our pricing situation."
- Strong: "Repricing twelve loss-making lanes recovers three margin points in 18 months without cutting headcount."

If you cannot write it, the analysis is not done yet, and more slides will not fix that. Ask the user what they want the audience to decide or believe.

## 2. Pyramid principle (Minto)

Put the answer first, then the three to five reasons that support it, then the evidence under each reason.

- Top: the governing thought (exec summary slide, and the title of the deck).
- Middle: key lines. Each one is an assertion that supports the top, usually a section of the deck.
- Bottom: evidence slides. Each proves one key line with one exhibit.

Checks:
- **Vertical:** every slide answers the question "why?" or "how?" raised by the level above it.
- **Horizontal:** key lines are MECE (mutually exclusive, collectively exhaustive) and all of the same kind: all reasons, or all steps, or all options. Do not mix.
- Group in threes where you honestly can. Seven key lines means the grouping is not done.

## 3. SCR for the opening

Use Situation, Complication, Resolution for the executive summary and for any slide that has to reset context.

- **Situation:** what the audience already knows and agrees with. ("Margin fell from 7.8% to 4.9% while volume grew 11%.")
- **Complication:** what changed or what is wrong, which creates the question. ("Twelve of 140 lanes generate 80% of the loss.")
- **Resolution:** the answer, which is the governing thought. ("Reprice those lanes in two waves.")

For a decision meeting, end the exec summary with the ask: "Decision today: approve Wave 1."

## 4. Action titles

The title is the takeaway of the slide, written as a full sentence.

| Topic label (bad) | Action title (good) |
|---|---|
| Lane profitability | Twelve of 140 lanes generate 80% of the operating loss |
| Competitive pricing | Competitors already charge 9-14% more on these lanes, so the increase is defensible |
| Rollout plan | A two-wave rollout captures 60% of the upside in the first two quarters |

Rules:
- A full sentence with a verb and a so-what. About 15 words or fewer, and no more than two lines in the template's title box.
- Quantify where possible ("80%", "three points", "18 months").
- Make one claim. If it needs "and", split the slide.
- The body proves the title and nothing else. Content that does not support the title moves to another slide, the notes, or the appendix.
- Do not put a question in the title. Answer it.
- Title slides, section dividers and quote slides are framing, and they are exempt.

## 5. Ghost deck (title test)

Before building, list the titles alone, numbered. That list is the ghost deck. Read it aloud, top to bottom:

- Does it make the whole argument without the bodies?
- Does each title follow from the one before ("so", "because", "therefore")?
- Would a board member who reads only the titles reach the same decision?

`qa_deck.py` prints this list as "Storyline" on every run. Re-read it after each fix loop. Titles drift when bodies get edited.

## 6. One message per slide

- One exhibit per slide, or two when they make one comparison.
- At most six bullets, in parallel grammar. Use `**Lead-in:** detail` so the slide can be skimmed.
- Put the detail the presenter will say in the speaker notes, not on the slide.
- Every number carries a unit and a period. Every exhibit carries a source line: `Source: <system/report>, <period>; <method note>`.

## 7. Chart choice follows the message

| Message is about | Use | Avoid |
|---|---|---|
| Ranking / comparison across items | Horizontal bar, sorted, with the key item highlighted | Pie with more than 3 slices |
| Change over time (few points) | Column | Line with 3 points |
| Trend over time (many points) | Line, with at most 4 series labeled directly | Legend-only lines |
| Part of a whole (2-3 parts) | Stacked bar/column, or a pie if really only 2-3 parts | Doughnut with 8 slices |
| Composition shift over time | 100% stacked column | Several pies |
| Correlation | Scatter (outside build_deck's category charts: use the pptx skill or an image) | Dual-axis lines |
| Exact values that matter | Table, numbers right-aligned, key row bold | A chart the audience must squint at |

Chart hygiene: no gridlines, direct data labels instead of a value axis, one highlighted bar, and the insight in the title rather than in the chart title. Order bars by value unless the categories have a natural order (time, stages).

## 8. Deck skeleton for a decision

1. Title
2. Executive summary (SCR plus the ask), the whole deck on one page
3. 3-5 key-line sections, each with 1-3 evidence slides
4. Recommendation and next steps (owners, dates)
5. Appendix: methodology, sensitivity, detailed tables

Keep a main body of 8-15 slides for a 30-minute discussion. Everything else goes to the appendix.
