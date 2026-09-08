from pathlib import Path
import requests,json,hashlib,concurrent.futures
from html.parser import HTMLParser
class Text(HTMLParser):
 def __init__(self): super().__init__(); self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ["script","style"]:self.skip+=1
 def handle_endtag(self,t):
  if t in ["script","style"]:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.parts.append(d.strip())
b=Path(__file__).parent/'external';b.mkdir(exist_ok=True)
items={
'lunel-letter':'https://geniza.princeton.edu/en/documents/19297/',
'paperclip-1946':'https://history.state.gov/historicaldocuments/frus1946v05/d448',
'gehlen-records':'https://www.archives.gov/iwg/about/press-releases/cold-war-spymaster-records.html',
'manzoni-1868':"https://it.wikisource.org/wiki/Dell%27unit%C3%A0_della_lingua_e_dei_mezzi_di_diffonderla",
'manzoni-critical-catalogue':'https://digit-manzoni.divsi.unimi.it/opere/13',
'hanegraaff':'https://www.wouterjhanegraaff.net/rejected-knowledge',
'hanegraaff-publisher-excerpt':'https://assets.cambridge.org/97805211/96215/excerpt/9780521196215_excerpt.pdf',
'fichte-1808':'https://germanhistorydocs.org/en/the-holy-roman-empire-1648-1815/ghdi:document-3596',
'reich-citizenship-1935':'https://germanhistorydocs.org/en/nazi-germany-1933-1945/the-reich-citizenship-law-september-15-1935-and-the-first-regulation-to-the-reich-citizenship-law-november-14-1935.pdf',
'welsh-blue-books-excerpt':'https://www.peoplescollection.wales/media/6108/download?attachment=',
'palestine-mandate':'https://digitallibrary.un.org/record/829707/files/A_292-EN.pdf',
'hebrew-language-war':'https://www.nli.org.il/en/education/teaching-resources/primary-sources/nnl_edu997013313315805171',
'pacioli-1509-object':'https://www.metmuseum.org/art/collection/search/336656',
'perdomo-2020':'https://proceedings.mlr.press/v119/perdomo20a.html'}
def get(kv):
 k,u=kv
 try:
  r=requests.get(u,timeout=35);r.raise_for_status();ext='pdf' if r.content.startswith(b'%PDF') else 'html';p=b/(k+'.'+ext);p.write_bytes(r.content)
  if ext=='html':
   parser=Text();parser.feed(r.text)
   (b/(k+'.txt')).write_text('\n'.join(parser.parts))
  return {'key':k,'url':u,'path':str(p),'sha256':hashlib.sha256(r.content).hexdigest(),'status':'retrieved','format':ext,'reading':'scope recorded separately, not presumed by acquisition'}
 except Exception as e:return {'key':k,'url':u,'status':'failed','error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(get,items.items()))
(b.parent/'external-acquisition.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps([{'key':x['key'],'status':x['status'],'format':x.get('format')} for x in rows],indent=2))
