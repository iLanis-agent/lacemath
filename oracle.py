#!/usr/bin/env python3
"""Oracle mirror of engine.js for Lace math. Writes expected.json (with trailing newline)."""
import json, math

def r1(x): return math.floor(x * 10 + 0.5) / 10
def r2(x): return math.floor(x * 100 + 0.5) / 100

def jsnum(x):
    if isinstance(x, float) and x == int(x) and abs(x) < 1e15:
        return int(x)
    return x

def fmt(x):
    if isinstance(x, float) and x == int(x):
        return str(int(x))
    return repr(x) if isinstance(x, float) else str(x)

SIZES = [60, 75, 90, 100, 120, 140, 160, 180, 200]

def lacePlan(pairs, gapH, gapV, tie):
    if not (pairs > 0) or not (gapH > 0) or not (gapV > 0) or not (tie > 0):
        return {"error": "all lace inputs must be positive"}
    if pairs != math.floor(pairs + 0.5):
        return {"error": "eyelet pairs must be a whole number"}
    diag = math.sqrt(gapH * gapH + gapV * gapV)
    length = gapH + 2 * (pairs - 1) * diag + 2 * tie
    return {"pairs": jsnum(float(pairs)), "gapH": jsnum(float(gapH)), "gapV": jsnum(float(gapV)),
            "tie": jsnum(float(tie)), "diagonal": jsnum(r2(diag)), "lengthCm": jsnum(r1(length))}

def sizePick(lengthCm):
    if not (lengthCm > 0):
        return {"error": "length must be positive"}
    for s in SIZES:
        if s >= lengthCm:
            return {"lengthCm": jsnum(float(lengthCm)), "size": s, "spare": jsnum(r1(s - lengthCm)), "over": False}
    return {"lengthCm": jsnum(float(lengthCm)), "size": SIZES[-1], "spare": jsnum(r1(SIZES[-1] - lengthCm)), "over": True}

def quickPlan(eu):
    if not (eu > 0):
        return {"error": "shoe size must be positive"}
    if eu != math.floor(eu + 0.5):
        return {"error": "EU size must be a whole number"}
    pairs = min(8, max(4, math.floor(eu / 6 - 1 + 0.5)))
    plan = lacePlan(pairs, 4.5, 2.5, 15)
    pick = sizePick(plan["lengthCm"])
    return {"eu": jsnum(float(eu)), "pairs": pairs, "lengthCm": plan["lengthCm"], "size": pick["size"], "spare": pick["spare"], "over": pick["over"]}

def renderLace(r):
    return (fmt(r["pairs"]) + " eyelet pair" + ("" if r["pairs"] == 1 else "s") + " at a labeled " + fmt(r["gapH"]) +
            " cm across and " + fmt(r["gapV"]) + " cm between rows, with " + fmt(r["tie"]) +
            " cm each end to tie, needs about " + fmt(r["lengthCm"]) + " cm of criss-cross lace.")

def renderSize(r):
    if r["over"]:
        return "At " + fmt(r["lengthCm"]) + " cm you are past the labeled standard sizes - buy a labeled 200 cm lace and trim it."
    return fmt(r["lengthCm"]) + " cm rounds up to a labeled " + str(r["size"]) + " cm lace - " + fmt(r["spare"]) + " cm spare."

def renderQuick(r):
    return ("An EU " + fmt(r["eu"]) + " usually means about " + str(r["pairs"]) + " eyelet pairs (labeled illustrative norm) - about " +
            fmt(r["lengthCm"]) + " cm of lace, so a labeled " + str(r["size"]) + " cm lace" +
            (" to trim" if r["over"] else " with " + fmt(r["spare"]) + " cm spare") + ".")

CASES = []
def add(fn, args):
    CASES.append({"fn": fn, "args": args})

for a in [(6, 4.5, 2.5, 15), (1, 4.5, 2.5, 15), (5, 4, 2, 12), (7, 5, 3, 20), (4, 3.5, 2.5, 10),
          (8, 4.5, 2.5, 15), (3, 6, 4, 18), (2, 4.5, 2.5, 15), (0, 4.5, 2.5, 15), (6.5, 4.5, 2.5, 15),
          (6, 0, 2.5, 15), (-2, 4.5, 2.5, 15)]:
    add("lacePlan", list(a))
for a in [(86.0,), (90.0,), (45.0,), (60.0,), (199.9,), (200.0,), (205.0,), (100.1,), (0,), (-5,)]:
    add("sizePick", list(a))
for a in [(36,), (42,), (30,), (46,), (50,), (28,), (40,), (44,), (35,), (48,), (0,), (41.5,), (-38,)]:
    add("quickPlan", list(a))

out = []
for c in CASES:
    fn = {"lacePlan": lacePlan, "sizePick": sizePick, "quickPlan": quickPlan}[c["fn"]]
    res = fn(*c["args"])
    is_err = "error" in res
    if is_err:
        render = res["error"]
    else:
        render = {"lacePlan": renderLace, "sizePick": renderSize, "quickPlan": renderQuick}[c["fn"]](res)
    out.append({"fn": c["fn"], "args": c["args"], "result": res, "render": render, "isError": is_err})

with open("expected.json", "w") as f:
    f.write(json.dumps(out, separators=(",", ":")) + "\n")
print("wrote", len(out), "cases")
