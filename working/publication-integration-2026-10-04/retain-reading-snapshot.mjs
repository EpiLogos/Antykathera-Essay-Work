/** Retain the exact curated reading inputs without changing canonical main. */
import { readEssayInputs } from '/Users/admin/Central/Work/O-I/site/essay-source.mjs';
import { execFileSync } from 'node:child_process';
import { mkdirSync, writeFileSync, readFileSync, existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { createHash } from 'node:crypto';
const repo = '/Users/admin/Central/Work/O-I/Antykathera-Essay-Work';
const here = resolve(repo,'working/publication-integration-2026-10-04');
const git = (args,opts={}) => execFileSync('git',args,{cwd:repo,...opts}).toString().trim();
const inputs = await readEssayInputs(resolve(repo,'submission-package/essay'));
// The author has concurrently collated a new section and manuscript body.
// Preserve that live work while the existing manuscript publication deferral holds.
const heldBasis = '8265f382177086daff1fbd461c932b521babc971';
const withheld = ['CONFRONTING-THE-LIMIT-S01.md'];
const manuscript = inputs.entries.find(entry => entry.rel === 'THE-RETURN-OF-ZERO.md');
const currentManuscriptSha256 = manuscript.sha256;
manuscript.bytes = execFileSync('git', ['show', `${heldBasis}:published-reading/2026-10-04/THE-RETURN-OF-ZERO.md`], {cwd:repo});
manuscript.sha256 = createHash('sha256').update(manuscript.bytes).digest('hex');
inputs.entries = inputs.entries.filter(entry => !withheld.includes(entry.rel));
inputs.files = inputs.entries.map(({rel,sha256,kind}) => ({path:rel,sha256,kind}));
inputs.inputSha256 = createHash('sha256').update(JSON.stringify(inputs.files)).digest('hex');
const basis = git(['rev-parse','origin/main']);
if (git(['rev-parse','HEAD']) !== basis) throw Error('Local main and fetched canonical main differ.');
const retained = resolve(here,'.legacy-reading-inputs');
const prefix = 'published-reading/2026-10-04';
const index = resolve(here,'reading-snapshot.index');
const env = {...process.env,GIT_INDEX_FILE:index};
git(['read-tree',basis],{env});
const updates=[];
for (const entry of inputs.entries) {
 const file=resolve(retained,entry.rel);mkdirSync(dirname(file),{recursive:true});writeFileSync(file,entry.bytes);
 const blob=git(['hash-object','-w','--stdin'],{input:entry.bytes});
 updates.push(`100644 ${blob}\t${prefix}/${entry.rel}\n`);
}
const receipt = {schema:'essay.curated-reading-snapshot/v1',canonical_main:basis,input_sha256:inputs.inputSha256,
 foundation_slug:inputs.foundationSlug,files:inputs.files,
 withheld_current_paths:withheld,
 held_publication_objects:[{path:manuscript.rel,publication_basis:heldBasis,publication_sha256:manuscript.sha256,current_live_sha256:currentManuscriptSha256}],
 standing:'Curated reading projection of recovered source and reader navigation. The concurrently collated §0/1 submission is withheld; the manuscript retains its previously published development-draft bytes under the existing deferral. Live authorial files are preserved. This snapshot is not new prose acceptance.'};
const bytes=Buffer.from(JSON.stringify(receipt,null,2)+'\n');
writeFileSync(resolve(here,'READING-INPUTS.json'),bytes);
const blob=git(['hash-object','-w','--stdin'],{input:bytes});updates.push(`100644 ${blob}\t${prefix}/PUBLICATION-INPUTS.json\n`);
git(['update-index','--index-info'],{env,input:updates.join('')});
const tree=git(['write-tree'],{env});
const metadataPath=resolve(here,'READING-SNAPSHOT.json');
const previous=existsSync(metadataPath) ? JSON.parse(readFileSync(metadataPath,'utf8')).commit : undefined;
const commit=git(['commit-tree',tree,'-p',previous || basis],{input:'Retain current essay reading edition and visual assets for site publication\n\nA byte-bound public projection; canonical main, protected notes and authorial working drafts are preserved.\n'});
const ref='refs/heads/publication/reading-2026-10-04';git(['update-ref',ref,commit]);
const changed=git(['diff','--name-only',basis,commit]).split('\n');
if(changed.some(p=>!p.startsWith(prefix+'/')))throw Error('Snapshot changes escaped publication prefix.');
writeFileSync(resolve(here,'READING-SNAPSHOT.json'),JSON.stringify({...receipt,commit,tree,ref,prefix,local_retained_inputs:retained},null,2)+'\n');
console.log(JSON.stringify({commit,ref,input_sha256:inputs.inputSha256,files:inputs.files.length,bytes:inputs.entries.reduce((n,e)=>n+e.bytes.length,0)}));
