"""Same native reader regression functions against the actually deployed domain.
Run only after the parent confirms deployment of the validated build.
"""
import importlib.util
import json
import os
import traceback
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

FOLDER = Path(__file__).resolve().parent
OUT = FOLDER / 'production-reader-controls'
os.environ['OI_READER_EVIDENCE'] = str(OUT)
SITE = Path('/Users/admin/Central/Work/O-I/site/.publication-verification/site')
spec = importlib.util.spec_from_file_location('native_reader', SITE / 'tests/essay-reader-controls.py')
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)
BASE = 'https://oi.epi-logos.org'
report = {'url': BASE, 'started_at': datetime.now(timezone.utc).isoformat(),
          'expected_product_build': '73a06f0e108dfb417ea42ac50130a6b681bd5e58',
          'expected_reading_source': 'b2b5b706105891f69e2a68ecd160dbe4add3828e',
          'cases': []}

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path='/Users/admin/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',
        args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    for kind, width in [('controls', 1440), ('controls', 900), ('controls', 390), ('routes-and-search', 1440), ('routes-and-search', 900)]:
        label = f'production-{width}-{kind}'
        context = browser.new_context(viewport={'width': width, 'height': 850}, reduced_motion='reduce')
        page = context.new_page()
        js_errors, console_errors, error_responses, documents = [], [], [], []
        page.on('pageerror', lambda err: js_errors.append(str(err)))
        page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)
        def response_seen(response):
            if response.status >= 400:
                error_responses.append({'url': response.url, 'status': response.status})
            if response.request.resource_type == 'document':
                documents.append({'url': response.url, 'status': response.status})
        page.on('response', response_seen)
        record = {'case': label, 'kind': kind, 'width': width, 'passed': False}
        try:
            if kind == 'controls':
                record.update(reader.controls(page, BASE, '', width, label))
            else:
                record.update(reader.deep_routes(page, BASE, '', label))
            assert not js_errors, js_errors
            assert not console_errors, console_errors
            assert not error_responses, error_responses
            record['passed'] = True
            print('PASS', label, flush=True)
        except Exception as err:
            record.update(error=str(err), traceback=traceback.format_exc())
            print('FAIL', label, str(err), flush=True)
            report['cases'].append(record)
            (OUT / 'production-reader.json').write_text(json.dumps(report, indent=2) + '\n')
            try:
                page.screenshot(path=str(OUT / f'{label}-failure.png'), timeout=5000)
            except Exception as screenshot_error:
                record['failure_screenshot_error'] = str(screenshot_error)
        finally:
            record.update(js_errors=js_errors, console_errors=console_errors,
                          http_errors=error_responses, documents=documents)
            if record not in report['cases']:
                report['cases'].append(record)
            context.close()
            (OUT / 'production-reader.json').write_text(json.dumps(report, indent=2) + '\n')
    browser.close()
report['completed_at'] = datetime.now(timezone.utc).isoformat()
report['passed'] = sum(case['passed'] for case in report['cases'])
report['failed'] = len(report['cases']) - report['passed']
(OUT / 'production-reader.json').write_text(json.dumps(report, indent=2) + '\n')
raise SystemExit(1 if report['failed'] else 0)
