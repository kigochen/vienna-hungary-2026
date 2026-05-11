#!/usr/bin/env python3
"""Fix places.json based on validation results"""
import json

with open('/home/node/.openclaw/workspace/vienna-trip/places.json') as f:
    data = json.load(f)

with open('/home/node/.openclaw/workspace/url-validation-report.json') as f:
    report = json.load(f)

# Build URL -> status map
url_status = {r['url']: r['status'] for r in report}
url_snippet = {r['url']: r['snippet'][:80] for r in report}

# URLs to remove (invalid, error, fake_404)
remove_urls = set()
for r in report:
    if r['status'] in ('invalid', 'error', 'fake_404'):
        remove_urls.add(r['url'])

# Suspicious URLs (403/blocked) - we'll keep them but flag for review
suspicious_urls = set()
for r in report:
    if r['status'] == 'suspicious':
        suspicious_urls.add(r['url'])

print("URLs to REMOVE:")
for url in sorted(remove_urls):
    print(f"  REMOVE: {url}")
    if url in url_snippet:
        print(f"         Reason: {url_snippet[url]}")

print("\nSuspicious URLs (403/blocked - will keep but flag):")
for url in sorted(suspicious_urls):
    print(f"  SUSPICIOUS: {url}")

# Fix places.json
fixed_count = 0
for place in data['places']:
    original_count = len(place.get('blogLinks', []))
    place['blogLinks'] = [
        link for link in place.get('blogLinks', [])
        if link['url'] not in remove_urls
    ]
    if len(place['blogLinks']) < original_count:
        fixed_count += 1
        print(f"\nFIXED: {place['nameZh']} ({place['id']})")
        print(f"  Before: {original_count} links, After: {len(place['blogLinks'])} links")

# Save fixed places.json
output_path = '/home/node/.openclaw/workspace/vienna-trip/places.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n=== SUMMARY ===")
print(f"Places fixed: {fixed_count}")
print(f"URLs removed: {len(remove_urls)}")
print(f"Suspicious URLs (kept): {len(suspicious_urls)}")
print(f"Saved to: {output_path}")
