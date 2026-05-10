# RFC: places.json 景點照片 + 中文名稱修正計畫（v2.0）

**日期:** 2026-05-09
**版本:** v2.0（納入 Lens 審查發現）
**提出者:** Prime-Architect
**狀態:** Draft → Pending Kigo Approval

---

## 0. 更新日誌（v2.0）

| 日期 | 版本 | 變更內容 |
|------|------|---------|
| 2026-05-09 | v1.0 | 初版：3 個 photoUrl 錯誤 + 中文名稱比對 |
| 2026-05-09 | v2.0 | Lens 審查後：新增 `gy-basilica` P0、發現 `photos[]` 佔位符全部 74 筆為同一 Unsplash URL、重估工作量 |

---

## 1. 現況分析（Lens 審查後更新）

### 1.1 問題分類

| 問題類型 | 數量 | 說明 |
|---------|------|------|
| `photoUrl` 錯誤 | 4 個 | bp-street-art(PDF), gy-bishops-castle(徽章), pc-mecsek(基地台), **gy-basilica(GIF)** |
| `photos[]` 佔位符 | **74 個（全部）** | 全部為同一個 Unsplash URL (`photo-1508009603885-50cf7c579365?w=800`) |
| 中文名稱需比對 | 74 個 | 以 Google Map 台灣繁體為準 |

### 1.2 P0 問題清單（photoUrl 錯誤，4 個）

| ID | 名稱 | 問題類型 | 說明 |
|-----|------|---------|------|
| `bp-street-art` | 猶太區街頭藝術 | PDF 檔案 | URL 指向 Jewish Encyclopedia PDF，並非景點照片 |
| `gy-bishops-castle` | 主教城堡 | 徽章圖示 | URL 指向 Coat of Arms，並非城堡實景 |
| `pc-mecsek` | 梅切克山丘 | 基地台照片 | URL 指向手機訊號塔，而非山丘風景 |
| `gy-basilica` | ~~Basilica~~ | **GIF 檔案（漏檢）** | URL 包含 `.gif` 格式，可能為錯誤檔案 |

### 1.3 P1 問題清單（`photos[]` 佔位符，全部 74 個）

**重大發現：** Lens 審查發現全部 74 筆 `photos[]` 都使用**同一個 Unsplash 佔位符 URL**：
```
https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=800
```

這不是真實景點照片，是通用佔位圖。

**實作策略：**
- 策略 A（首選）：若該景點的 `photoUrl` 為正確 Wikimedia URL，則直接複製到 `photos[0]`
- 策略 B（備選）：對每個景點執行 `web_search` 批次搜尋新的 Wikimedia 圖片

### 1.4 P2 問題：`vn-fasanviertel` 非景點

| ID | 名稱 | 問題 | 說明 |
|-----|------|------|------|
| `vn-fasanviertel` | 法桑維爾特社區 | 非知名景點 | URL 指向普通街道建築照片，非旅遊景點 |

建議：確認是否為正確景點，或以真實景點替換。

### 1.5 P3 問題：中文名稱比對（74 個）

全部 74 個景點需要與 Google Map 台灣繁體中文名稱比對，更新 `nameZh` 欄位。

---

## 2. 實作策略（v2.0 更新）

### Phase 1: photoUrl 錯誤修正（4 個 P0）

**目標：** 修復 4 個明確錯誤的 `photoUrl`

| 步驟 | 動作 |
|------|------|
| 1.1 | 備份：`cp places.json places.json.backup.$(date +%Y%m%d)` |
| 1.2 | 對 `bp-street-art`、`gy-bishops-castle`、`pc-mecsek`、`gy-basilica` 各執行 web_search |
| 1.3 | 關鍵字：`[景點名] site:commons.wikimedia.org` |
| 1.4 | 驗證：確認圖片為正確主體（非 PDF/COA/基地台/GIF）|
| 1.5 | 更新 places.json（atomic write）|
| 1.6 | 驗證：`python3 -c "import json; json.load(open('places.json'))"` |

**驗收標準：**
- ✅ 檔案類型為圖片（jpg/png/webp），非 PDF/GIF
- ✅ 圖片主體為景點本身

### Phase 2: photos[] 佔位符修正（74 個 P1）

**目標：** 將 `photos[]` 全部替換為真實圖片

| 步驟 | 動作 |
|------|------|
| 2.1 | 對每個景點檢查 `photoUrl` 是否為有效 Wikimedia URL |
| 2.2 | 若 `photoUrl` 有效：直接複製到 `photos[0]` |
| 2.3 | 若 `photoUrl` 無效（如上 Phase 1 的 4 個）：執行 web_search 找新圖片 |
| 2.4 | 更新 `places.json`（atomic write）|
| 2.5 | 驗證：`python3 -c "import json; d=json.load(open('places.json')); print(len(d['places']))"` |

**預估：** 74 個景點中，70 個可採用策略 A（直接複製 photoUrl），4 個需先完成 Phase 1。

### Phase 3: 中文名稱比對（74 個 P3）

**目標：** 更新全部 74 個景點的 `nameZh` 欄位

| 步驟 | 動作 |
|------|------|
| 3.1 | 批次搜尋：`[景點英文名] Google Maps 台灣 繁體中文` |
| 3.2 | 比對現有 `nameZh` 與 Google Map 顯示名稱 |
| 3.3 | 差異處更新（需 Kigo 確認重要異動）|
| 3.4 | 更新 `places.json`（atomic write）|

**命名規範（台灣繁體）：**
- 使用 Google Map 台灣用戶看到的正式名稱
- 例: "Schönbrunn Palace" → "美泉宮"（而非 "熊布朗宮"）

---

## 3. 優先順序（更新版）

| 優先級 | 景點/問題 | 數量 | 原因 |
|--------|---------|------|------|
| **P0** | `bp-street-art` | 1 | PDF 檔根本無法顯示為圖片 |
| **P0** | `gy-bishops-castle` | 1 | 徽章圖示完全無法代表城堡 |
| **P0** | `pc-mecsek` | 1 | 基地台照片完全不代表山丘 |
| **P0** | `gy-basilica` | 1 | GIF 檔案格式錯誤（Lens 新發現）|
| **P1** | `photos[]` 佔位符 | 74 | 全部為同一 Unsplash 佔位符 |
| **P2** | `vn-fasanviertel` | 1 | 普通街道建築，非知名景點 |
| **P3** | `nameZh` 中文名稱 | 74 | 以 Google Map 繁體為準 |

---

## 4. 實作流程（含備份機制）

### 4.1 Coder 工作流程

```
Step 1: 備份
    $ cp places.json places.json.backup.$(date +%Y%m%d)

Step 2: Phase 1 — 修復 4 個 P0 photoUrl
    → web_search 找正確 Wikimedia URL
    → 更新 places.json（atomic write）

Step 3: Phase 2 — 修復 74 個 photos[] 佔位符
    → 複製 photoUrl 到 photos[0]
    → 更新 places.json（atomic write）

Step 4: Phase 3 — 中文名稱比對
    → web_search Google Map 繁體名稱
    → 更新 nameZh（差異處標記供 Kigo 確認）

Step 5: 驗證
    $ python3 -c "import json; json.load(open('places.json'))"
    （JSON 格式驗證）
```

### 4.2 備份機制（強制）

```bash
# 每次修改前自動備份
cp places.json places.json.backup.$(date +%Y%m%d)

# 修改後驗證 JSON 有效性
python3 -c "import json; json.load(open('places.json'))"

# 如需回滾
cp places.json.backup.20260509 places.json
```

### 4.3 Atomic Write 方式

```python
import json, shutil, tempfile, os

def atomic_write(path, data):
    """寫入前先寫入暫存檔，確認成功後再 rename（atomic）"""
    dirname = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(dir=dirname, suffix='.tmp')
    with os.fdopen(fd, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.rename(tmp, path)

# 使用
atomic_write('places.json', updated_data)
```

---

## 5. 預估工作量（更新版）

| Phase | 景點數 | 動作 | 預估時間 |
|-------|--------|------|---------|
| Phase 1 (P0) | 4 個 | web_search × 4 + 更新 | ~20 min |
| Phase 2 (P1) | 74 個 | photoUrl → photos[0]（70 個直接複製，4 個等 Phase 1）| ~25 min（含驗證）|
| Phase 3 (P3) | 74 個 | web_search × 74 批次搜尋 | ~60 min（可並發）|

**總計：** 約 **105 分鐘**（含驗證與 Kigo 確認時間）

**分階段交付：**
- Phase 1 完成後 → 第一次 Kigo 確認
- Phase 2 完成後 → 第二次 Kigo 確認（可選）
- Phase 3 完成後 → 第三次 Kigo 確認

---

## 6. 風險與緩解

| 風險 | 機率 | 影響 | 緩解措施 |
|------|------|------|---------|
| web_search 找不到正確 Wikimedia 圖片 | 低 | 中 | 擴大搜尋關鍵字至 Wikipedia 主站 |
| Google Map 中文名稱與現有完全一致 | 中 | 低 | 直接跳過，無需修改 |
| Atomic write 失敗 | 極低 | 高 | 備份檔案存在，可隨時回滾 |
| GIF 檔案實際為有效圖片 | 低 | 中 | Phase 1 驗證時二次確認 |

---

## 7. 不在此次範圍的項目

- ❌ 新增景點
- ❌ 調整 places.json 結構（除 `photos[]` 更新外）
- ❌ 調整 `rating`、`reviewCount` 等非圖片/名稱欄位

---

## 8. 待確認事項

- [ ] Kigo 是否同意「Phase 1 完成後即交付」的節奏？
- [ ] `vn-fasanviertel` 是否需要替換為其他景點，或直接移除？
- [ ] Phase 3 中文名稱如有重大差異（如「美泉宮」vs 現有翻譯），是否需要 Kigo 逐筆確認？

---

**📐 Prime-Architect v2.0 簽核**
