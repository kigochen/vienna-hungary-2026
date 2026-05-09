const fs = require('fs');
const path = require('path');

const ATTRACTIONS_FILE = '/home/node/.openclaw/workspace/vienna-trip/src/attractions_compact.json';
const OUTPUT_FILE = '/home/node/.openclaw/workspace/vienna-trip/src/places.json';
const FALLBACK_PHOTO = 'https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=800';

const attractions = JSON.parse(fs.readFileSync(ATTRACTIONS_FILE, 'utf8'));

const places = attractions.map(a => ({
  id: a.id,
  name: a.name,
  nameZh: a.nameZh,
  city: a.city,
  category: a.category,
  coordinates: a.coords,
  rating: a.rating,
  pros: a.pros,
  cons: a.cons,
  cost: a.cost,
  bestTime: a.bestTime,
  tips: a.tips,
  photos: [FALLBACK_PHOTO]
}));

const placesJson = {
  version: '1.0',
  tripInfo: {
    destination: '維也納+匈牙利',
    startDate: '2026-08-30',
    endDate: '2026-09-12',
    base: '布達佩斯（匈牙利定點深度遊）',
    viennaDays: '最後4天（9/9-9/12）',
    totalDays: 14
  },
  places,
  itinerary: [
    { day: 1, date: '2026-08-30', theme: '抵達布達佩斯', places: ['bp-new-york-cafe', 'bp-buda-castle', 'bp-fishermans-bastion'] },
    { day: 2, date: '2026-08-31', theme: '布達佩斯經典', places: ['bp-szechenyi', 'bp-city-park', 'bp-vajdahunyad'] },
    { day: 3, date: '2026-09-01', theme: '多瑙河畔', places: ['bp-liberty-bridge', 'bp-central-market', 'bp-st-stephens'] },
    { day: 4, date: '2026-09-02', theme: '布達佩斯深度', places: ['bp-rudas-bath', 'bp-cave-church', 'bp-hospital-rock'] },
    { day: 5, date: '2026-09-03', theme: '歷史探索', places: ['bp-house-terror', 'bp-synagogue', 'bp-street-art'] },
    { day: 6, date: '2026-09-04', theme: '近郊健行', places: ['bp-chairlift', 'bp-castle-caves', 'bp-margaret-island'] },
    { day: 7, date: '2026-09-05', theme: '休閒日', places: ['bp-ruin-pubs', 'bp-a38', 'bp-ferris-wheel'] },
    { day: 8, date: '2026-09-06', theme: '匈牙利其他城市', places: ['lb-badacsony', 'lb-tihany'] },
    { day: 9, date: '2026-09-07', theme: '佩奇/塞格德', places: ['pc-necropolis', 'pc-zsolnay', 'pc-cathedral'] },
    { day: 10, date: '2026-09-08', theme: '移動至維也納', places: ['vn-schonbrunn', 'vn-prater', 'vn-cafe-central'] },
    { day: 11, date: '2026-09-09', theme: '維也納經典', places: ['vn-st-stephens', 'vn-state-opera', 'vn-hofburg'] },
    { day: 12, date: '2026-09-10', theme: '維也納深度', places: ['vn-belvedere', 'vn-albertina-modern', 'vn-hundertwasserhaus'] },
    { day: 13, date: '2026-09-11', theme: '維也納自然', places: ['vn-wachau-valley', 'vn-grinzing', 'vn-tuerkenschanzpark'] },
    { day: 14, date: '2026-09-12', theme: '離開維也納', places: ['vn-zentralfriedhof', 'vn-palais-ferstel', 'vn-augarten'] }
  ],
  transport: {
    flight: { to: '維也納國際機場 (VIE)', from: '台灣' },
    train: { viennaToBudapest: { duration: '2.5小時', operator: 'OBB', cost: '€29-50', bookingUrl: 'https://www.oebb.at' } },
    localTransport: {
      budapest: '地鐵+電車（€1.15/程，或購買24小時券€15）',
      vienna: '地鐵+電車（€2.40/程，或購買48小時券€14.10）'
    },
    carRental: { recommended: false, reason: '布達佩斯和維也納市區停車費用昂貴，建議使用大眾交通' }
  },
  budget: {
    currency: '歐元 (EUR)',
    estimatedTotal: '€2,500-3,500',
    categories: {
      flights: { estimated: '€800-1200', notes: '商務艙或豪華經濟' },
      accommodation: { estimated: '€800-1200', notes: '€100-150/晚 x 13晚' },
      food: { estimated: '€400-600', notes: '€30-50/天' },
      transport: { estimated: '€150-250', notes: '火車+市內交通' },
      attractions: { estimated: '€200-350', notes: '門票+導覽' },
      misc: { estimated: '€150-200', notes: '紀念品+意外' }
    }
  },
  food: [
    { name: '匈牙利紅椒雞 (Paprikás Csirke)', type: 'main', country: 'Hungary', description: '匈牙利經典料理，用紅椒粉燉煮的雞肉' },
    { name: '匈牙利魚湯', type: 'main', country: 'Hungary', description: '塞格德最出名，濃郁的魚湯' },
    { name: '鵝肝 (Libamáj)', type: 'appetizer', country: 'Hungary', description: '匈牙利特產，配麵包或蘋果片' },
    { name: 'Goulash (匈牙利燉肉)', type: 'main', country: 'Hungary', description: '匈牙利國菜，牛肉燉紅椒' },
    { name: '炸肉排 (Wiener Schnitzel)', type: 'main', country: 'Vienna', description: '維也納經典，外酥內嫩的小牛肉排' },
    { name: '薩赫蛋糕 (Sachertorte)', type: 'dessert', country: 'Vienna', description: '維也納最著名的巧克力蛋糕' },
    { name: '維也納咖啡 (Wiener Melange)', type: 'drink', country: 'Vienna', description: '維也納咖啡館文化代表作' },
    { name: 'Grüner Veltliner 白酒', type: 'drink', country: 'Vienna', description: '奧地利代表性白酒' }
  ],
  todo: [
    { item: '護照確認有效期限（需6個月以上）', done: false },
    { item: '申請申根簽證或確認免簽狀況', done: false },
    { item: '旅遊不便險（航班延誤/取消）', done: false },
    { item: '國際駕照（若租車）', done: false },
    { item: '歐洲通用轉接頭', done: false },
    { item: '歐元現金（匈牙利福林可在當地換）', done: false },
    { item: 'OBB 火車票提前預購（維也納-布達佩斯）', done: false },
    { item: '布達佩斯溫泉提前預約（魯達斯/塞切尼）', done: false },
    { item: '美泉宮門票預購（避免排隊）', done: false },
    { item: '下載離線地圖（Maps.me）', done: false },
    { item: '航空公司貴賓室預約（長程航班）', done: false },
    { item: '緊急聯絡電話（中華民國駐奧地利代表處）', done: false }
  ]
};

fs.writeFileSync(OUTPUT_FILE, JSON.stringify(placesJson, null, 2), 'utf8');
console.log(`✅ places.json written with ${places.length} places`);
