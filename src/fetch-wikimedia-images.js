/**
 * fetch-wikimedia-images.js
 * 使用 Wikimedia Commons API 為 62 個景點抓取真實圖片
 * 更新 places.json：新增 photoUrl + googleSearchUrl
 */

const fs = require('fs');
const https = require('https');

const PLACES_JSON_PATH = '/home/node/.openclaw/workspace/vienna-trip/src/places.json';
const OUTPUT_PATH = '/home/node/.openclaw/workspace/vienna-trip/src/places.json';

// 延遲函式
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// 查詢 Wikimedia Commons API
function searchWikimediaImage(query) {
  return new Promise((resolve, reject) => {
    const encodedQuery = encodeURIComponent(query + ' site:commons.wikimedia.org');
    const url = `https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=${encodedQuery}&srnamespace=6&srlimit=5&format=json&origin=*`;

    https.get(url, { headers: { 'User-Agent': 'ViennaTripBot/1.0' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          const results = json.query?.search || [];
          if (results.length > 0) {
            // 取得第一個結果的標題，然後獲取實際 URL
            const title = results[0].title.replace(/ /g, '_');
            resolve(title);
          } else {
            resolve(null);
          }
        } catch (e) {
          resolve(null);
        }
      });
    }).on('error', () => resolve(null));
  });
}

// 從檔案標題取得實際圖片 URL
function getImageInfo(title) {
  return new Promise((resolve) => {
    const encodedTitle = encodeURIComponent(title);
    const url = `https://commons.wikimedia.org/w/api.php?action=query&titles=File:${encodedTitle}&prop=imageinfo&iiprop=url&format=json&origin=*`;

    https.get(url, { headers: { 'User-Agent': 'ViennaTripBot/1.0' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          const pages = json.query?.pages || {};
          for (const pageId in pages) {
            const imageinfo = pages[pageId].imageinfo;
            if (imageinfo && imageinfo[0]) {
              resolve(imageinfo[0].url);
              return;
            }
          }
          resolve(null);
        } catch (e) {
          resolve(null);
        }
      });
    }).on('error', () => resolve(null));
  });
}

// 為景點建 googleSearchUrl
function makeGoogleSearchUrl(name, city) {
  const q = encodeURIComponent(`${name} ${city}`);
  return `https://www.google.com/search?q=${q}&tbm=isch`;
}

async function main() {
  console.log('⚡ 讀取 places.json...');
  const raw = fs.readFileSync(PLACES_JSON_PATH, 'utf8');
  const data = JSON.parse(raw);

  let updated = 0;
  let skipped = 0;

  for (let i = 0; i < data.places.length; i++) {
    const place = data.places[i];
    const searchQuery = `${place.name} ${place.city}`;

    // 顯示進度
    process.stdout.write(`[${i + 1}/62] ${place.nameZh} (${place.city})... `);

    // 檢查是否已有有效的 photoUrl（非假圖）
    const FAKE = 'https://images.unsplash.com/photo-1508009603885-50cf7c579365';
    if (place.photoUrl && place.photoUrl !== FAKE && place.photoUrl.startsWith('http')) {
      // 已有有效 URL，加上 googleSearchUrl
      place.googleSearchUrl = makeGoogleSearchUrl(place.name, place.city);
      skipped++;
      console.log('✅ 已有有效圖片，跳過');
      continue;
    }

    try {
      // 搜尋圖片
      const title = await searchWikimediaImage(searchQuery);

      if (title) {
        await sleep(200); // 避免觸發 rate limit
        const imageUrl = await getImageInfo(title);

        if (imageUrl) {
          place.photoUrl = imageUrl;
          place.googleSearchUrl = makeGoogleSearchUrl(place.name, place.city);
          updated++;
          console.log(`✅ ${imageUrl.substring(0, 60)}...`);
        } else {
          place.photoUrl = FAKE;
          place.googleSearchUrl = makeGoogleSearchUrl(place.name, place.city);
          console.log('⚠️ 找不到圖片，用 fallback');
        }
      } else {
        place.photoUrl = FAKE;
        place.googleSearchUrl = makeGoogleSearchUrl(place.name, place.city);
        console.log('⚠️ 搜尋無結果，用 fallback');
      }
    } catch (e) {
      place.photoUrl = FAKE;
      place.googleSearchUrl = makeGoogleSearchUrl(place.name, place.city);
      console.log(`⚠️ 錯誤: ${e.message}`);
    }

    // 每 10 個景點存一次進度
    if ((i + 1) % 10 === 0) {
      fs.writeFileSync(OUTPUT_PATH, JSON.stringify(data, null, 2, 128));
      console.log(`💾 已儲存進度（${i + 1}/62）`);
    }

    // 額外延遲避免 Wikimedia API 限制
    await sleep(300);
  }

  // 最終儲存
  fs.writeFileSync(OUTPUT_PATH, JSON.stringify(data, null, 2, 128));

  console.log('\n========================================');
  console.log(`✅ 完成！更新了 ${updated} 個景點的 photoUrl`);
  console.log(`⏭️  跳過（已有有效圖片）: ${skipped} 個`);
  console.log(`📁 輸出至: ${OUTPUT_PATH}`);
  console.log('========================================');
}

main().catch(console.error);