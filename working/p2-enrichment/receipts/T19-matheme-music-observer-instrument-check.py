from pathlib import Path
import math,json
s=Path('submission-package/essay/symbolon/matheme/music/observer-instrument.md').read_text()
assert '\\nu(f)=12\\log_2' in s
p=lambda f:round(12*math.log2(f/256))%12
examples=[]
for n in range(12):
 f=256*2**(n/12)
 assert p(f)==n and p(2*f)==n
 examples.append({'semitone':n,'frequency_Hz':f,'class':p(f),'octave_class':p(2*f)})
kappa=531441/524288;cents=1200*math.log2(kappa)
assert abs(cents-23.460010384649)<1e-8 and cents<50
for n in range(12):assert p(256*2**(n/12)*kappa)==n
before={7,11,2};after={0,4,7}
assert {(x-2)%12 for x in before}=={5,9,0}
assert {(x-2)%12 for x in after}=={10,2,5}
assert before|after=={0,2,4,7,11}
assert (2*2+1)==5 and(2*1+1)==3
Path('working/p2-enrichment/receipts/T19-matheme-music-observer-instrument-arithmetic.json').write_text(json.dumps({'standing':'Calculations on explicitly constructed frequencies and written note sets; not recorded sound or current-runtime output','method':'Python math.log2 projection and exact pitch-class set operations','constructed_frequency_cases':examples,'comma_cents':cents,'comma_bin_centre_invariance_cases':12,'cadence_reanchor_before':sorted((x-2)%12 for x in before),'cadence_reanchor_after':sorted((x-2)%12 for x in after),'passed':True},indent=2)+'\n')
print('Constructed frequency/address, octave, comma-bin and written cadence checks passed; no acoustic observation claimed.')
