#!/usr/bin/env bash
# End-to-end test: sample template -> inspect -> good build + QA (expect 0 errors)
# -> bad build + sloppy hand edit + QA (expect errors caught). Output goes to $1.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
S="$HERE/../scripts"
OUT="${1:?usage: run_tests.sh OUT_DIR (keep it outside the skill folder)}"
mkdir -p "$OUT"
python3 -c "import pptx" 2>/dev/null || { echo "python-pptx missing: pip install python-pptx"; exit 2; }

echo "== 1. sample template"
python3 "$HERE/make_sample_template.py" "$OUT" || exit 1
echo "== 2. inspect (.potx path)"
python3 "$S/inspect_template.py" "$OUT/sample_template.potx" -o "$OUT/layout_map.json" || exit 1

echo "== 3. good storyboard: build + QA (expect exit 0)"
python3 "$S/build_deck.py" "$HERE/storyboard_good.json" --template "$OUT/sample_template.potx" -o "$OUT/good.pptx" || exit 1
python3 "$S/qa_deck.py" "$OUT/good.pptx" --storyboard "$HERE/storyboard_good.json" --out-dir "$OUT/qa_good"
good=$?

echo "== 4. bad storyboard: build + sloppy edit + QA (expect exit 1)"
python3 "$S/build_deck.py" "$HERE/storyboard_bad.json" --template "$OUT/sample_template.potx" -o "$OUT/bad_built.pptx"
python3 "$HERE/sloppy_edit.py" "$OUT/bad_built.pptx" "$OUT/bad.pptx" || exit 1
python3 "$S/qa_deck.py" "$OUT/bad.pptx" --storyboard "$HERE/storyboard_bad.json" --out-dir "$OUT/qa_bad"
bad=$?

echo "== 5. edit mode: change slide 3 title + notes in place, keep masters"
cat > "$OUT/edits.json" <<'JSON'
{"slides": [{"edit": 3, "title": "Twelve lanes drive 80% of the loss, so the fix is targeted", "notes": "Edited in place."}],
 "expected_slide_count": 6}
JSON
python3 "$S/build_deck.py" "$OUT/edits.json" --edit "$OUT/good.pptx" -o "$OUT/good_edited.pptx" || exit 1
python3 "$S/qa_deck.py" "$OUT/good_edited.pptx" --storyboard "$OUT/edits.json" --out-dir "$OUT/qa_edit" --no-render
edit=$?

echo
echo "RESULT good_qa_exit=$good (want 0)  bad_qa_exit=$bad (want 1)  edit_qa_exit=$edit (want 0)"
[ "$good" = 0 ] && [ "$bad" = 1 ] && [ "$edit" = 0 ] && echo PASS || { echo FAIL; exit 1; }
