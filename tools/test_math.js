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
// --- ROI: unified model (all lines added up)
const base = { s_transfer: 150000, r_transfer: 0.9, s_processing: 600000, r_processing: 0.8, s_storage: 240000, r_storage: 0.9,
               s_training: 400000, r_training: 0.8, s_energy: 100000, r_energy: 0.86, s_prep: 300000, r_prep: 0.7,
               c_dist: 16000, c_sol: 0, c_impl: 0 };
let v = Object.assign({}, base), o = roi.calc(v);
eq("roi lines", o.lines.length, 6);
eq("roi gross", o.gross, 135000 + 480000 + 216000 + 320000 + 86000 + 210000);
eq("roi net", o.net, 1447000 - 16000); eq("roi spend", o.spend, 1790000); eq("roi share", o.share, 1447000 / 1790000);
eq("roi 3y", o.three, 1431000 * 3); eq("roi payback immediate", o.payback, 0); eq("roi roi", o.roi, 1431000 / 16000);
v = Object.assign({}, base, { c_sol: 200000, c_impl: 300000 }); o = roi.calc(v);
eq("roi net lic", o.net, 1447000 - 216000); eq("roi first", o.first, 1231000 - 300000);
eq("roi payback", o.payback, Math.ceil(300000 / (1231000 / 12))); eq("roi 3y impl", o.three, 1231000 * 3 - 300000);
eq("roi roi impl", o.roi, (1231000 - 300000) / (216000 + 300000));
// --- second round: eligibility, baseline/eligible expenditure, first year, ROI and payback states
r = sim.simulate({ n: 4, vol: 25, tx: 0.8, el: 0.25, red: 0.6 });
eq("sim elig", r.eligible, 4 * 25 * 0.8 * 0.25); eq("sim raw kept", r.rawResidual, 80 * 0.75);
eq("sim opt partial", r.optimized, 60 + 20 * 0.4); eq("sim avoid partial", r.avoided, 20 * 0.6);
eq("sim conservation", r.optimized + r.avoided, r.baseline);
eq("sim zero elig avoided", sim.simulate({ n: 3, vol: 7, tx: 1, el: 0, red: 0.9 }).avoided, 0);
eq("sim zero elig dist", sim.simulate({ n: 3, vol: 7, tx: 1, el: 0, red: 0.9 }).distilled, 0);
eq("sim min", sim.simulate({ n: 1, vol: 0.001, tx: 0.01, el: 0.01, red: 0.01 }).avoided, 0.001 * 0.01 * 0.01 * 0.01);
v = Object.assign({}, base, { r_transfer: 0, r_processing: 0, r_storage: 0, r_training: 0, r_energy: 0, r_prep: 0 }); o = roi.calc(v);
eq("roi zero red gross", o.gross, 0); eq("roi zero red net", o.net, -16000); eq("roi zero red payback", o.payback === null ? 1 : 0, 1);
v = { c_dist: 0 }; o = roi.calc(v); eq("roi empty spend", o.spend, 0); eq("roi empty roi undefined", o.roi === null ? 1 : 0, 1);
eq("roi empty share", o.share, 0);
v = Object.assign({}, base, { c_impl: 5e6, c_dist: 2e6 }); o = roi.calc(v);
n++; if (!(o.roi < 0 && o.first < 0)) { fails++; console.log("FAIL negative roi"); }
v = Object.assign({}, base, { s_processing: 1e12, r_processing: 0.99 }); o = roi.calc(v);
n++; if (!isFinite(o.net) || !isFinite(o.roi)) { fails++; console.log("FAIL huge inputs not finite"); }
console.log(`${n - fails}/${n} assertions passed`); process.exit(fails ? 1 : 0);
