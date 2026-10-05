import importlib.util,os,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright, Locator
site=Path('/Users/admin/Central/Work/O-I/site/.publication-verification/site')
spec=importlib.util.spec_from_file_location('reader',site/'tests/essay-reader-controls.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
server,port=r.host.start('vercel','')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Users/admin/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
 page=b.new_page(viewport={'width':900,'height':850});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.add_init_script("window.repeatSearchEvents=[];document.addEventListener('input',e=>{if(e.target.matches('.search-bar')) window.repeatSearchEvents.push({value:e.target.value,time:performance.now()})},true)")
 fills=[]
 original_fill=Locator.fill
 def traced_fill(locator,value,**kwargs):
  before=locator.evaluate("e=>({value:e.value,connected:e.isConnected,layout:e.closest('.search').querySelector('.search-layout').isConnected,results:[...e.closest('.search').querySelectorAll('.results-container')].map(r=>({connected:r.isConnected,children:r.children.length}))})")
  c=page.context.new_cdp_session(page)
  listeners={}
  for selector in ['.search-button','.search-bar']:
   obj=c.send('Runtime.evaluate',{'expression':f'document.querySelector("{selector}")'})['result']['objectId']
   ls=c.send('DOMDebugger.getEventListeners',{'objectId':obj})['listeners']
   listeners[selector]=[l['type'] for l in ls]
  fills.append({'query':value,'before':before,'listeners':listeners})
  return original_fill(locator,value,**kwargs)
 Locator.fill=traced_fill
 try: result=r.deep_routes(page,f'http://127.0.0.1:{port}','','trace');result['passed']=True
 except Exception as e: result={'passed':False,'error':str(e),'traceback':traceback.format_exc()}
 result['fills']=fills
 result['state']=page.evaluate("({events:window.repeatSearchEvents,searches:[...document.querySelectorAll('.search')].map(s=>({active:s.querySelector('.search-container').className,value:s.querySelector('.search-bar').value,layouts:[...s.querySelectorAll('.results-container')].map(r=>({connected:r.isConnected,html:r.innerHTML.slice(0,500)}))}))})")
 result['page_errors']=errors
 c=page.context.new_cdp_session(page)
 result['listeners']={}
 for selector in ['.search-button','.search-bar']:
  obj=c.send('Runtime.evaluate',{'expression':f'document.querySelector("{selector}")'})['result']['objectId']
  ls=c.send('DOMDebugger.getEventListeners',{'objectId':obj})['listeners']
  result['listeners'][selector]=[{'type':l['type'],'handler':l.get('handler',{}).get('description',''),'line':l.get('lineNumber')}for l in ls]
 Path('/Users/admin/Central/Work/O-I/Antykathera-Essay-Work/working/oi-publication-review-2026-10-04/REPEAT-SEARCH-TRACE.json').write_text(json.dumps(result,indent=2))
 print(json.dumps(result,indent=2));b.close()
r.host.stop(server)
