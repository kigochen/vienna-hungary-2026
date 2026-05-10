#!/usr/bin/env python3
"""Fix 404 Wikimedia URLs in places.json - Phase 2 with retry and longer delays"""
import json
import urllib.request
import urllib.parse
import time

WORKSPACE = '/home/node/.openclaw/workspace/vienna-trip'

def check_file_exists(filename):
    api_url = 'https://commons.wikimedia.org/w/api.php?action=query&titles=File:' + urllib.parse.quote(filename) + '&prop=imageinfo&iiprop=url&format=json'
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

def search_for_image(place_name, city, country):
    search_query = place_name + ' ' + city + ' ' + country
    search_url = 'https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=' + urllib.parse.quote(search_query) + '&srnamespace=6&format=json&srlimit=10'
    try:
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0 (OpenClaw Fixer/1.0)'})
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode('utf-8'))
        return data.get('query', {}).get('search', [])
    except Exception as e:
        return []

def find_best_match(place_name, search_results):
    name_lower = place_name.lower()
    for r in search_results:
        fname = r['title'].lower().replace('file:', '')
        if name_lower in fname or fname in name_lower:
            return r
    if search_results:
        return search_results[0]
    return None

def get_country(city):
    city_lower = city.lower()
    if city_lower in ['vienna', 'wien']:
        return 'Austria'
    return 'Hungary'

print('Loading places.json...')
with open(WORKSPACE + '/places.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 讀取上一輪的錯誤列表
error_ids = [
    'bp-gul-baba', 'bp-hospital-rock', 'bp-house-terror', 'bp-jewish-museum',
    'bp-karolyi-garden', 'bp-kolodko', 'bp-liberty-bridge', 'bp-library',
    'bp-margaret-island', 'bp-memento-park', 'bp-three-borders', 'bp-vajdahunyad',
    'bp-veli-bej', 'bp-wekerletelep', 'db-deri-museum', 'db-great-forest',
    'db-reformed-college', 'gy-basilica', 'gy-bishops-castle', 'hu-aggtelek-cave',
    'hu-bokodi-floating', 'hu-ferto-lake', 'hu-holloko', 'hu-hortobagy',
    'hu-megyer-tengerszem', 'hu-sopron', 'hu-tapolca-cave', 'lb-badacsony',
    'lb-keszthely', 'lb-tihany', 'pc-cathedral', 'pc-mecsek', 'pc-necropolis',
    'vn-fasanviertel', 'vn-grinzing', 'vn-hofburg', 'vn-hundertwasserhaus',
    'vn-karlskirche', 'vn-naschmarkt', 'vn-palais-ferstel', 'vn-prater',
    'vn-schonbrunn', 'vn-st-stephens', 'vn-state-opera', 'vn-tuerkenschanzpark',
    'vn-wachau-valley', 'vn-zentralfriedhof'
]

# 建立 id -> place 的 map
place_map = {p['id']: p for p in data['places']}

fixed = []
still_broken = []
retry_delay = 2.0  # 2秒延遲避免 429

for bid in error_ids:
    if bid not in place_map:
        continue
    place = place_map[bid]
    url = place.get('photoUrl', '')

    # 從 URL 取原始檔名
    if 'Special:FilePath/' in url:
        filename = url.split('Special:FilePath/')[-1]
        original_filename = urllib.parse.unquote(filename)
    else:
        original_filename = url

    city = place.get('city', '')
    country = get_country(city)

    print('Processing: ' + bid + ' (' + original_filename + ')')

    # 先重試檢查原始檔名（有時候檔名稍微不同）
    ok, direct_url, title = check_file_exists(original_filename)
    if ok:
        place['photoUrl'] = direct_url
        if place.get('photos'):
            place['photos'][0] = direct_url
        fixed.append((bid, 'RECHECK_OK', original_filename))
        print('  -> RECHECK OK: ' + direct_url)
        time.sleep(retry_delay)
        continue

    # 搜尋新圖
    search_results = search_for_image(place.get('name', ''), city, country)
    if not search_results:
        # 試純 name
        search_results = search_for_image(place.get('name', ''), '', country)

    match = find_best_match(place.get('name', ''), search_results)

    if match:
        matched_title = match['title'].replace('File:', '')
        ok2, direct_url2, title2 = check_file_exists(matched_title)
        if ok2:
            place['photoUrl'] = direct_url2
            if place.get('photos'):
                place['photos'][0] = direct_url2
            fixed.append((bid, 'FIXED', original_filename + ' -> ' + matched_title))
            print('  -> FIXED: ' + direct_url2)
        else:
            still_broken.append((bid, 'BAD_MATCH', matched_title))
            print('  -> BAD MATCH: ' + matched_title)
    else:
        still_broken.append((bid, 'NO_RESULT', original_filename))
        print('  -> NO RESULT')

    time.sleep(retry_delay)

print('')
print('=== Phase 2 Results ===')
print('Fixed this round: ' + str(len(fixed)))
for f in fixed:
    print('  ' + f[0] + ': ' + f[1] + ' -> ' + f[2])
print('Still broken: ' + str(len(still_broken)))
for b in still_broken:
    print('  ' + b[0] + ': ' + b[1] + ' -> ' + b[2])

# 寫入
with open(WORKSPACE + '/places.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('')
print('Places.json updated.')

with open(WORKSPACE + '/places.json', 'r', encoding='utf-8') as f:
    json.load(f)
print('JSON valid: YES')