# OCR for scanned statements

## When

`extract_statement.py` counts characters per page before doing anything else.
- Every page empty (or under 20 chars per page on average): exits 3 with `NO TEXT LAYER`. OCR the whole file.
- Some pages empty: continues, and prints `pages with no text layer: [...]`. Those pages yield no rows and prove.py will fail on counts or tie-out. OCR the file (ocrmypdf skips pages that already have text) and re-run.
- Text layer present but garbage (a bad OCR layer from the scanner: `l` for `1`, `O` for `0`, missing decimals): extraction produces few rows or many `unparsed`/no-amount flags. Redo OCR with `--force-ocr`.

Quick manual check: `pdftotext -layout file.pdf - | head -50` (poppler). No output means no text layer.

## How

Install (optional dependency, not needed for digital PDFs):

```
brew install ocrmypdf tesseract tesseract-lang      # macOS
apt-get install ocrmypdf tesseract-ocr-deu           # Debian/Ubuntu, plus language packs
```

Run:

```
ocrmypdf --deskew --rotate-pages --clean -l eng --output-type pdf in.pdf ocr.pdf
ocrmypdf --force-ocr -l deu+eng in.pdf ocr.pdf        # replace a bad existing text layer
ocrmypdf --redo-ocr in.pdf ocr.pdf                    # keep vector text, OCR only images
```

- Set `-l` to the statement language. The language model decides whether `1.234,56` survives OCR intact.
- Use `--deskew` for phone photos and fax scans, because column bands assume columns are vertical.
- Resolution: 300 dpi source is the floor for 8pt statement text. When the scan is lower, `--oversample 300` helps a little.
- Then run `extract_statement.py ocr.pdf ...` as normal. OCR text layers are word-positioned, so the same band logic applies. Expect looser line spacing, and use `--dump-words` to set `--bands` if the header was misread.

Without ocrmypdf, tesseract alone can make a searchable PDF page by page:

```
pdftoppm -r 300 -png in.pdf page
for f in page-*.png; do tesseract "$f" "${f%.png}" -l eng pdf; done
# then merge (qpdf --empty --pages page-*.pdf -- ocr.pdf)
```

## Confidence

OCR output is a reading, not a fact. Treat it as such:
- tesseract reports a confidence for every word: `tesseract page.png - --psm 6 tsv`, column `conf`. Words under about 80 in an amount column deserve a look. The skill does not import that score automatically. When a proof fails on an OCR'd page, pull the TSV for that page and check the confidence of the amounts in the localized span.
- Typical OCR confusions in amounts: `1`/`7`, `3`/`8`, `5`/`6`, `0`/`8`, a decimal point dropped or read as a comma, a minus sign or trailing `-` lost, `(` read as `1` or `C`. Each produces a specific proof signature: a single-digit error gives a gap that is a multiple of 1, 10 or 100 in one row, while a lost sign gives twice the amount.

## Re-check

The proof is what makes OCR usable. After OCR:
1. Run prove.py. With a running balance, every OCR digit error in an amount breaks the chain at that row, and every error in a balance produces two opposite breaks. Both get pinpointed.
2. For each break, crop the page image around the reported y (`pdftoppm -r 300 -f N -l N -x ... -y ... -W ... -H ...`) and read that one figure. Correct it in the CSV only when the image clearly shows the figure, add `source=visual` to that row's flags, and re-run prove.py.
3. Without a running balance, OCR errors can only be caught by the tie-out, the summary totals and the counts. Say so in the handoff, and list rows where OCR confidence was low.
4. Never accept an OCR'd statement as final because it "looks right". Accept it when prove.py says PROVEN, or report the remaining gap.
