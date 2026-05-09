/**
 * retry-missing-images.js
 * 重試還沒有真實 photoUrl 的景點（32 個）
 * 每次只處理 10 個，等待較長時間避免 rate limit
 */

const fs = require('fs');
const https = require('https');

const PLACES_JSON_PATH = '/home/node/.openclaw/workspace/vienna-trip/src/places.json';

const FAKE = 'https://images.unsplash.com/photo-1508009603885-50cf7c579365';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function httpGet(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'ViennaTripBot/1.0 (educational project)' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({ statusCode: res.statusCode, body: data }));
    }).on('error', reject);
  });
}

async function searchWikimediaCommons(query, retryCount = 0) {
  try {
    const encodedQuery = encodeURIComponent(query);
    const url = `https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=${encodedQuery}&gsrnamespace=6&prop=imageinfo&iiprop=url&iilimit=1&format=json&origin=*`;

    const result = await httpGet(url);

    // Rate limited - retry after delay
    if (result.statusCode === 429 || result.body.startsWith('You are making requests')) {
      if (retryCount < 3) {
        const waitTime = (retryCount + 1) * 5000;
        console.log(`  ⏳ Rate limited，等待 ${waitTime}ms...`);
        await sleep(waitTime);
        return searchWikimediaCommons(query, retryCount + 1);
      }
      return null;
    }

    const json = JSON.parse(result.body);
    const pages = json.query?.pages || {};

    for (const pageId in pages) {
      const page = pages[pageId];
      if (page.imageinfo && page.imageinfo[0] && page.imageinfo[0].url) {
        return page.imageinfo[0].url;
      }
    }
    return null;
  } catch (e) {
    if (e.message.includes('JSON')) {
      // Malformed response, might be rate limit page
      if (retryCount < 2) {
        await sleep(5000);
        return searchWikimediaCommons(query, retryCount + 1);
      }
    }
    return null;
  }
}

function makeGoogleSearchUrl(name, city) {
  const q = encodeURIComponent(`${name} ${city}`);
  return `https://www.google.com/search?q=${q}&tbm=isch`;
}

async function processBatch(places, startIndex, batchSize) {
  const batch = places.slice(startIndex, startIndex + batchSize);
  console.log(`\n📦 Batch ${Math.floor(startIndex / batchSize) + 1}: 處理 ${batch.length} 個景點\n`);

  for (let i = 0; i < batch.length; i++) {
    const globalIdx = startIndex + i;
    const place = batch[i];
    const searchQueries = [
      `${place.name} ${place.city}`,
      place.nameZh,
      place.name
    ];

    process.stdout.write(`[${globalIdx + 1}/62] ${place.nameZh} (${place.city})... `);

    let foundUrl = null;

    for (const q of searchQueries) {
      if (foundUrl) break;
      foundUrl = await searchWikimediaCommons(q);
      if (!foundUrl) await sleep(500);
    }

    if (foundUrl) {
      place.photoUrl = foundUrl;
      console.log(`✅ ${foundUrl.substring(0, 70)}...`);
    } else {
      console.log('⚠️ 找不到圖片');
    }

    // 儲存進度
    fs.writeFileSync(PLACES_JSON_PATH, JSON.stringify(JSON.parse(fs.readFileSync(PLACES_JSON_PATH, 'utf8')), null, 2));

    // 請求間隔
    await sleep(800);
  }
}

async function main() {
  console.log('⚡ 讀取 places.json...');
  const raw = fs.readFileSync(PLACES_JSON_PATH, 'utf8');
  const data = JSON.parse(raw);

  // 找出還沒有真實 photoUrl 的景點
  const missingPlaces = data.places
    .map((p, i) => ({ place: p, index: i }))
    .filter(({ place }) => !place.photoUrl || place.photoUrl === FAKE)
    .map(({ place, index }) => ({ ...place, _index: index }));

  console.log(`⚡ 找到 ${missingPlaces.length} 個景點需要更新 photoUrl\n`);

  // 分批處理：每批 10 個，每批之間休息 15 秒
  const BATCH_SIZE = 10;
  for (let i = 0; i < missingPlaces.length; i += BATCH_SIZE) {
    const batch = missingPlaces.slice(i, i + BATCH_SIZE);
    await processBatch(
      batch.map(bp => data.places[bp._index]),
      0,
      batch.length
    );

    if (i + BATCH_SIZE < missingPlaces.length) {
      console.log('\n💤 批次間隔 20 秒...\n');
      await sleep(20000);
    }
  }

  // 最終儲存
  fs.writeFileSync(PLACES_JSON_PATH, JSON.stringify(data, null, 2));

  const updated = data.places.filter(p => p.photoUrl && p.photoUrl !== FAKE).length;
  console.log('\n========================================');
  console.log(`✅ 完成！共 ${updated}/62 個景點有真實 photoUrl`);
  console.log('========================================');
}

main().catch(console.error);