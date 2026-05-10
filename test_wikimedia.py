#!/usr/bin/env python3
"""Test suite for Wikimedia URL fixer"""
import json
import urllib.request
import urllib.parse
import urllib.error
import time
import sys

WORKSPACE = '/home/node/.openclaw/workspace/vienna-trip'

def check_file_exists(filename):
    """用 Wikimedia API 檢查檔案是否存在並取得 URL"""
    api_url = f'https://commons.wikimedia.org/w/api.php?action=query&titles=File:{urllib.parse.quote(filename)}&prop=imageinfo&iiprop=url&format=json'
    try:
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0 (OpenClaw Fixer/1.0)'})
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode('utf-8'))
        pages = data.get('query', {}).get('pages', {})
        for pageid, page in pages.items():
            if pageid == '-1':
                return (False, None, None)
            imageinfo = page.get('imageinfo', [{}])[0]
            direct_url = imageinfo.get('thumburl') or imageinfo.get('url')
            return (True, direct_url, page.get('title'))
        return (False, None, None)
    except Exception as e:
        return (False, None, str(e))

def search_files(query, city, country="Hungary"):
    """搜尋 Wikimedia Commons 檔案"""
    search_query = f"{query} {city} {country}"
    search_url = f'https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(search_query)}&srnamespace=6&format=json&srlimit=5'
    try:
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0 (OpenClaw Fixer/1.0)'})
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode('utf-8'))
        results = data.get('query', {}).get('search', [])
        return results
    except Exception as e:
        return []

def test_check_file_exists_valid():
    """測試：已知的有效檔案"""
    ok, url, title = check_file_exists('Buda Castle.jpg')
    print(f"  [CHECK] Buda Castle.jpg: ok={ok}, title={title}")
    assert ok == True, "Buda Castle.jpg should exist"

def test_check_file_exists_invalid():
    """測試：不存在的檔案"""
    ok, url, title = check_file_exists('Nonexistent file xyz 12345.jpg')
    print(f"  [CHECK] Nonexistent xyz: ok={ok}")
    assert ok == False, "Nonexistent file should return False"

def test_search_files():
    """測試：搜尋功能"""
    results = search_files('A38 Ship', 'Budapest')
    print(f"  [SEARCH] A38 Ship Budapest: found={len(results)}")
    assert len(results) > 0, "Should find at least one result"

def test_places_json_loads():
    """測試：places.json 可正確讀取"""
    with open(f'{WORKSPACE}/places.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert 'places' in data
    assert len(data['places']) > 0
    print(f"  [JSON] places count: {len(data['places'])}")

def test_audit_all_urls():
    """測試：審計所有 URL"""
    with open(f'{WORKSPACE}/places.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 從 Special:FilePath URL 取出檔名
    broken = []
    checked = 0
    for place in data['places']:
        url = place.get('photoUrl', '')
        if not url:
            broken.append((place['id'], 'NO_URL', ''))
            continue

        # 從 URL 取出檔名
        if 'Special:FilePath/' in url:
            filename = url.split('Special:FilePath/')[-1]
            filename = urllib.parse.unquote(filename)
        else:
            filename = None

        checked += 1
        if filename:
            ok, direct_url, title = check_file_exists(filename)
            if not ok:
                broken.append((place['id'], 'NOT_FOUND', filename))
        else:
            broken.append((place['id'], 'BAD_URL_FORMAT', url))

    print(f"  [AUDIT] checked={checked}, broken={len(broken)}")
    for bid, reason, detail in broken[:10]:
        print(f"         - {bid}: {reason} -> {detail}")
    return broken

if __name__ == '__main__':
    print("=== Running Tests ===")
    tests = [
        ('check_file_exists_valid', test_check_file_exists_valid),
        ('check_file_exists_invalid', test_check_file_exists_invalid),
        ('search_files', test_search_files),
        ('places_json_loads', test_places_json_loads),
        ('audit_all_urls', test_audit_all_urls),
    ]
    for name, fn in tests:
        print(f"[*] Running {name}...")
        try:
            fn()
            print(f"  PASS")
        except AssertionError as e:
            print(f"  FAIL: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"  ERROR: {e}")
            sys.exit(1)
    print("=== All Tests Passed ===")