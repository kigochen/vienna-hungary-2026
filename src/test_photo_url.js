/**
 * Vienna Trip - places.json Photo URL Smoke Test
 * 測試 photoUrl 和 googleSearchUrl 格式
 */

const fs = require('fs');
const path = require('path');

let passCount = 0;
let failCount = 0;

function assert(condition, message) {
  if (condition) {
    passCount++;
    console.log(`  ✅ PASS: ${message}`);
  } else {
    failCount++;
    console.log(`  ❌ FAIL: ${message}`);
  }
}

const PLACES_JSON_PATH = path.join(__dirname, 'data', 'places.json');

console.log('=== Vienna Trip - places.json Photo URL Smoke Test ===\n');

// 1. 檔案存在
console.log('[1] 檔案存在檢查');
let fileExists = false;
try {
  fileExists = fs.existsSync(PLACES_JSON_PATH);
} catch (e) {}
assert(fileExists, `places.json 存在於 ${PLACES_JSON_PATH}`);

// 2. JSON 可正確解析
console.log('\n[2] JSON 解析檢查');
let data = null;
if (fileExists) {
  try {
    const raw = fs.readFileSync(PLACES_JSON_PATH, 'utf8');
    data = JSON.parse(raw);
    assert(true, 'JSON 格式正確，可正確解析');
  } catch (e) {
    assert(false, `JSON 解析失敗: ${e.message}`);
  }
} else {
  assert(false, '跳過 JSON 解析（檔案不存在）');
}

// 3. photoUrl 欄位檢查
console.log('\n[3] photoUrl 欄位檢查');
const PHOTO_URL_PATTERN = /^https?:\/\/.+\.(jpg|jpeg|png|webp)/i;
if (data && Array.isArray(data.places)) {
  let allValid = true;
  for (let i = 0; i < data.places.length; i++) {
    const place = data.places[i];
    const hasPhotoUrl = Object.prototype.hasOwnProperty.call(place, 'photoUrl') && typeof place.photoUrl === 'string' && place.photoUrl.length > 0;
    if (!hasPhotoUrl) {
      allValid = false;
      assert(false, `places[${i}].photoUrl 缺失或為空（${place.name}）`);
    }
  }
  if (allValid) {
    assert(true, `所有 ${data.places.length} 個景點都有 photoUrl`);
  }
} else {
  assert(false, '跳過 photoUrl 檢查（places 未正確載入）');
}

// 4. photoUrl 是有效 URL
console.log('\n[4] photoUrl URL 格式檢查');
if (data && Array.isArray(data.places)) {
  let allValid = true;
  for (let i = 0; i < data.places.length; i++) {
    const place = data.places[i];
    if (place.photoUrl) {
      // 檢查是否為 http/https URL
      const isValidHttpUrl = place.photoUrl.startsWith('http://') || place.photoUrl.startsWith('https://');
      if (!isValidHttpUrl) {
        allValid = false;
        assert(false, `places[${i}].photoUrl 不是 HTTP(S) URL（${place.name}）`);
      }
    }
  }
  if (allValid) {
    assert(true, `所有 ${data.places.length} 個 photoUrl 都是 HTTP(S) URL`);
  }
} else {
  assert(false, '跳過 photoUrl URL 格式檢查');
}

// 5. googleSearchUrl 欄位檢查
console.log('\n[5] googleSearchUrl 欄位檢查');
const GOOGLE_SEARCH_PATTERN = /^https:\/\/www\.google\.com\/search\?q=.+/i;
if (data && Array.isArray(data.places)) {
  let allValid = true;
  for (let i = 0; i < data.places.length; i++) {
    const place = data.places[i];
    const hasGoogleSearchUrl = Object.prototype.hasOwnProperty.call(place, 'googleSearchUrl') && typeof place.googleSearchUrl === 'string' && place.googleSearchUrl.length > 0;
    if (!hasGoogleSearchUrl) {
      allValid = false;
      assert(false, `places[${i}].googleSearchUrl 缺失或為空（${place.name}）`);
    }
  }
  if (allValid) {
    assert(true, `所有 ${data.places.length} 個景點都有 googleSearchUrl`);
  }
} else {
  assert(false, '跳過 googleSearchUrl 檢查');
}

// 6. googleSearchUrl 格式檢查
console.log('\n[6] googleSearchUrl 格式檢查');
if (data && Array.isArray(data.places)) {
  let allValid = true;
  for (let i = 0; i < data.places.length; i++) {
    const place = data.places[i];
    if (place.googleSearchUrl) {
      const isValidFormat = place.googleSearchUrl.startsWith('https://www.google.com/search?q=');
      if (!isValidFormat) {
        allValid = false;
        assert(false, `places[${i}].googleSearchUrl 格式錯誤（${place.name}）: ${place.googleSearchUrl}`);
      }
    }
  }
  if (allValid) {
    assert(true, `所有 ${data.places.length} 個 googleSearchUrl 格式正確`);
  }
} else {
  assert(false, '跳過 googleSearchUrl 格式檢查');
}

// 總結
console.log('\n========================================');
console.log(`測試結果：✅ ${passCount} passed | ❌ ${failCount} failed`);
if (failCount === 0) {
  console.log('🎉 所有 photo URL test 通過！');
} else {
  console.log('⚠️  有測試失敗，請檢查上述 ❌ 項目。');
}
console.log('========================================');

process.exit(failCount > 0 ? 1 : 0);
