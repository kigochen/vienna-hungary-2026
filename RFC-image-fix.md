# RFC: 修補「所有景點顯示同一張照片」Bug

**文件狀態：** ✅ 已完成  
**產出日期：** 2026-05-09  
**Author：** 📐 Prime-Architect  
**適用網站：** https://kigochen.github.io/vienna-hungary-2026/#places  

---

## 1. Bug 根因分析

### 1.1 症狀
網站上所有景點卡片顯示的照片完全相同（都是同一張 Unsplash 照片）。

### 1.2 根因定位

**地點：**
- `index.html` 第 158 行（`renderPlaces()` 函式）：
  ```html
  <img src="${p.photos[0]}" alt="${p.nameZh}" ... />
  ```
- `places.json` — 每個景點的 `photos[]` 陣列

**分析結果：**

| 層面 | 狀態 | 說明 |
|------|------|------|
| `index.html` 顯示邏輯 | ✅ 正確 | `p.photos[0]` 取第一張，正確 |
| `places.json` 資料 | ❌ 錯誤 | **所有 50 個景點使用完全相同的 placeholder URL** |

**問題細節：**
places.json 中，每個景點的 `photos[]` 陣列內容都是：
```json
"photos": [
  "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=800"
]
```

這是一個未替換的假資料（Dummy Data）。所有 50 個景點從未分得真實圖片。

### 1.3 受影響範圍

- **受影響景點總數：** 50 個
  - Budapest: 24 個
  - Vienna: 17 個
  - 其他匈牙利城市: 9 個
- **佔景點總數：** 100%（全部受影響）

---

## 2. 修正策略

### 選項 A：每個景點手動找圖
- **人力成本：** 高（約 3-5 小時）
- **準確度：** 高
- **缺點：** 瑣碎重複，易疲勞出錯
- **適用場景：** 小規模、已知道準確圖源

### 選項 B：批次 web_search 搜圖 + 自動替換（✅ 推薦）
- **人力成本：** 低（交由 subagent 批次處理）
- **準確度：** 中高（需人工抽檢）
- **優點：** 可大規模執行、記錄圖源 URL
- **流程：**
  1. 對每個景點執行 `web_search` 查詢真實圖片
  2. 從搜尋結果取 Wikimedia Commons 圖片 URL
  3. 批次更新 `places.json`
  4. 人工抽檢確認

### 選項 C：使用統一边片
- **人力成本：** 極低
- **缺點：** 所有景點仍是相同圖片，失去景點特異性
- **結論：** ❌ 不接受（等於沒修）

### 最終推薦：選項 B（批次搜圖 + 半自動更新）

---

## 3. 實作計劃

### Step 1：確認 places.json 結構（✅ 已完成）
- 照片欄位：`photos[]`（陣列，第一張為顯示用）
- 將新增：`photoUrl`（純量，用於直接引用）與 `googleSearchUrl`

### Step 2：批次 web_search 搜圖（交由 Coder 執行）
**圖源優先順序：**
1. **Wikimedia Commons** — 免費、開放授權、可穩定訪問
   - 格式：`https://commons.wikimedia.org/wiki/Special:FilePath/`
   - 搜尋關鍵字：`site:commons.wikimedia.org [景點名] Budapest`
2. **Wikipedia** — CC-BY-SA 授權，可引用
   - 格式：`https://en.wikipedia.org/wiki/[景點名]`
3. **其他旅遊網站** — 僅當前兩者都找不到時使用

**搜圖關鍵字策略：**
```
"[景點英文名]" Budapest OR Vienna wikipedia
"[景點英文名]" wikimedia commons
```

### Step 3：更新 places.json
將每個景點的 `photos[0]` 替換為真實 Wikimedia Commons URL，並新增：
```json
{
  "photos": ["https://commons.wikimedia.org/wiki/Special:FilePath/..."],
  "photoUrl": "https://commons.wikimedia.org/wiki/Special:FilePath/...",
  "googleSearchUrl": "https://www.google.com/search?q=[景點名]+Budapest+photo"
}
```

### Step 4：修正 index.html（如需要）
目前邏輯無需修改。如需強化，考慮：
- 圖片載入失敗時的 fallback 機制
- 新增 `photoUrl` 純量欄位作為主要顯示圖片

### Step 5：測試驗證
- 本地跑 `python3 -m http.server 8000` 確認顯示正常
- 抽檢 10 個景點圖片是否正確對應

---

## 4. 景點清單（共 50 個）

### Budapest（24 個）
| ID | 英文名 | 中文名 |
|----|--------|--------|
| bp-st-stephens | St. Stephen's Basilica | 聖史蒂芬教堂 |
| bp-memento-park | Memento Park | 紀念品公園 |
| bp-rudas-bath | Rudas Bath | 魯達斯溫泉 |
| bp-liberty-bridge | Liberty Bridge | 自由橋 |
| bp-kolodko | Kolodko Small Statues | 迷你雕像尋寶 |
| bp-library | Metropolitan Ervin Szabó Library | 薩博都會圖書館 |
| bp-ferris-wheel | Budapest Ferris Wheel Park | 摩天輪公園 |
| bp-ruin-pubs | Ruin Pubs - Szimpla Kert | 廢墟酒吧 |
| bp-cave-church | Gellért Hill Cave Church | 蓋勒特丘洞穴教堂 |
| bp-metro1 | Metro Line 1 | 地鐵一號線 |
| bp-vajdahunyad | Vajdahunyad Castle | Vajdahunyad城堡 |
| bp-hospital-rock | Hospital in the Rock | 岩中醫院 |
| bp-castle-caves | Budapest Castle Caves | 布達城堡洞穴 |
| bp-margaret-island | Margaret Island | 瑪格麗特島 |
| bp-synagogue | Dohány Street Synagogue | 多翰街猶太教堂 |
| bp-street-art | Jewish Quarter Street Art | 猶太區街頭藝術 |
| bp-szechenyi | Széchenyi Baths | 塞切尼溫泉 |
| bp-buda-castle | Buda Castle | 布達城堡 |
| bp-a38 | A38 Ship | A38船 |
| bp-new-york-cafe | New York Café | 新紐約咖啡館 |
| bp-house-terror | House of Terror | 恐怖之屋博物館 |
| bp-chairlift | Zugliget Chairlift | 瓊格萊特纜車 |
| bp-danube-cruise | Danube Cruises | 多瑙河游船 |
| bp-city-park | City Park | 城市公園 |
| bp-fishermans-bastion | Fisherman's Bastion | 漁人堡 |
| bp-central-market | Central Market Hall | 中央市場 |
| bp-karolyi-garden | Károlyi Garden | 卡羅利花園 |
| bp-jewish-museum | Hungarian Jewish Museum | 匈牙利猶太博物館 |

### Vienna（17 個）
| ID | 英文名 | 中文名 |
|----|--------|--------|
| vn-st-stephens | St. Stephen's Cathedral | 聖斯特凡大教堂 |
| vn-state-opera | Vienna State Opera | 維也納國家歌劇院 |
| vn-schonbrunn | Schönbrunn Palace | 美泉宮 |
| vn-hofburg | Hofburg Palace | 霍夫堡皇宮 |
| vn-wachau-valley | Wachau Valley | 瓦豪河谷 |
| vn-albertina-modern | Albertina Modern | 阿爾貝蒂娜現代美術館 |
| vn-naschmarkt | Naschmarkt | 納旭市場 |
| vn-prater | Prater Park | 普拉特公園 |
| vn-cafe-central | Café Central | 中央咖啡館 |
| vn-hundertwasserhaus | Hundertwasserhaus | 百水公寓 |
| vn-karlskirche | Karlskirche | 卡默萊特教堂 |
| vn-grinzing | Grinzing Heuriger | 格林沁小酒館區 |
| vn-belvedere | Belvedere Palace | 貝維德雷宮 |
| vn-botanical-garden | Vienna University Botanical Garden | 維也納大學植物園 |
| vn-zentralfriedhof | Zentralfriedhof | 中央公墓 |
| vn-palais-ferstel | Palais Ferstel | 費斯特爾宮 |
| vn-augarten | Augarten Porcelain Factory | Augarten瓷器工廠 |
| vn-tuerkenschanzpark | Türkenschanzpark | 圖爾肯斯坎茲公園 |
| vn-fasanviertel | Fasanviertel | 法桑維爾特社區 |

### 其他匈牙利城市（9 個）
| ID | 英文名 | 中文名 | 城市 |
|----|--------|--------|------|
| db-reformed-college | Debrecen Reformed College | 德布勒森改革宗教會學院 | Debrecen |
| db-deri-museum | Déri Museum | 德瑞博物館 | Debrecen |
| db-great-forest | Great Forest Park | 大森林公園 | Debrecen |
| sg-votive-church | Szeged Votive Church | 塞格德大教堂 | Szeged |
| sg-napfenyfurdo | Napfényfürdő Aquapolis | 日光水療水上樂園 | Szeged |
| sg-reok-palace | Reök Palace | 雷奧克宮殿 | Szeged |
| pc-cathedral | Pécs Cathedral | 佩奇大教堂 | Pécs |
| pc-necropolis | Early Christian Necropolis | 早期基督教墓窟 | Pécs |
| pc-zsolnay | Zsolnay Cultural Quarter | Zsolnay文化區 | Pécs |
| pc-mecsek | Mecsek Hills | 梅切克山丘 | Pécs |
| lb-badacsony | Badacsony | 巴達克尼山 | Lake Balaton |
| lb-keszthely | Festetics-kastály | 費斯提提茲宮 | Lake Balaton |
| lb-tihany | Tihany Abbey | 蒂豪尼修道院 | Lake Balaton |
| gy-basilica | Győr Basilica | 艾爾大教堂 | Győr |
| gy-bishops-castle | Bishop's Castle | 主教城堡 | Győr |

---

## 5. 風險評估

| 風險 | 等級 | 緩解措施 |
|------|------|---------|
| 網站無法訪問 Wikimedia | 低 | 同時爬取 Wikipedia 圖片 |
| 某些小眾景點找不到圖 | 中 | 該景點保留 fallback 圖片 |
| 圖片 URL 失效 | 低 | 使用 `onerror` fallback 機制 |
| 部署後圖片載入過慢 | 中 | 考慮使用 `loading="lazy"` + 預覽圖 |

---

## 6. 下一步行動

| 負責人 | 動作 |
|--------|------|
| 📐 Prime-Architect（本檔案） | ✅ RFC 完成 |
| ⚡ Implementation-Coder | 執行批次 web_search + 更新 places.json |
| 🔍 Lens | 審查 places.json 更新結果 |
| 🚥 Ops-Tester | 本地測試驗證 |

**RFC 狀態：通過，可進入實作階段。** 📐