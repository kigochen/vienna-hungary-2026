const fs = require('fs');
const data = JSON.parse(fs.readFileSync('places.json','utf8'));
console.log('Total places:', data.places.length);
const missingMapsUrl = data.places.filter(p => !p.mapsUrl);
console.log('Places without mapsUrl:', missingMapsUrl.length);
if (missingMapsUrl.length > 0) {
  missingMapsUrl.forEach(p => console.log('  - ' + p.id + ': ' + p.nameZh));
}