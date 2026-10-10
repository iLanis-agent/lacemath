/* Lace math engine - pure arithmetic, every borrowed number labeled. */
(function (root) {
  "use strict";
  function r1(x) { return Math.round(x * 10) / 10; }
  function r2(x) { return Math.round(x * 100) / 100; }
  var SIZES = [60, 75, 90, 100, 120, 140, 160, 180, 200];

  function lacePlan(pairs, gapH, gapV, tie) {
    if (!(pairs > 0) || !(gapH > 0) || !(gapV > 0) || !(tie > 0)) return { error: "all lace inputs must be positive" };
    if (pairs !== Math.round(pairs)) return { error: "eyelet pairs must be a whole number" };
    var diag = Math.sqrt(gapH * gapH + gapV * gapV);
    var length = gapH + 2 * (pairs - 1) * diag + 2 * tie;
    return { pairs: pairs, gapH: gapH, gapV: gapV, tie: tie, diagonal: r2(diag), lengthCm: r1(length) };
  }

  function sizePick(lengthCm) {
    if (!(lengthCm > 0)) return { error: "length must be positive" };
    for (var i = 0; i < SIZES.length; i++) {
      if (SIZES[i] >= lengthCm) return { lengthCm: lengthCm, size: SIZES[i], spare: r1(SIZES[i] - lengthCm), over: false };
    }
    return { lengthCm: lengthCm, size: SIZES[SIZES.length - 1], spare: r1(SIZES[SIZES.length - 1] - lengthCm), over: true };
  }

  function quickPlan(eu) {
    if (!(eu > 0)) return { error: "shoe size must be positive" };
    if (eu !== Math.round(eu)) return { error: "EU size must be a whole number" };
    var pairs = Math.min(8, Math.max(4, Math.round(eu / 6 - 1)));
    var plan = lacePlan(pairs, 4.5, 2.5, 15);
    var pick = sizePick(plan.lengthCm);
    return { eu: eu, pairs: pairs, lengthCm: plan.lengthCm, size: pick.size, spare: pick.spare, over: pick.over };
  }

  function renderLace(r) {
    return r.pairs + " eyelet pair" + (r.pairs === 1 ? "" : "s") + " at a labeled " + r.gapH + " cm across and " + r.gapV + " cm between rows, with " + r.tie + " cm each end to tie, needs about " + r.lengthCm + " cm of criss-cross lace.";
  }

  function renderSize(r) {
    if (r.over) return "At " + r.lengthCm + " cm you are past the labeled standard sizes - buy a labeled 200 cm lace and trim it.";
    return r.lengthCm + " cm rounds up to a labeled " + r.size + " cm lace - " + r.spare + " cm spare.";
  }

  function renderQuick(r) {
    return "An EU " + r.eu + " usually means about " + r.pairs + " eyelet pairs (labeled illustrative norm) - about " + r.lengthCm + " cm of lace, so a labeled " + r.size + " cm lace" + (r.over ? " to trim" : " with " + r.spare + " cm spare") + ".";
  }

  var api = { lacePlan: lacePlan, sizePick: sizePick, quickPlan: quickPlan, renderLace: renderLace, renderSize: renderSize, renderQuick: renderQuick };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.LaceMath = api;
})(typeof window !== "undefined" ? window : this);
