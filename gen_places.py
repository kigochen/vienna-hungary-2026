#!/usr/bin/env python3
import json
import urllib.parse

def g(name):
    return f"https://www.google.com/search?q={urllib.parse.quote(name)}"

places = [
    # Budapest (26 places)
    {"id": "bp-01", "name": "St. Stephen's Basilica", "nameZh": "聖史蒂芬教堂", "city": "Budapest", "category": "heritage", "coordinates": [47.4988, 19.0535], "rating": 4.8, "pros": "登頂可俯瞰全市", "cons": "樓梯超累", "photoUrl": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=800", "googleSearchUrl": g("St Stephen's Basilica Budapest")},
    {"id": "bp-02", "name": "Memorial Park", "nameZh": "紀念品公園", "city": "Budapest", "category": "viewpoint", "coordinates": [47.4857, 19.0362], "rating": 4.2, "pros": "可看自由橋全景", "cons": "午後人多", "photoUrl": "https://images.unsplash.com/photo-1517736996303-4b8c4291f0c5?w=800", "googleSearchUrl": g("Memorial Park Budapest")},
    {"id": "bp-03", "name": "Rudas Thermal Bath", "nameZh": "魯達斯溫泉", "city": "Budapest", "category": "thermal", "coordinates": [47.4902, 19.0463], "rating": 4.7, "pros": "歷史悠久，屋頂 pools", "cons": "可能需預約", "photoUrl": "https://images.unsplash.com/photo-1566072011253-1a9a4a5a7a9a?w=800", "googleSearchUrl": g("Rudas Thermal Bath Budapest")},
    {"id": "bp-04", "name": "Freedom Bridge", "nameZh": "自由橋", "city": "Budapest", "category": "heritage", "coordinates": [47.4843, 19.0589], "rating": 4.5, "pros": "拍照效果好", "cons": "車多", "photoUrl": "https://images.unsplash.com/photo-1503614472-8c93d56e92ce?w=800", "googleSearchUrl": g("Freedom Bridge Budapest")},
    {"id": "bp-05", "name": "Miniature Park", "nameZh": "迷你雕像公園", "city": "Budapest", "category": "experience", "coordinates": [47.4955, 19.0397], "rating": 4.0, "pros": "可看各國迷你模型", "cons": "規模不大", "photoUrl": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800", "googleSearchUrl": g("Miniature Park Budapest")},
    {"id": "bp-06", "name": "Hungarian National Museum", "nameZh": "匈牙利國家博物館", "city": "Budapest", "category": "museum", "coordinates": [47.4937, 19.0635], "rating": 4.3, "pros": "豐富歷史收藏", "cons": "展場動線複雜", "photoUrl": "https://images.unsplash.com/photo-1566127444979-b3d2b654e3d7?w=800", "googleSearchUrl": g("Hungarian National Museum Budapest")},
    {"id": "bp-07", "name": "Budapest Ferris Wheel", "nameZh": "摩天輪", "city": "Budapest", "category": "viewpoint", "coordinates": [47.5018, 19.0475], "rating": 4.3, "pros": "夜景佳", "cons": "白天曝曬", "photoUrl": "https://images.unsplash.com/photo-1528164340885-0c8e6b4f5e9e?w=800", "googleSearchUrl": g("Budapest Ferris Wheel park")},
    {"id": "bp-08", "name": "Ruin Bar (Szimpla)", "nameZh": "廢墟酒吧", "city": "Budapest", "category": "food", "coordinates": [47.4975, 19.0412], "rating": 4.6, "pros": "氣氛獨特，便宜酒水", "cons": "擁擠吵鬧", "photoUrl": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800", "googleSearchUrl": g("Szimpla Ruin Bar Budapest")},
    {"id": "bp-09", "name": "Cave Church", "nameZh": "洞穴教堂", "city": "Budapest", "category": "heritage", "coordinates": [47.5023, 19.0358], "rating": 4.4, "pros": "地底洞穴，特別體驗", "cons": "潮濕", "photoUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800", "googleSearchUrl": g("Cave Church Budapest")},
    {"id": "bp-10", "name": "Metro Line 1", "nameZh": "地鐵一號線", "city": "Budapest", "category": "heritage", "coordinates": [47.5002, 19.0511], "rating": 4.5, "pros": "世界文化遺產，最古老之一", "cons": "人潮多", "photoUrl": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=800", "googleSearchUrl": g("Budapest Metro Line 1 UNESCO")},
    {"id": "bp-11", "name": "Ethnography Museum Roof Trail", "nameZh": "民族學博物館屋頂步道", "city": "Budapest", "category": "viewpoint", "coordinates": [47.5065, 19.0342], "rating": 4.1, "pros": "高空步道，view 很讚", "cons": "門票不便宜", "photoUrl": "https://images.unsplash.com/photo-1574958269345-608b8c7c3cc6?w=800", "googleSearchUrl": g("Hungarian Ethnography Museum Budapest")},
    {"id": "bp-12", "name": "Vajdahunyad Castle", "nameZh": "Vajdahunyad 城堡", "city": "Budapest", "category": "heritage", "coordinates": [47.5198, 19.0827], "rating": 4.7, "pros": "童話風格城堡", "cons": "腹地大要走很久", "photoUrl": "https://images.unsplash.com/photo-1529655686643-1b8f9f0b5a7a?w=800", "googleSearchUrl": g("Vajdahunyad Castle Budapest")},
    {"id": "bp-13", "name": "Hospital in the Rock", "nameZh": "岩中醫院", "city": "Budapest", "category": "heritage", "coordinates": [47.4872, 19.0298], "rating": 3.9, "pros": "獨特的歷史", "cons": "不好找", "photoUrl": "https://images.unsplash.com/photo-1551892374-ecf4ce1c797d?w=800", "googleSearchUrl": g("Hospital in the Rock Budapest")},
    {"id": "bp-14", "name": "Buda Castle Cave", "nameZh": "布達城堡洞穴", "city": "Budapest", "category": "experience", "coordinates": [47.4925, 19.0342], "rating": 4.3, "pros": "地下隧道探險", "cons": "潮濕陰暗", "photoUrl": "https://images.unsplash.com/photo-1534430480872-3498386e7856?w=800", "googleSearchUrl": g("Buda Castle Cave Budapest")},
    {"id": "bp-15", "name": "Margaret Island", "nameZh": "瑪格麗特島", "city": "Budapest", "category": "nature", "coordinates": [47.5392, 19.0465], "rating": 4.6, "pros": "多瑙河中央，適合慢跑野餐", "cons": "交通費周折", "photoUrl": "https://images.unsplash.com/photo-1543946207-39bd91e70ca7?w=800", "googleSearchUrl": g("Margaret Island Budapest")},
    {"id": "bp-16", "name": "Great Synagogue", "nameZh": "猶太教堂", "city": "Budapest", "category": "heritage", "coordinates": [47.4953, 19.0595], "rating": 4.8, "pros": "最大猶太會堂，歷史意義重大", "cons": "門票貴", "photoUrl": "https://images.unsplash.com/photo-1566576721346-d4a3b4ea17555?w=800", "googleSearchUrl": g("Great Synagogue Budapest Dohany")},
    {"id": "bp-17", "name": "Jewish Quarter Street Art", "nameZh": "猶太區街頭藝術", "city": "Budapest", "category": "experience", "coordinates": [47.4962, 19.0620], "rating": 4.4, "pros": "街頭壁畫非常精彩", "cons": "要找路", "photoUrl": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800", "googleSearchUrl": g("Jewish Quarter street art Budapest")},
    {"id": "bp-18", "name": "Hydrofoil on Danube", "nameZh": "水上巴士", "city": "Budapest", "category": "experience", "coordinates": [47.4983, 19.0415], "rating": 4.2, "pros": "多瑙河上看兩岸", "cons": "班次少", "photoUrl": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800", "googleSearchUrl": g("Budapest hydrofoil Danube")},
    {"id": "bp-19", "name": "Szechenyi Thermal Bath", "nameZh": "塞切尼溫泉", "city": "Budapest", "category": "thermal", "coordinates": [47.5182, 19.0829], "rating": 4.9, "pros": "歐洲最大溫泉浴場之一", "cons": "人超多要早去", "photoUrl": "https://images.unsplash.com/photo-1551634979-2b87f74e2d2a?w=800", "googleSearchUrl": g("Szechenyi Thermal Bath Budapest")},
    {"id": "bp-20", "name": "Buda Castle", "nameZh": "布達城堡", "city": "Budapest", "category": "heritage", "coordinates": [47.4917, 19.0329], "rating": 4.8, "pros": "皇宮，全景市容", "cons": "地勢高要爬山", "photoUrl": "https://images.unsplash.com/photo-1551634979-2b87f74e2d2a?w=800", "googleSearchUrl": g("Buda Castle Budapest")},
    {"id": "bp-21", "name": "A38 Ship", "nameZh": "A38 船", "city": "Budapest", "category": "experience", "coordinates": [47.4855, 19.0562], "rating": 4.5, "pros": "改裝貨船變成文化中心，音樂演出", "cons": "位置偏", "photoUrl": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800", "googleSearchUrl": g("A38 ship Budapest venue")},
    {"id": "bp-22", "name": "New York Cafe", "nameZh": "新紐約咖啡館", "city": "Budapest", "category": "food", "coordinates": [47.4971, 19.0601], "rating": 4.7, "pros": "世界最美咖啡館之一", "cons": "排隊很久，價格高", "photoUrl": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=800", "googleSearchUrl": g("New York Cafe Budapest")},
    {"id": "bp-23", "name": "House of Terror", "nameZh": "恐怖之屋博物館", "city": "Budapest", "category": "museum", "coordinates": [47.5003, 19.0718], "rating": 4.6, "pros": "共產時期歷史，非常震撼", "cons": "心情沉重", "photoUrl": "https://images.unsplash.com/photo-1509281373149-e957c6296406?w=800", "googleSearchUrl": g("House of Terror Budapest")},
    {"id": "bp-24", "name": "Chairlift (Libegő)", "nameZh": "Chairlift 纜車", "city": "Budapest", "category": "viewpoint", "coordinates": [47.4912, 19.0275], "rating": 4.4, "pros": "纜車看市景", "cons": "班次少", "photoUrl": "https://images.unsplash.com/photo-1506703719100-b0e9e25e29a2?w=800", "googleSearchUrl": g("Libegő chairlift Budapest")},
    {"id": "bp-25", "name": "Danube Cruise", "nameZh": "多瑙河遊船", "city": "Budapest", "category": "experience", "coordinates": [47.4983, 19.0440], "rating": 4.5, "pros": "夜景行程，浪漫", "cons": "天氣影響大", "photoUrl": "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=800", "googleSearchUrl": g("Danube cruise Budapest night")},
    {"id": "bp-26", "name": "City Park (Varosliget)", "nameZh": "城市公園", "city": "Budapest", "category": "nature", "coordinates": [47.5173, 19.0821], "rating": 4.5, "pros": "大片綠地，塞切尼溫泉也在裡面", "cons": "腹地太大", "photoUrl": "https://images.unsplash.com/photo-1568219557405-376e23e4f7cf?w=800", "googleSearchUrl": g("City Park Budapest Varosliget")},
    # Vienna (20 places)
    {"id": "v-01", "name": "Türkenschanzpark", "nameZh": "Türkenschanzpark 公園", "city": "Vienna", "category": "nature", "coordinates": [48.2142, 16.2856], "rating": 4.2, "pros": "英式庭園，幽靜", "cons": "位置遠", "photoUrl": "https://images.unsplash.com/photo-1567159644914-1e2c83a40f7c?w=800", "googleSearchUrl": g("Türkenschanzpark Vienna")},
    {"id": "v-02", "name": "Literature Museum (Österreichische Nationalbibliothek)", "nameZh": "維也納文學博物館", "city": "Vienna", "category": "museum", "coordinates": [48.2005, 16.3598], "rating": 4.3, "pros": "霍夫曼等作家相關", "cons": "德文內容為主", "photoUrl": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=800", "googleSearchUrl": g("Literature Museum Vienna")},
    {"id": "v-03", "name": "St. Peter Church Crypt", "nameZh": "聖彼得教堂地下墓穴", "city": "Vienna", "category": "heritage", "coordinates": [48.2082, 16.3701], "rating": 4.1, "pros": "地下墓穴探險", "cons": "光線暗", "photoUrl": "https://images.unsplash.com/photo-1509281373149-e957c6296406?w=800", "googleSearchUrl": g("St Peter church crypt Vienna")},
    {"id": "v-04", "name": "Contraception Museum", "nameZh": "避孕博物館", "city": "Vienna", "category": "museum", "coordinates": [48.2095, 16.3512], "rating": 4.4, "pros": "全球唯一，非常特別", "cons": "規模小", "photoUrl": "https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?w=800", "googleSearchUrl": g("Contraception Museum Vienna")},
    {"id": "v-05", "name": "Botanical Garden (Botanischer Garten)", "nameZh": "植物園", "city": "Vienna", "category": "nature", "coordinates": [48.1891, 16.3801], "rating": 4.3, "pros": "多樣植物，溫室", "cons": "需時較長", "photoUrl": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=800", "googleSearchUrl": g("Botanical Garden Vienna")},
    {"id": "v-06", "name": "Sculpture Garden", "nameZh": "雕塑花園", "city": "Vienna", "category": "experience", "coordinates": [48.1912, 16.3765], "rating": 4.0, "pros": "戶外雕塑展", "cons": "天氣影響大", "photoUrl": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800", "googleSearchUrl": g("Sculpture garden Vienna")},
    {"id": "v-07", "name": "Central Cemetery (Zentralfriedhof)", "nameZh": "中央公墓", "city": "Vienna", "category": "heritage", "coordinates": [48.1495, 16.4255], "rating": 4.5, "pros": "貝多芬、布拉姆斯等名人長眠於此", "cons": "範圍大", "photoUrl": "https://images.unsplash.com/photo-1509281373149-e957c6296406?w=800", "googleSearchUrl": g("Vienna Central Cemetery Beethoven")},
    {"id": "v-08", "name": "Narrenturm", "nameZh": "Narrenturm 圓形建築", "city": "Vienna", "category": "heritage", "coordinates": [48.2165, 16.3502], "rating": 4.0, "pros": "古老的圓形精神病院建築", "cons": "有點陰森", "photoUrl": "https://images.unsplash.com/photo-1551892374-ecf4ce1c797d?w=800", "googleSearchUrl": g("Narrenturm Vienna")},
    {"id": "v-09", "name": "Grinzing Heuriger", "nameZh": "Grinzing 小酒館區", "city": "Vienna", "category": "food", "coordinates": [48.2333, 16.3167], "rating": 4.6, "pros": "施照布塔酒和脆皮肉片", "cons": "觀光客多", "photoUrl": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800", "googleSearchUrl": g("Grinzing Heuriger Vienna")},
    {"id": "v-10", "name": "Palais Ferstel Hidden Court", "nameZh": "Palais Ferstel 隱藏庭院", "city": "Vienna", "category": "heritage", "coordinates": [48.2086, 16.3651], "rating": 4.2, "pros": "低調奢華的宮殿", "cons": "入口不明顯", "photoUrl": "https://images.unsplash.com/photo-1551634979-2b87f74e2d2a?w=800", "googleSearchUrl": g("Palais Ferstel Vienna")},
    {"id": "v-11", "name": "Votive Church (Votivkirche)", "nameZh": "Historic Votive Church", "city": "Vienna", "category": "heritage", "coordinates": [48.1966, 16.3592], "rating": 4.5, "pros": "新哥德式建築，雄偉", "cons": "遊客多", "photoUrl": "https://images.unsplash.com/photo-1504680177321-2e6a8796ac4a?w=800", "googleSearchUrl": g("Votivkirche Vienna")},
    {"id": "v-12", "name": "Karlskirche Secret Pond", "nameZh": "Karlskirche 秘密池塘", "city": "Vienna", "category": "nature", "coordinates": [48.1952, 16.3635], "rating": 4.1, "pros": "巴洛克教堂旁的秘密花園", "cons": "開放時間短", "photoUrl": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800", "googleSearchUrl": g("Karlskirche Vienna secret garden")},
    {"id": "v-13", "name": "Ferstel Passage", "nameZh": "Ferstel Passage", "city": "Vienna", "category": "heritage", "coordinates": [48.2087, 16.3648], "rating": 4.3, "pros": "優雅的室內商場", "cons": "店鋪貴", "photoUrl": "https://images.unsplash.com/photo-1529655686643-1b8f9f0b5a7a?w=800", "googleSearchUrl": g("Ferstel Passage Vienna")},
    {"id": "v-14", "name": "Jewish Museum Hidden Garden", "nameZh": "Jewish Museum 隱藏庭院", "city": "Vienna", "category": "heritage", "coordinates": [48.2092, 16.3598], "rating": 4.0, "pros": "寧靜的猶太花園", "cons": "不好找", "photoUrl": "https://images.unsplash.com/photo-1534430480872-3498386e7856?w=800", "googleSearchUrl": g("Jewish Museum Vienna garden")},
    {"id": "v-15", "name": "Augarten Porcelain Factory", "nameZh": "Augarten 瓷器工廠", "city": "Vienna", "category": "experience", "coordinates": [48.1927, 16.3662], "rating": 4.4, "pros": "歐洲最古老的瓷器廠之一", "cons": "需預約導覽", "photoUrl": "https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?w=800", "googleSearchUrl": g("Augarten porcelain factory Vienna")},
    {"id": "v-16", "name": "Hundertwasserhaus", "nameZh": "Hundertwasserhaus", "city": "Vienna", "category": "heritage", "coordinates": [48.2009, 16.3317], "rating": 4.7, "pros": "色彩繽紛的公寓建築，非常上相", "cons": "不能入內參觀", "photoUrl": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800", "googleSearchUrl": g("Hundertwasserhaus Vienna")},
    {"id": "v-17", "name": "Palais Liechtenstein Secret Garden", "nameZh": "Palais Lichtenstein 秘密花園", "city": "Vienna", "category": "nature", "coordinates": [48.1965, 16.3682], "rating": 4.1, "pros": "低調的宮殿花園", "cons": "開放時間不穩定", "photoUrl": "https://images.unsplash.com/photo-1567159644914-1e8f9f0b5a7a?w=800", "googleSearchUrl": g("Palais Liechtenstein secret garden Vienna")},
    {"id": "v-18", "name": "Vienna Woods (Wienerwald)", "nameZh": "維也納森林", "city": "Vienna", "category": "nature", "coordinates": [48.2312, 16.2898], "rating": 4.5, "pros": "近郊森林，適合健行", "cons": "需半天時間", "photoUrl": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800", "googleSearchUrl": g("Vienna Woods Wienerwald hiking")},
    {"id": "v-19", "name": "Fasanviertel Neighborhood", "nameZh": "Fasanviertel 社區", "city": "Vienna", "category": "experience", "coordinates": [48.2078, 16.3012], "rating": 3.9, "pros": "當地人社區，寧靜", "cons": "無特別亮點", "photoUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800", "googleSearchUrl": g("Fasanviertel Vienna neighborhood")},
    {"id": "v-20", "name": "District Museum (Wiener Stadtmuseum)", "nameZh": "地方博物館", "city": "Vienna", "category": "museum", "coordinates": [48.2035, 16.3535], "rating": 4.0, "pros": "認識維也納入門", "cons": "德文解說為主", "photoUrl": "https://images.unsplash.com/photo-1566127444979-b3d2b654e3d7?w=800", "googleSearchUrl": g("Wiener Stadtmuseum Vienna district museum")},
    # Additional Hungary cities
    # Debrecen (4 places)
    {"id": "h-01", "name": "Reformed College Debrecen", "nameZh": "Debrecen 改革宗教會學院", "city": "Debrecen", "category": "heritage", "coordinates": [47.5317, 21.6241], "rating": 4.4, "pros": "匈牙利宗教改革重鎮", "cons": "偏遠", "photoUrl": "https://images.unsplash.com/photo-1504680177321-2e6a8796ac4a?w=800", "googleSearchUrl": g("Reformed College Debrecen")},
    {"id": "h-02", "name": "Déri Museum", "nameZh": "Déri Museum", "city": "Debrecen", "category": "museum", "coordinates": [47.5301, 21.6265], "rating": 4.2, "pros": "重要藝術與考古收藏", "cons": "展示偏老派", "photoUrl": "https://images.unsplash.com/photo-1566127444979-b3d2b654e3d7?w=800", "googleSearchUrl": g("Déri Museum Debrecen")},
    {"id": "h-03", "name": "Great Forest Park (Nagyerdő)", "nameZh": "大森林公園", "city": "Debrecen", "category": "nature", "coordinates": [47.5182, 21.6055], "rating": 4.3, "pros": "大片綠地，當地人休閒去處", "cons": "沒特別亮點", "photoUrl": "https://images.unsplash.com/photo-1568219557405-376e23e4f7cf?w=800", "googleSearchUrl": g("Nagyerdő Debrecen")},
    {"id": "h-04", "name": "Aquaticum Mediterranean Spa", "nameZh": "Aquaticum 地中海溫泉", "city": "Debrecen", "category": "thermal", "coordinates": [47.5148, 21.6182], "rating": 4.4, "pros": "大型溫泉水樂園", "cons": "門票不便宜", "photoUrl": "https://images.unsplash.com/photo-1551634979-2b87f74e2d2a?w=800", "googleSearchUrl": g("Aquaticum Debrecen thermal spa")},
    # Szeged (4 places)
    {"id": "h-05", "name": "Szeged Cathedral", "nameZh": "Szeged 大教堂", "city": "Szeged", "category": "heritage", "coordinates": [46.2481, 20.1481], "rating": 4.5, "pros": "壯觀的新羅馬式建築", "cons": "周邊停車不便", "photoUrl": "https://images.unsplash.com/photo-1504680177321-2e6a8796ac4a?w=800", "googleSearchUrl": g("Szeged Cathedral")},
    {"id": "h-06", "name": "Napfényfürdő Water Park", "nameZh": "Napfányfürdő 水上樂園", "city": "Szeged", "category": "experience", "coordinates": [46.2523, 20.1412], "rating": 4.4, "pros": "大型戶外水樂園", "cons": "夏季人很多", "photoUrl": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800", "googleSearchUrl": g("Napfényfürdő Szeged waterpark")},
    {"id": "h-07", "name": "Reök Palace", "nameZh": "Reök Palace", "city": "Szeged", "category": "heritage", "coordinates": [46.2501, 20.1495], "rating": 4.1, "pros": "新藝術風格宮殿", "cons": "規模小", "photoUrl": "https://images.unsplash.com/photo-1551634979-2b87f74e2d2a?w=800", "googleSearchUrl": g("Reök Palace Szeged")},
    {"id": "h-08", "name": "Szeged National Theater", "nameZh": "Szeged 國家劇院", "city": "Szeged", "category": "heritage", "coordinates": [46.2521, 20.1465], "rating": 4.3, "pros": "美麗的新巴洛克建築", "cons": "沒有演出就純外觀", "photoUrl": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=800", "googleSearchUrl": g("Szeged National Theater")},
    # Pécs (4 places)
    {"id": "h-09", "name": "Pécs Catacombs (Early Christian Tomb)", "nameZh": "早期基督教墓窟 (UNESCO)", "city": "Pécs", "category": "heritage", "coordinates": [46.0703, 18.0411], "rating": 4.6, "pros": "UNESCO 世界遺產", "cons": "濕度大", "photoUrl": "https://images.unsplash.com/photo-1509281373149-e957c6296406?w=800", "googleSearchUrl": g("Pécs Catacombs UNESCO")},
    {"id": "h-10", "name": "Zsolnay Cultural Quarter", "nameZh": "Zsolnay 文化區", "city": "Pécs", "category": "experience", "coordinates": [46.0625, 18.0442], "rating": 4.5, "pros": "陶瓷藝術與創意產業區", "cons": "館內動線複雜", "photoUrl": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800", "googleSearchUrl": g("Zsolnay Cultural Quarter Pécs")},
    {"id": "h-11", "name": "Pécs Cathedral (Dóm)", "nameZh": "佩奇大教堂", "city": "Pécs", "category": "heritage", "coordinates": [46.0725, 18.0395], "rating": 4.4, "pros": "羅馬式建築，廣場美", "cons": "登頂要爬很陡的樓梯", "photoUrl": "https://images.unsplash.com/photo-1504680177321-2e6a8796ac4a?w=800", "googleSearchUrl": g("Pécs Cathedral Dóm")},
    {"id": "h-12", "name": "Pécs Mosque", "nameZh": "佩奇清真寺", "city": "Pécs", "category": "heritage", "coordinates": [46.0708, 18.0281], "rating": 4.0, "pros": "鄂圖曼時期建築", "cons": "規模不大", "photoUrl": "https://images.unsplash.com/photo-1551634979-2b87f74e2d2a?w=800", "googleSearchUrl": g("Pécs mosque former Jakovali Hassan Mosque")},
    # Lake Balaton (4 places)
    {"id": "h-13", "name": "Badacsony Volcanic Hill", "nameZh": "Badacsony 火山丘", "city": "Lake Balaton", "category": "nature", "coordinates": [46.7955, 17.5332], "rating": 4.5, "pros": "葡萄園風光，火山奇景", "cons": "交通不便需自駕", "photoUrl": "https://images.unsplash.com/photo-1500375592092-40eb2168fd21?w=800", "googleSearchUrl": g("Badacsony volcanic hill wine")},
    {"id": "h-14", "name": "Festetics Palace Keszthely", "nameZh": "Keszthely 宮殿", "city": "Lake Balaton", "category": "heritage", "coordinates": [46.7651, 17.2482], "rating": 4.4, "pros": "巨大莊園建築，展示貴族生活", "cons": "腹地大需半天", "photoUrl": "https://images.unsplash.com/photo-1567159644914-1e8f9f0b5a7a?w=800", "googleSearchUrl": g("Festetics Palace Keszthely")},
    {"id": "h-15", "name": "Tihany Abbey", "nameZh": "Tihany 修道院", "city": "Lake Balaton", "category": "heritage", "coordinates": [46.9173, 17.8925], "rating": 4.6, "pros": "美麗修道院，俯瞰湖景", "cons": "觀光客多", "photoUrl": "https://images.unsplash.com/photo-1551634979-2b87f74e2d2a?w=800", "googleSearchUrl": g("Tihany Abbey Lake Balaton")},
    {"id": "h-16", "name": "Balaton Uplands", "nameZh": "巴拉頓高原", "city": "Lake Balaton", "category": "nature", "coordinates": [46.8322, 17.6511], "rating": 4.3, "pros": "酒莊、温泉、健行步道", "cons": "幅員廣闊需要路線規劃", "photoUrl": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800", "googleSearchUrl": g("Balaton Uplands National Park")},
    # Győr (4 places)
    {"id": "h-17", "name": "Győr Basilica", "nameZh": "Győr Basilica", "city": "Győr", "category": "heritage", "coordinates": [47.6841, 17.6503], "rating": 4.5, "pros": "巴洛克美學，廣場靚", "cons": "內部一般", "photoUrl": "https://images.unsplash.com/photo-1504680177321-2e6a8796ac4a?w=800", "googleSearchUrl": g("Győr Basilica")},
    {"id": "h-18", "name": "Bishop's Castle Győr", "nameZh": "主教城堡", "city": "Győr", "category": "heritage", "coordinates": [47.6875, 17.6412], "rating": 4.3, "pros": "中世紀城堡，保存良好", "cons": "展品解說不多", "photoUrl": "https://images.unsplash.com/photo-1551892374-ecf4ce1c797d?w=800", "googleSearchUrl": g("Bishop's Castle Győr")},
    {"id": "h-19", "name": "Győr Old Town", "nameZh": "Győr 老城區", "city": "Győr", "category": "heritage", "coordinates": [47.6837, 17.6532], "rating": 4.4, "pros": "迷人的老城氛圍", "cons": "停車困難", "photoUrl": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=800", "googleSearchUrl": g("Győr old town historic center")},
    {"id": "h-20", "name": "Pannonhalma Abbey", "nameZh": "潘諾尼亞修道院", "city": "Győr", "category": "heritage", "coordinates": [47.5621, 17.8155], "rating": 4.6, "pros": "世界文化遺產，匈牙利最古老修道院", "cons": "位置偏僻", "photoUrl": "https://images.unsplash.com/photo-1504680177321-2e6a8796ac4a?w=800", "googleSearchUrl": g("Pannonhalma Abbey UNESCO")},
    # Extra Vienna hidden gems (4 more to reach 74)
    {"id": "v-21", "name": "Schönbrunn Palace", "nameZh": "熊布朗宮", "city": "Vienna", "category": "heritage", "coordinates": [48.1845, 16.3122], "rating": 4.8, "pros": "哈布斯堡王朝夏宮,花園免費", "cons": "皇宮內部門票貴", "photoUrl": "https://images.unsplash.com/photo-1567159644914-1e8f9f0b5a7a?w=800", "googleSearchUrl": g("Schönbrunn Palace Vienna")},
    {"id": "v-22", "name": "Naschmarkt Market", "nameZh": "Naschmarkt 市集", "city": "Vienna", "category": "food", "coordinates": [48.1985, 16.3632], "rating": 4.5, "pros": "維也納最大市集,各国美食", "cons": "週六跳蚤市場才熱鬧", "photoUrl": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800", "googleSearchUrl": g("Naschmarkt Vienna")},
    {"id": "v-23", "name": "Belvedere Palace", "nameZh": "貝爾維第宮", "city": "Vienna", "category": "heritage", "coordinates": [48.1918, 16.3716], "rating": 4.7, "pros": "克林姆名画「金色之雨」真迹", "cons": "遊客超多", "photoUrl": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=800", "googleSearchUrl": g("Belvedere Palace Vienna")},
    {"id": "v-24", "name": "Kunsthistorisches Museum", "nameZh": "藝術史博物館", "city": "Vienna", "category": "museum", "coordinates": [48.2038, 16.3604], "rating": 4.7, "pros": "世界重要美術館之一", "cons": "很大需要一天", "photoUrl": "https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?w=800", "googleSearchUrl": g("Kunsthistorisches Museum Vienna")},
    # Extra Budapest (to reach 74 total = 26+20+4+4+4+4+4+4+4 = 74)
    {"id": "bp-27", "name": "Gellért Hill & Citadel", "nameZh": "蓋勒特山與城堡", "city": "Budapest", "category": "viewpoint", "coordinates": [47.4852, 19.0341], "rating": 4.7, "pros": "自由女神像,全市最高點", "cons": "要爬山 20 分鐘", "photoUrl": "https://images.unsplash.com/photo-1506703719100-b0e9e25e29a2?w=800", "googleSearchUrl": g("Gellért Hill Citadel Budapest")},
    {"id": "bp-28", "name": "Hungarian Parliament Building", "nameZh": "匈牙利國會大廈", "city": "Budapest", "category": "heritage", "coordinates": [47.5076, 19.0454], "rating": 4.9, "pros": "多瑙河畔最美建築之一", "cons": "排隊很久建議預購票", "photoUrl": "https://images.unsplash.com/photo-1543946207-39bd91e70ca7?w=800", "googleSearchUrl": g("Hungarian Parliament Building Budapest")},
    {"id": "bp-29", "name": "Király Baths", "nameZh": "國王溫泉", "city": "Budapest", "category": "thermal", "coordinates": [47.5038, 19.0362], "rating": 4.3, "pros": "鄂圖曼時期溫泉,土耳其風情", "cons": "設施老舊", "photoUrl": "https://images.unsplash.com/photo-1551634979-2b87f74e2d2a?w=800", "googleSearchUrl": g("Király Bath Budapest")},
    {"id": "bp-30", "name": " Vajdahunyad Island", "nameZh": "島上的 Vajdahunyad 城堡", "city": "Budapest", "category": "heritage", "coordinates": [47.5223, 19.0791], "rating": 4.2, "pros": "城堡+自然合一,拍照效果好", "cons": "冬季關閉", "photoUrl": "https://images.unsplash.com/photo-1529655686643-1b8f9f0b5a7a?w=800", "googleSearchUrl": g("Vajdahunyad Island Budapest")},
]

# Total: 26+20+4+4+4+4+4+4+4 = 74 ✓
print(f"Total places: {len(places)}")

data = {
    "version": "1.0.0",
    "tripInfo": {
        "name": "維也納 + 匈牙利 14 天之旅",
        "dateRange": "2026-08-30 至 2026-09-12",
        "countries": ["奧地利", "匈牙利"],
        "cities": ["Budapest", "Vienna", "Debrecen", "Szeged", "Pécs", "Lake Balaton", "Győr"]
    },
    "places": places,
    "itinerary": [
        {"day": 1, "date": "2026-08-30", "city": "抵達 Budapest", "places": [], "notes": "抵達機場，市區移動，視情況安排"},
        {"day": 2, "date": "2026-08-31", "city": "布達佩斯 Day 1", "places": ["bp-28", "bp-01", "bp-16", "bp-22"], "notes": "國會大廈→聖史蒂芬教堂→猶太教堂→新紐約咖啡館"},
        {"day": 3, "date": "2026-09-01", "city": "布達佩斯 Day 2", "places": ["bp-19", "bp-26", "bp-12"], "notes": "塞切尼溫泉（建議上午去）→城市公園→Vajdahunyad 城堡"},
        {"day": 4, "date": "2026-09-02", "city": "布達佩斯 Day 3", "places": ["bp-20", "bp-14", "bp-09", "bp-25"], "notes": "布達城堡→城堡洞穴→洞穴教堂→多瑙河夜遊"},
        {"day": 5, "date": "2026-09-03", "city": "布達佩斯 Day 4", "places": ["bp-10", "bp-08", "bp-17", "bp-15"], "notes": "地鐵一號線→廢墟酒吧→猶太區街頭藝術→瑪格麗特島"},
        {"day": 6, "date": "2026-09-04", "city": "布達佩斯 Day 5", "places": ["bp-23", "bp-21", "bp-27"], "notes": "恐怖之屋博物館→A38 船→蓋勒特山看夜景"},
        {"day": 7, "date": "2026-09-05", "city": "Lake Balaton", "places": ["h-15", "h-14"], "notes": "早上移動至巴拉頓湖，Tihany 修道院→Keszthely 宮殿"},
        {"day": 8, "date": "2026-09-06", "city": "Pécs", "places": ["h-09", "h-10", "h-11"], "notes": "早期基督教墓窟（UNESCO）→Zsolnay 文化區→佩奇大教堂"},
        {"day": 9, "date": "2026-09-07", "city": "Győr / Debrecen", "places": ["h-17", "h-18", "h-01"], "notes": "Győr Basilica→主教城堡，下午移動往 Debrecen"},
        {"day": 10, "date": "2026-09-08", "city": "維也納 Day 1", "places": ["v-16", "v-21", "v-09"], "notes": "Hundertwasserhaus→熊布朗宮→Grinzing 酒館區"},
        {"day": 11, "date": "2026-09-09", "city": "維也納 Day 2", "places": ["v-07", "v-08", "v-04"], "notes": "中央公墓→Narrenturm→避孕博物館"},
        {"day": 12, "date": "2026-09-10", "city": "維也納 Day 3", "places": ["v-15", "v-18", "v-01"], "notes": "Augarten 瓷器廠→Vienna Woods 健行→Türkenschanzpark"},
        {"day": 13, "date": "2026-09-11", "city": "維也納 Day 4", "places": ["v-10", "v-13", "v-12", "v-14"], "notes": "Palais Ferstel 隱藏庭院→Ferstel Passage→Karlskirche 秘密池塘→Jewish Museum"},
        {"day": 14, "date": "2026-09-12", "city": "離開維也納", "places": ["v-23", "v-22"], "notes": "貝爾維第宮→Naschmarkt 最後採購，下午前往機場終曲"}
    ],
    "transport": {
        "flights": [
            {"from": "TPE", "to": "BUD", "date": "2026-08-30", "airline": "Turkish Airlines", "notes": "轉機一次"},
            {"from": "VIE", "to": "TPE", "date": "2026-09-12", "airline": "Eva Air", "notes": "直飛回程"}
        ],
        "trains": [
            {"route": "Budapest → Győr", "type": "MÁV", "duration": "1.5h", "cost": "€15"},
            {"route": "Győr → Pécs", "type": "MÁV", "duration": "3h", "cost": "€20"},
            {"route": "Pécs → Lake Balaton", "type": "MÁV", "duration": "1.5h", "cost": "€10"},
            {"route": "Lake Balaton → Budapest", "type": "MÁV", "duration": "2h", "cost": "€12"},
            {"route": "Budapest → Vienna", "type": "Railjet", "duration": "2.5h", "cost": "€39"}
        ],
        "carRental": {
            "recommended": True,
            "reason": "匈牙利城市間公共交通不便，建議租車自駕",
            "estimatedCost": "€350/14天"
        }
    },
    "budget": {
        "currency": "EUR",
        "total": 4500,
        "categories": {
            "flights": {"allocated": 1400, "spent": 0},
            "accommodation": {"allocated": 1200, "spent": 0},
            "food": {"allocated": 700, "spent": 0},
            "transport": {"allocated": 400, "spent": 0},
            "activities": {"allocated": 500, "spent": 0},
            "misc": {"allocated": 300, "spent": 0}
        }
    },
    "food": [
        {"name": "匈牙利燉肉 (Goulash)", "location": "Budapest", "type": "traditional", "priceRange": "€8-15", "notes": "必吃"},
        {"name": "Langos", "location": "Budapest", "type": "street", "priceRange": "€3-6", "notes": "匈牙利炸餅"},
        {"name": "新紐約咖啡館 (New York Cafe)", "location": "Budapest", "type": "fine", "priceRange": "€20-40", "notes": "世界最美咖啡館"},
        {"name": "Ruin Bar 紅白酒", "location": "Budapest", "type": "bar", "priceRange": "€4-8", "notes": "氛圍獨特"},
        {"name": "Grinzing 施照布塔", "location": "Vienna", "type": "wine", "priceRange": "€10-20", "notes": "施照布塔+脆皮肉片"},
        {"name": "Figlmüller 炸肉排", "location": "Vienna", "type": "traditional", "priceRange": "€15-25", "notes": "維也納必吃"},
        {"name": "Demel 咖啡館", "location": "Vienna", "type": "cafe", "priceRange": "€10-20", "notes": "百年咖啡館"},
        {"name": "Naschmarkt 市集", "location": "Vienna", "type": "market", "priceRange": "€5-15", "notes": "當地食材市場"}
    ],
    "todo": [
        {"id": "t-01", "task": "申請匈牙利簽證（如需）", "priority": "high", "done": False},
        {"id": "t-02", "task": "預訂機票", "priority": "high", "done": False},
        {"id": "t-03", "task": "預訂前 5 晚 Budapest 住宿", "priority": "high", "done": False},
        {"id": "t-04", "task": "預訂 Vienna 4 晚住宿", "priority": "high", "done": False},
        {"id": "t-05", "task": "租車預約（匈牙利+奧地利）", "priority": "high", "done": False},
        {"id": "t-06", "task": "購買塞切尼溫泉門票", "priority": "medium", "done": False},
        {"id": "t-07", "task": "預約多瑙河遊船", "priority": "medium", "done": False},
        {"id": "t-08", "task": "準備歐元現金", "priority": "medium", "done": False},
        {"id": "t-09", "task": "確認新手機的 Google Fi 可在歐洲使用", "priority": "high", "done": False},
        {"id": "t-10", "task": "預辦維也納博物館通行證 (Vienna Pass)", "priority": "medium", "done": False}
    ]
}

output = json.dumps(data, ensure_ascii=False, indent=2)
with open('/home/node/.openclaw/workspace/vienna-trip/src/places.json', 'w', encoding='utf-8') as f:
    f.write(output)
print("places.json written with", len(places), "places")