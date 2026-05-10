#!/usr/bin/env python3
"""Fix 404 Wikimedia URLs in places.json"""
import json
import urllib.request
import urllib.parse
import time
import sys

WORKSPACE = '/home/node/.openclaw/workspace/vienna-trip'

def check_file_exists(filename):
    """檢查檔案是否存在並取得 direct URL"""
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
    """搜尋 Wikimedia Commons 找圖片"""
    search_query = place_name + ' ' + city + ' ' + country
    search_url = 'https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=' + urllib.parse.quote(search_query) + '&srnamespace=6&format=json&srlimit=10'
    try:
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0 (OpenClaw Fixer/1.0)'})
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode('utf-8'))
        return data.get('query', {}).get('search', [])
    except Exception as e:
        print('    SEARCH ERROR: ' + str(e))
        return []

def find_best_match(place_name, search_results):
    """從搜尋結果中找最好的匹配"""
    name_lower = place_name.lower()
    for r in search_results:
        fname = r['title'].lower().replace('file:', '')
        if name_lower in fname or fname in name_lower:
            return r
    if search_results:
        return search_results[0]
    return None

def get_country(city):
    """根據城市判斷國家"""
    city_lower = city.lower()
    if city_lower in ['vienna', 'wien']:
        return 'Austria'
    return 'Hungary'

print('Loading places.json...')
with open(WORKSPACE + '/places.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 備份
backup_ts = time.strftime('%Y%m%d%H%M%S')
backup_file = WORKSPACE + '/places.json.backup.' + backup_ts
with open(backup_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('Backup saved: ' + backup_file)

fixed = []
skipped = []
errors = []

for place in data['places']:
    url = place.get('photoUrl', '')
    if not url or 'Special:FilePath/' not in url:
        skipped.append(place['id'])
        continue

    filename = url.split('Special:FilePath/')[-1]
    original_filename = urllib.parse.unquote(filename)

    ok, direct_url, title = check_file_exists(original_filename)

    if ok:
        place['photoUrl'] = direct_url
        fixed.append((place['id'], 'OK_ALREADY', original_filename))
        continue

    # 404，找替代圖片
    city = place.get('city', '')
    country = get_country(city)
    search_results = search_for_image(place.get('name', ''), city, country)

    if not search_results:
        search_results = search_for_image(place.get('name', ''), '', country)

    match = find_best_match(place.get('name', ''), search_results)

    if match:
        matched_title = match['title'].replace('File:', '')
        ok2, direct_url2, title2 = check_file_exists(matched_title)
        if ok2:
            place['photoUrl'] = direct_url2
            if len(place.get('photos', [])) > 0:
                place['photos'][0] = direct_url2
            fixed.append((place['id'], 'FIXED', original_filename + ' -> ' + matched_title))
        else:
            errors.append((place['id'], 'VERIFIED_BAD', matched_title))
    else:
        errors.append((place['id'], 'NO_SEARCH_RESULT', original_filename))

    time.sleep(0.3)

ok_already = len([x for x in fixed if x[1] == 'OK_ALREADY'])
replaced = len([x for x in fixed if x[1] == 'FIXED'])

print('')
print('=== Results ===')
print('OK (already valid): ' + str(ok_already))
print('Fixed (replaced):  ' + str(replaced))
print('Skipped:           ' + str(len(skipped)))
print('Errors:            ' + str(len(errors)))
print('')
if errors:
    print('Errors:')
    for e in errors:
        print('  ' + e[0] + ': ' + e[1] + ' -> ' + e[2])

with open(WORKSPACE + '/places.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('')
print('Places.json updated.')

# 驗證
with open(WORKSPACE + '/places.json', 'r', encoding='utf-8') as f:
    json.load(f)
print('JSON valid: YES')