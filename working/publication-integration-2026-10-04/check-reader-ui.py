from pathlib import Path
import importlib.util, json, os, sys, re
from playwright.sync_api import sync_playwright, expect
SITE=Path('/Users/admin/Central/Work/O-I/site')
OUT=Path(__file__).parent
spec=importlib.util.spec_from_file_location('native_essay_host',SITE/'tests/essay-host-smoke.py');host=importlib.util.module_from_spec(spec);spec.loader.exec_module(host)
server=None
if len(sys.argv)>1: base=sys.argv[1].rstrip('/');label='production'
else:
 server,port=host.start('vercel','');base=f'http://127.0.0.1:{port}';label='local'
foundation='section-rooms/00-integral-threshold/ROOM-00-integral-threshold'
result={'base':base,'checks':[]}
try:
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/Users/admin/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',args=['--enable-unsafe-swiftshader','--use-gl=angle','--use-angle=swiftshader'])
  ctx=b.new_context(viewport={'width':1440,'height':960});ctx.set_default_timeout(60000);page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(base+'/essay/',wait_until='load');expect(page.locator('.graph-container canvas').first).to_be_visible(timeout=60000)
  page.locator('.essay-anchor a').filter(has_text='§0/1').click();page.wait_for_url('**/'+foundation);expect(page.locator('.graph-container canvas').first).to_be_visible(timeout=60000)
  result['checks'].append('foundation route and rendered local graph')
  expect(page.locator('.explorer-ul li').first).to_be_attached(timeout=60000);assert page.locator('.explorer-ul li').count()>10
  button=page.locator('.explorer-ul .folder-icon').first;container=button.locator('xpath=..').locator('xpath=following-sibling::div[1]');before=container.get_attribute('class');button.click();expect(container).not_to_have_attribute('class',before);button.click();expect(container).to_have_attribute('class',before)
  result['checks'].append('nested explorer folders fold and reopen')
  page.screenshot(path=str(OUT/f'{label}-foundation.png'),full_page=False)
  page.locator('.global-graph-icon').click();expect(page.locator('.global-graph-container canvas')).to_be_visible(timeout=60000);page.keyboard.press('Escape');result['checks'].append('global graph opens with actual canvas')
  page.locator('.search-button').first.click();search=page.locator('.search-bar').first;expect(search).to_be_visible();search.fill('winding');expect(page.locator('.search-layout a').first).to_be_visible(timeout=60000);page.keyboard.press('Escape');result['checks'].append('search returns field pages')
  page.goto(base+'/essay/symbolon/matheme/diagrams/torus-square-quotient-and-winding',wait_until='load');img=page.locator('img[src*="torus-square-quotient-and-winding.svg"]');expect(img).to_be_visible();assert img.evaluate('(im)=>im.complete&&im.naturalWidth>0');page.screenshot(path=str(OUT/f'{label}-formal-diagram.png'));result['checks'].append('formal SVG actually loads in its page')
  mobile=b.new_context(viewport={'width':390,'height':844});q=mobile.new_page();q.goto(base+'/essay/'+foundation,wait_until='load');toggle=q.locator('.mobile-explorer');expect(toggle).to_be_visible(timeout=60000);toggle.click();assert q.evaluate('document.documentElement.classList.contains("mobile-no-scroll")');toggle.click();assert not q.evaluate('document.documentElement.classList.contains("mobile-no-scroll")');q.screenshot(path=str(OUT/f'{label}-mobile-foundation.png'));result['checks'].append('mobile explorer drawer opens and closes')
  assert not errors,errors
  b.close()
 result['pass']=True
finally:
 if server:host.stop(server)
 (OUT/f'READER-UI-{label.upper()}.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
