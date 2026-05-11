#!/usr/bin/env python3
"""
URL Validation Script - TDD approach
Validates all blog URLs in places.json
"""
import json
import subprocess
import time
import sys

def fetch_url(url, timeout=15):
    """Fetch URL using web_fetch tool via jina AI extractor"""
    try:
        result = subprocess.run(
            ['python3', '-c', f'''
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    "{url}",
    headers={{"User-Agent": "Mozilla/5.0 (compatible; URLValidator/1.0)"}}
)
with urllib.request.urlopen(req, timeout={timeout}, context=ctx) as resp:
    return resp.status, len(resp.read())
'''],
            capture_output=True, text=True, timeout=timeout+5
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            status = int(lines[0]) if lines else 0
            length = int(lines[1]) if len(lines) > 1 else 0
            return status, length
        return 0, 0
    except Exception as e:
        return 0, 0

def main():
    with open('places.json') as f:
        data = json.load(f)
    
    urls = []
    for place in data['places']:
        for link in place.get('blogLinks', []):
            urls.append({
                'place_id': place['id'],
                'place_name': place['nameZh'],
                'url': link['url'],
                'title': link['title'],
                'source': link.get('source', '')
            })
    
    print(f"Total URLs to validate: {len(urls)}")
    
    report = []
    for i, u in enumerate(urls):
        print(f"[{i+1}/{len(urls)}] Checking: {u['url']}", flush=True)
        status, length = fetch_url(u['url'])
        u['http_status'] = status
        u['content_length'] = length
        u['status'] = 'valid' if status == 200 and length > 100 else ('suspicious' if status == 200 else 'invalid')
        report.append(u)
        time.sleep(0.5)  # Rate limiting
        
        if (i+1) % 10 == 0:
            with open('/home/node/.openclaw/workspace/url-validation-report.json', 'w') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
    
    with open('/home/node/.openclaw/workspace/url-validation-report.json', 'w') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # Summary
    valid = sum(1 for r in report if r['status'] == 'valid')
    suspicious = sum(1 for r in report if r['status'] == 'suspicious')
    invalid = sum(1 for r in report if r['status'] == 'invalid')
    print(f"\n=== SUMMARY ===")
    print(f"Valid: {valid}, Suspicious: {suspicious}, Invalid: {invalid}")
    
    with open('/home/node/.openclaw/workspace/PLAN-url-verification-lessons.jsonl', 'w') as f:
        f.write(json.dumps({'timestamp': time.time(), 'summary': {'valid': valid, 'suspicious': suspicious, 'invalid': invalid}}, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    main()
