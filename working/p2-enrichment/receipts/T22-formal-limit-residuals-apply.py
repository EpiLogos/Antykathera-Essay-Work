from pathlib import Path
import json,hashlib
p=Path('submission-package/essay/symbolon/episteme/dossiers/formal-limit.md');s=p.read_text();before=s
additions=[
('Its consequence for the dossier is to keep the use of an elucidation', '''<a id="ethics-value-and-the-mystical"></a>
At [6.4–6.522](https://www.gutenberg.org/files/5740/5740-pdf.pdf), this boundary reaches value. Facts describe contingent arrangements; adding another arrangement cannot give them unconditional worth (6.41). Ethics therefore cannot consist of further factual propositions (6.42–6.421). Ethical reward belongs to the act itself rather than an ensuing event (6.422); willing as a psychological phenomenon remains distinguishable from its ethical office (6.423). Good or bad willing changes the world's limits, its character as a whole, rather than adding a fact (6.43). The mystical concerns the world's existence and apprehension as a bounded whole (6.44–6.45). Even a complete scientific account leaves the problem of life untouched; its resolution appears in the problem's disappearance, while the inexpressible shows itself (6.52–6.522). These are positive Tractarian propositions about the relation between factual description and value, not missing entries in a catalogue. The dossier receives an exact limit on what further information accomplishes. Its native determining-act argument and faithful continuation retain their own warrants; silence alone establishes neither.

'''),
('A limit can also motivate the development of another formalism.', '''<a id="optical-figure-and-experiential-verification"></a>
The [inherited Blind Spot note](../concepts/reference-notes/blind-spot-frank-gleiser-thompson.md) **figures** the difference through the optic nerve's location: a local gap in visual reception can itself become an object of anatomical inquiry. Experience as the condition of observing has a different office. Adding an account of the gap still requires an encounter in which that account is read, tested and understood. The figure retains this asymmetry without assigning an unverified passage to the book. In the essay's technical return, model provenance must lead back to the observations, situated judgments and people through whom a result is checked. Human experiential verification includes the ability to contest a model's description of an encounter and make that contest consequential for its next use. An AI system's own confidence report cannot discharge that independent return. This is the essay's argued responsibility for verification; the book's exact AI passages remain a named source task, and artificial phenomenality remains Open.

'''),
("[Whitehead's *Process and Reality*]", '''<a id="frequency-retention-and-signed-dia-research"></a>
The [re-entry note](../concepts/reference-notes/re-entry.md) retains the authorial chain distinction → re-entry → oscillation → frequency → retention as **Argued**. Varela's printed p.21 offers temporal alternation and possible frequency modulation, then expressly leaves frequency characterisation for investigation. It therefore supplies a particular research opening in that chain, not its completed frequency-to-retention derivation. The remaining work here is to specify what recurs, how a frequency is measured, what retains a prior state and how that retention changes the next crossing. The note's signed dia-ballein `(+1)/(−1)` as the `0/1` seam unrolled through generated time remains **Offered, undeveloped authorial research**: it requires an explicit mapping of signs, states and temporal order, with rules preserving the distinction between a re-entering form and its temporal interpretation. The equation `x = not-x` alone supplies none of those specifications. The [developed Laws of Form / Varela comparison](../../matheme/formal-neighbours/laws-of-form-varela.md) **qualifies** the formal boundary; the open development belongs to the native comparison, without downgrading the note's declared argument or assigning it to Varela.

''')]
for marker,insert in additions:
 assert s.count(marker)==1,(marker,s.count(marker));s=s.replace(marker,insert+marker,1)
old="**grounds** the performed return that the sparse File One reference note could only indicate."
assert s.count(old)==1
s=s.replace(old,"**grounds** the performed theological return in its own identified manuscript.")
marker='The [complete Investigation and Faith aphorism]'
insert='''<a id="file-one-identity-and-provenance"></a>
The [Binary Explication source house](../sources/internal-corpus/taylor/taylor-2026-binary-explication/SOURCE.md) **historicises** a distinct, present object: `canonical-candidate/file-one-definitional.md`, titled *File 1 — The Definitional §0/1*, is the definition member of the four-file candidate set. Its work identity differs from the older `file-one/the-self-proving-self.md` stratum and from *The Definition of God — Draft 3*, which the house identifies as a parallel theological application. The sparse [File One Definitional reference](../concepts/reference-notes/file-one-definitional.md) preserves an earlier unresolved source pointer. The present candidate is an exact available title/path match; that does not establish which historical object the note originally designated. The alias decision therefore remains **unresolved** pending a dated citation, explicit crosswalk or authorial identification. The old blanket missing-file statement is not repeated as current locality, and the performed definition remains grounded in Draft 3 without substituting that work for File One.

'''
assert s.count(marker)==1;s=s.replace(marker,insert+marker,1)
# Fresh read immediately before write protects concurrent insertions.
assert p.read_text()==before,'Concurrent body change; rebase exact insertions before writing'
p.write_text(s)
r=Path('working/p2-enrichment/receipts')
(r/'T22-formal-limit-residuals-targets.json').write_text(json.dumps({'elements':[{'canonical_home':str(p),'register':'episteme','record_id':'dossier-formal-limit'}]},indent=2)+'\n')
(r/'T22-formal-limit-residuals-change.json').write_text(json.dumps({'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(s.encode()).hexdigest(),'anchors':['ethics-value-and-the-mystical','optical-figure-and-experiential-verification','frequency-retention-and-signed-dia-research','file-one-identity-and-provenance'],'replaced_exact':old,'preservation':'Four insertions and one scoped identity-clause replacement; existing E paragraphs and all remaining text preserved.'},indent=2)+'\n')
print('Landed four residuals')
