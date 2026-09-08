# T19 — Parent mathematics independent audit

Date: 2026-09-07. Writer barrier and cross-writer audit explicitly authorized by parent. Scope: exactly 19 assigned pages, listed below. All 19 actual drafts read in full. No other agent drafts or canonical source houses edited; no global or local hygiene sweep run.

## Findings and repairs

The principal mathematical constructions and worked examples survive substantive review. No false theorem was found in the 19 assigned drafts. Repaired pervasive prose joins around numerals, units, inline formulas and Greek symbols while preserving mathematical code, URLs and frontmatter. Examples include `a240Hz`, `4nor5divides6`, `firstnpositive`, `angleθabout`, and missing spaces at inline-code boundaries. Standardised prose 12-TET spacing; Q8 and E4 identities preserved.

Removed both unverified NASA fragment suffixes in Metonic, preserving the exact base URL https://eclipse.gsfc.nasa.gov/LEsaros/LEperiodicity.html . Opened the actual NASA page independently: the three lunar periods, 223-month Saros and variation qualifications are present; no fragment validity claim retained.

Two mathematical exposition repairs make implicit conditions explicit:

- Grothendieck: supplied transitivity witness d+t+u, displaying the equality without assuming cancellation in the source monoid. The original theorem and injectivity criterion are preserved.
- Qubit: stated r_z=(1−|z|²)/(1+|z|²) for z=beta/alpha. Its north-at-zero convention differs by vertical reflection from the companion Riemann-sphere page's south-at-zero stereographic convention. Both constructions remain correct; the comparison now names the coordinate change.

No authorial operation was weakened or recast as a mathematical mistake. Native signatures, exact external operations and Argued/Offered cross-register relations remain distinct.

## Actual coverage and checks

| Assigned page | Substantive checks |
|---|---|
| harmonics/whole-tone-return | Multiplicative 9/8 residue; 240/480 Hz examples; 64/36 equivalence; pure/tempered distinction. |
| harmonics/cymatics-standing-waves | Exact wave equation substitution, fixed-end spectrum, four n=3 nodes and three antinodes; proposed 8+4 and experimental source boundary. |
| harmonics/cycle-interval-octave | Log-frequency quotient, six even/odd orbits and twelve fifth steps, octave displacements, A-sharp→C two-semitone return. |
| harmonics/pythagorean-comma | 531441/524288 from twelve fifths and six tones; D-sharp/E-flat quotient; 23.46 cents; logarithmic tempering. |
| harmonics/tetraktys-triangle | Sum10, 3–4–5 metric/area6/perimeter12, factor-occurrence counts and asymmetric exponent flip. |
| harmonics/perfect-six | Divisor enumeration and minimality; product coincidence; 28 sum/product counterexample; zero and quotient offices. |
| harmonics/metonic-antikythera-cycle | Exact228+7=235 and twelve ordinary/seven intercalary count; symbolic residual; Saros distinction; NASA links repaired. |
| topology/projective-line | Nonzero homogeneous classes, both charts, reciprocal involution, real/complex dimensional difference. |
| topology/riemann-sphere | Sphere equation and inverse algebra; reciprocal extension; one-point completion versus torus quotient; no sphere/no-dynamics claim. |
| topology/projective-completion | Explicit parallel-line intersection [1:2:0]; homogeneous/intrinsic dimension; point versus line at infinity. |
| topology/mobius-klein-surfaces | a b a-inverse=b-inverse; a-squared translation; orientation parity and index-two torus cover. |
| formal-neighbours/crt-z6 | Six images, inverse3a+4b, all36 input pairs for addition/multiplication; coprimality and zero divisors. |
| formal-neighbours/trivial-ring | Manual distributivity/additive-cancellation proof of zero absorption and a=a1=a0=0; compatible singleton convention and distinct native slash. |
| formal-neighbours/grothendieck-group-loss | Stabilised equivalence and explicit transitivity; universal property; injectivity iff cancellation; all16 pair comparisons in idempotent example collapse. |
| formal-neighbours/calculus-infinity-dx | MVT argument on interval; disconnected counterexample; F=x²+3 condition; definite integral/initial datum distinction. |
| formal-neighbours/cross-ratio | Determinant/difference formula, 4/3 example, reciprocal permutation, infinity limit, 32/27 nonlinear counterexample; non-affine fractional-linear numerical checks. |
| formal-neighbours/qubit-bloch-sphere | Pure-state parameterisation, orthogonal plus/minus, density characteristic polynomial and positivity; common/relative phase; coordinate reflection clarified. |
| formal-neighbours/quaternion-q8 | Matrix generators, all64 products for closure, conjugation half-turn, six-unit nonclosure, continuous cover kernel distinct from Q8. |
| formal-neighbours/chaos-attractors | Exact gradient decrease; equilibrium derivative; explicit positive-basin solution and limit; boundary sensitivity not chaotic dynamics. |

Computational verification: the script is retained at `working/p2-enrichment/receipts/T19-parent-mathematics-check.py` (original run from `/tmp/T19-parent-mathematics-check.py`) run under `/tmp/T19-noether-check-venv/bin/python`, with actual rational arithmetic, SymPy differentiation/algebra/matrices and explicit recurrence/flow calculations. All checks passed. The proof arguments above additionally received manual review; the calculation script is not represented as proving topology or general abstract algebra by finite sampling.

## Source and continuity standing

Fresh full Scholtz and NIST SOURCE reads, sibling NOTES absent; their verified ratio and complex-analysis cards match the uses. Ran source effects depth4 for both into `/tmp/T19-audit-scholtz-effects.json` and `/tmp/T19-audit-nist-effects.json`; inspected declared section consumers and three previously recovered transverse-thread memberships. The current core/native whole and source-specific recovery from this writing session remain the authorial ground. This bounded audit does not claim a new universal primary-source reacquisition or fresh whole-corpus reread.

Source debts remain exactly scoped: physical cymatics apparatus and proposed 8+4 demonstration; historical Pythagorean testimony beyond arithmetic; uncollated Antikythera gearing/kinematic specifics; Hatcher exact quotation locators; distinct primary quantum/historical source intake beyond the explicit mathematical state model; Grothendieck/K-theory bibliography beyond the supplied construction; psychological empirical or passage-level claims beyond their housed standing. No citation/quotation readiness was promoted and no source NOTES was changed.

## Final file hashes

- `submission-package/essay/symbolon/matheme/harmonics/whole-tone-return.md`: `5490bd2a2644d3d58109e149db18211ec6a6b8dcc403aa4e9820a09273dc2b6c`
- `submission-package/essay/symbolon/matheme/harmonics/cymatics-standing-waves.md`: `18844ff980c111bc0cf8f589e8c343edb944b2012b4ca6f10a22ecd36acda8da`
- `submission-package/essay/symbolon/matheme/harmonics/cycle-interval-octave.md`: `e753292d9ede4e64b90c67c95b926e7ae811eab6c9937fda94b3de149a8b036e`
- `submission-package/essay/symbolon/matheme/harmonics/pythagorean-comma.md`: `85b771ca4c20fc56dd72dd4851dae39137757cd1b6005b51754aec3a0a66d668`
- `submission-package/essay/symbolon/matheme/harmonics/tetraktys-triangle.md`: `32a0d3a26386446a4bc2a06f2a67e0247f3c8e71bf9c81ad81c376f133373362`
- `submission-package/essay/symbolon/matheme/harmonics/perfect-six.md`: `27a6d07a07deb05d9b4a6869b7e2fa262accc542167c46adccb3a72dc66f9ebb`
- `submission-package/essay/symbolon/matheme/harmonics/metonic-antikythera-cycle.md`: `0d844379502a1ea08034a7adebe48909f77b1e14d083a60a3c6914e890ce871b`
- `submission-package/essay/symbolon/matheme/topology/projective-line.md`: `f7bfe18a3e899398ce4d3f9e68c7ce0a23d27899d208ff485cfd1b35e13df072`
- `submission-package/essay/symbolon/matheme/topology/riemann-sphere.md`: `c20fdc470303a0e2749b28c701b201a9d4f846373b7db419e2e3384350c30070`
- `submission-package/essay/symbolon/matheme/topology/projective-completion.md`: `a568aba0008093bfc796bfc47600a5dd1ed22ccb7b2b795b4dd50994315a997f`
- `submission-package/essay/symbolon/matheme/topology/mobius-klein-surfaces.md`: `94c800528c38963522c423e3a2215b42a3cd93ca73ce07785c807a7ba09fdda2`
- `submission-package/essay/symbolon/matheme/formal-neighbours/crt-z6.md`: `f67e21e17286a077a64c4ce8d69d671c5727cf26e0966db0b79088c3c0ff4929`
- `submission-package/essay/symbolon/matheme/formal-neighbours/trivial-ring.md`: `c305239e2daadce852e9d589c3cc97aeca81f28cb44d4677976f0a0a0e468e96`
- `submission-package/essay/symbolon/matheme/formal-neighbours/grothendieck-group-loss.md`: `2919163a8bc9c96b69b70343f99685ccd6a6d26b886b0fda960b7bbc1fd83c23`
- `submission-package/essay/symbolon/matheme/formal-neighbours/calculus-infinity-dx.md`: `7065c58175076854296aae758cd7a39e348bf241f0b91d0361172ed9dd614bbf`
- `submission-package/essay/symbolon/matheme/formal-neighbours/cross-ratio.md`: `1c5123237f479f5fec3ddf7dd397ed02f3176b727aa787b190f4ffb6c6309272`
- `submission-package/essay/symbolon/matheme/formal-neighbours/qubit-bloch-sphere.md`: `190f48437afc8a87b864293093a3f23bb91458ad9c60695b549c70c882073104`
- `submission-package/essay/symbolon/matheme/formal-neighbours/quaternion-q8.md`: `4d5b99654e90cdeeb13d8094a9d7c5d315b31aafed7408970d8a60912a3f3a77`
- `submission-package/essay/symbolon/matheme/formal-neighbours/chaos-attractors.md`: `a233295a47894c3c9274a72cd88e52ede7b2e46d4e7343c3ee6728d8c541e2d9`
