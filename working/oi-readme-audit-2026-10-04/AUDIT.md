# README audit: O:I and its six products

4 October 2026. Prepared for Frank Taylor. Nothing in any repository was edited, committed or pushed. The proposed replacements sit beside this file.

**Ranking, worst first:** O:I (no technical account at all; 83% in before the first command) > Software Factory (62% before any command; no install, no command list) > Quaternal Logic / MEF (opens with internal issue numbers; never says plainly what `ql` does) > Actuation (35% of constitutional prose before a strong command reference) > Workcell (purpose is clear early, but no CLI, no install and two dead links) > AIKit (concrete early, but install at 75%, plus two stale claims) > Central (least bad: it says "plain files" by 11%, but `ctrl` first appears at 78%).

## How this was checked

- **README text.** Each README was read in full. All seven local README blobs match current remote `main` byte for byte (GitHub contents API, 4 Oct 2026).
- **Binaries.** I ran each installed binary's own help and a few read-only commands: `oi` 0.1.0 (515d3485), `ctrl` 0.1.0 (2a604574, an ancestor of Central `origin/main`), `aikit` 0.1.0 (e8ba9689), `actuation` 0.2.1 (69bdc351), `factory` 0.1.0 (ef2817ce), `workcell` 0.1.0 (174fa1c3), `ql` 0.1.0 (6a81fc44). The commands were `oi products|status|world|act`, `ctrl actions`, `actuation harness catalog|detect`, `actuation verify`, `workcell status|discover|providers|places`, `ql mef lenses`, `ql verify`, `ql vak compose fixtures/kernel/vak-composition-v1.json --json`, and `aikit client status`.
- **Links and release pages.** Local links in every README were checked against the checkouts, and external repository links against GitHub. Release lists came from `gh release list`.
- **Code checked for specific claims:** crate manifests, `rust-toolchain.toml`, Actuation's command table (`crates/actuation-cli/src/dispatch.rs`), AIKit's CLI parser (`crates/aikit-cli/src/cli.rs`), O:I's `cli/src/frontdoor.rs` and `surfaces.json`, and Central's `ctrl/src`.

**Fraction read.** For each README, this is how far into the text (by characters) a reader gets before learning what the thing technically is and does: what kind of software it is, and at least one real command or object it works on.

**How the proposals are built.** Each product proposal has a new hand-written opening. Everything after it is the current README's own text, moved and not rewritten. Philosophy goes under a closing "Design background" section, with the corrections listed below. A line-by-line check confirms that every line of each current README survives in its proposal, apart from the corrections and the duplicated install paragraphs. The O:I proposal is a full redraft. Its long conceptual sections should move verbatim to a new `docs/PRIMITIVES.md` rather than be lost.

**An earlier brief.** `oi-publication-review-2026-10-04/CLAUDE-COPY-BRIEF.md` concluded that "no blanket rewrite of the six native READMEs is warranted". Your verdict today supersedes that conclusion. Its factual findings (the Factory URL and the stray "D") still stand and are included here.

---

## 1. O:I — `EpiLogos/O-I`, README.md (3,311 words)

**Verdict.** It is a philosophy essay standing where a README should be. It never says what O:I is as software: six Rust CLIs plus an installer and doorway. It never says the one thing a developer needs to hear, that O:I is the layer underneath the agent harness that keeps your agent world outside any one harness. "Harness" appears in the body only as a word in a list of runtime parts. The phrase "harness before the harness" appears nowhere in the repository or the essay tree.

**Fraction read before it says what it technically is and does.** It never states this outright. The six products are first named concretely in the table at **71%**. The first command (`oi central ...`) comes at **83%**. There is no install or quick start anywhere in the README.

**Waffle passages:**
- The first sentence: "names and develops the technological field in which model capacity becomes situated agency."
- "**Provisioning** makes conditions for action available; **potentiation** changes what can become actual through them."
- "The smallest useful case and the richest research case are points in one possibility space".
- The six "contact points" (Authorship, Authority, Commission, Recognition, Revision, Refusal), and "ordinary constitutional acts rather than exceptional failure modes".
- "The six centres are not a product catalogue. They are custodians of stretches of this circuit".
- "The primitives are structure, not incantation." This opens about 1,300 words of Ground, Actor, Act, Across acts, Claims, Between worlds, Material and Horizon, each with capitalised terms of art, before the product table.
- "{O:I} itself is the Idea and whole relating these centres."

**Keep:**
- **The `oi` doorway block and the namespace mapping.**
- **The six-product table and its links.** The "What it changes" column has some real substance.
- **The design distinctions,** which are genuinely useful once stated plainly: authored vs observed vs inferred; identity surviving model/harness change; evidence returning to whoever started the work; the claim ladder (authored position → design → architecture → implementation fact → evidence → agent inference).
- **The "Reading further" table** keyed by kind of claim. It is a good idea.
- **The pointer to `skills/oi/SKILL.md`.**
- **The research stance** of holding model capacity constant and treating the arrangement as the variable, including the line that a simpler arrangement winning is a legitimate result.

**Accuracy problems:**
- **Factory link.** The six-centre table links Software Factory to `https://github.com/EpiLogos/agent-system-design`. That old name redirects, but the current address is `https://github.com/EpiLogos/Factory`.
- **Stray "D".** A lone `D` sits on line 261, directly under "### Current state (temporal)".
- **The `oi` section misdescribes `oi`.** It calls `oi` "the shared doorway" and lists only the namespace dispatch. The binary's own help describes it first as the tool that "installs, inspects and verifies the suite's recorded product builds". The README omits `oi install`, `init`, `status`, `doctor`, `verify`, `update`, `world`, `search`, `act`, `agent roster` and `dev`, which are the commands a newcomer actually uses.
- **`oi prove factory`.** This command is on `main` (`cli/src/frontdoor.rs`), but the installed release-line `oi` (515d3485) answers "unknown command 'prove'", and `oi help` does not list it. Readers on a release build will hit that.
- **Internal references with no context:** "physical #97 acceptance", "`suite/mainline.json` for the standing qualifications".
- **No essay link.** The essay (*Confronting the Limit*, https://oi.epi-logos.org/essay/) and the public site are not linked.
- **No release state.** Nothing says the builds are pre-releases (`0.1.0-prelocal.6`), that `oi` itself reports "These builds have not passed physical acceptance", or which platforms are supported (Apple Silicon macOS, x64 Linux).
- **Adjacent, not the README.** `docs/INSTALL.md` gives the developer path as `$HOME/Central/Work/Software-Factory`, but the checkout on this machine and in the suite is `Work/Factory`.

**Proposed:** `PROPOSED-O-I-README.md`, a full redraft. Its plain sentence: "O:I is a harness before the harness: it keeps the world your agents work from — your authored ground, what agents may do and on whose behalf, the capabilities and sources they can reach, the machines they run on, and the evidence that comes back — outside any one model or harness, owned by you."

---

## 2. Software Factory — `EpiLogos/Factory`, README.md (2,216 words)

**Verdict.** A product with a large, working CLI (`factory --help` runs to over a hundred lines of grouped commands) has a README containing no command list, no install and no example. The reader gets about 1,400 words of "telos" and "developmental relation" first. The first concrete section is then a single paragraph about file-publisher internals (xattr and ACL limits, descriptor admission). That is the wrong level of detail for a front door.

**Fraction read before it says what it technically is and does.** **62%**. The first command (`factory development admit-routine-continuation`) appears in "Current repository". Even there the reader is never told plainly that `factory` is a Rust CLI keeping file-based records of Commissions, Runs, attempts and Returns.

**Waffle passages:**
- The first sentence: "making agentic software development durable and intelligible from authored intention through design, development, evidence, candidate formation, Recognition and Return".
- "The Factory is successful when greater agentic capability gives the human **more room for vision, judgement and life away from babysitting agent mechanics**".
- "Recognition is not a ceremonial approval button".
- "The durable result is not only code. It is a Project that knows more about itself."

**Keep:**
- **The intent-drift problem statement.** The second and third paragraphs, about software preserving the nouns while losing why they mattered, are genuinely good and specific.
- **The "Returned reality can revise the plan" table** (implementation defect → revise development, and so on). It is concrete.
- **All of "Current repository".** It is accurate implementation truth. It belongs lower, not removed.
- **The repository layer map** (canon / factory / contracts / skills / provenance / ql-agent-experiments).
- **The "Read first" list.**
- **The Workcell resource-usage consumption note.**

**Accuracy problems:**
- **No install path.** It should be `cargo install --path factory`; the binary is `factory/src/bin/factory.rs`. Alternatively `oi install software-factory`, or the pre-release `software-factory-v0.1.0-prelocal.6`.
- **The most concrete current features are missing:** `factory workflow check|compile|commission` (typed TypeScript workflows), `factory attempt ...` and `factory telemetry ...`. The telemetry reads GitHub issues and workflow runs plus Factory's own failures.
- **QL-prefixed doc names.** The canon documents are still named `QL-SOFTWARE-FACTORY-*`, while the README says ordinary Factory operation must not require QL. Worth a sentence, or a rename later.
- **No GitHub description.** The repository has an empty description, so the search results show nothing.

**Proposed sentence:** "Software Factory is a Rust CLI (`factory`) that keeps a durable record of agent-driven software work — what was asked for and why, the runs and attempts made against it, what each produced, the evidence gathered, and how the result was judged — so a project can later explain why its code is the way it is."

---

## 3. Quaternal Logic / MEF — `EpiLogos/QL-MEF`, README.md (1,940 words)

**Verdict.** The opening is written for the project's own maintainers mid-programme, not for anyone arriving. Before the reader learns what `ql` is, they meet three paragraphs of issue and PR numbers (#123, #83, #138, AIKit #267, Factory #217, O:I #216, #122, PR #137, a full commit hash), plus internal terms ("L5 is the concrescence of the existing L0 / L0′ / L5′ / L5 articulation square"). The body below, on operational parity, null results, QL being optional and the product boundary, is some of the clearest writing in the suite, and it is buried.

**Fraction read before it says what it technically is and does.** About **3%** before "implementation home for the standalone executable QL/MEF product", after a navigation disclaimer, and **21%** before the first command (`ql vak compose`). Neither tells a newcomer what the kernel or MEF actually computes. The plain list of what QL owns is at **67%**.

**Waffle passages:**
- "**formal and experimental field in which the wider Epi-Logos programme attempts to make archetypal and relational form technically answerable**".
- "Context-Frame identity propagates from harmonic determination into Geometry, Meta Epistemic Framework and generative use".
- "That executable boundary matters, but it is not the whole meaning of the project."

**Keep:**
- **"The epistemic discipline: operational parity",** with its `position = 5 / meaning = return` example. It is excellent and should sit near the top.
- **"Negative and null results are legitimate".**
- **"Minimal O:I does not require QL".**
- **"Alignment, not translation. Refraction, not renaming."**
- **The owns / does-not-own lists.**
- **The working `ql vak compose` example.** It was run, and it returns `ql.vak-composition/v1` JSON.

**Accuracy problems:**
- **No install section.** It should be `cargo install --path crates/ql-cli`, or `oi install quaternal-logic`, or the pre-release `quaternal-logic-v0.1.0-prelocal.6`.
- **The real CLI is never shown.** `ql kernel apply` with its three deterministic operators, `ql mef lenses`, `ql service negotiate`, `ql verify` and `ql matheme` are all missing.
- **Self-described stale status.** The opening carries its own "older ... paragraphs ... are historical status" caveat, which signals stale status text that should be resolved rather than annotated.
- **Three names for one thing.** The repository is `QL-MEF`, the product is "Quaternal Logic", and the local checkout is `Quaternal-Logic`. This is fine, but the opening should name the repository once.
- **No GitHub description.**

**Proposed sentence:** "Quaternal Logic / MEF is a Rust library and CLI (`ql`) that implements the formal structures of Quaternal Logic — a six-position (0–5) coordinate kernel with addresses and deterministic operators, and the Meta-Epistemic Framework (MEF), a registry of twelve lenses for reading one subject from different angles — as typed, testable operations that return JSON with provenance attached."

---

## 4. Actuation — `EpiLogos/Actuation`, README.md (2,836 words)

**Verdict.** It has the best command reference in the suite: complete, derived from one command table, and accurate against 0.2.1. But the reader must first get through about 1,000 words of "constitution", "political questions", "Metagency" and a formal tuple. The first line calls Actuation a "developmental and reference home" when it ships a released, attested binary. Below the command list, the reference then becomes a wall of protocol detail (the `nara serve` pipe limits, the config argument grammar, occupancy refusal codes) that belongs in `docs/`.

**Fraction read before it says what it technically is and does.** **35%** ("Install and use"). The tuple `Actuation(g, W, I) = C⟨g, L, D, Γ, B, R⟩` at 25% is precise but tells a developer nothing about what to run.

**Waffle passages:**
- The first sentence: "the developmental and reference home for **the constitution and management of technological agency**".
- "These are political questions in the literal architectural sense".
- "whole-preserving relation by which a situated Agency determines a bounded plurality of agentic loci".
- "Metagency is an Agency's capacity to take agency itself as an object of action".

**Keep:**
- **The whole command reference.**
- **The note that help, capabilities and dispatch come from one table,** so "the CLI cannot lie about itself".
- **Harness catalog and detection.**
- **The occupancy ledger semantics.**
- **The `stream usage` adapters** and their no-content guarantee.
- **The Agent / Agency / AgentSession / Execution / Harness distinction.** It is load-bearing and should be defined plainly once.
- **The four determination kinds.**
- **The repository map.**
- **The honest research caveat** of "zero claimed live Series 1 capability runs".

**Accuracy problems:**
- **The opening undersells the product.** As noted in the verdict, it calls Actuation a "developmental and reference home"; it should say it ships `actuation-v0.2.1` (macOS arm64, Linux x86_64, with sha256 sidecars, all verified on the release page).
- **Stray HTML comment.** A trailing `<!-- branch-protection proof: PR + required native-cli check + squash merge -->` is left in the README.
- **Spot-checked commands are accurate.** `verify`, `system`, `harness *`, `occupancy *`, `stream *` and `config *` are all present in 0.2.1, and `actuation verify` returns `status: ok`.
- **No GitHub description.**

**Proposed sentence:** "Actuation is a Rust CLI (`actuation`) and set of crates that record which agent is acting, in what role, on whose authority and within what limits, and keep an append-only record of what each act did and what came back."

---

## 5. Workcell — `EpiLogos/Workcell`, README.md (1,159 words)

**Verdict.** It has the most concrete opening of the six. By the third paragraph it says Workcell turns "provider-neutral demand into a reachable, inspectable material world". But the README never shows the `workcell` CLI at all, has no install, and says almost nothing about what works today. Its "Current implementation" section is three sentences of hedging. Meanwhile the binary does a great deal: cross-machine connections with expiring grants, secret scan and vault with projection by reference, live harness-process census and resource readings, and a full prepare-to-release lifecycle with receipts.

**Fraction read before it says what it technically is and does.** It conveys what Workcell is conceptually by about **9%**. The first command anywhere is `./scripts/verify.sh` at **99%**. The `workcell` CLI never appears.

**Waffle passages:**
- The first sentence: "the relatively standalone **technological materialisation product** beneath EpiLogos semantic clients".
- "The result should be **less infrastructure babysitting without loss of material intelligibility**."
- "the **material conditions in which the act can actually occur**".

**Keep:**
- **The "More than execution" list.**
- **The semantic-demand → bindings → evidence diagram.**
- **The required/preferred/optional example.**
- **The control-plane vs native data-plane section.**
- **"Material placement is part of provenance".**
- **The verify-script note.**

**Accuracy problems:**
- **Two dead links:** `docs/MATERIALISATION-SPEC.md` and `docs/LIFECYCLE-AND-CANDIDATES.md` do not exist, and never existed in git history. The nearest existing docs are `docs/CANDIDATE-MATERIALISATION.md` and `docs/LIFECYCLE-RECONCILIATION.md`. The proposal swaps them in, and adds `CROSS-CELL-CONNECTIONS.md` and `PROVIDER-SDK.md`.
- **exe.dev.** It is named as a proving specimen, but appears only in design docs. There is no provider crate for it. The crates that do exist are Docker, Arrakis, OpenSandbox, Tailscale, 1Password and keychain.
- **No install.** It should be `cargo install --path crates/workcell-cli` (package `epilogos-workcell-cli`, binary `workcell`), or `oi install workcell`, or the pre-release `workcell-v0.1.0-prelocal.6`.
- **Title and description.** The title "EpiLogos Workcell" is inconsistent with the other five, and the GitHub description is just "Workcell".

**Proposed sentence:** "Workcell is a Rust CLI and control service (`workcell`) that turns a request for an environment — 'a writable checkout at this revision, a shell, these services, internet access' — into a real workspace, process, service or machine, and records what was actually provided, where, and what happened to it."

---

## 6. AIKit — `EpiLogos/ai-kit`, README.md (2,251 words)

**Verdict.** The second paragraph lists the actual problem in concrete terms: models, CLI agents, skills, tmux and cmux sessions, several harnesses. "Why this exists" is a good list of real failures (skills copied by several installers, hooks with no clear active relation). But "operative composition and disclosure layer" leads. The implemented-capabilities table is at 60% and install at 75%. Before install, the reader hits two dense paragraphs of `aikit adopt ... --control-ground ... --projection CURRENT/...` procedure.

**Fraction read before it says what it technically is and does.** About **2–5%** for the problem domain. **60%** before the reader learns what it concretely does (the implementation table). **75%** before install.

**Waffle passages:**
- The bold line: "**The operative composition and disclosure layer for heterogeneous agentic worlds.**"
- "It is therefore not a bag of agent features."
- "This makes context cognition possible".

**Keep:**
- **"Why this exists".**
- **The "exists ≠ eligible ≠ available ≠ selected ≠ projected ≠ loaded ≠ invoked" ladder.** It is the best one-glance statement of the design in the suite.
- **The implementation table.**
- **Install, portable sessions, worktree projection, verification and development commands.**
- **The adoption procedure.** It is accurate and useful, but should sit below install.

**Accuracy problems:**
- **Wrong Rust version.** The README says "Rust 1.88 or newer". The workspace declares `rust-version = "1.98"` and pins `1.98.0` in `rust-toolchain.toml`.
- **Stale harness-profile claim.** The Harness profiles row says "there is no public validate/register verb for external profile documents yet". `aikit harness-profile` (validate) now exists, both in the binary and in `crates/aikit-cli/src/cli.rs`. Registration is still absent.
- **Old command spellings.** The README uses pre-grouping spellings (`aikit status`, `aikit tree`). These still work, but the CLI's own everyday heads (`world`, `search`, `act`, `compose`, `work`, `knowledge`, `praxis`, `explain`) never appear.
- **Client support understated.** The table says projections for "Claude and Codex". `aikit client status` also reports descriptor support for gemini-cli, pi, openclaw and zcode.
- **A paragraph after the License.** It should go into Documentation.
- **The GitHub repository description says "production-grade".** The README says "production-oriented alpha". The README is the honest one; the description should change.

**Proposed sentence:** "AIKit is a Rust CLI and terminal UI (`aikit`) that works out which skills, tools, models, knowledge sources and sessions apply to an agent in a given project, and installs exactly that set into the agent harnesses you already use — reversibly, and without taking ownership of them."

---

## 7. Central — `EpiLogos/Central`, README.md (1,560 words)

**Verdict.** It is the least bad. By the second section a reader knows Central is ordinary files with stable Actions and replaceable connectors. "Control says what should persist. `ctrl` says what can be done. Connectors say how it can be done here." is a model one-line architecture statement. The problems are the soft first sentence, the CLI arriving at 78%, and a status sentence that now undersells what is on `main`.

**Fraction read before it says what it technically is and does.** **11%** before "Central uses ordinary files", **24%** before the directory layout, and **78%** before `ctrl` and its commands.

**Waffle passages:**
- The first sentence: "a **human-owned operating root for a technological life**".
- "The larger product is the relation between **human authorship, continuity, ordinary work and changing technological implementations**."
- "**less repeated re-authoring of the same technological life**".

**Keep:**
- **The authored / observed / inferred block.**
- **The Action → Port → Connector diagram.**
- **The two-worlds tree** (personal root vs product checkout).
- **The `mixed_root` doctor check.**
- **The ten product principles.**
- **The install commands, the init shape and the ProjectCentral lifecycle Actions.**
- **The documentation route.**

**Accuracy problems:**
- **The status sentence is stale.** It says "Open extension PRs — including richer authored-ground, NOW/DAY, governance and physical-machine lines — remain development state". In fact `central.now.*`, `central.day.*`, `projectcentral.now.*`, `machine.*` and `ctrl recover` are on `main`. The installed `ctrl` (2a604574) is an ancestor of `origin/main` and lists 188 Actions including them.
- **The everyday CLI is missing:** `ctrl work list|search|open`, `ctrl pick`, `ctrl control open|search`, `ctrl git census`, `ctrl machine ...`, `ctrl action run|describe`.
- **Connectors and surfaces are never named.** The connectors are chezmoi, Homebrew, macOS, Ubuntu, git-sync, Shortcuts and harness; the surfaces are Raycast, Shortcuts and macOS host.
- **No toolchain warning.** The `oi install central` route builds from source, so it needs Rust, and the README does not say so.
- **The GitHub description is just "Central".**

**Proposed sentence:** "Central keeps what you have written about yourself, your projects and your machines as plain files in a personal root (`~/Central`), and gives people and agents one Rust CLI, `ctrl`, to read and change that material through named, typed Actions."

---

## Cross-cutting

- **Each README re-explains O:I in its own vocabulary.** Every product has a "Relation to the wider {O:I} field" section, each written fresh. The proposals add one shared sentence to every opening, "O:I is a harness before the harness: the person-owned world agents work from, kept outside any one model or agent harness", and keep each product's longer relation section lower down.
- **Philosophy moves, it is not cut.** In every proposal the philosophy sits under "Design background", which opens with one paragraph defining Objective Internality in plain words and linking the essay at https://oi.epi-logos.org/essay/.
- **GitHub "About" descriptions** are empty or one word for O:I, Actuation, Factory, Workcell and QL-MEF, and AIKit's says "production-grade". They are worth setting when the READMEs are applied, since they are what GitHub search shows.
- **Not verified by this audit:** artifact attestations on the releases, the internal behaviour of the `factory-ui/` and desktop surfaces, and the standing of each Workcell provider crate. The proposals avoid claims that depend on them.
