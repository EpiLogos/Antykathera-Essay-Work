---
aliases:
- Stern — Ueber eine zahlentheoretische Funktion (1858)
- Stern 1858
- Moritz Abraham Stern — Ueber eine zahlentheoretische Funktion (1858)
record_type: journal-article
source_role:
- mathematical-primary
- stern-brocot-construction
- qualifying-source
citation_style: chicago-notes-bibliography-18
metadata_status: verified
edition_status: selected
citation_status: citation-ready
quote_status: quotation-ready
chicago_ready: true
author:
- Moritz Abraham Stern
title_full: Ueber eine zahlentheoretische Funktion
container_title: Journal für die reine und angewandte Mathematik
volume: 55
issue: 3
year: 1858
page_range: 193–220
doi: 10.1515/crll.1858.55.193
url: https://doi.org/10.1515/crll.1858.55.193
carrier_url: https://zenodo.org/records/1448876
accessed: '2026-10-05'
consumed_by_sections:
- §1
consumed_by_arguments: []
tags:
- epi-logos/antikythera-essay
- source-bank/record
- source-bank/mathematics
title: Moritz Abraham Stern — Ueber eine zahlentheoretische Funktion (1858)
source_id: stern-1858-zahlentheoretische-funktion
primary_domain: mathematics-logic
node_type: source-house
ownership: canonical-source-house
schema_version: 1
passage_surface: '#passages'
main_source_for:
- "§1 · #5→0 · the sum written between two numbers (Stern's half of the Stern–Brocot construction)"
---
# Moritz Abraham Stern — Ueber eine zahlentheoretische Funktion (1858)

## Bibliographic identity

Article no. 12 in *Journal für die reine und angewandte Mathematik* (Crelle's journal), vol. 55, no. 3 (printed footer "Journal für Mathematik Bd. LV. Heft 3."), pp. 193–220, byline "(Von Herrn Stern zu Göttingen.)". The closing line on p. 220 dates the manuscript "Göttingen, im Juli 1855."; the volume is dated 1858. DOI 10.1515/crll.1858.55.193.

**Carrier consulted:** the De Gruyter page-image PDF of the article (28 pages, printed pp. 193–220, with a De Gruyter download stamp of 2015), deposited openly on Zenodo, record 1448876, licence CC0, title "Ueber eine zahlentheoretische Funktion.", creator "Stern, M.", DOI as above. Fetched with curl on 2026-10-05; pages rendered to images locally and read directly. A second lawful carrier is the Göttingen digitisation (DigiZeitschriften/GDZ, PPN002150301), not consulted here.

Title, volume, issue, year and page range were verified from the page images (title page p. 193, final page p. 220, footers on pp. 193 and 201).

## Chicago 18 forms

**Full note:** Moritz Abraham Stern, "Ueber eine zahlentheoretische Funktion," *Journal für die reine und angewandte Mathematik* 55 (1858): {page}, https://doi.org/10.1515/crll.1858.55.193.

**Shortened note:** Stern, "Ueber eine zahlentheoretische Funktion," {page}.

**Bibliography:** Stern, Moritz Abraham. "Ueber eine zahlentheoretische Funktion." *Journal für die reine und angewandte Mathematik* 55 (1858): 193–220. https://doi.org/10.1515/crll.1858.55.193.

## Source scholarship

Stern writes in answer to Eisenstein's 1850 note in the Berlin *Monatsberichte* on a number-theoretic function and the "merkwürdige Zahlenreihe" it led to; Eisenstein had asked Stern in a letter of 14 January 1850 for more elementary proofs (p. 193). Stern's aim is to derive the properties of the series and of the function "aus den elementarsten Betrachtungen."

**What Stern actually does.** He starts from two *arbitrary* positive numbers `m` and `n`, not literally from `0/1` and `1/0` (§1, p. 194). He writes their sum between them, then repeats the operation on every adjacent pair, row after row, "ins Unendliche." The whole family of rows he calls the *Entwickelung* `(m, n)`, with `m` the first and `n` the second *Argument*; the starting pair `m, n` is the *nullte Entwickelungsreihe*; each inserted number is a *Summenglied*, every other number a *Stammglied*. His objects are rows of integers and adjacent pairs (*Gruppen*) of integers, not fractions and not a tree: neither "Baum" nor any word like "diatomic" occurs in the article (checked against the full extracted text). On p. 196 he restricts the arguments to integers and explicitly lets one of them be zero, writing sums over the developments `(1, 0)` and `(0, 1)`. The main study (§3 onward) is the development `(1, 1)`, "auf welche sich … alle übrigen Fälle zurückführen lassen."

**The results that later carry the Stern–Brocot tree.** For `(1, 1)`: two adjacent members never share a factor (§5, p. 199); a given adjacent pair `a, b` occurs at most once in the whole development (§6, p. 200); every pair `a, c` of relatively prime numbers does occur (§8, p. 201). Together these say that the adjacent pairs of `(1, 1)` run through every coprime ordered pair exactly once. Stern reads a pair as a quotient only in §10 (p. 203), where he locates the row of a pair `a, c` by expanding `a/c` as a continued fraction. On p. 204 he writes out the development `(0, 1)`: `(0, 1)₂ = 0, 1, 1, 2, 1` and `(0, 1)₃ = 0, 1, 1, 2, 1, 3, 2, 3, 1`.

**Relation to the modern tree (this house's own reasoning, not Stern's claim).** If one writes mediants between `0/1` and `1/0`, the numerators obey Stern's rule by themselves and form his `(0, 1)` rows, and the denominators form the `(1, 0)` rows: row 2 of the mediant construction is `0/1, 1/2, 1/1, 2/1, 1/0`, whose numerators `0, 1, 1, 2, 1` are Stern's printed `(0, 1)₂`. Stern supplies the additive insertion and the coprimality and once-only theorems; he does not supply the fraction tree, the ordering of fractions, or the determinant identity `bc − ad = 1` in fraction form. The fraction reading belongs to Brocot ([[brocot-1862-calcul-des-rouages]]) and to the later textbook synthesis (Graham, Knuth and Patashnik, *Concrete Mathematics* (1994)).

**Typography.** The page images set the ß-ligature as "fs" (e.g. "dafs," "läfst," "heifsen"); transcriptions below keep the printed letters and the printed spacing of formulae, and mark italics only where noted.

<a id="passages"></a>
## Passages and excerpts

### Material metadata

- **Quote status:** quotation-ready for q001–q005.
- **Edition consulted:** *Journal für die reine und angewandte Mathematik* 55 (1858), pp. 193–220, De Gruyter page images via Zenodo record 1448876.
- **Access provenance:** curl download 2026-10-05; pages rendered at 1300 px and read as images; text extraction used only to locate passages.

<a id="stern-1858-zahlentheoretische-funktion-q001"></a>
## Passage card — `stern-1858-zahlentheoretische-funktion-q001` — the sum written between two numbers
^stern-1858-zahlentheoretische-funktion-q001

> Es seien zwei positive Zahlen m und n gegeben, man addire sie und setze die Summe m + n zwischen dieselben, so erhält man die Folge
> (1.) m, m + n, n.
> […] und man sieht, dafs sich das Verfahren ins Unendliche fortsetzen läfst.

Agent's working English, not for quotation as Stern's words: "Let two positive numbers m and n be given; add them and set the sum m + n between them, and one obtains the sequence (1.) m, m + n, n. […] and one sees that the procedure can be continued to infinity."

- **Locator:** §1, p. 194 (opening sentence of §1; the second sentence closes the paragraph after formula (3.)). Zenodo PDF p. 2.
- **Status:** quotation-ready.
- **Verification:** transcribed from the rendered page image of p. 194, collated against extracted text (OCR errors "m-^n," "m-\-n" rejected), agent, 2026-10-05. The ellipsis omits the second and third rows, formulae (2.) and (3.).
- **Source relation:** extracted.
- **Evidential action:** supports.
- **Consumers:** §1 · #5→0 (reworked draft, 2026-10-05).
- **Use boundary:** Stern starts from any two positive numbers `m, n`, not from `0/1` and `1/0`, and he inserts sums of integers, not mediants of fractions. The passage supports "write the sum between the two and repeat without end"; it does not support "Stern built a tree of fractions."

<a id="stern-1858-zahlentheoretische-funktion-q002"></a>
## Passage card — `stern-1858-zahlentheoretische-funktion-q002` — one argument may be zero
^stern-1858-zahlentheoretische-funktion-q002

> Im Folgenden sollen die Argumente immer *ganze* Zahlen sein, doch darf eines derselben auch Null werden.

Followed on the same page by the displayed equation `S_p(1, 1) = S_p(1, 0) + S_p(0, 1)`, where `S_p(m, n)` is the sum of the p-th row of the development `(m, n)`.

- **Locator:** §2, p. 196, first sentence of the page. Zenodo PDF p. 4.
- **Status:** quotation-ready.
- **Verification:** transcribed from the rendered page image of p. 196 ("ganze" italic in print), agent, 2026-10-05.
- **Source relation:** extracted.
- **Evidential action:** supports and qualifies.
- **Consumers:** §1 · #5→0 (reworked draft, 2026-10-05).
- **Use boundary:** Stern admits zero as one *argument* of a development of integers and decomposes `(1, 1)` into `(1, 0)` and `(0, 1)` by row sums. He does not write `1/0` as a fraction or speak of infinity here; reading `(1, 0)` and `(0, 1)` as the fractions `1/0` and `0/1` is the essay's or the textbook's step, not Stern's.

<a id="stern-1858-zahlentheoretische-funktion-q003"></a>
## Passage card — `stern-1858-zahlentheoretische-funktion-q003` — neighbours share no factor
^stern-1858-zahlentheoretische-funktion-q003

> Es können nie zwei aufeinander folgende Glieder einer Reihe einen gemeinschaftlichen Faktor haben.

- **Locator:** §5, p. 199 (italic theorem sentence opening §5), stated for the development `(1, 1)`. Zenodo PDF p. 7.
- **Status:** quotation-ready.
- **Verification:** transcribed from the rendered page image of p. 199, agent, 2026-10-05.
- **Source relation:** extracted.
- **Evidential action:** supports.
- **Consumers:** §1 · #5→0 (reworked draft, 2026-10-05).
- **Use boundary:** a theorem about adjacent integers in `(1, 1)`; it becomes "every fraction appears in lowest terms" only under the later fraction reading.

<a id="stern-1858-zahlentheoretische-funktion-q004"></a>
## Passage card — `stern-1858-zahlentheoretische-funktion-q004` — each coprime pair once, and every one
^stern-1858-zahlentheoretische-funktion-q004

> Eine bestimmte Gruppe a, b, kann also überhaupt nicht mehr als einmal in der Entwickelung (1, 1) vorkommen.

> In der Entwickelung (1, 1) kommt jede Gruppe a, c vor, bei welcher a und c relative Primzahlen sind.

- **Locator:** first sentence: end of §6, p. 200; second sentence: §8, p. 201 (second theorem of §8). Both italic in print. Zenodo PDF pp. 8–9.
- **Status:** quotation-ready.
- **Verification:** transcribed from the rendered page images of pp. 200–201 (OCR "Enlwickeluny" rejected), agent, 2026-10-05.
- **Source relation:** extracted.
- **Evidential action:** supports.
- **Consumers:** §1 · #5→0 (reworked draft, 2026-10-05).
- **Use boundary:** "at most once" (p. 200) and "every coprime pair occurs" (p. 201) are two separate theorems about ordered integer pairs in `(1, 1)`. The statement "every positive fraction appears exactly once in lowest terms" is their later fraction-form consequence, not a sentence of Stern's.

<a id="stern-1858-zahlentheoretische-funktion-q005"></a>
## Passage card — `stern-1858-zahlentheoretische-funktion-q005` — the quotient read as a continued fraction; the development (0, 1)
^stern-1858-zahlentheoretische-funktion-q005

> Um zu erfahren in welcher Reihe die Gruppe a, c vorkommt, verwandele man den Quotienten a/c in einen Kettenbruch, die Summe der Theilnenner um eine Einheit vermindert giebt die Zahl der Reihe.

> So ist z. B. (0, 1)₂ = 0, 1, 1, 2, 1 und (0, 1)₃ = 0, 1, 1, 2, 1, 3, 2, 3, 1, und es ist leicht zu sehen, dafs dies allgemein so sein mufs.

- **Locator:** first passage: §10, p. 203 (italic rule; the quotient is printed as a stacked fraction a over c); second passage: §11, p. 204. Zenodo PDF pp. 11–12.
- **Status:** quotation-ready (the stacked fraction is rendered inline as `a/c`; subscripts as printed).
- **Verification:** transcribed from the rendered page images of pp. 203–204, agent, 2026-10-05.
- **Source relation:** extracted.
- **Evidential action:** qualifies.
- **Consumers:** §1 · #5→0 (reworked draft, 2026-10-05).
- **Use boundary:** the only place Stern treats a pair as a quotient is through continued fractions, to find which row the pair stands in. The `(0, 1)` rows coincide with the numerators of the mediant rows between `0/1` and `1/0`; that identification is this house's reasoning (see Source scholarship), not Stern's statement.

## Essay uses

§1 · #5→0 (reworked draft, 2026-10-05): Stern is the first half of the Stern–Brocot attribution. He can be cited for the operation of writing the sum between two given numbers and repeating it without end, for admitting zero as an argument, and for the coprimality and once-only theorems. He cannot be cited for the fraction tree rooted at `0/1` and `1/0`.

## Open acquisition and verification

- Optional: collate the same pages in the GDZ/DigiZeitschriften scan (PPN002150301) to record a second carrier.
- The phrase "Stern's diatomic sequence/series" is later terminology and is not Stern's. Its origin (commonly credited to D. H. Lehmer, 1929) is unverified here and needs its own source before the essay uses the word.

## Returns

This source serves: [§1 · #5→0 — The Loan Returns](../../../../../../section-rooms/02-return-of-zero/movements/18-s1-p5-loan-returns.md).
