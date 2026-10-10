# Lace math

Replacement shoelaces, picked honestly. Count the eyelet pairs, walk the criss-cross, get the length your shoes actually need, then round up to a standard size off the rack. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/lacemath/

## The three tools

- **Lace length** - `lacePlan(pairs, gapH, gapV, tie)`: the bottom rung plus two diagonals per extra row plus tie allowance at each end, rounded to 0.1 cm.
- **Size pick** - `sizePick(lengthCm)`: rounds up to a labeled standard lace size (60, 75, 90, 100, 120, 140, 160, 180, 200 cm) and counts the spare.
- **Quick pick** - `quickPlan(eu)`: a labeled illustrative eyelet-pair norm for an EU shoe size, fed through the same length and size math.

## Labeled norms (illustrative references, not rules)

- Criss-cross model: base rung + 2 diagonals per extra row + tie allowance per end.
- Labeled typicals: 4.5 cm between eyelet columns, 2.5 cm between rows, 15 cm per end to tie.
- Labeled standard lace sizes: 60-200 cm; always round up.
- Labeled quick-pick norm: about 4-8 eyelet pairs across EU sizes.

Measure your own shoe when it matters.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (35 cases, 105 checks)

Regenerate the oracle expectations: `python3 oracle.py`
