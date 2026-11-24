/* Math tests for the simulator and ROI calculator. Run: node tools/test_math.js */
const path = require("path");
const root = process.argv[2] || path.join(__dirname, "..");
const sim = require(path.join(root, "assets/js/simulator.js"));
const roi = require(path.join(root, "assets/js/roi.js"));
let fails = 0, n = 0;
function eq(name, a, b, tol = 1e-6) { n++; if (Math.abs(a - b) > tol * Math.max(1, Math.abs(b))) { fails++; console.log("FAIL", name, a, "!=", b); } }
// --- simulator: manufacturing preset (spec 7.4)
let r = sim.simulate({ n: 20, vol: 10, tx: 1, el: 1, red: 0.9 });
eq("orig", r.original, 200); eq("base", r.baseline, 200); eq("opt", r.optimized, 20); eq("avoid", r.avoided, 180); eq("rel", r.relative, 0.9);
// partial eligibility and transfer
r = sim.simulate({ n: 10, vol: 50, tx: 0.6, el: 0.5, red: 0.8, ctr: 20, cproc: 30 });
eq("base2", r.baseline, 300); eq("raw2", r.rawResidual, 150); eq("dist2", r.distilled, 30); eq("opt2", r.optimized, 180); eq("avoid2", r.avoided, 120);
eq("identity", r.avoided, r.baseline * 0.5 * 0.8); eq("money2", r.money, 120 * 50);
// boundaries
r = sim.simulate({ n: 0, vol: 10, tx: 1, el: 1, red: 0.9 }); eq("zero n", r.baseline, 0); eq("zero rel", r.relative, 0);
r = sim.simulate({ n: 5, vol: 10, tx: 0, el: 1, red: 0.9 }); eq("no transfer", r.optimized, 0); eq("no transfer orig", r.original, 50);
r = sim.simulate({ n: 5, vol: 10, tx: 1, el: 0, red: 0.9 }); eq("none eligible", r.avoided, 0); eq("none eligible opt", r.optimized, 50);
r = sim.simulate({ n: 5, vol: 10, tx: 1, el: 1, red: 0 }); eq("no reduction", r.avoided, 0);
r = sim.simulate({ n: 200, vol: 100000, tx: 1, el: 1, red: 0.99 }); eq("max", r.optimized, 200000); eq("max avoid", r.avoided, 19800000);
console.log("fmt", sim.fmtTB(0), "|", sim.fmtTB(0.25), "|", sim.fmtTB(2.5), "|", sim.fmtTB(180), "|", sim.fmtTB(19800000));
// scenario D telecom & E multicloud arithmetic from case content
eq("telecom", sim.simulate({ n: 12, vol: 50, tx: 1, el: 1, red: 0.85 }).optimized, 90);
eq("telecom avoid", sim.simulate({ n: 12, vol: 50, tx: 1, el: 1, red: 0.85 }).avoided, 510);
eq("multicloud", 40 * 0.6 * 0.8, 19.2);
// --- ROI: transfer model
const base = { c_red: 0.7, c_val: 15000, c_sol: 0, c_impl: 0, c_hrs: 0, c_hsave: 0, c_rate: 0 };
let v = Object.assign({}, base, { t_dom: 4, t_vol: 20, t_elig: 0.5, t_ctr: 20, t_cing: 10, t_cproc: 20, t_cst: 25, t_ret: 12, t_over: 5 });
let o = roi.calc("transfer", v);
const moved = 4 * 20 * 12 * 0.5, stored = 4 * 20 * 0.5 * 12;            // 480 TB/yr, 480 TB held
eq("roi transfer", o.lines[0][1], moved * 0.7 * 20); eq("roi ingest", o.lines[1][1], moved * 0.7 * 10);
eq("roi proc", o.lines[2][1], moved * 0.7 * 20); eq("roi store", o.lines[3][1], stored * 0.7 * 25 * 12);
const gross = moved * 0.7 * 50 + stored * 0.7 * 300; eq("roi gross", o.gross, gross);
eq("roi net", o.net, gross - moved * 5 - 15000);
// license, implementation and payback
v.c_sol = 20000; v.c_impl = 60000; o = roi.calc("transfer", v);
eq("roi net lic", o.net, gross - moved * 5 - 15000 - 20000); eq("roi 3y", o.three, o.net * 3 - 60000);
eq("roi payback", o.payback, Math.ceil(60000 / (o.net / 12)));
// training model: only data-proportional share, energy informational (no double count)
v = Object.assign({}, base, { r_spend: 400000, r_share: 0.6, r_runs: 12, r_rcost: 1500, r_kwh: 100000, r_dkwh: 200, r_price: 0.15, r_hours: 1000 });
o = roi.calc("training", v);
eq("roi train", o.gross, 400000 * 0.6 * 0.7); eq("roi train net", o.net, 168000 - 18000 - 15000);
eq("roi energy net", o.energy.net, 100000 * 0.6 * 0.7 - 12 * 200);
eq("roi train lines", o.lines.length, 1);  // energy not added as a saving line
// infrastructure model
v = Object.assign({}, base, { i_tb: 500, i_cst: 25, i_comp: 300000, i_share: 0.6, i_kwh: 0, i_price: 0.15, i_ocost: 20000, i_okwh: 0, i_grid: 0 });
o = roi.calc("infrastructure", v);
eq("roi infra", o.gross, 500 * 0.7 * 25 * 12 + 300000 * 0.6 * 0.7); eq("roi infra lines", o.lines.length, 2);
v.i_kwh = 50000; v.i_okwh = 5000; v.i_grid = 0.25; o = roi.calc("infrastructure", v);
eq("roi infra energy", o.lines[2][1], 50000 * 0.7 * 0.15); eq("roi infra co2", o.energy.co2, (50000 * 0.7 - 5000) * 0.25 / 1000);
eq("roi infra ded", o.deductions, 20000 + 5000 * 0.15 + 15000);
// zeros and negative net
v = Object.assign({}, base, { c_red: 0, t_dom: 4, t_vol: 20, t_elig: 0.5, t_ctr: 20, t_cing: 10, t_cproc: 20, t_cst: 25, t_ret: 12, t_over: 5 });
o = roi.calc("transfer", v); eq("roi zero red gross", o.gross, 0); n++; if (!(o.net < 0)) { fails++; console.log("FAIL net should be negative"); }
eq("roi zero red payback", o.payback === null ? 0 : 1, 0);
// operational hours are reported but not added to net
v = Object.assign({}, base, { c_hrs: 2000, c_hsave: 0.25, c_rate: 80, r_spend: 0, r_share: 0, r_runs: 0, r_rcost: 0, r_kwh: 0, r_dkwh: 0, r_price: 0, r_hours: 0 });
o = roi.calc("training", v); eq("ops hours", o.ops[0][1], 500); eq("ops value", o.ops[1][1], 40000); eq("ops not in net", o.net, -15000);

// --- second round: eligibility, baseline/eligible expenditure, first year, ROI and payback states
r = sim.simulate({ n: 4, vol: 25, tx: 0.8, el: 0.25, red: 0.6 });
eq("sim elig", r.eligible, 4 * 25 * 0.8 * 0.25); eq("sim raw kept", r.rawResidual, 80 * 0.75);
eq("sim opt partial", r.optimized, 60 + 20 * 0.4); eq("sim avoid partial", r.avoided, 20 * 0.6);
eq("sim conservation", r.optimized + r.avoided, r.baseline);
eq("sim zero elig avoided", sim.simulate({ n: 3, vol: 7, tx: 1, el: 0, red: 0.9 }).avoided, 0);
eq("sim zero elig dist", sim.simulate({ n: 3, vol: 7, tx: 1, el: 0, red: 0.9 }).distilled, 0);
eq("sim min", sim.simulate({ n: 1, vol: 0.001, tx: 0.01, el: 0.01, red: 0.01 }).avoided, 0.001 * 0.01 * 0.01 * 0.01);
v = Object.assign({}, base, { t_dom: 4, t_vol: 20, t_elig: 0.5, t_ctr: 20, t_cing: 10, t_cproc: 20, t_cst: 25, t_ret: 12, t_over: 5 });
o = roi.calc("transfer", v);
eq("roi baseline", o.baseline, 4 * 20 * 12 * 50 + 4 * 20 * 12 * 25 * 12); eq("roi eligible", o.eligible, o.baseline * 0.5);
eq("roi gross = eligible x r", o.gross, o.eligible * 0.7);
eq("roi first (no impl)", o.first, o.net); eq("roi payback immediate", o.payback, 0);
eq("roi roi", o.roi, o.first / o.deductions);
v.c_val = 0; v.t_over = 0; o = roi.calc("transfer", v); eq("roi undefined roi", o.roi === null ? 1 : 0, 1);
v = Object.assign({}, base, { c_val: 0, r_spend: 0, r_share: 0.6, r_runs: 0, r_rcost: 0, r_kwh: 0, r_dkwh: 0, r_price: 0, r_hours: 0 });
o = roi.calc("training", v); eq("roi zero baseline", o.baseline, 0); eq("roi zero baseline net", o.net, 0);
eq("roi zero baseline payback", o.payback === null ? 1 : 0, 1);
v = Object.assign({}, base, { c_impl: 50000, r_spend: 100000, r_share: 0.5, r_runs: 10, r_rcost: 5000, r_kwh: 0, r_dkwh: 0, r_price: 0, r_hours: 0 });
o = roi.calc("training", v); eq("roi negative net", o.net, 35000 - 50000 - 15000);
eq("roi negative roi", o.roi, (o.net - 50000) / (65000 + 50000)); eq("roi negative payback", o.payback === null ? 1 : 0, 1);
v = Object.assign({}, base, { i_tb: 1e6, i_cst: 1000, i_comp: 1e12, i_share: 1, i_kwh: 0, i_price: 0, i_ocost: 0, i_okwh: 0, i_grid: 0, c_red: 0.99 });
o = roi.calc("infrastructure", v); n++; if (!isFinite(o.net) || !isFinite(o.roi)) { fails++; console.log("FAIL huge inputs not finite"); }
console.log(`${n - fails}/${n} assertions passed`); process.exit(fails ? 1 : 0);
