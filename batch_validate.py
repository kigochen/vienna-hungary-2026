#!/usr/bin/env python3
"""
URL Validation - Batch Processor
Validates all 123 URLs in places.json using web_fetch
"""
import json
import time
import urllib.request
import ssl

def check_url(url):
    """Check URL using direct HTTP request"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            content = resp.read()
            return resp.status, len(content), content[:500].decode('utf-8', errors='ignore')
    except urllib.error.HTTPError as e:
        return e.code, 0, f"HTTP {e.code}"
    except Exception as e:
        return 0, 0, str(e)[:100]

def main():
    with open('/home/node/.openclaw/workspace/vienna-trip/places.json') as f:
        data = json.load(f)
    
    all_urls = []
    for place in data['places']:
        for link in place.get('blogLinks', []):
            all_urls.append({
                'place_id': place['id'],
                'place_name': place['nameZh'],
                'url': link['url'],
                'title': link['title'],
                'source': link.get('source', '')
            })
    
    print(f"Total URLs: {len(all_urls)}")
    
    results = []
    for i, u in enumerate(all_urls):
        url = u['url']
        short_src = u['source'][:20]
        print(f"[{i+1:3d}/{len(all_urls)}] {short_src:<20} {url[:60]}", flush=True)
        
        status, length, snippet = check_url(url)
        u['http_status'] = status
        u['content_length'] = length
        u['snippet'] = snippet[:200]
        
        if status == 200 and length > 500:
            if '找不到頁面' in snippet or '404' in snippet or 'Not Found' in snippet:
                u['status'] = 'fake_404'
            else:
                u['status'] = 'valid'
        elif status == 404 or status == 410:
            u['status'] = 'invalid'
        elif status == 0:
            u['status'] = 'error'
        else:
            u['status'] = 'suspicious'
        
        results.append(u)
        time.sleep(0.3)
        
        if (i+1) % 20 == 0:
            with open('/home/node/.openclaw/workspace/url-validation-report.json', 'w') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
    
    with open('/home/node/.openclaw/workspace/url-validation-report.json', 'w') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    valid = sum(1 for r in results if r['status'] == 'valid')
    fake_404 = sum(1 for r in results if r['status'] == 'fake_404')
    invalid = sum(1 for r in results if r['status'] == 'invalid')
    error = sum(1 for r in results if r['status'] == 'error')
    suspicious = sum(1 for r in results if r['status'] == 'suspicious')
    
    print(f"\n=== FINAL SUMMARY ===")
    print(f"Valid (200+content): {valid}")
    print(f"Fake 404 (200 but page not found): {fake_404}")
    print(f"Invalid (404/410): {invalid}")
    print(f"Error (connection error): {error}")
    print(f"Suspicious: {suspicious}")
    
    # Write lessons
    with open('/home/node/.openclaw/workspace/PLAN-url-verification-lessons.jsonl', 'w') as f:
        f.write(json.dumps({
            'timestamp': time.time(),
            'total': len(all_urls),
            'valid': valid,
            'fake_404': fake_404,
            'invalid': invalid,
            'error': error,
            'suspicious': suspicious
        }, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    main()
