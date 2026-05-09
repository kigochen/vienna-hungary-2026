/**
 * fetch-wikimedia-images-v2.js
 * 使用 Wikimedia Commons API 直接搜尋圖片
 */

const fs = require('fs');
const https = require('https');

const PLACES_JSON_PATH = '/home/node/.openclaw/workspace/vienna-trip/src/places.json';
const OUTPUT_PATH = '/home/node/.openclaw/workspace/vienna-trip/src/places.json';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function httpGet(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'ViennaTripBot/1.0 (educational project)' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

// 使用 Wikimedia Commons API 搜尋圖片
async function searchWikimediaCommons(query) {
  try {
    const encodedQuery = encodeURIComponent(query);
    // 使用 action=query&generator=search 在命名空間 6 (檔案) 中搜尋
    const url = `https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=${encodedQuery}&gsrnamespace=6&prop=imageinfo&iiprop=url&iilimit=1&format=json&origin=*`;

    const data = await httpGet(url);
    const json = JSON.parse(data);
    const pages = json.query?.pages || {};

    for (const pageId in pages) {
      const page = pages[pageId];
      if (page.imageinfo && page.imageinfo[0] && page.imageinfo[0].url) {
        return page.imageinfo[0].url;
      }
    }
    return null;
  } catch (e) {
    console.error(`  API錯誤: ${e.message}`);
    return null;
  }
}

function makeGoogleSearchUrl(name, city) {
  const q = encodeURIComponent(`${name} ${city}`);
  return `https://www.google.com/search?q=${q}&tbm=isch`;
}

async function main() {
  console.log('⚡ 讀取 places.json...');
  const raw = fs.readFileSync(PLACES_JSON_PATH, 'utf8');
  const data = JSON.parse(raw);

  const FAKE = 'https://images.unsplash.com/photo-1508009603885-50cf7c579365';
  let updated = 0;
  let skipped = 0;

  for (let i = 0; i < data.places.length; i++) {
    const place = data.places[i];
    const searchQueries = [
      `${place.name} ${place.city}`,
      place.nameZh,
      place.name
    ];

    process.stdout.write(`[${i + 1}/62] ${place.nameZh} (${place.city})... `);

    // 檢查是否已有有效的 photoUrl
    if (place.photoUrl && place.photoUrl !== FAKE && place.photoUrl.startsWith('http')) {
      place.googleSearchUrl = makeGoogleSearchUrl(place.name, place.city);
      skipped++;
      console.log('✅ 已有有效圖片');
      continue;
    }

    let foundUrl = null;

    for (const q of searchQueries) {
      if (foundUrl) break;
      foundUrl = await searchWikimediaCommons(q);
      if (!foundUrl) await sleep(250);
    }

    if (foundUrl) {
      place.photoUrl = foundUrl;
      place.googleSearchUrl = makeGoogleSearchUrl(place.name, place.city);
      updated++;
      console.log(`✅ ${foundUrl.substring(0, 70)}...`);
    } else {
      place.photoUrl = FAKE;
      place.googleSearchUrl = makeGoogleSearchUrl(place.name, place.city);
      console.log('⚠️ 找不到圖片，用 fallback');
    }

    if ((i + 1) % 10 === 0) {
      fs.writeFileSync(OUTPUT_PATH, JSON.stringify(data, null, 2));
      console.log(`💾 已儲存進度（${i + 1}/62）`);
    }

    await sleep(350);
  }

  fs.writeFileSync(OUTPUT_PATH, JSON.stringify(data, null, 2));

  console.log('\n========================================');
  console.log(`✅ 完成！更新了 ${updated} 個景點的 photoUrl`);
  console.log(`⏭️  跳過（已有有效圖片）: ${skipped} 個`);
  console.log(`📁 輸出至: ${OUTPUT_PATH}`);
  console.log('========================================');
}

main().catch(console.error);