# PLAN: Vienna Hungary 2026 — Task 2 & Task 3 實作規劃

**產出日期**：2026-05-10  
**Task 2**：補足 74 個景點的 `blogLinks`（每個 2-5 個真實遊記連結）  
**Task 3**：補足 74 個景點的 `mustBuy`（tourist + local 各 1-2 項）

---

## 📊 現況盤點

| 項目 | 已具備 | 需補足 | 備註 |
|------|--------|--------|------|
| `blogLinks` | 11 個景點（33 條連結）| **63 個景點**（約 150-300 條）| 11 個景點已完成，可直接跳過 |
| `mustBuy.tourist` | 11 個景點 | **63 個景點** | 必須與 blogLinks 同步新增 |
| `mustBuy.local` | 11 個景點 | **63 個景點** | 必須與 blogLinks 同步新增 |

**地理分布**：
- Budapest: 32 個景點（最密集）
- Vienna: 19 個景點
- 其他（Debrecen, Pécs, Szeged, Lake Balaton 等）: 23 個景點

---

## 🎯 實作策略

### 雙軌並行研究法

每個景點查詢時，同時收集：
1. **blogLinks** → 搜「{景點名} 遊記/攻略/自由行」
2. **mustBuy.tourist** → 搜「{景點} 必買/紀念品/伴手禮」
3. **mustBuy.local** → 搜「{景點} 在地人推薦/隱藏版」

### 資料來源優先順序

**部落格（blogLinks）**：
1. 窮遊馬蜂窩（mandysu.com / qiongyou）
2. 背包客棧（backpackers.com.tw）
3. Mook / Trip.com（中文遊記）
4. 痞客邦（PIXNET）個人部落格
5. Udn 部落格

**mustBuy 觀光客**：
1. Mook 景點頁面
2. Trip.com 景點評論
3. 窮遊 景點購物指南

**mustBuy 在地人**：
1. PTT Travel 版（dcard / PT TTravel）
2. 小紅書（deep travel recommendations）
3. 背包客棧當地人攻略

### 驗證機制
每個連結必須：
- ✅ 成功存取（HTTP 200）
- ✅ 標題與景點相關
- ✅ 原文為中文（正體中文優先）

---

## 📋 執行步驟（共 7 步）

---

### Step 1：建立研究框架與模板（0.5 小時）

**目的**：建立可複製的研究模板，確保後續批次一致性

**DoD**：
- [ ] 撰寫 `vienna-trip/research-template.md`：說明每個景點的查詢關鍵字公式
- [ ] 建立 `vienna-trip/research-batch-*.json`：每批景點清單（含名稱、城市、查詢關鍵字）
- [ ] 確認 places.json 格式正確（blogLinks / mustBuy 欄位位置）

**Rollback Strategy**：模板錯誤 → 重新產出，不影響 places.json

**預估時間**：30 分鐘

---

### Step 2：Phase A — Budapest 核心區（第一批 11 景點）（3 小時）

**目的**：涵蓋最重要的布達佩斯景點，與現有 11 個已具備資料的景點共同構成核心

**範圍**：Budapest 的 11 個無 blogLinks 景點（32 - 21 = 11）
- Hospital in the Rock
- House of Terror
- Hungarian Jewish Museum
- Dohány Street Synagogue
- St. Stephen's Basilica
- Liberty Bridge
- Margaret Island
- Memento Park
- Metro Line 1（Fővám tér → Mexikói út）
- Ruin Pubs（除了 Szimpla Kert 以外的 Ruin Pub）
- New York Café

**DoD**：
- [ ] 11 個景點全部具備 `blogLinks`（每個 2-5 條）
- [ ] 11 個景點全部具備 `mustBuy.tourist`（1-2 項）
- [ ] 11 個景點全部具備 `mustBuy.local`（1-2 項）
- [ ] 所有連結已驗證可存取

**Rollback Strategy**：若某景點找不到足夠資料 → 標記「需實地確認」，放寬至 1 條 blogLink

**預估時間**：3 小時（每景點約 15-18 分鐘，含驗證）

---

### Step 3：Phase B — Budapest 擴展區（第二批 10 景點）（3 小時）

**目的**：補足布達佩斯剩餘熱門景點

**範圍**：Budapest 另外 10 個景點
- Gellért Hill Cave Church（已部分有連結，補足至 2-5 條）
- Vajdahunyad Castle
- Ráth György Museum → 改為 Castle Cave
- Metropolitan Ervin Szabó Library
- Jewish Quarter Street Art
- Kolodko Small Statues
- Károlyi Garden
- Zugliget Chairlift（已部分有連結，補足）
- Hármashatárhegy
- Wekerletelep（匈牙利小人國）

**DoD**：同 Step 2

**Rollback Strategy**：同 Step 2

**預估時間**：3 小時

---

### Step 4：Phase C — Vienna 核心區（第一批 10 景點）（3 小時）

**目的**：處理維也納最重要景點

**範圍**：Vienna 的 10 個景點
- Belvedere Palace
- Albertina Modern
- Augarten Porcelain Factory
- Vienna University Botanical Garden
- 視覺藝術學院（Akademie der bildenden Künste）
- MAK (Museum of Applied Arts)
- Weltmuseum Wien
- Haus der Musik
- Kunsthalle Wien
- Schubert's Birthplace / Mozart Memorial

**DoD**：同 Step 2

**Rollback Strategy**：同 Step 2

**預估時間**：3 小時

---

### Step 5：Phase D — Vienna 擴展區 + 其他城市（第二批 10 景點）（3 小時）

**目的**：涵蓋維也納邊緣景點與其他城市

**範圍**：
- Vienna 其餘 9 個景點
- Debrecen（3 景點）
- Győr（2 景點）
- Pécs（4 景點）
- Szeged（3 景點）

→ 從中選取 10 個優先景點

**DoD**：同 Step 2

**Rollback Strategy**：同 Step 2

**預估時間**：3 小時

---

### Step 6：Phase E — 偏遠城市 Final Batch（11 景點）（3 小時）

**目的**：涵蓋所有剩餘景點

**範圍**：Lake Balaton（3）、Hortobágy（1）、Aggtelek（1）、Sopron（2）、Sárospatak（1）、Tapolca（1）、Oroszlány（1）、Nógrád（1）

**DoD**：同 Step 2

**Rollback Strategy**：同 Step 2

**預估時間**：3 小時

---

### Step 7：整合、驗證與最終 Commit（1 小時）

**目的**：確保所有資料正確寫入 places.json，並完成 Git Commit

**DoD**：
- [ ] 驗證所有 74 個景點皆具備 `blogLinks`（≥1 條）
- [ ] 驗證所有 74 個景點皆具備 `mustBuy.tourist`（≥1 項）
- [ ] 驗證所有 74 個景點皆具備 `mustBuy.local`（≥1 項）
- [ ] JSON 格式正確（無 Syntax Error）
- [ ] Commit 至 Git（message: "feat: add blogLinks and mustBuy for all 74 attractions"）

**Rollback Strategy**：格式錯誤 → 回歸上一次 places.json backup

**預估時間**：1 小時

---

## 📅 時程預估

| 步驟 | 內容 | 預估時間 | 累計 |
|------|------|----------|------|
| Step 1 | 建立研究框架 | 0.5h | 0.5h |
| Step 2 | Budapest Phase A（11 景點）| 3h | 3.5h |
| Step 3 | Budapest Phase B（10 景點）| 3h | 6.5h |
| Step 4 | Vienna Phase C（10 景點）| 3h | 9.5h |
| Step 5 | Vienna + 其他 Phase D（10 景點）| 3h | 12.5h |
| Step 6 | 偏遠城市 Phase E（11 景點）| 3h | 15.5h |
| Step 7 | 整合驗證 Commit | 1h | **16.5h** |

**總時程**：約 16.5 小時手動研究（每節奏 3 小時，可分 5-6 天執行）

---

## ⚠️ 風險與對策

| 風險 | 機率 | 影響 | 對策 |
|------|------|------|------|
| 部分偏遠景點找不到遊記 | 中 | 中 | 放寬至 1 條 blogLink，標記「待充实」 |
| 小紅書/PTT 連結無法驗證 | 低 | 高 | 改用窮遊/背包客棧作為主要來源 |
| places.json 格式衝突 | 低 | 高 | 每次更新前先 backup |
| 研究時間超出預期 | 中 | 中 | Phase E 可拆成兩批次 |

---

## 🔄 與現有 Taskflow 的整合

此任務適合以 **手動研究 + 直接寫入** 的方式執行，不需要动用完整的 Architect → Coder → Lens → Tester 流水線。原因：

1. **重複性高、創造性低**：每個景點的 research pattern 相同
2. **驗證簡單**：只需要確認連結可存取 + JSON 格式正確
3. **不可逆風險低**：places.json 有完整的 Git 版本控制

**建議 Kigo 裁示**：是否授權以手動模式直接執行？還是需要透過 Coder subagent 分批實作？

---

## 📁 產出檔案

- `~/.openclaw/workspace/vienna-trip/PLAN-task2-task3.md`（本檔案）
- `~/.openclaw/workspace/vienna-trip/research-template.md`
- `~/.openclaw/workspace/vienna-trip/research-batch-*.json`（5 批次）
- 更新 `~/.openclaw/workspace/vienna-trip/places.json`