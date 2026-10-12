# T25 census receipt refresh — 2026-09-20

Companion to the receipt refresh on branch `receipt/t25-refresh-20260920` (PR to `main`).
The acceptance receipt `T25-current-census-acceptance.json` carried 163 stale sha256
values out of 288 records. This pass rebinds every record hash to the actual bytes of
its canonical home and hardens the builder's `--check` so staleness fails loudly.

## Provenance

- Finding of record: `working/expression-corpus/E0-COMPLETION-REPORT.md` §1 (E0, 2026-09-17):
  163/288 receipt hashes stale; the builder's `--check` did not verify base-record hashes.
- Why: the 281 baseline hashes were inherited verbatim from the September-9
  `T20-T21-current-census-acceptance.json`. Content then moved at `5c22906` (2026-09-10,
  "Land the T23 navigable surface and the T24 whole-field repair") and again in the T25
  refinement wave of 2026-09-15/16 (`R2`–`R6` commits), while the builder kept re-emitting
  the baseline hashes. The receipt as committed at `c665bd9` (2026-09-16) was therefore
  already stale at its own commit.
- E0 deliberately did NOT silently refresh this receipt, because it is the packet the owner
  is asked to ratify (T26). This refresh is that named remainer, executed mechanically:
  hashes only, plus the receipt-level refresh note in `standing`.

## What changed in the receipt

| item | change |
|---|---|
| record hashes | 163 of 288 updated to actual-bytes sha256 at HEAD `a468559` |
| `standing` | one refresh sentence added (dated 2026-09-20, states the actual-bytes rule) |
| identities, homes, registers, types | **unchanged** (0 differences) |
| `counts`, `base_receipt`, record order | **unchanged** |

Cross-check: all 288 refreshed hashes equal the actual-bytes hashes E0 computed at `dbf3b17`
(`E0-INVENTORY.json`), so no census content moved between `dbf3b17` and `a468559`. Rerunning
`working/expression-corpus/build-inventory.py` after the refresh reports **288/288 covered,
receipt-stale 0/288** (was 163/288).

## FLAG — 42 records changed semantically (not reformat)

These records' bytes differ beyond link paths, frontmatter metadata and navigation blocks.
The differences are the **T25 paradigm/product refinement passages themselves** (the 2026-09-15/16
`R2`–`R6` commits, already part of the owned T25 programme and awaiting T26 ratification). The
receipt refresh re-binds their hashes; it does not adjudicate them. Each gist below is the first
text delta (truncated).

### A — 14 record(s)

| record | first text delta (gist) |
|---|---|
| `A04` | That **co-presence gives the essay an epistemic office for psychic fact**. An experience can be received first as som… |
| `A06` | This gives the essay's new paradigm formulation its articulation-side. C41 — Objective Internality names the paradigm… |
| `A09` | This makes A09 one of the essay's deepest accounts of **paradigmatic existence before explicit paradigm**. A Life doe… |
| `A10` | ### The Indian mathematical–metaphysical hinge The relation the essay needs here is historically narrower and philoso… |
| `A13` | Three developments carried from the historical carrier `03-two-logics-and-sym-ballein.md` complete this return. Super… |
| `A22` | The T25 paradigmatic field names the general relation already operating here. A world-picture is not only a represent… |
| `A26` | **Objective Internality is the means through which a Life knows and acts within a World.** Subjective Immediacy is th… |
| `A29` | The six Objective Internality products now make the distribution of Power explicit rather than leaving “Return” as on… |
| `A31` | The paradigm development sharpens the depth of this claim. A local model can be revised while the **enacted pattern t… |
| `A32` | The paradigm development gives the three motions one further unity. Humanity does not exteriorise only isolated belie… |
| `A33` | The paradigm development now supplies A33 with its most exact technical burden. If Objective Internality is lived/ena… |
| `A34` | The middle term in the inherited arrow is **mind in its mediating office**, not Mind as the exhaustive name of realit… |
| `A35` | The paradigmatic refinement sharpens what counts as an origin. A determination does not arise only from an explicit s… |
| `A36` | A10 now gives this braid its specific Indian hinge rather than a generic metaphysics of nothing. Abhinavagupta's conv… |

### C — 25 record(s)

| record | first text delta (gist) |
|---|---|
| `C09` | Gebserian co-presence gives this concept a second office that is not reducible to perspective metadata. **A report of… |
| `C10` | Within the essay’s argued whole, **pramāṇa is Objective Internality as means**, between Subjective Immediacy as knowe… |
| `C14` | The T25 paradigmatic refinement gives this operation a new downstream consumer without renaming the Śaiva term. A **p… |
| `C19` | This distinction becomes load-bearing in the paradigm development. A Life can remember the rules, concepts and histor… |
| `C21` | The paradigm development gives this old distinction a direct contemporary office. C41 — Objective Internality names t… |
| `C22` | The restored paradigm field gives counterfeit Symbolon a precise expressive form. A representation of a paradigm can … |
| `C27` | The inherited **Antichrist field** gives this operation its darkest symbolic name: **counterfeit sourcehood**. A repr… |
| `C38` | The T25 paradigm/project relation gives this reflection a general causal office without changing its ontological stan… |
| `C39` | The §5 product field gives this principle a concrete sixfold without reducing MEF to product architecture. Each produ… |
| `C40` | Its boundary is now especially important. C41 — Objective Internality names the broader **lived/enacted paradigm** th… |
| `C41` | **Objective |
| `C42` | With C41 — Objective Internality's paradigm formulation explicit, this becomes **reciprocal paradigmatic constitution… |
| `C43` | The word **functional** does essential work. A technical system can become reflexive in a real and consequential sens… |
| `C45` | The restored paradigm language gives this criterion a new load-bearing case. If a system claims not merely to *repres… |
| `C46` | With C41 — Objective Internality's paradigm office explicit, cultivation is the **ongoing tending of an enacted parad… |
| `C47` | Within the restored paradigm language, this can reach deeper than a local model update. C41 — Objective Internality n… |
| `C50` | A concrete return makes the formal distinction usable. Suppose a commissioned inquiry produces an answer and then enc… |
| `C51` | The September 15 authorial development gives this return a further exactness: **Objective Internality is paradigmatic… |
| `C55` | The paradigm development sharpens what the third motion must disclose. The mirror does not only explain how one answe… |
| `C56` | Within the restored Power/Antichrist field, compassion is the direct contrary of **counterfeit sourcehood** without b… |
| `C59` | With the Power/Antichrist field restored, the cultural problem can be stated more exactly: a culture becomes possesse… |
| `C60` | **Life / Mind names the whole; the arrow’s middle term names mind’s mediating, objective-internal office within it.**… |
| `C61` | The newer Expression development belongs here as a **projection surface of the same disclosure architecture**, not as… |
| `C62` | The paradigm development adds a precise reason scale matters. A local technical decision can become part of the ambie… |
| `C64` | The T25 paradigmatic field specifies one important form of this operation. A paradigm normally disappears behind what… |

### A′ — 3 record(s)

| record | first text delta (gist) |
|---|---|
| `A26p` | A26’s |
| `A34p` | The relay is investigated within Life / Mind as the whole relation, not inside a claim that the inspectable relay exh… |
| `A/C` | canonical |

## Mechanical changes — 121 records (no semantic content change)

Classifications: **link-only** (wiki/markdown link targets rewritten from repo-absolute to
relative paths; visible text unchanged), **navigation-block-added** (paired-field-navigation
blocks), **frontmatter-metadata** (added `record_id` / `source_id` / `aliases` fields). No
record changed by whitespace alone.

| family | stale | mechanical | semantic |
|---|---|---|---|
| C | 63 | 38 | 25 |
| A′ | 37 | 34 | 3 |
| A | 36 | 22 | 14 |
| histories | 10 | 10 | 0 |
| Mytheme wholes | 9 | 9 | 0 |
| Matheme | 3 | 3 | 0 |
| etymologies | 3 | 3 | 0 |
| dossiers | 2 | 2 | 0 |
| **total** | **163** | **121** | **42** |

Families with zero stale hashes at HEAD: Symbolon (root-relations + spine-index), lenses,
aphorism, S-family products (S/S0–S5).

## Per-record hash table (all 163 refreshed hashes)

Old = hash carried by the receipt before refresh (traced to the last historical blob matching
it). New = actual bytes at HEAD. Class: `S` = semantic text change, `L` = link-only, `N` =
navigation block, `F` = frontmatter metadata (mechanical classes combine).

| record | family | old sha256 (16) | new sha256 (16) | class | last change |
|---|---|---|---|---|---|
| `A01` | A | `e7d88ae66c41e30c` | `43d8d1b647d6d815` | LN | 5c22906 @ 2026-09-10 |
| `A02` | A | `6b0d27da3d93277b` | `68e62bc7f25f8608` | LN | 5c22906 @ 2026-09-10 |
| `A03` | A | `566d991665331b88` | `60fb85d54eb368ef` | LNF | 5c22906 @ 2026-09-10 |
| `A04` | A | `45d2026a0122a91c` | `76087050e4723971` | SLNF | 76019cd @ 2026-09-15 |
| `A05` | A | `022a3f817ac10439` | `5691ddb99686ac21` | LNF | 5c22906 @ 2026-09-10 |
| `A06` | A | `9573209edc0511e3` | `cf8db86c40e8d36e` | SLNF | a01d165 @ 2026-09-15 |
| `A07` | A | `9bd3a94289813308` | `1ec9c1d33d06879a` | LNF | 5c22906 @ 2026-09-10 |
| `A08` | A | `147076134423dfba` | `bd93645225d6f269` | LNF | 5c22906 @ 2026-09-10 |
| `A09` | A | `dc05bdc7b3173936` | `486e4ba1e00bded2` | SLNF | 5bb4a84 @ 2026-09-15 |
| `A10` | A | `70bd61eae087ac27` | `37c5fa2c734e7602` | SLNF | 6107252 @ 2026-09-15 |
| `A11` | A | `5fad3792b2fbc673` | `a2548789600a9b52` | LNF | 5c22906 @ 2026-09-10 |
| `A12` | A | `d8108bbef31d46ae` | `f0101e1c941d9063` | LNF | 5c22906 @ 2026-09-10 |
| `A13` | A | `35a937a6ff1c5817` | `a37b98507afc71ad` | SLNF | 5c22906 @ 2026-09-10 |
| `A14` | A | `6d71cda9fd1a03cc` | `b038b43c66362e26` | LNF | 5c22906 @ 2026-09-10 |
| `A15` | A | `b749243203623008` | `d6238163af627a22` | LN | 5c22906 @ 2026-09-10 |
| `A16` | A | `a26b070d7710ef14` | `bda5b8bbb2224fc4` | LNF | 5c22906 @ 2026-09-10 |
| `A17` | A | `7e7d78c817f675f2` | `f73c25f40a7560b4` | LNF | 5c22906 @ 2026-09-10 |
| `A18` | A | `1cd68de4c18c6125` | `11517bef25bd5ea6` | LN | 5c22906 @ 2026-09-10 |
| `A19` | A | `3c6196436fd7061d` | `9f4b047c0ce63568` | LN | 5c22906 @ 2026-09-10 |
| `A20` | A | `78fc35cd345aa0d2` | `e89d75b1ceba32d3` | LN | 5c22906 @ 2026-09-10 |
| `A21` | A | `44769154f862e026` | `d74bcfac899b1147` | LN | 5c22906 @ 2026-09-10 |
| `A22` | A | `36a857ec953ad104` | `fdd96a1e8130b7f7` | SLN | 171ecfb @ 2026-09-15 |
| `A23` | A | `aeb6948cbdd93d99` | `6620befe8395b0d7` | LNF | 5c22906 @ 2026-09-10 |
| `A24` | A | `6227e28c2ef52533` | `6a59bfa5c289baf9` | LN | 5c22906 @ 2026-09-10 |
| `A25` | A | `23bc59d5134fb5fe` | `a4e4b3c36bf6e47b` | LN | 5c22906 @ 2026-09-10 |
| `A26` | A | `e38289d5d513c846` | `d80829bbe46b9fe7` | SLNF | 1c0ab71 @ 2026-09-10 |
| `A27` | A | `772c8375bd87d115` | `b5dccd6f1a17d0df` | LN | 5c22906 @ 2026-09-10 |
| `A28` | A | `0741739318f6956f` | `60673f654d632e79` | LN | 5c22906 @ 2026-09-10 |
| `A29` | A | `53ca7dc586138670` | `63edfcffb9f59194` | SLN | 7fa792c @ 2026-09-15 |
| `A30` | A | `298f480eecc27752` | `32c25fa2d680ffd3` | LN | 5c22906 @ 2026-09-10 |
| `A31` | A | `6bfb6dc3b7ec2389` | `0351744b02faa702` | SLNF | 8a70bd1 @ 2026-09-15 |
| `A32` | A | `304a536ec000b2c9` | `680ccb7c690f2587` | SLNF | 72c226c @ 2026-09-15 |
| `A33` | A | `3dd86a0d84b54b78` | `21cdf6c161ee578a` | SLN | c4279b8 @ 2026-09-15 |
| `A34` | A | `02d9ed7be5b06588` | `a67481ea059d2894` | SLN | 7783d28 @ 2026-09-15 |
| `A35` | A | `145922ab29e6cf76` | `aefa44225c53c11c` | SLN | 686c31e @ 2026-09-15 |
| `A36` | A | `6323457b71a8e304` | `b0965598db54d9a5` | SLN | 6e9fd62 @ 2026-09-16 |
| `A/C` | A′ | `3243978521525ca1` | `1afdc69d30554add` | SLN | 6e9fd62 @ 2026-09-16 |
| `A01p` | A′ | `4a2f07e07c642bbe` | `992dc01598a1964d` | LN | 5c22906 @ 2026-09-10 |
| `A02p` | A′ | `a451b1140a7b613f` | `84e23f8bc8a15fe7` | LN | 5c22906 @ 2026-09-10 |
| `A03p` | A′ | `8b6ccc94fc3643f7` | `e0d82794ca90130a` | LN | 5c22906 @ 2026-09-10 |
| `A04p` | A′ | `2671c65596452bea` | `b111f01a7d6caa42` | LN | 5c22906 @ 2026-09-10 |
| `A05p` | A′ | `a77aa12fc179cd72` | `ae2cc706083815f6` | LN | 5c22906 @ 2026-09-10 |
| `A06p` | A′ | `8c908079a96bd2d2` | `f78bc8f0495af078` | LN | 5c22906 @ 2026-09-10 |
| `A07p` | A′ | `32db575e1b670cbb` | `35eb1b947b87cfd3` | LN | 5c22906 @ 2026-09-10 |
| `A08p` | A′ | `94bc534450673995` | `71c46295287d6715` | LN | 5c22906 @ 2026-09-10 |
| `A09p` | A′ | `2ebe65fbf9df106a` | `cebb93abb91ef13e` | LN | 5c22906 @ 2026-09-10 |
| `A10p` | A′ | `4c8501a886adcf09` | `85429ac59e54a254` | LN | 5c22906 @ 2026-09-10 |
| `A11p` | A′ | `a230084d817c48c8` | `ab3b0a4cd48f0529` | LN | 5c22906 @ 2026-09-10 |
| `A12p` | A′ | `715731bc5928296f` | `a13410c104bcdfb3` | LN | 5c22906 @ 2026-09-10 |
| `A13p` | A′ | `db4c3a40b679308b` | `b948faf81058552d` | LN | 5c22906 @ 2026-09-10 |
| `A14p` | A′ | `04570283edf025bf` | `3740ab471d003f2e` | LN | 5c22906 @ 2026-09-10 |
| `A15p` | A′ | `0403c2cd2e466042` | `bae8059ce012838c` | LN | 5c22906 @ 2026-09-10 |
| `A16p` | A′ | `0af944d467567f52` | `20364446b5439c1d` | LN | 5c22906 @ 2026-09-10 |
| `A17p` | A′ | `c223093419776da9` | `d06820718286fd2d` | LN | 5c22906 @ 2026-09-10 |
| `A18p` | A′ | `2d58c991c956a831` | `f5ce255ec09def08` | LN | 5c22906 @ 2026-09-10 |
| `A19p` | A′ | `8e50618f29e32a37` | `edacbac34b1e9c53` | LN | 5c22906 @ 2026-09-10 |
| `A20p` | A′ | `ac4181ac0f25b083` | `6f1a4d63b264e43b` | LN | 5c22906 @ 2026-09-10 |
| `A21p` | A′ | `58153d6e30b4c0ca` | `e2949efc3ac886de` | LN | 5c22906 @ 2026-09-10 |
| `A22p` | A′ | `d89b642a7782f395` | `b76e1be4e04f19c2` | LN | 5c22906 @ 2026-09-10 |
| `A23p` | A′ | `38ef5e26bdb92db6` | `a8ae824c35119beb` | LN | 5c22906 @ 2026-09-10 |
| `A24p` | A′ | `79646e36ee986dcb` | `3b1c271af28be750` | LN | 5c22906 @ 2026-09-10 |
| `A25p` | A′ | `2c5f726471d41780` | `021161459f703369` | LN | 5c22906 @ 2026-09-10 |
| `A26p` | A′ | `103b32a4d28d6e1e` | `a7504f5670b6ded2` | SLN | 1c0ab71 @ 2026-09-10 |
| `A27p` | A′ | `5ec35764bc7af361` | `d6748f14e9ca58e1` | LN | 5c22906 @ 2026-09-10 |
| `A28p` | A′ | `3082e0b3fe7d2e4b` | `037188197f8f79d8` | LN | 5c22906 @ 2026-09-10 |
| `A29p` | A′ | `b9ef746f28c455e0` | `9ec52f0785d052bf` | LN | 5c22906 @ 2026-09-10 |
| `A30p` | A′ | `18f1a0e6daaf45f7` | `7fcd9185a20e7c9e` | LN | 5c22906 @ 2026-09-10 |
| `A31p` | A′ | `7f0cf0b55916b316` | `244b65af407298fa` | LN | 5c22906 @ 2026-09-10 |
| `A32p` | A′ | `37aca079448e6857` | `765e4fc0ed2af8ff` | LN | 5c22906 @ 2026-09-10 |
| `A33p` | A′ | `4f24252a6ba70732` | `f08662fd1b1ed2d6` | LN | 5c22906 @ 2026-09-10 |
| `A34p` | A′ | `5069076d03d91c20` | `778adcfa7f6e1be1` | SLN | 1c0ab71 @ 2026-09-10 |
| `A35p` | A′ | `c5f859c431c51a97` | `dde4a32441ae9195` | LN | 5c22906 @ 2026-09-10 |
| `A36p` | A′ | `8b5657361edda21a` | `75f924334a4b3291` | LN | 5c22906 @ 2026-09-10 |
| `C01` | C | `c3e78c2c1dec7881` | `698985115706165b` | L | 5c22906 @ 2026-09-10 |
| `C03` | C | `290a6c8febac1464` | `36eceb4d3ee026c5` | L | 5c22906 @ 2026-09-10 |
| `C04` | C | `5bb78309872e2812` | `eaa4532ad65a282e` | L | 5c22906 @ 2026-09-10 |
| `C05` | C | `cdba439fcbda5b43` | `da7304560864e10f` | L | 5c22906 @ 2026-09-10 |
| `C06` | C | `4986ca50ff5f68c5` | `21ff4eaad14203a3` | L | 5c22906 @ 2026-09-10 |
| `C07` | C | `9880e6f1b33d062a` | `868b90b98b5144a6` | L | 5c22906 @ 2026-09-10 |
| `C08` | C | `d6e4d6512378b517` | `e38a3de8294d9022` | L | 5c22906 @ 2026-09-10 |
| `C09` | C | `46f9a2a2ad7d501f` | `fbeb94a77d12e5da` | SL | 7348397 @ 2026-09-15 |
| `C10` | C | `f0bd77cbab0be92e` | `d104361f1dfa4a71` | SL | 1c0ab71 @ 2026-09-10 |
| `C11` | C | `ac854490c281b920` | `ea1b5f51e19dfff7` | L | 5c22906 @ 2026-09-10 |
| `C12` | C | `c607111810107cb7` | `dd5942bfd5a36ef4` | L | 5c22906 @ 2026-09-10 |
| `C13` | C | `b2629b9f55a27484` | `8fb9e3702f00c9d5` | L | 5c22906 @ 2026-09-10 |
| `C14` | C | `a4f55336cd57cc5e` | `c8d14531064efe54` | SL | 0bab2fa @ 2026-09-15 |
| `C15` | C | `c027f399447f6631` | `272d029dc64c5be2` | L | 5c22906 @ 2026-09-10 |
| `C16` | C | `5a00a4107bb31a2b` | `e74e839f75f6e899` | L | 5c22906 @ 2026-09-10 |
| `C17` | C | `bb9278b7143dcd3a` | `1d5cd1141f63bd60` | L | 5c22906 @ 2026-09-10 |
| `C18` | C | `53cd708255759d3b` | `d271c967a9ba8a8f` | L | 5c22906 @ 2026-09-10 |
| `C19` | C | `581013c2c228b0c9` | `6c7f7cfc0816a3e5` | SL | 4cdfb48 @ 2026-09-15 |
| `C20` | C | `dc0e09a046970c8e` | `5c41cdbc400ce14e` | L | 5c22906 @ 2026-09-10 |
| `C21` | C | `eebc80e938dfd531` | `81e501b743597f1c` | SL | 650f6ca @ 2026-09-15 |
| `C22` | C | `ae7833804db2f889` | `9040bb6664f13d26` | SL | 14b27e6 @ 2026-09-15 |
| `C23` | C | `a15d4607f4e25b67` | `5fd5e3612dd11f78` | L | 5c22906 @ 2026-09-10 |
| `C24` | C | `02eecc76161d9310` | `7d6dc77209cea8b8` | L | 5c22906 @ 2026-09-10 |
| `C25` | C | `337ee1468492561f` | `b74ba84bce8c92b5` | F | 5c22906 @ 2026-09-10 |
| `C26` | C | `77fced4a60e8114f` | `2ae8e0eeea7a5568` | LF | 5c22906 @ 2026-09-10 |
| `C27` | C | `1424096d1a7b2824` | `54b3b17acfe4670d` | SLF | 3c4373f @ 2026-09-15 |
| `C28` | C | `615ae7cf198d4acc` | `e26ccf9bfef85013` | F | 5c22906 @ 2026-09-10 |
| `C29` | C | `50585afbbfd190bc` | `04b51b2f5e5e48fc` | L | 5c22906 @ 2026-09-10 |
| `C30` | C | `b503e87d30738c51` | `9ed2196a76a86f2e` | L | 5c22906 @ 2026-09-10 |
| `C31` | C | `95452ed6b422c56a` | `0a09377d3c777223` | L | 5c22906 @ 2026-09-10 |
| `C32` | C | `969a7e00c77f3f86` | `6a6577093e0ca6d9` | L | 5c22906 @ 2026-09-10 |
| `C33` | C | `3fc264fe5b769f39` | `79045eee79ca0393` | F | 5c22906 @ 2026-09-10 |
| `C34` | C | `d3004de47ed24308` | `e25fb07609b01c2f` | F | 5c22906 @ 2026-09-10 |
| `C35` | C | `de2e0bac6f3f9391` | `1aaca77dd229a37d` | F | 5c22906 @ 2026-09-10 |
| `C36` | C | `31846b67222d662a` | `e6f77d7c475ee6eb` | F | 5c22906 @ 2026-09-10 |
| `C37` | C | `6839156b4da6b994` | `e1d621337b3ef00d` | LF | 5c22906 @ 2026-09-10 |
| `C38` | C | `23fade4d1bf16368` | `e193a9ef386cae04` | SLF | 11f3234 @ 2026-09-15 |
| `C39` | C | `6697333019ad8d25` | `34ed246c80a0bac4` | SLF | af56a34 @ 2026-09-15 |
| `C40` | C | `b01dc2cd66b85913` | `f19e23e2ae500c8b` | SLF | 07f3106 @ 2026-09-15 |
| `C41` | C | `2d95f27df8ec539c` | `f412ee36087f330c` | SF | fdae96f @ 2026-09-15 |
| `C42` | C | `2bf66f359de7a753` | `a7ee7e7b08ada797` | SF | 7e43b23 @ 2026-09-15 |
| `C43` | C | `716dacb5d29f2a70` | `d51cc85748ff9202` | SF | 454f89d @ 2026-09-15 |
| `C44` | C | `18d902f7f65c7bdc` | `1cf57fa6b50dd40a` | F | 5c22906 @ 2026-09-10 |
| `C45` | C | `0b55f4f45b8085ca` | `88416ddde055a71b` | SF | c7a2449 @ 2026-09-15 |
| `C46` | C | `18045feda000d4d6` | `4ab32d4e46105416` | SF | 647d1c0 @ 2026-09-15 |
| `C47` | C | `b6730156fbeee37f` | `2adb00fe3e8ecb0f` | SF | 368a332 @ 2026-09-15 |
| `C48` | C | `1a06d2bc720327e3` | `7ff506d88764a113` | LF | 5c22906 @ 2026-09-10 |
| `C49` | C | `2dfbabc31db288b9` | `56c421fd766b92a5` | LF | 5c22906 @ 2026-09-10 |
| `C50` | C | `fe5539234a8fc5b5` | `eda8cdd7480bec82` | SF | 6c8eaac @ 2026-09-15 |
| `C51` | C | `b87abb64a5a17faa` | `f511f57fbd68cdf2` | SLF | 50147ac @ 2026-09-16 |
| `C52` | C | `06a23819c23d8bd0` | `6139fe6cd42eb227` | LF | 5c22906 @ 2026-09-10 |
| `C53` | C | `e80b07553252d62c` | `d7d74fd4e9606b13` | L | 5c22906 @ 2026-09-10 |
| `C54` | C | `9b7c8a4376f061e9` | `2e6eff41f71f3bd1` | L | 5c22906 @ 2026-09-10 |
| `C55` | C | `962b4e484a04c5ef` | `fe518dad05da0357` | SL | 85e5991 @ 2026-09-15 |
| `C56` | C | `43368a44737e2a6f` | `6ebf2329c955d310` | SLF | 5540599 @ 2026-09-15 |
| `C57` | C | `fd5babf55c64c8bc` | `e1ca274b8cdb027d` | L | 5c22906 @ 2026-09-10 |
| `C58` | C | `f6f999394d9c7409` | `a7e9b00dc47d0945` | L | 5c22906 @ 2026-09-10 |
| `C59` | C | `aa44a1711960c1ed` | `3d5d4df234dd3195` | SLF | c5574eb @ 2026-09-15 |
| `C60` | C | `5017929ff790ce77` | `6715c5f0e4854e39` | SL | d993bb5 @ 2026-09-15 |
| `C61` | C | `462ecda8f013761a` | `9c9f4d1aeedd476c` | SLF | a0b789d @ 2026-09-15 |
| `C62` | C | `1ff2b8557d13ab6e` | `32ec0e0f26a83578` | SLF | da44f47 @ 2026-09-15 |
| `C63` | C | `d989bdc87840a52d` | `8379dcf18e8139d8` | L | 5c22906 @ 2026-09-10 |
| `C64` | C | `587c01a9e72d9003` | `b7af2e489d849215` | SLF | 8aa15cc @ 2026-09-15 |
| `matheme-fde-catuskoti` | Matheme | `820974af1b819b72` | `7f9de27a51ae2b00` | L | 5c22906 @ 2026-09-10 |
| `matheme-kauffman-iterants` | Matheme | `af712057ee478e3c` | `a5b6d9bfdc902a79` | L | 5c22906 @ 2026-09-10 |
| `matheme-noether-symmetry-conservation` | Matheme | `3cd9a2847f1efee0` | `b04b6fb015cd1795` | L | 5c22906 @ 2026-09-10 |
| `mytheme-apollo-eros-daphne-peneus` | Mytheme wholes | `f4837d9f88f1d663` | `5a24300768dbf448` | L | 5c22906 @ 2026-09-10 |
| `mytheme-goethe-permanence-change` | Mytheme wholes | `532c4b27a5b051c4` | `b4be3bd1b5910997` | L | 5c22906 @ 2026-09-10 |
| `mytheme-indra-net` | Mytheme wholes | `a8b35f4e88bfc1a0` | `1cfa960f75399bbb` | L | 5c22906 @ 2026-09-10 |
| `mytheme-job` | Mytheme wholes | `0db8bced14174a2a` | `412ba0131524794d` | L | 5c22906 @ 2026-09-10 |
| `mytheme-maya-eye-veil-frame-horizon` | Mytheme wholes | `f50f92ae34794ebd` | `93c8697717063816` | L | 5c22906 @ 2026-09-10 |
| `mytheme-mirror-that-moves-first` | Mytheme wholes | `03bf3fb7b74e2ee2` | `89a4f3873b83b941` | L | 5c22906 @ 2026-09-10 |
| `mytheme-myth-attica-athena-poseidon-cecrops` | Mytheme wholes | `68aa4168cf423d97` | `0ce5ecbdc362909d` | L | 5c22906 @ 2026-09-10 |
| `mytheme-the-prisoner` | Mytheme wholes | `1d3b11444a4a79bb` | `27af157e16012248` | L | 5c22906 @ 2026-09-10 |
| `mytheme-travelling-jigsaw-atlas` | Mytheme wholes | `c141e5f85381fa84` | `c5190aaa4de6c71c` | L | 5c22906 @ 2026-09-10 |
| `dossier-bohm` | dossiers | `71170770d756b5f7` | `3094efc89557a121` | F | 5c22906 @ 2026-09-10 |
| `dossier-oi-technical-responsibility` | dossiers | `5924569cead2b4d3` | `355d3208a6131c0f` | L | 5c22906 @ 2026-09-10 |
| `etymology-homology-and-analogy` | etymologies | `3ca34b8ab15d6502` | `cfb9d9e20f69a1a1` | L | 5c22906 @ 2026-09-10 |
| `etymology-symbol-account-and-trust` | etymologies | `e0291913d331cea9` | `385454d303dc3358` | LF | 5c22906 @ 2026-09-10 |
| `etymology-trust-place-logos-nomos-natio-credere` | etymologies | `575c84bd751d3f4e` | `00a5ff94e6612747` | L | 5c22906 @ 2026-09-10 |
| `history-ancient-philosophy` | histories | `d4ada784572c85c9` | `3b3cc972c6224044` | F | 5c22906 @ 2026-09-10 |
| `history-indian-philosophy` | histories | `cddc8cfd0de71514` | `fcb1f4bdc8077622` | F | 5c22906 @ 2026-09-10 |
| `history-language-law-nation-centralisation` | histories | `fce96725ed4bb5c8` | `51267ef14beb2722` | LF | 5c22906 @ 2026-09-10 |
| `history-language-symbol-dialogue` | histories | `e754f5f8b8dee193` | `98b8aeff68ae5e87` | F | 5c22906 @ 2026-09-10 |
| `history-mathematics` | histories | `c36c40889031d7a9` | `50559b5edcd74354` | F | 5c22906 @ 2026-09-10 |
| `history-myth` | histories | `9a741a09d2467c98` | `6ca618e99afb2176` | F | 5c22906 @ 2026-09-10 |
| `history-process-systems-science` | histories | `0d8e8f7517b5b52f` | `f50195a96dcd5dc5` | F | 5c22906 @ 2026-09-10 |
| `history-psychology` | histories | `e21e9814a2767f24` | `d374decba65b1e49` | F | 5c22906 @ 2026-09-10 |
| `history-technology-politics` | histories | `75aa957131cdcc39` | `f20427fde27147f7` | F | 5c22906 @ 2026-09-10 |
| `history-zero-subject-advent` | histories | `3823064d0fb3650d` | `c22c5dd6553f238a` | F | 5c22906 @ 2026-09-10 |

## Method and limits

Each old hash was located in reachable history by hashing every distinct blob of its
canonical home (`git rev-list --all -- <path>`), so every one of the 163 old contents was
recovered exactly; none were missing. Classification normalizes both link forms to their
visible text (so `[[path|alias]]` → `[alias](relpath)` conversions cancel), strips
paired-field-navigation blocks, treats frontmatter regions as metadata, and word-diffs the
residue; every residual delta of every flagged record was then read by hand before counting
it semantic. Limits: the `A26′` changes are tense/voice edits ("is" → "was") plus the nav
block — editorial, but they do change what the text asserts, so they are counted semantic.
`etymology-symbol-account-and-trust` gained a frontmatter block (`source_id`) only; it is
counted mechanical.

## Verification transcript

```text
$ python3 tools/build-t25-refinement-admission.py --check   # refreshed receipt
{"admitted": 288, "counts": {"episteme": 170, "matheme": 80, "mytheme": 25, "symbolon": 13}}
exit=0
$ python3 tools/build-t25-refinement-admission.py --check   # original stale receipt
stale hash: A01 (submission-package/essay/symbolon/episteme/arguments/A01-Subject-God-and-Faithful-Definition.md) receipt=e7d88ae66c41e30c… actual=43d8d1b647d6d815…
… 163 `stale hash:` lines, one per stale record
exit=1
$ python3 working/expression-corpus/build-inventory.py
covered 288/288 records; 57/57 surfaces; 52 artifacts, 473 scenes; receipt-stale 0/288
```

The committed `E0-INVENTORY.json` / `E0-COVERAGE.md` still describe the old receipt (163
stale); they are corpus artifacts outside this task's scope — rerunning the inventory tool
regenerates them against the refreshed receipt at any time.

**This refresh does not ratify anything. T26 ratification of the refreshed packet remains
the owner's judgement.**
