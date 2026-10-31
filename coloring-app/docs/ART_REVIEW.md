# Art review: the new line art (31 October 2026)

On 31 October 2026 every page was replaced by the owner's new line art (1448×1086, black lines only, no colour file), 8 regions × 8 pages; Tabuk was dropped from the app. Najran's line art was already in the app and is unchanged; only its colours were corrected.

## How the pages were coloured

The new drawings carry no colours, and Paint by Number needs every shape to have the right one. Each page was coloured by looking at what it shows (sky, sand, walls, faces and hands, thobes and shemaghs, animals, water, plants) and recording it in the scene's `art/paint.json`, which `Scripts/paint_shapes.py` turns into `art/color.png`:

- New compositions (all of Riyadh, plus Al-Ahsa's palm oasis and Hofuf train) were painted from a blank page.
- Redraws that trace the old composition (every other page) started from the old page's colours carried over by position (`Scripts/adopt_line_art.py`) with `"keep": true`, and every shape whose colour did not fit the picture was repainted.

Then `Scripts/import_illustration.py` builds the scene as before. No page has a gap in its lines (a shape holding two colours) and every page is within 18 colours.

The importer now keeps a small shape (300 to 1,200 px) as its own region when it is painted a clear colour and no same-coloured shape is close enough to join, so small hands, fists and kite bows no longer turn white. Smaller shapes, and small shapes painted white or near black, still become paper or ink.

## Things to look at in the app before approving

- hegra-tombs: the guide's face and the left drape of his shemagh are one shape in the line art, so the drape is skin coloured.
- riyadh-season-fair: a gap in the lines joins the first boy's hoodie to a bush, so both are green.
- date-market: the boy's right shoe shares a shape with the ground, so his shoes are sand coloured.
- mangroves: in the dense root tangle some gaps between roots are brown rather than water.
- tower-houses-harvest: the far hills and a small palm's leaves are one shape, so both are light green.
- palm-basket-workshop: the bottom-left bowl is the same shape as the floor.
- jubbah-rock-art: the ibex carving's outline is open into the cliff, so it cannot be coloured on its own.
- The night pages (elephant-rock, star-gazing, hijazi-wedding) use a navy sky; falconry uses a dawn peach sky; dhow-sail a sunset sky.

## Too many shapes (57 pages over the 90-region guide)

The new drawings are more detailed than the brief's 25 to 90 shapes. Paint by Number on these pages means a lot of small numbers; zoom helps.

| Page | Regions | Colours |
|---|---|---|
| asir/flower-men: Flower-men of Rijal Almaa wearing herb crowns on a mountain path | 255 | 15 |
| asir/stone-village: Stone tower houses of Rijal Almaa village | 230 | 13 |
| jazan/fifa-mountains: Terraced Fifa Mountains with a village on the peak | 229 | 16 |
| najran/tower-houses-harvest: Date harvest among Najran mudbrick tower houses | 205 | 15 |
| hail/qishlah-palace: Horse parade in front of Al-Qishlah Palace | 200 | 15 |
| asir/asir-market: Tuesday market with pottery, baskets and spices | 195 | 15 |
| jazan/coffee-terraces: Coffee farmers picking beans on mountain terraces | 191 | 17 |
| jeddah/hijazi-wedding: Hijazi wedding with mizmar dancers and lanterns | 190 | 16 |
| hail/hail-farm: Wheat and peach farms with tractors | 185 | 16 |
| al-ahsa/qaisariah-souq: Lantern-lit Qaisariah Souq with cloth and spice stalls | 183 | 14 |
| jazan/mangroves: Kayaking through the mangrove forests | 179 | 18 |
| al-ahsa/palm-oasis: Date harvest in the world's largest palm oasis | 177 | 16 |
| najran/palm-basket-workshop: Palm-leaf basket workshop in Aba Al-Saud souq | 172 | 11 |
| hail/hail-rally: Desert rally cars and buggies jumping over dunes | 168 | 12 |
| riyadh/date-market: A date-market merchant and children with bowls of dates | 161 | 15 |
| al-ahsa/bisht-weaving: Bisht cloak weavers at work with golden thread | 156 | 11 |
| jazan/sabya-market: Market day with jasmine garlands and fuul pots | 155 | 14 |
| al-ahsa/ibrahim-palace: Horse riders at Ibrahim Palace | 154 | 12 |
| hail/hatim-tai: Hatim Al-Tai welcoming guests with a feast of generosity | 152 | 15 |
| asir/honey-bees: Beekeeper collecting Sidr honey in the mountains | 151 | 12 |
| jeddah/al-balad-rawashin: Old Jeddah street with wooden rawashin balconies and cats | 150 | 12 |
| najran/al-aan-palace: Al-Aan Palace above the palm-filled valley | 150 | 11 |
| alula/maraya-mirror: Maraya mirror building reflecting the desert | 147 | 16 |
| jeddah/corniche-fountain: Kids on the Corniche watching King Fahd's Fountain and boats | 145 | 14 |
| najran/courtyard-bread: Traditional bread and hospitality in a Najrani courtyard | 142 | 13 |
| riyadh/masmak-fort: Three boys riding camels past Masmak Fort | 142 | 14 |
| al-ahsa/hofuf-train: Hofuf railway station with a modern passenger train arriving | 141 | 15 |
| asir/al-qatt-houses: Painting colorful Al-Qatt Al-Asiri patterns on a house | 141 | 16 |
| jazan/jazan-port: Jazan port with cargo ships and cranes | 139 | 17 |
| najran/al-ukhdood: Young explorers at Al-Ukhdood archaeological site | 135 | 13 |
| riyadh/kingdom-tower-skyline: Children flying kites beside the Riyadh skyline | 135 | 17 |
| asir/abha-fog: Foggy terraces of Abha with sheep and a shepherd | 133 | 13 |
| jazan/heritage-village: Jazan heritage village with straw-roofed huts | 133 | 16 |
| najran/najrani-pottery: Potter making a traditional Najrani coffee pot | 133 | 11 |
| asir/cable-car: Cable car over green mountains to Al-Souda | 126 | 16 |
| jeddah/dhow-sail: Traditional dhow sailing past the city at sunset | 124 | 11 |
| riyadh/riyadh-season-fair: Children with cotton candy at a Riyadh Season funfair | 119 | 17 |
| alula/oasis-walk: Shaded palm oasis walk with a stream and frogs | 116 | 16 |
| riyadh/camel-festival: Children meeting a decorated camel and its handler | 115 | 16 |
| najran/najran-dam: Family outing at the Najran dam overlook | 114 | 14 |
| alula/hegra-tombs: Camel caravan passing the carved tombs of Hegra | 113 | 14 |
| najran/hima-rock-art: Hima rock-art discovery | 113 | 15 |
| alula/hot-air-balloons: Hot-air balloons floating over sandstone canyons | 112 | 13 |
| alula/old-town-alula: Old Town mud houses and the hilltop castle | 112 | 13 |
| riyadh/ardah-dance: Ardah sword-dance celebration with two drummers | 110 | 15 |
| riyadh/desert-picnic: Falconry and a family picnic at a desert camp | 109 | 17 |
| hail/aarif-fort: Aarif Fort on the hill above the old town | 108 | 14 |
| jeddah/jeddah-sculptures: Playing among the giant sculptures of the Corniche | 106 | 16 |
| al-ahsa/al-ahsa-pottery: Potter's workshop with children shaping clay jars | 105 | 13 |
| jazan/mango-harvest: Mango harvest at a Jazan farm | 104 | 18 |
| alula/elephant-rock: Family picnic under Elephant Rock at night with stars | 103 | 15 |
| hail/jubbah-rock-art: Children discovering ancient rock carvings at Jubbah | 102 | 14 |
| riyadh/diriyah-mudbrick: A family visiting the adobe alleys of Diriyah | 99 | 16 |
| jeddah/red-sea-reef: Snorkelers above a Red Sea coral reef full of fish | 95 | 14 |
| al-ahsa/jabal-qarah-caves: Kids exploring the cool caves of Jabal Al-Qarah | 94 | 14 |
| al-ahsa/yellow-lake: Birds and reeds at Al-Asfar (Yellow) Lake | 93 | 13 |
| jeddah/floating-mosque: Floating Mosque by the sea with pelicans | 93 | 13 |

## Small shapes (every page)

Every page has shapes under 1,200 px (about 40×40) that are too small for a child to tap on their own. The importer handles each one in this order:

1. It joins a fillable shape of the same colour (in `color.png`) within 30 px, so it colours with that shape, like a bit of leaf between two stems.
2. If it is painted a clear colour and is at least 300 px, it stays a small region of its own, like a hand or a kite bow.
3. If it is dark, it is drawn as solid ink, like hair or a shoe.
4. If it is light, it stays paper white, like teeth or the shine in an eye.

The shine on a pupil is often left open to the face in the line art, so it would have taken the face's colour. The importer keeps narrow white gaps beside solid black (pupils, hair, mouths) white too.

## Not checked by the importer

The importer checks shapes and colours, not meaning. Before marking a scene `approved` in its `region.json`, look at it in the app for two objects joined into one fillable shape and for landmark and costume accuracy.
