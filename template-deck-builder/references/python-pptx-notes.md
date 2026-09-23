# python-pptx notes for template-bound decks

Checked against the python-pptx docs (https://python-pptx.readthedocs.io, "Understanding placeholders", "Working with placeholders", "Charts", the text auto-fit analysis pages) and against python-pptx 1.0.2 behavior in this skill's tests. Items marked *(observed)* were verified by running code, not taken from the docs.

## Units

- EMU (English Metric Unit): 914,400 per inch, 12,700 per point, 360,000 per cm. Use `pptx.util.Inches/Pt/Emu/Cm`.
- A 16:9 slide is 12,192,000 x 6,858,000 EMU (13.333 x 7.5 in). A 4:3 slide is 9,144,000 x 6,858,000 (10 x 7.5 in). Always read `prs.slide_width/height` and never assume.
- Font sizes in XML are hundredths of a point (`sz="1800"` = 18pt). Spacing: `spcPts val="600"` = 6pt, `spcPct val="20000"` = 20% of a line.

## Masters, layouts, placeholders

- Inheritance, from the docs: "A layout placeholder inherits from the master placeholder sharing the same type. A slide placeholder inherits from the layout placeholder having the same *idx* value." Position, size, fill, line and font all inherit.
- Access placeholders by idx, not by position: "Item access on the placeholders collection is like that of a dictionary rather than a list." `slide.placeholders[1]` means idx 1.
- `prs.slides.add_slide(layout)` clones the layout's placeholders **except date, footer and slide number** *(observed)*. Footers come from the master/layout only when the header-footer settings enable them. Do not fake them with text boxes.
- A placeholder with no `<a:xfrm>` of its own inherits its geometry. Reading `.left` returns the inherited value. **Setting `.left` alone creates a new xfrm with y=0 and height=0** *(observed)*: always set all four (left, top, width, height), or none.
- Placeholder types that matter: TITLE / CENTER_TITLE (title), SUBTITLE, BODY (text only), OBJECT (generic content: text, chart, table or picture), CHART, TABLE, PICTURE, plus DATE / FOOTER / SLIDE_NUMBER chrome. A placeholder with no `type` attribute is OBJECT.
- Only picture, table and chart placeholders have insertion methods (`insert_picture`, `insert_table`, `insert_chart`). "A reference to a ... placeholder becomes invalid after its insert_... method is called." Record the idx before inserting. The new shape can be fetched with `slide.placeholders[idx]`.
- To put a chart or table into an OBJECT placeholder, the way PowerPoint itself does it, wrap the element: `ChartPlaceholder(ph._element, ph._parent).insert_chart(...)` or `TablePlaceholder(...).insert_table(rows, cols)`. The result is a graphicFrame with `<p:ph idx=.../>`, positioned at the placeholder. `build_deck.py` does this. For a text-only BODY placeholder, it copies the geometry and removes the placeholder.
- Empty placeholders show "Click to add text" in edit view only. They are invisible in slideshow and PDF, which is why they slip through. Remove them: `ph._element.getparent().remove(ph._element)`.
- `SlideLayouts.remove(layout)` raises ValueError if any slide uses the layout. `layout.used_by_slides` tells you which ones do.

## Slides

- No API deletes a slide. Drop the relationship and the id: `prs.part.drop_rel(sldId.rId); prs.slides._sldIdLst.remove(sldId)`. The orphaned part is not written on save.
- Reorder by moving `sldId` elements within `prs.slides._sldIdLst`.
- Copying a slide between presentations is not supported. Deep-copying shapes loses rels (images, charts). Rebuild from the target deck's own layouts instead.
- Speaker notes: `slide.notes_slide.notes_text_frame.text = "..."` creates the notes slide from the notes master on first access.

## Opening .potx

python-pptx rejects a .potx because its main part content type is `presentationml.template.main+xml`. Rewrite `[Content_Types].xml` to `presentationml.presentation.main+xml` in memory and open that (`tdb_common.open_presentation`). Save the output as .pptx.

## Text and autofit (the overflow trap)

- `text_frame.auto_size`: `MSO_AUTO_SIZE.NONE`, `SHAPE_TO_FIT_TEXT` (`<a:spAutoFit/>`, the shape grows), `TEXT_TO_FIT_SHAPE` (`normAutofit`, shrink on overflow).
- Setting `TEXT_TO_FIT_SHAPE` writes `<a:normAutofit/>` but python-pptx does **not** compute the shrink. The docs note that PowerPoint writes a calculated `fontScale` and that "Later edits to that text using PowerPoint will re-fit the text automatically." PowerPoint generally shows such text at full size, overflowing, until someone edits it. LibreOffice applies its own shrink at render time *(observed)*, so a PDF can look fine while the .pptx does not.
- `text_frame.fit_text(font_family, max_size, bold, italic, font_file)` needs a TrueType file, sets `auto_size = NONE`, and writes one fixed size into every run. That breaks the template's type scale. Prefer cutting words.
- Many corporate masters set `normAutofit` on title and body. Treat it as a safety net, not a layout tool. `qa_deck.py` estimates fit at the nominal size and reports reliance on autofit.
- Text frame defaults: insets of 0.1in left/right and 0.05in top/bottom, word wrap on for placeholders. A new text box from `add_textbox` gets `wrap="none"` and `<a:spAutoFit/>` *(observed)*: set `word_wrap = True` or a long line runs off the slide.
- Setting `run.font.size` or `run.font.name` writes run-level overrides that beat the template. Only set them when the spec requires it (tables, source lines). Never set typefaces: the theme's `+mj-lt` / `+mn-lt` references keep the deck re-themeable.
- `paragraph.level` (0-8) selects the master's lvlNpPr bullet style. Use levels, not manual indents or typed bullet characters.

## Charts

- `CategoryChartData(number_format=...)`, `.categories = [...]`, `.add_series(name, values)`. Use `XyChartData` / `BubbleChartData` for scatter and bubble.
- The docs: "By default, the colors assigned to each series in a chart are the theme colors Accent 1 through Accent 6, in that order." Set colors explicitly with `fill.fore_color.theme_color = MSO_THEME_COLOR.ACCENT_n` (and `.brightness` for tints). Never use `.rgb`, which hard-codes a color that survives a re-theme. QA flags any srgbClr outside the theme palette.
- Per-point color: `series.points[i].format.fill`. It highlights one bar.
- `chart.font.size` sets the default text size for the whole chart. Data labels: `plot.has_data_labels = True`, `plot.data_labels.number_format = '0%'`, `number_format_is_linked = False` (otherwise the source format wins).
- `value_axis.has_major_gridlines = False`, `value_axis.visible = False` when labels carry the values. For bar charts, `category_axis.reverse_order = True` so the first category is on top.
- `chart.replace_data(chart_data)` updates an existing chart in place and keeps its formatting. Use it when editing decks.
- The chart workbook is embedded. The numbers are editable in PowerPoint, which is an advantage over pasting images.

## Tables

- `insert_table(rows, cols)` / `shapes.add_table(...)` sizes the frame to the placeholder and divides the height evenly across rows. The row height is a minimum: rows grow with wrapped text when rendered, so a long table can run off the slide even though its frame fits. `qa_deck.py` estimates the grown height.
- The default table style is `{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}` (Medium Style 2 - Accent 1) *(observed)*, which is theme-driven. `table.first_row = True` styles the header. Leave the style in place and change only what the message needs (bold key row, right-aligned numbers).
- Merge cells with `cell.merge(other_cell)`. Set column widths through `table.columns[i].width`, and make them sum to the frame width.

## Common breakages and their fixes

| Symptom | Cause | Fix |
|---|---|---|
| Deck looks right but "does not use the template" | Built on Blank with text boxes | Use the layouts from `layout_map.json` |
| Title jumps position slide to slide | Placeholder xfrm overridden | Remove the slide-level `<a:xfrm>` so it inherits |
| Chart colors ignore the brand | `.rgb` fills, or a chart pasted as an image | Theme colors, native chart |
| Text fine in PDF, overflowing in PowerPoint | `normAutofit` without fontScale | Cut text, then re-check with QA |
| "Click to add text" in the client's edit view | Empty placeholders left behind | Remove unused placeholders |
| Wrong fonts after sending | Run-level `latin typeface` overrides | Remove them, inherit `+mn-lt` / `+mj-lt` |
| Footer and slide number missing | python-pptx does not clone them | Enable them in the template's header/footer settings |
| Zero-height placeholder at the top of the slide | Set `.left` on an inheriting placeholder | Set all four geometry values |
| PPTX will not open after an XML edit | Child elements out of schema order (for example `buNone` after `defRPr`) | Insert elements in the CT_ order, or rebuild the element |
