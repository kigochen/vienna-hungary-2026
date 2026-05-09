/**
 * Vienna Trip - places.json Full Validation Test (Updated for photoUrl + googleSearchUrl)
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

const PLACES_JSON_PATH = path.join(__dirname, 'places.json');

console.log('=== Vienna Trip - places.json Full Validation Test ===\n');

// 1. File exists
console.log('[1] 檔案存在檢查');
let fileExists = false;
try {
  fileExists = fs.existsSync(PLACES_JSON_PATH);
} catch (e) {}
assert(fileExists, `places.json 存在於 ${PLACES_JSON_PATH}`);

// 2. JSON parseable
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

// 3. Required top-level fields
console.log('\n[3] 必填欄位檢查');
const requiredFields = ['version', 'tripInfo', 'places', 'itinerary', 'transport', 'budget', 'food', 'todo'];
if (data) {
  for (const field of requiredFields) {
    assert(Object.prototype.hasOwnProperty.call(data, field), `必填欄位 "${field}" 存在`);
  }
}

// 4. places array
console.log('\n[4] places 陣列檢查');
if (data) {
  assert(Array.isArray(data.places), 'places 是陣列');
  assert(data.places.length > 0, 'places 非空陣列');
  assert(data.places.length === 62, `places 有 62 個景點（實際: ${data.places.length}）`);
} else {
  assert(false, '跳過 places 檢查（資料未載入）');
}

// 5. New fields: photoUrl and googleSearchUrl for ALL 62 places
console.log('\n[5] photoUrl 欄位檢查（62 個景點）');
const FAKE_UNSPLASH = 'https://images.unsplash.com/photo-1508009603885-50cf7c579365';
if (data && Array.isArray(data.places)) {
  let allHavePhotoUrl = true;
  let allRealPhotoUrls = true;
  let updatedCount = 0;
  for (let i = 0; i < data.places.length; i++) {
    const place = data.places[i];
    const hasPhotoUrl = Object.prototype.hasOwnProperty.call(place, 'photoUrl') && typeof place.photoUrl === 'string' && place.photoUrl.length > 0;
    if (!hasPhotoUrl) {
      allHavePhotoUrl = false;
      assert(false, `places[${i}].photoUrl 缺失（${place.nameZh}）`);
    }
    // Check it's not the fake Unsplash placeholder
    if (hasPhotoUrl && place.photoUrl === FAKE_UNSPLASH) {
      allRealPhotoUrls = false;
      updatedCount++;
    }
  }
  if (allHavePhotoUrl && allRealPhotoUrls) {
    assert(true, `所有 62 個景點都有真實的 photoUrl（非假圖）`);
  } else if (allHavePhotoUrl && !allRealPhotoUrls) {
    assert(false, `有 ${updatedCount} 個景點仍使用假 Unsplash 圖片`);
  }
} else {
  assert(false, '跳過 photoUrl 檢查（places 未正確載入）');
}

// 6. googleSearchUrl with encodeURIComponent
console.log('\n[6] googleSearchUrl 欄位檢查（62 個景點）');
if (data && Array.isArray(data.places)) {
  let allHaveGoogleSearchUrl = true;
  let allEncodedCorrectly = true;
  for (let i = 0; i < data.places.length; i++) {
    const place = data.places[i];
    const hasGoogleSearchUrl = Object.prototype.hasOwnProperty.call(place, 'googleSearchUrl') && typeof place.googleSearchUrl === 'string' && place.googleSearchUrl.length > 0;
    if (!hasGoogleSearchUrl) {
      allHaveGoogleSearchUrl = false;
      assert(false, `places[${i}].googleSearchUrl 缺失（${place.nameZh}）`);
      continue;
    }
    // Check that the URL contains properly encoded query
    const url = place.googleSearchUrl;
    const hasQParam = url.includes('?q=') || url.includes('&q=');
    if (!hasQParam) {
      allEncodedCorrectly = false;
      assert(false, `places[${i}].googleSearchUrl 格式錯誤（${place.nameZh}）: ${url}`);
    }
    // Check for literal spaces (unencoded)
    if (url.includes('?q=') && url.includes(' ')) {
      allEncodedCorrectly = false;
      assert(false, `places[${i}].googleSearchUrl 包含未編碼的空格（${place.nameZh}）`);
    }
  }
  if (allHaveGoogleSearchUrl && allEncodedCorrectly) {
    assert(true, `所有 62 個景點都有正確格式的 googleSearchUrl`);
  }
} else {
  assert(false, '跳過 googleSearchUrl 檢查（places 未正確載入）');
}

// 7. Valid categories
console.log('\n[7] category 合法性檢查');
const VALID_CATEGORIES = ['heritage', 'nature', 'food', 'experience', 'museum', 'thermal', 'viewpoint'];
if (data && Array.isArray(data.places)) {
  let allValid = true;
  for (let i = 0; i < data.places.length; i++) {
    if (!VALID_CATEGORIES.includes(data.places[i].category)) {
      allValid = false;
      assert(false, `places[${i}].category="${data.places[i].category}" 不在允許清單內`);
    }
  }
  if (allValid) {
    assert(true, `所有 ${data.places.length} 個景點的 category 都是有效值`);
  }
}

// 8. Valid coordinates
console.log('\n[8] coordinates 格式檢查');
if (data && Array.isArray(data.places)) {
  let allValid = true;
  for (let i = 0; i < data.places.length; i++) {
    const coords = data.places[i].coordinates;
    const isArray = Array.isArray(coords) && coords.length === 2;
    const latOk = isArray && typeof coords[0] === 'number' && coords[0] >= -90 && coords[0] <= 90;
    const lngOk = isArray && typeof coords[1] === 'number' && coords[1] >= -180 && coords[1] <= 180;
    if (!isArray || !latOk || !lngOk) {
      allValid = false;
    }
  }
  if (allValid) {
    assert(true, `所有 ${data.places.length} 個景點的 coordinates 格式正確`);
  }
}

// 9. Rating range
console.log('\n[9] rating 範圍檢查');
if (data && Array.isArray(data.places)) {
  let allValid = true;
  for (let i = 0; i < data.places.length; i++) {
    const rating = data.places[i].rating;
    if (typeof rating !== 'number' || rating < 0 || rating > 5) {
      allValid = false;
    }
  }
  if (allValid) {
    assert(true, `所有 ${data.places.length} 個景點的 rating 都在 0-5 範圍內`);
  }
}

// Summary
console.log('\n========================================');
console.log(`測試結果：✅ ${passCount} passed | ❌ ${failCount} failed`);
if (failCount === 0) {
  console.log('🎉 所有測試通過！');
} else {
  console.log('⚠️  有測試失敗，請檢查上述 ❌ 項目。');
}
console.log('========================================');

process.exit(failCount > 0 ? 1 : 0);