import assert from 'node:assert/strict';
import fs from 'node:fs';
import { createSharedField, validateSharedFieldNesting, createContribution, createEncounter, selfOtherReadModel } from '/Users/admin/Central/Work/O-I/shared-field/social.mjs';
const results=[];
function check(name,fn){fn();results.push({name,status:'passed'});}
const provenance=[{kind:'test-input',ref:'private:dossier-functional-probe',source_system:'essay-audit'}];
const f=createSharedField({field_ref:'field:a',provenance});
check('Required provenance rejected when absent',()=>assert.throws(()=>createSharedField({field_ref:'field:a'}),/provenance/));
check('Containment cycles rejected',()=>assert.throws(()=>validateSharedFieldNesting([createSharedField({field_ref:'a',parent_field_ref:'b',provenance}),createSharedField({field_ref:'b',parent_field_ref:'a',provenance})]),/cycle/));
check('External parent retained without falsely claiming a complete graph',()=>assert.equal(validateSharedFieldNesting([createSharedField({field_ref:'a',parent_field_ref:'external',provenance})])[0].parent_field_ref,'external'));
check('Metric contribution retains attributed basis and target',()=>{const c=createContribution({contribution_ref:'contribution:a',field_ref:'field:a',contributor_participant_ref:'participant:a',created_at:'2026-09-08T00:00:00Z',mode:'metric',target:{ref:'contribution:prior',kind:'oi.contribution'},relation:{kind:'compares',basis:'declared-private-test'},representation:{kind:'json',payload:{value:1}},provenance});assert.equal(c.target.ref,'contribution:prior');assert.equal(c.contributor_participant_ref,'participant:a');assert.equal(c.relation.basis,'declared-private-test');});
check('Encounter reconstructs selected fields without importing subjective claim',()=>{const e=createEncounter({encounter_ref:'e:a',field_ref:'field:a',participant_ref:'participant:a',occurred_at:'2026-09-08T00:00:00Z',mediation:{kind:'direct'},items:[],provenance,understood:true});assert.ok(!('understood' in e));assert.deepEqual(e.items,[]);});
check('Self/Other rejects a participant from another field',()=>assert.throws(()=>selfOtherReadModel({self:{schema:'oi.participant/v1',participant_ref:'p:a',field_ref:'field:a'},others:[{schema:'oi.participant/v1',participant_ref:'p:b',field_ref:'field:b'}],field:f}),/selected SharedField/));
const receipt={date:'2026-09-08',implementation:'/Users/admin/Central/Work/O-I/shared-field/social.mjs',method:'Direct calls to actual checked-in implementation; no mocks, no network or source mutation',scope:'Six local constructor/validation behaviours; no authentication, source-acceptance, hosted service, UI, learning or deployment claim',passed:results.length,failed:0,results};
fs.writeFileSync(new URL('implementation-probe.json',import.meta.url),JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt));
