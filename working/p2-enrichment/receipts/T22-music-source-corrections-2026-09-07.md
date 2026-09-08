# T22 — Material music-source corrections

Disposition: correction receipt only. The four-file and v3 raw source bodies were not edited. These results constrain later projections and can be considered at the source-maintenance stage. The native operations survive the corrections.

## 1. Square count: seven unique unordered tetrads

**Affected passage:** Binary Explication File Four §2, “The 3×3 squares” (source slice 137–204); matching music/pairing-grammar README/packet description; inherited recovery claim “nine entries, eight unique tetrads.”

The source table has nine functional entries. Their base pairs yield eight distinct ordered pairs because A-sq2 and B-sq3 both use (2,3). But B-sq1 uses (0,5) and C-sq3 uses (5,0): their unordered endpoints, and thus their four-state squares, are also the same.

- A-sq2=B-sq3: `{2,3,2′,3′}`; chromatic `{E,F♯,F,G}`.
- B-sq1=C-sq3 as unordered sets: `{0,5,0′,5′}`; chromatic `{C,A♯,C♯,B}`.

**Correct count:** nine family entries, eight distinct ordered base pairs, seven unique unordered base pairs/tetrads. The nine grammatical offices remain. If source intends “tetrad” to retain a directed ordering, that convention must be stated; it cannot simultaneously use ordinary unordered-sonority counting without the second coincidence.

Verification: `T19-matheme-music-pairing-grammar-check.py` parses every printed interval/square row. Its first run failed the inherited eight-tetrad assertion; the corrected seven-count passes. Both coincidences are invariant under the bijective change of substrate map. Canonical projection already corrected; no raw source amendment made.

## 2. Architectural 8+4 is not a sounding-subset claim

**Affected passage:** File Four §4’s inner-eight/bebop and nodal-four account, read against §5’s CF-major table.

At the source’s C anchor, the inner positions 1–4 and 1′–4′ map to `{D,D♯,E,F,F♯,G,G♯,A}`; the outer positions 0,5,0′,5′ map to `{C,C♯,A♯,B}`. File Four’s C-major selection `{C,D,E,F,G,A,B}` therefore contains five inner and two outer positions. It cannot be a seven-note subset of the inner-eight collection alone. The complete twelve-state palette supplies that selection.

**Surviving proposition:** the doubled 4+2 architecture has eight articulating and four framing addresses; scale membership requires its own selected position set. The address partition alone neither establishes a named Barry Harris scale nor a physical plate-node assignment. The lens projection retains the architectural operation and scopes those source comparisons to their actual evidence.

Verification: `T19-matheme-music-lens-anchors-check.py` parses both complete lens maps and computes the 8+4 and 5+2 partitions exactly.

## 3. Modal faces under the stated fixed Lens-0 map

**Affected passage:** File Four §5, the seven-mode table; parallel table in musical-v3. The tonic, mode and CF columns specify rotations of the same C-major collection. Its fixed-map faces are NNNPPPP for C,D,E,F,G,A,B. Rotating these assignments yields:

| Mode | Correct fixed-map pattern |
|---|---|
| Ionian | NNNPPPP |
| Dorian | NNPPPPN |
| Phrygian | NPPPPNN |
| Lydian | PPPPNNN |
| Mixolydian | PPPNNNP |
| Aeolian | PPNNNPP |
| Locrian | PNNNPPP |

The source’s last four patterns do not follow from those fixed notes and assignments. A fresh local-coordinate map could change face labels, but that would require an explicitly stated operation. This correction preserves the source’s tonic/mode/CF identities and computes faces from the actual printed notes. Parallel C natural minor is a different operation and has pattern NNPPPNN; its lowered third changes position 2→1′ while its sixth/seventh preserve the index and flip face.

Verification: `T19-matheme-music-diatonic-cf-grammar-check.py` parses the actual seven mode rows, rotates the source scale, subtracts each tonic and checks every face string. All pass.

## 4. The CF1–CF5 cluster is not a major-ninth chord

**Affected passage:** File Four §5’s voicing landscape; musical-v3’s corresponding cluster treatment. The printed set `{C,D,E,F,G}` contains F and lacks B; a C-major-ninth set is `{C,E,G,B,D}`. Preserving the actual cluster repairs the label without replacing its CF selections. Over D it gives degrees 1,2,♭3,4,♭7; it can suggest a Dorian context but lacks the major sixth needed to establish that modal distinction. A sounded subset and the modal field it suggests must remain separate objects. The same reusable check verifies these exact set differences.

## 5. The 84/60 partition: an explicit correspondence and a failed containment claim

**Affected passage:** File Four §5’s 144-grid paragraph and musical-v3 §II-4.8.

The earlier recovery debt concerning 84+60 can now be refined. Define parent major-scale S_a, first-five-degree upper cluster K_a, modal indices M={(a,m)} and cluster/bass indices V={(a,b)}. The explicit map Φ(a,m)=(a,a+S[m] mod12) is a bijection from the 84 modal indices onto V_in={(a,b):b∈S_a}. Its complement V_out contains 60 entries. Thus 144=84+60 is a valid indexed-grid partition under the declared definitions. The map preserves parent/tonic identity; it does not equate the five-tone upper cluster with a seven-tone scale. The source’s count survives once that distinction is supplied.

The further assertion that each outside-parent bass moves the whole sonority into another diatonic lens is false for these exact clusters. At C, K={C,D,E,F,G}. Of the outside basses C♯,D♯,F♯,G♯,B♭, only B♭ yields a union contained in any other transposed major collection: F major. The other four unions fit no major collection. Transposition gives 12 qualifying cases and 48 nonqualifying cases across the 60 outside-parent entries. Those 48 remain playable chromatic configurations; the source must not automatically call them another member of the defined diatonic modal field.

Verification: `T19-matheme-music-field-check.py` exhausts all 144 grid entries, proves the 84-index bijection, and tests all 720 combinations of outside-parent sonority and candidate major collection. The canonical field page includes the resulting five-row C-parent example. Raw source remains unchanged.
