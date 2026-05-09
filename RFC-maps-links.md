# RFC: 景點地圖 + 照片搜尋連結實作

**檔案：** `RFC-maps-links.md`
**作者：** 📐 Prime-Architect
**日期：** 2026-05-09
**狀態：** Draft

---

## 1. 現況分析

### 1.1 places.json 結構確認

| 欄位 | 現況 |
|------|------|
| `coordinates` | ✅ 已存在，所有景點都有 `[lat, lng]` 格式 |
| `googleSearchUrl` | ✅ 已存在，格式為 `https://www.google.com/search?q={name_encoded}&tbm=isch` |
| `mapsUrl` | ❌ 不存在（需要新增） |

**現有 `googleSearchUrl` 範例：**
```
https://www.google.com/search?q=St.%20Stephen%27s%20Basilica%20Budapest&tbm=isch
```
→ 已包含 `&tbm=isch`，等同於專用圖片搜尋，**格式已正確**，無需調整。

**結論：** `googleSearchUrl` 現況充足，只需要新增 `mapsUrl` 並在 UI 渲染兩者。

---

## 2. 實作策略

### 2.1 Google Maps URL 格式推薦

| 格式 | URL 範例 | 優缺點 |
|------|---------|--------|
| 名稱搜尋 | `https://www.google.com/maps/search/?api=1&query={encoded_name}` | ✅ 為人類可讀，自動定位景點<br>⚠️ 名稱若有歧義，可能定位到其他結果 |
| 座標直接定位 | `https://www.google.com/maps/place/{lat},{lng}` | ✅ 精準定位<br>⚠️ 不顯示景點名稱，使用者不知道看哪裡 |
| 座標+名稱（推薦） | `https://www.google.com/maps/search/?api=1&query={encoded_name}%40{lat},{lng}` | ✅ 名稱 + 座標，最精準 |

**📐 Architect 推薦：`query={encoded_name}%40{lat},{lng}` 格式**
（`%40` = URL encode of `@`），結合名稱關鍵詞與座標，Google Maps 會直接定位到正確位置。

### 2.2 顯示方式

| 連結類型 | UI 呈現 |
|---------|---------|
| Google Maps | 🗺️ icon 按鈕（藍色系） |
| 圖片搜尋 | 📷 icon 按鈕（amber/金色系） |

→ 兩者皆使用 **icon button**，置於景點 card 底部操作區，與 `cost`、`bestTime` 同列。

---

## 3. places.json 欄位建議

### 3.1 新增 `mapsUrl` 欄位

**Schema：**
```json
{
  "id": "bp-st-stephens",
  "name": "St. Stephen's Basilica",
  "nameZh": "聖史蒂芬教堂",
  "coordinates": [47.5008, 19.0936],
  "googleSearchUrl": "https://www.google.com/search?q=St.%20Stephen%27s%20Basilica%20Budapest&tbm=isch",
  "mapsUrl": "https://www.google.com/maps/search/?api=1&query=St.%20Stephen%27s%20Basilica%20Budapest%4047.5008%2C19.0936"
}
```

**注意：** `googleSearchUrl` 不變（已是 `tbm=isch` 格式）。

### 3.2 未來自動化建議（可後期實作）

若 `mapsUrl` 未手動填寫，index.html 的 JS 可提供 fallback：
```javascript
function getMapsUrl(place) {
  if (place.mapsUrl) return place.mapsUrl;
  const encodedName = encodeURIComponent(place.name + ' ' + place.city);
  const [lat, lng] = place.coordinates;
  return `https://www.google.com/maps/search/?api=1&query=${encodedName}@${lat},${lng}`;
}
```
→ 降低必須手動填寫全部 59 筆資料的成本。

---

## 4. index.html 修改計劃

### 4.1 Card 結構變更

**現況（card 底部）：**
```html
<div class="mt-3 pt-3 border-t border-amber/10 flex justify-between text-xs text-gray-400">
  <span>💰 ${p.cost}</span>
  <span>🕐 ${p.bestTime}</span>
</div>
```

**修改後：**
```html
<div class="mt-3 pt-3 border-t border-amber/10 flex justify-between items-center text-xs text-gray-400">
  <div class="flex gap-3">
    <span>💰 ${p.cost</span>
    <span>🕐 ${p.bestTime}</span>
  </div>
  <div class="flex gap-2">
    <!-- Maps -->
    <a href="${p.mapsUrl || fallbackMapsUrl(p)}" target="_blank" rel="noopener"
       class="flex items-center gap-1 px-2 py-1 rounded-lg bg-blue-500/20 text-blue-400 hover:bg-blue-500/30 transition text-xs"
       title="在 Google Maps 開啟">
      <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
      地圖
    </a>
    <!-- Image Search -->
    <a href="${p.googleSearchUrl}" target="_blank" rel="noopener"
       class="flex items-center gap-1 px-2 py-1 rounded-lg bg-amber/20 text-amber hover:bg-amber/30 transition text-xs"
       title="搜尋照片">
      <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg>
      照片
    </a>
  </div>
</div>
```

### 4.2 Map Popup 增強

**現況（Leaflet popup）：**
```javascript
.bindPopup(`<b>${p.nameZh}</b><br>${p.city}<br>⭐ ${p.rating}`)
```

**修改後：**
```javascript
const mapsLink = p.mapsUrl || fallbackMapsUrl(p);
.bindPopup(`
  <b>${p.nameZh}</b><br>
  ${p.city} · ⭐ ${p.rating}<br>
  <a href="${mapsLink}" target="_blank" rel="noopener" style="color:#d4a017">🗺️ 在 Google Maps 開啟</a>
`)
```

### 4.3 全域 helper 函式（新增）

```javascript
function fallbackMapsUrl(place) {
  const encodedName = encodeURIComponent(place.name + ' ' + place.city);
  const [lat, lng] = place.coordinates;
  return `https://www.google.com/maps/search/?api=1&query=${encodedName}@${lat},${lng}`;
}
```

---

## 5. 測試計劃

### 5.1 單一景點驗證（手動 Smoke Test）

| # | 測試項目 | 預期結果 |
|---|---------|---------|
| T1 | 點擊「地圖」按鈕 | 開啟新分頁，Google Maps 正確定位景點 |
| T2 | 點擊「照片」按鈕 | 開啟新分頁，Google 圖片搜尋顯示景點相關圖片 |
| T3 | Map popup 點擊「在 Google Maps 開啟」 | 開啟新分頁，正確顯示該景點位置 |
| T4 | `mapsUrl` 為空時（fallback） | 使用 `fallbackMapsUrl()` 正確產生 URL |
| T5 | 所有外連結皆 `target="_blank"` | 新分頁開啟，不流失當前頁面 |

### 5.2 跨瀏覽器驗證

- Desktop Chrome / Firefox / Safari
- Mobile Safari (iOS) / Chrome (Android)
- 確認 `target="_blank"` + `rel="noopener"` 安全性

### 5.3 資料完整性檢查

```bash
# 確認所有 places 都有 coordinates
jq '.places[] | select(.coordinates == null)' places.json | wc -l
# 預期：0

# 確認 googleSearchUrl 都有 tbm=isch
jq '.places[] | select(.googleSearchUrl | contains("tbm=isch") | not)' places.json | wc -l
# 預期：0
```

---

## 6. 實作順序

```
Step 1: 更新 places.json（新增 mapsUrl 欄位）
        → 可用 script 批次產生（見下方的批次產生指令）

Step 2: 更新 index.html（新增 helper + UI 按鈕）

Step 3: 更新 Leaflet popup（新增 maps 連結）

Step 4: 本地 smoke test（T1-T5）

Step 5: commit + push
```

### 批次產生 mapsUrl（可選）

```bash
cd /home/node/.openclaw/workspace/vienna-trip
node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('places.json','utf8'));
data.places.forEach(p => {
  const encodedName = encodeURIComponent(p.name + ' ' + p.city);
  const [lat, lng] = p.coordinates;
  p.mapsUrl = \`https://www.google.com/maps/search/?api=1&query=\${encodedName}@\${lat},\${lng}\`;
});
fs.writeFileSync('places.json', JSON.stringify(data, null, 2));
console.log('Done');
"
```

---

## 7. 風險與限制

| 風險 | 等級 | 緩解 |
|------|------|------|
| 手動填寫 59 筆 mapsUrl 費時 | 🟡 中 | 使用 Step 6 的批次 script 自動化 |
| Google Maps URL 可能過期或格式變更 | 🟢 低 | 使用 `search/?api=1` 而非 `place/` 格式，相對穩定 |
| `googleSearchUrl` 若已有 `tbm=isch` 就不需動 | 🟢 低 | 已確認所有 URL 格式正確 |

---

## 8. 決策點（⭐ Decision Gate）

需 Kigo 裁示以下事項：

1. **按鈕顏色偏好：** 藍色（地圖）+ 金色（照片）是否滿意？或希望統一風格？
2. **Fallback 機制：** 若 `mapsUrl` 為空，是否接受 JS 自動產生？（可省去手動填寫）
3. **實作順序：** 是否同意依「實作順序」章節執行？
