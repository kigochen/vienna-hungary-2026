/**
 * Vienna Trip - places.json Smoke Test
 * 測試 places.json 的結構是否符合預期
 */

const fs = require('fs');
const path = require('path');

// 測試結果計數
let passCount = 0;
let failCount = 0;

// 斷言函式
function assert(condition, message) {
  if (condition) {
    passCount++;
    console.log(`  ✅ PASS: ${message}`);
  } else {
    failCount++;
    console.log(`  ❌ FAIL: ${message}`);
  }
}

// places.json 路徑
const PLACES_JSON_PATH = path.join(__dirname, 'data', 'places.json');

console.log('=== Vienna Trip - places.json Smoke Test ===\n');

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

// 3. 必要欄位檢查
console.log('\n[3] 必要欄位檢查');
const requiredFields = ['version', 'tripInfo', 'places', 'itinerary', 'transport', 'budget', 'food', 'todo'];
if (data) {
  for (const field of requiredFields) {
    assert(Object.prototype.hasOwnProperty.call(data, field), `必填欄位 "${field}" 存在`);
  }
} else {
  for (const field of requiredFields) {
    assert(false, `跳過欄位 "${field}"（資料載入失敗）`);
  }
}

// 4. places 是非空陣列
console.log('\n[4] places 陣列檢查');
if (data) {
  assert(Array.isArray(data.places), 'places 是陣列');
  assert(data.places.length > 0, 'places 非空陣列');
} else {
  assert(false, '跳過 places 檢查（資料未載入）');
}

// 5. 前5個景點結構檢查
console.log('\n[5] 前5個景點欄位檢查');
const requiredPlaceFields = ['id', 'name', 'nameZh', 'city', 'category', 'coordinates', 'rating'];
if (data && Array.isArray(data.places) && data.places.length >= 5) {
  for (let i = 0; i < 5; i++) {
    const place = data.places[i];
    for (const field of requiredPlaceFields) {
      assert(Object.prototype.hasOwnProperty.call(place, field), `places[${i}].${field} 存在`);
    }
  }
} else if (data && data.places.length > 0) {
  const limit = Math.min(5, data.places.length);
  for (let i = 0; i < limit; i++) {
    const place = data.places[i];
    for (const field of requiredPlaceFields) {
      assert(Object.prototype.hasOwnProperty.call(place, field), `places[${i}].${field} 存在`);
    }
  }
  if (data.places.length < 5) {
    assert(false, `景點總數 ${data.places.length} < 5，跳過其餘檢查`);
  }
} else {
  for (const field of requiredPlaceFields) {
    assert(false, `跳過 places[0~4] 檢查（places 未正確載入）`);
  }
}

// 6. 所有 category 必須是有效值
console.log('\n[6] category 合法性檢查');
const VALID_CATEGORIES = ['heritage', 'nature', 'food', 'experience', 'museum', 'thermal', 'viewpoint'];
if (data && Array.isArray(data.places)) {
  let allValid = true;
  for (let i = 0; i < data.places.length; i++) {
    const cat = data.places[i].category;
    if (!VALID_CATEGORIES.includes(cat)) {
      allValid = false;
      assert(false, `places[${i}].category="${cat}" 不在允許清單內`);
    }
  }
  if (allValid) {
    assert(true, `所有 ${data.places.length} 個景點的 category 都是有效值`);
  }
} else {
  assert(false, '跳過 category 檢查（places 未正確載入）');
}

// 7. 所有 coordinates 格式檢查
console.log('\n[7] coordinates 格式檢查');
if (data && Array.isArray(data.places)) {
  let allValid = true;
  for (let i = 0; i < data.places.length; i++) {
    const coords = data.places[i].coordinates;
    const isArray = Array.isArray(coords) && coords.length === 2;
    const latOk = isArray && typeof coords[0] === 'number' && coords[0] >= -90 && coords[0] <= 90;
    const lngOk = isArray && typeof coords[1] === 'number' && coords[1] >= -180 && coords[1] <= 180;
    if (!isArray || !latOk || !lngOk) {
      allValid = false;
      const lat = isArray ? coords[0] : 'N/A';
      const lng = isArray ? coords[1] : 'N/A';
      assert(false, `places[${i}].coordinates=[${lat}, ${lng}] 無效（需為 [lat(-90~90), lng(-180~180)]）`);
    }
  }
  if (allValid) {
    assert(true, `所有 ${data.places.length} 個景點的 coordinates 格式正確`);
  }
} else {
  assert(false, '跳過 coordinates 檢查（places 未正確載入）');
}

// 8. rating 必須是 0-5 的數字
console.log('\n[8] rating 範圍檢查');
if (data && Array.isArray(data.places)) {
  let allValid = true;
  for (let i = 0; i < data.places.length; i++) {
    const rating = data.places[i].rating;
    if (typeof rating !== 'number' || rating < 0 || rating > 5) {
      allValid = false;
      assert(false, `places[${i}].rating=${rating} 無效（需為 0-5 的數字）`);
    }
  }
  if (allValid) {
    assert(true, `所有 ${data.places.length} 個景點的 rating 都在 0-5 範圍內`);
  }
} else {
  assert(false, '跳過 rating 檢查（places 未正確載入）');
}

// 9. itinerary 結構檢查
console.log('\n[9] itinerary 結構檢查');
if (data && Array.isArray(data.itinerary)) {
  assert(true, 'itinerary 是陣列');
  let allValid = true;
  for (let i = 0; i < data.itinerary.length; i++) {
    const day = data.itinerary[i];
    const hasRequired = (
      Object.prototype.hasOwnProperty.call(day, 'day') &&
      Object.prototype.hasOwnProperty.call(day, 'date') &&
      Object.prototype.hasOwnProperty.call(day, 'theme') &&
      Object.prototype.hasOwnProperty.call(day, 'places')
    );
    if (!hasRequired) {
      allValid = false;
      assert(false, `itinerary[${i}] 缺少必要欄位（需有 day, date, theme, places）`);
    }
  }
  if (allValid) {
    assert(true, `所有 ${data.itinerary.length} 個 itinerary 項目結構正確`);
  }
} else {
  assert(false, '跳過 itinerary 檢查（不是陣列或未定義）');
}

// 10. 景點必須涵蓋 Budapest 和 Vienna
console.log('\n[10] 城市覆蓋檢查（BUDAPEST & VIENNA）');
if (data && Array.isArray(data.places)) {
  const cities = data.places.map(p => p.city);
  const hasBudapest = cities.some(c => c.toLowerCase().includes('budapest'));
  const hasVienna = cities.some(c => c.toLowerCase().includes('vienna'));
  assert(hasBudapest, '景點涵蓋 Budapest');
  assert(hasVienna, '景點涵蓋 Vienna');
} else {
  assert(false, '跳過城市檢查（places 未正確載入）');
}

// 總結
console.log('\n========================================');
console.log(`測試結果：✅ ${passCount} passed | ❌ ${failCount} failed`);
if (failCount === 0) {
  console.log('🎉 所有 smoke test 通過！');
} else {
  console.log('⚠️  有測試失敗，請檢查上述 ❌ 項目。');
}
console.log('========================================');

process.exit(failCount > 0 ? 1 : 0);