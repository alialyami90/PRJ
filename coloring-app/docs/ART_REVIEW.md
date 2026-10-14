# Art review: first import of the 72-scene pack

Imported on 14 October 2026 from the `Saudi_Colors_72_Scenes` pack with `Scripts/import_illustration.py`. All 72 pages imported without errors and every page is now in the app. No page showed a gap in its lines (a region holding two different colours), and every page is within the 18-colour limit.

What still needs fixing in the art is below. These pages work in the app today, but are harder for a small finger than the brief allows. Fix them in the SVG source (merge or enlarge the small shapes), re-export `line.png` + `color.png`, drop them into the scene's `art/` folder and run `python3 Scripts/build_scenes.py <region>` then `python3 Scripts/sync_scenes.py`.

## Redrawn pages (Najran)

The 8 Najran pages were replaced on 14 October 2026 by redrawn line art (1448×1086, line art only, no colour file), with closed eyes and cleaner lines. `Scripts/adopt_line_art.py` crops off the frame drawn around each page, scales it to 2048×1536 and colours every shape with the colour the old `color.png` had under it, since the redraws trace the old compositions. Check these pages for a shape that moved and picked up a neighbour's colour. The redraws have more shapes than the first pack (marked "redrawn" in the table below).

## Too many shapes (43 pages over the 90-region limit)

Sorted from busiest. Paint by Number on these pages means a lot of small numbers.

| Page | Pack id | Regions | Also |
|---|---|---|---|
| asir/flower-men: Flower-men of Rijal Almaa wearing herb crowns on a mountain path | asir_01 | 208 |  |
| najran/tower-houses-harvest: Date harvest among Najran mudbrick tower houses | najran_07 | 185 | redrawn |
| jazan/fifa-mountains: Terraced Fifa Mountains with a village on the peak | jazan_02 | 179 |  |
| al-ahsa/qaisariah-souq: Lantern-lit Qaisariah Souq with cloth and spice stalls | al_ahsa_02 | 167 |  |
| najran/palm-basket-workshop: Palm-leaf basket workshop in Aba Al-Saud souq | najran_02 | 163 | redrawn |
| asir/asir-market: Tuesday market with pottery, baskets and spices | asir_08 | 162 |  |
| jazan/coffee-terraces: Coffee farmers picking beans on mountain terraces | jazan_04 | 161 | heavy outline (20%+ of the page is black) |
| hail/qishlah-palace: Horse parade in front of Al-Qishlah Palace | hail_06 | 157 |  |
| hail/hail-rally: Desert rally cars and buggies jumping over dunes | hail_03 | 150 |  |
| asir/honey-bees: Beekeeper collecting Sidr honey in the mountains | asir_06 | 148 |  |
| najran/al-aan-palace: Al-Aan Palace above the palm-filled valley | najran_01 | 143 | redrawn |
| al-ahsa/hofuf-train: Old Hofuf railway station with a steam train arriving | al_ahsa_08 | 140 |  |
| tabuk/hejaz-railway: Old Hejaz Railway station and locomotive | tabuk_03 | 140 |  |
| najran/courtyard-bread: Traditional bread and hospitality in a Najrani courtyard | najran_08 | 137 | redrawn |
| hail/hail-farm: Wheat and peach farms with tractors | hail_07 | 135 |  |
| al-ahsa/ibrahim-palace: Horse riders at Ibrahim Palace | al_ahsa_07 | 131 | heavy outline (20%+ of the page is black) |
| najran/al-ukhdood: Young explorers at Al-Ukhdood archaeological site | najran_03 | 130 | redrawn |
| jeddah/corniche-fountain: Kids on the Corniche watching King Fahd's Fountain and boats | jeddah_02 | 129 |  |
| najran/najrani-pottery: Potter making a traditional Najrani coffee pot | najran_05 | 128 | redrawn |
| jazan/jazan-port: Jazan port with cargo ships and cranes | jazan_06 | 122 |  |
| asir/stone-village: Stone tower houses of Rijal Almaa village | asir_07 | 120 |  |
| asir/al-qatt-houses: Painting colorful Al-Qatt Al-Asiri patterns on a house | asir_02 | 119 |  |
| jazan/sabya-market: Market day with jasmine garlands and fuul pots | jazan_07 | 119 |  |
| jazan/heritage-village: Jazan heritage village with straw-roofed huts | jazan_05 | 117 |  |
| riyadh/riyadh-season-fair: Ferris wheel and fireworks at a Riyadh Season fair | riyadh_05 | 115 |  |
| jeddah/dhow-sail: Traditional dhow sailing past the city at sunset | jeddah_06 | 114 |  |
| jazan/mangroves: Kayaking through the mangrove forests | jazan_08 | 111 |  |
| al-ahsa/palm-oasis: Date harvest in the world's largest palm oasis | al_ahsa_01 | 109 |  |
| riyadh/masmak-fort: Boys on camels racing past Masmak Fort at sunset | riyadh_01 | 109 |  |
| riyadh/ardah-dance: Ardah sword-dance celebration with drummers and flags | riyadh_03 | 108 |  |
| najran/hima-rock-art: Hima rock-art discovery | najran_04 | 108 | redrawn |
| najran/najran-dam: Family outing at the Najran dam overlook | najran_06 | 108 | redrawn |
| tabuk/neom-future: Futuristic coastal city with flying taxis | tabuk_08 | 107 |  |
| tabuk/tabuk-castle: Tabuk Castle with pilgrims and their camels | tabuk_04 | 104 |  |
| hail/hatim-tai: Hatim Al-Tai welcoming guests with a feast of generosity | hail_05 | 103 |  |
| jeddah/hijazi-wedding: Hijazi wedding with mizmar dancers and lanterns | jeddah_07 | 103 |  |
| tabuk/snow-mountain: Rare snow day on Jabal Al-Lawz with kids making a snowman | tabuk_06 | 100 |  |
| jeddah/jeddah-sculptures: Playing among the giant sculptures of the Corniche | jeddah_05 | 97 |  |
| riyadh/camel-festival: Decorated camels at a camel beauty festival | riyadh_08 | 97 |  |
| alula/old-town-alula: Old Town mud houses and the hilltop castle | alula_03 | 96 |  |
| asir/baboons-road: Baboons watching cars on the mountain road | asir_05 | 95 |  |
| hail/aarif-fort: Aarif Fort on the hill above the old town | hail_02 | 91 |  |
| tabuk/wadi-disah: Wadi Al-Disah canyon with palms and a river | tabuk_05 | 91 |  |

## Heavy outlines (2 pages)

20% or more of the page is black line, counting tiny dark shapes drawn as ink; the page reads as dark and busy.

| Page | Pack id |
|---|---|
| al-ahsa/ibrahim-palace: Horse riders at Ibrahim Palace | al_ahsa_07 |
| jazan/coffee-terraces: Coffee farmers picking beans on mountain terraces | jazan_04 |

## Small shapes (every page)

Every page has shapes under 1,200 px (about 40×40) that are too small for a child to tap on their own. The importer handles each one in this order:

1. It joins a fillable shape of the same colour (in `color.png`) within 30 px, so it colours with that shape, like a bit of leaf between two stems.
2. If it is dark, it is drawn as solid ink, like hair or a shoe.
3. If it is light, it stays paper white, like teeth or the shine in an eye.

The shine on a pupil is often left open to the face in the line art, so it would have taken the face's colour. The importer keeps narrow white gaps beside solid black (pupils, hair, mouths) white too. Pages listing 40 or more shapes that could not join a neighbour are the ones to check first for faces or patterns that look odd.

| Page | Shapes drawn as ink or left white |
|---|---|
| jazan/coffee-terraces | 53 |
| jazan/sabya-market | 51 |

## Not checked by the importer

The importer checks shapes and colours, not meaning. Before marking a scene `approved` in its `region.json`, look at it in the app for: two objects joined into one fillable shape, landmark and costume accuracy (the pack's README notes no reference photos were used), and the interpretive scenes the pack calls out (Tabuk future city, Hofuf steam train, Hatim Al-Tai, the Aarif Fort bell).
