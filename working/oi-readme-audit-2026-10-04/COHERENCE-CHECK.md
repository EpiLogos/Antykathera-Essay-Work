# Coherence check: public site against the proposed READMEs

5 October 2026. This compares the rewritten public site (`O-I/site/content/public-site.md`, working-tree copy with the new `[home]` and `[role]` lines) with the seven proposed READMEs in this folder. Nothing in any repository or on the site was edited, committed or pushed.

Every claim was checked against code, `--help` of the installed binaries and tests, not against the current READMEs:

| Product | Checkout | Installed binary |
|---|---|---|
| O:I | `5c74f161`, plus `origin/main` `9455d892` for the architecture docs | `oi` `31cf5a5c` |
| Central | `341569f` | `ctrl` `1a94aeef` |
| Actuation | `origin/main` `7a685ad`, plus GitHub `2139d78` for docs | `actuation` 0.2.1 `69bdc351` |
| AIKit | `origin/main` `12ccb272` | `aikit` `e8ba9689` |
| Factory | `24ea894` | `factory` `ef2817ce` |
| Workcell | `c7261e2` | `workcell` `174fa1c3`, which is on open PR #109 |
| QL-MEF | `origin/main` `f9089b1` | `ql` `6a81fc44` |

## 1. Site sentence against README opening

**Facet names.** The site's six `[role]` lines are Ground, Agency, Capability, Development, Environment and Reflection. Each README names exactly that facet in its opening paragraph, and the O:I README's facet table uses the same role descriptions as `[what]`. No facet-name mismatches.

### O:I

- **Site (`[what]` + `[centres]` intro).** "O:I stands for Objective : Internality: the means through which a life knows and acts within a world…" It names the six facets. "O:I differentiates them. Each facet gets its own tool, its own records and its own contracts…" "Each facet is built as its own product: a command-line tool and libraries in their own repository, usable alone or together, meeting the others through versioned contracts rather than a shared runtime. All six are in use and still developing."
- **README opening.** "O:I is a suite of six command-line products, plus a front-door tool, `oi`, that installs and joins them. Together they give an AI agent's world six explicit parts: ground, agency, capability, development, environment and reflection. Each part gets its own tool, its own records and its own contracts…" The second paragraph quotes the site's Objective : Internality definition.
- **Facet.** Six facets, same names.
- **Claim.** Matches. The README adds what the site leaves implicit: `oi` is a seventh executable but not a seventh facet.
- **Status.** The site says "in use and still developing". The README says pre-release `0.1.0-prelocal.6`, and that physical acceptance has not been run. Consistent; the README is more specific.

### Central

- **Site.** "Central holds the ground: a person's authored material and projects, kept as ordinary files and read or changed through named actions."
- **README opening.** "Central is a Rust command-line tool, `ctrl`, together with a plain-file layout for a personal root folder… `ctrl` gives people and agents one set of named, typed Actions for reading and changing that material. Central holds O:I's ground facet…"
- **Facet.** Ground. Same.
- **Claim.** Match, with one nuance. "Read or changed through named actions" can be read as *only* through Actions. In the code and the spec, people edit the files directly, and Actions are the shared doorway for software. Agent sessions cannot write human-authored source; they propose. The README says this. See site correction S1.
- **Status.** The site gives none. The README: 188 Actions, NOW/DAY on `main`, pre-release, no physical acceptance.

### Actuation

- **Site.** "Actuation holds agency: which agent acts, on whose authority and within what bounds, with a record of what each act did."
- **README opening.** "…It records which agent holds which position, on whose authority and within what bounds, and the events and results reported for each act. It keeps those records in append-only files…"
- **Facet.** Agency. Same.
- **Claim.** **Mismatch.** "A record of what each act did" overstates the code. Actuation's stream records what callers and adapters *report*; its own help says the stream "records evidence rather than performing the corresponding real action". Admission receipts say `materialisation: not-performed`. Identities are references supplied by the caller. See site correction S2.
- **Status.** The README states that the released 0.2.1 archive lacks the occupancy, Nara and intake commands that are on `main`.

### AIKit

- **Site.** "AIKit holds capability: it works out which skills, tools, models and sources apply in a project and installs them into the harness already in use."
- **README opening.** "…For each project, agent and task, it works out which skills, tools, models and knowledge sources apply. It then makes exactly that set available to the agent harness you already use, writing into the harness's own settings where it has a declared, reversible way to do so…"
- **Facet.** Capability. Same.
- **Claim.** **Mismatch on "installs".**
  - AIKit writes into Claude Code (hooks and MCP; skills reach it through a launch flag from AIKit's own generation directory), Codex (isolated tasks only), zcode, pi and openclaw.
  - Every other detected harness is brokered: AIKit writes nothing into it.
  - Models are selected and admitted through Actuation, not installed.
  - Sources are disclosed and retrieved, not installed.
  - See site correction S3.
- **Status.** The README states the alpha status and that harness-profile registration is absent.

### Software Factory

- **Site.** "Software Factory holds development: the request and its reasons, the runs and attempts, the evidence and the judgement."
- **README opening.** "…It keeps a file-based record of agent-driven software work: what was asked for and why, the runs and attempts made against it, what each produced, the evidence gathered, and where a person's judgement was asked for and recorded…"
- **Facet.** Development. Same.
- **Claim.** **Mismatch on "the judgement".** Factory never performs Recognition. It records the human request and a correlation to a judgement made in Central, and its help says repeatedly that receipts and receiving "are not human Recognition". See site correction S4.
- **Status.** **The site's `[factory]` section overstates.** It says Factory "carries a Project … through design, Runs, implementation and tests into evidenced Candidates that can be encountered, recognised, redirected and returned".
  - No production command writes Candidate, Claim or Evidence records; only tests do.
  - Factory's own capability matrix marks `whole_development_run: unfinished`.
  - In Factory's dogfood state every Run is `seeded`, with 0 Candidates, 0 Returns and 0 Recognitions.
  - The README states this. See S5.

### Workcell

- **Site.** "Workcell holds the environment: it turns a request for a workspace, service or machine into a real one and records what was provided."
- **README opening.** "…It turns a request for a place to work, such as a workspace at a given revision, a shell or a set of services, into a real workspace, process or service, on this machine or on a connected one. It records what was actually provided, where, and what became of it…"
- **Facet.** Environment. Same.
- **Claim.** **Mismatch on "machine".** Workcell does not create machines. `workcell machine add` declares an existing machine that already runs Workcell, and `connect` reaches it. Machine creation exists only as a bash bootstrap script for exe.dev. See S6.
- **Status.** **The site's `[workcell]` section overstates.** It lists "containers, MicroVMs or VMs, remote hosts, storage, databases, network relationships, credentials and browser-accessible applications", and its capability line reads "container / MicroVM / VM / host".
  - In the shipped binary there is host-process execution, directory and git-worktree workspaces, declared services and OpenSandbox sandboxes.
  - Docker and Arrakis (MicroVM) exist only as libraries not linked into `workcell`.
  - There is no VM provider, no database provider, and no fabric provider in the binary.
  - See S7.

### Quaternal Logic / MEF

- **Site.** "Quaternal Logic and the Meta-Epistemic Framework hold reflection: the formal structures, as typed operations, through which the other five can be read."
- **README opening.** "Quaternal Logic / MEF is a Rust workspace and command-line tool, `ql`, that implements the formal structures of Quaternal Logic as typed, versioned operations. It holds O:I's reflection facet: a formal way of reading the rest of an agent's world."
- **Facet.** Reflection. Same.
- **Claim.** **Partial mismatch.** "Through which the other five can be read" is a contract shape plus specific seams, not a working general reader.
  - There are readings of Factory records, AIKit syntax, Central documents and NOW refs, and a generic Context-Frame reading of any six-part mapping.
  - All of them consume JSON that a host supplies. No code fetches another product's records.
  - There is no Workcell reader.
  - `relate` and `synthesise` have no provider.
  - The CLI cannot run `locate` or `refract` on a subject.
  - The README says this. See S8.
- **Naming.** The site heading is "Quaternal Logic", the `[centres]` text says "Quaternal Logic and the Meta-Epistemic Framework", and the repository is `QL-MEF`. The README title "Quaternal Logic / MEF" sits between them. This is not a contradiction.

### The Cradle (O:I README only)

- **Site (`[cradle]`).** "…It is the O:I desktop application, and it bootstraps the agent's world as such… held together as one working situation that any harness can then act within… The Cradle is being built now."
- **README.** Same framing: "comes before the harness", "a meta-harness, not a dashboard", "being built now". It adds the technical shape and the one Linux pre-release bundle.
- **Facet.** —
- **Claim.** Match. The site's "lets the right workspace or machine be provided underneath" is design intent. It inherits the Workcell limit above: machines are connected, not provided.
- **Status.** "Being built" on both.

"Harness before the harness" appears in none of the seven proposals. "Before the harness" and "pre-harness" are used only of the Cradle.

## 2. Proposed site corrections

These apply where the site states something the code does not support. Each is the smallest change that makes the sentence true.

| # | Site location | Current | Proposed |
|---|---|---|---|
| S1 | `[centres]`, Central sentence | "…kept as ordinary files and read or changed through named actions." | "…kept as ordinary files that a person edits directly and that software reads or changes through named actions." |
| S2 | `[centres]`, Actuation sentence | "…with a record of what each act did." | "…with an append-only record of what each act reported and what came back." |
| S3 | `[centres]`, AIKit sentence | "…and installs them into the harness already in use." | "…and makes them available to the harness already in use, writing into its settings where it can do so reversibly." |
| S4 | `[centres]`, Factory sentence | "…the evidence and the judgement." | "…the evidence, and where a person's judgement is asked for and recorded." |
| S5 | `[products]` `[factory]` `[what]`, second paragraph | "…carries a Project from authored intention … into evidenced Candidates that can be encountered, recognised, redirected and returned into future development." | "…is built to carry a Project from authored intention through Commissions, Runs and attempts to evidence that a person can judge. Commissions, Runs, attempts and Returns for review work today; candidate versions and an end-to-end development Run are in development." |
| S6 | `[centres]`, Workcell sentence | "…turns a request for a workspace, service or machine into a real one…" | "…turns a request for a workspace, process or service, here or on a connected machine, into a real one…" |
| S7 | `[products]` `[workcell]` `[what]` and `[capabilities]` | lists containers, MicroVMs, VMs, databases and browser applications as what Workcell resolves | Mark the reach honestly: "…host processes, workspaces, declared services and sandboxes today, with container, MicroVM and remote-host providers in development…". In `[capabilities]`, replace "container / MicroVM / VM / host" with "host process / sandbox (container and MicroVM providers in development)". |
| S8 | `[centres]`, QL sentence | "…through which the other five can be read." | "…the formal structures, as typed operations, through which records from the other products can be read." Optionally add "as that reading is developed". |
| S9 | `[products]` `[actuation]` `[capabilities]` (optional) | omits what is live | Add "World Position occupancy · harness detection · Agency Gateway". These are the parts the other products use today. |
| S10 | `[products]` `[central]` `[capabilities]` (optional) | "replaceable connectors" | Accurate as architecture. Note for copy: the stock `ctrl` mounts only the reference and harness connectors. macOS, git-sync and Shortcuts are in the unreleased `ctrl-macos`; Homebrew and chezmoi are in no shipped binary. |

`[what]`, `[cradle]`, the `[centres]` introduction and all six `[role]` lines need no change.

## 3. AUDIT.md factual errors, and where each is fixed

| Error (AUDIT.md) | Fix |
|---|---|
| Central's stale "Open extension PRs — including … NOW/DAY, governance and physical-machine lines" | Removed from `PROPOSED-Central-README.md`. The README now says NOW/DAY, machine and recovery are on `main`, names the one open PR (#245, personal-history intake), and keeps physical acceptance as the real gap. The general "open PRs are development state" sentence is kept without the stale list. |
| AIKit "Rust 1.88 or newer" | `PROPOSED-AIKit-README.md` says Rust 1.98, pinned in `rust-toolchain.toml` (`rust-version = "1.98"`). The stale Node.js requirement is dropped: lock hashing is native. |
| AIKit "no public validate/register verb" for harness profiles | Corrected: `aikit harness-profile validate <FILE>` exists (admit/refuse). Registration is still absent. |
| AIKit "Context projections for Claude and Codex" | Corrected to the real per-harness behaviour from `aikit client status`. The misplaced post-License paragraph is moved into Documentation. |
| Workcell dead links `docs/MATERIALISATION-SPEC.md`, `docs/LIFECYCLE-AND-CANDIDATES.md` | Replaced with `docs/LIFECYCLE-RECONCILIATION.md` and `docs/CANDIDATE-MATERIALISATION.md`. Added `CROSS-CELL-CONNECTIONS.md`, `PROVIDER-SDK.md`, `PLACE-CENSUS.md` and `ARCHITECTURE-NAVIGATION.md`. exe.dev is now described as a remote bootstrap script, not a provider. |
| O:I Factory URL `agent-system-design` | `https://github.com/EpiLogos/Factory` in both the README table and `PROPOSED-O-I-PRIMITIVES.md`. |
| O:I stray footer "D" | Gone. The "Current state (temporal)" section is replaced by "Status". |
| O:I `docs/INSTALL.md` path `$HOME/Central/Work/Software-Factory` | Not a README, so it is not in this folder. Proposed one-line patch: replace `$HOME/Central/Work/Software-Factory   # historical agent-system-design remote remains accepted` with `$HOME/Central/Work/Factory            # Work/Software-Factory and Work/agent-system-design are still recognised`. This matches `dev_source_path()` in `cli/src/suite_v2.rs`. Note that `oi dev adopt` (same file, around line 2089) still targets `Work/Software-Factory`, so that path is inconsistent in code too. |
| Actuation stray `<!-- branch-protection proof … -->` | Removed. The repository map's nonexistent `actuation-migration-gate` crate is also corrected, and the "zero claimed live Series 1 capability runs" caveat is updated: live runs are recorded, but no capability effect is claimed. |
| `oi prove` mismatch | Re-checked. The help text has listed `oi prove factory …` since at least `prelocal.6`, and the installed `oi` (`31cf5a5c`) dispatches it. The real defect is the error messages: `oi prove` alone says "unknown command 'prove'", and `oi prove factory --help` says "unknown Factory proving option". The O:I README documents the full required argument form and says that `oi prove` alone is refused. A code fix to name the `factory` subject in that error is worth a small issue. |

**Release-relevant constraint kept.** `crates/actuation-cli/tests/readme_law.rs` requires every one of the 38 command usage strings to appear verbatim in Actuation's README. All 38 appear verbatim in the proposal, checked against `dispatch.rs`. Central's `ctrl/tests/public_docs.rs` requires the string `docs/README.md`; it is present.

## 4. Defects found in passing (not README text)

These turned up while grounding the READMEs. They are code or documentation faults in the products, recorded here so they are not lost. None was changed.

1. **Actuation's revision field.** `actuation capabilities --json` reports `revision` from `git rev-parse HEAD` in the caller's working directory. That is the wrong repository, or "unknown".
2. **`actuation harness self`.** It cannot identify Claude Code or most harnesses: only two catalogue descriptors declare an environment probe.
3. **Actuation release version.** The release `actuation-v0.2.1` was built from `36bbf93`, which lacks 9 of the 38 commands. `main` still reports version 0.2.1.
4. **Actuation docs.** Several docs still cite the retired `fixtures/migration/oracle.json`.
5. **`ctrl control search`.** It fails on the real `~/Central` with "Native source exceeds the 4 MiB eager read capacity". One oversized file breaks the whole search.
6. **`ctrl actions` availability.** It reports `work.open`, `work.reveal` and `central.git.census` as available in the stock `ctrl`, where no connector implements them.
7. **Central docs drift.**
   - `docs/CLI-REFERENCE.md` documents only 79 of 188 Actions.
   - `docs/INSTALL.md`'s init-shape block is stale.
   - `CENTRAL-SYSTEM-SPEC.md` §1 still says the personal root is a Git repository.
   - `PROJECTCENTRAL-NOW.md` mentions the retired `projectcentral.flow.*`.
8. **Workcell help.** `workcell --help` advertises `secret project … --to-workcell`, but the code refuses every Workcell target.
9. **Workcell reference.** The CLI defaults to `workcell:local`, while Central binds this machine to `workcell:mac`. `oi world` already warns about this.
10. **QL repository name.** The canonical repository name `EpiLogos/Quaternal-Logic` is declared in `.oi/product.json`, but that address returns 404.
11. **Project CLAUDE.md.** The `aikit wiki ingest` example in this repository's CLAUDE.md omits the required `--file <wiki.json>`.
12. **Factory build records.** Factory has no production writer for Candidate, Claim or Evidence build records; only tests write them.
