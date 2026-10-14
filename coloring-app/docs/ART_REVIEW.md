# Art review: first import of the 72-scene pack

Imported on 14 October 2026 from the `Saudi_Colors_72_Scenes` pack with `Scripts/import_illustration.py`. All 72 pages imported without errors and every page is now in the app. No page showed a gap in its lines (a region holding two different colours), and every page is within the 18-colour limit.

What still needs fixing in the art is below. These pages work in the app today, but are harder for a small finger than the brief allows. Fix them in the SVG source (merge or enlarge the small shapes), re-export `line.png` + `color.png`, drop them into the scene's `art/` folder and run `python3 Scripts/build_scenes.py <region>` then `python3 Scripts/sync_scenes.py`.

## Too many shapes (42 pages over the 90-region limit)

Sorted from busiest. Paint by Number on these pages means a lot of small numbers.

| Page | Pack id | Regions | Also |
|---|---|---|---|
| asir/flower-men: Flower-men of Rijal Almaa wearing herb crowns on a mountain path | asir_01 | 208 | heavy outline (20%+ of the page is black) |
| jazan/fifa-mountains: Terraced Fifa Mountains with a village on the peak | jazan_02 | 179 | heavy outline (20%+ of the page is black) |
| al-ahsa/qaisariah-souq: Lantern-lit Qaisariah Souq with cloth and spice stalls | al_ahsa_02 | 167 |  |
| asir/asir-market: Tuesday market with pottery, baskets and spices | asir_08 | 162 |  |
| jazan/coffee-terraces: Coffee farmers picking beans on mountain terraces | jazan_04 | 161 | heavy outline (20%+ of the page is black) |
| hail/qishlah-palace: Horse parade in front of Al-Qishlah Palace | hail_06 | 157 |  |
| hail/hail-rally: Desert rally cars and buggies jumping over dunes | hail_03 | 150 |  |
| asir/honey-bees: Beekeeper collecting Sidr honey in the mountains | asir_06 | 148 |  |
| najran/tower-houses-harvest: Date harvest among Najran mudbrick tower houses | najran_07 | 141 |  |
| al-ahsa/hofuf-train: Old Hofuf railway station with a steam train arriving | al_ahsa_08 | 140 |  |
| tabuk/hejaz-railway: Old Hejaz Railway station and locomotive | tabuk_03 | 140 |  |
| najran/courtyard-bread: Traditional bread and hospitality in a Najrani courtyard | najran_08 | 137 |  |
| hail/hail-farm: Wheat and peach farms with tractors | hail_07 | 135 |  |
| al-ahsa/ibrahim-palace: Horse riders at Ibrahim Palace | al_ahsa_07 | 131 | heavy outline (20%+ of the page is black) |
| jeddah/corniche-fountain: Kids on the Corniche watching King Fahd's Fountain and boats | jeddah_02 | 129 |  |
| najran/palm-basket-workshop: Palm-leaf basket workshop in Aba Al-Saud souq | najran_02 | 126 |  |
| jazan/jazan-port: Jazan port with cargo ships and cranes | jazan_06 | 122 |  |
| asir/stone-village: Stone tower houses of Rijal Almaa village | asir_07 | 120 |  |
| asir/al-qatt-houses: Painting colorful Al-Qatt Al-Asiri patterns on a house | asir_02 | 119 |  |
| jazan/sabya-market: Market day with jasmine garlands and fuul pots | jazan_07 | 119 |  |
| jazan/heritage-village: Jazan heritage village with straw-roofed huts | jazan_05 | 117 |  |
| riyadh/riyadh-season-fair: Ferris wheel and fireworks at a Riyadh Season fair | riyadh_05 | 115 |  |
| jeddah/dhow-sail: Traditional dhow sailing past the city at sunset | jeddah_06 | 114 |  |
| jazan/mangroves: Kayaking through the mangrove forests | jazan_08 | 111 |  |
| najran/al-ukhdood: Young explorers at Al-Ukhdood archaeological site | najran_03 | 110 |  |
| al-ahsa/palm-oasis: Date harvest in the world's largest palm oasis | al_ahsa_01 | 109 |  |
| riyadh/masmak-fort: Boys on camels racing past Masmak Fort at sunset | riyadh_01 | 109 |  |
| riyadh/ardah-dance: Ardah sword-dance celebration with drummers and flags | riyadh_03 | 108 |  |
| tabuk/neom-future: Futuristic coastal city with flying taxis | tabuk_08 | 107 |  |
| najran/najrani-pottery: Potter making a traditional Najrani coffee pot | najran_05 | 106 |  |
| tabuk/tabuk-castle: Tabuk Castle with pilgrims and their camels | tabuk_04 | 104 |  |
| hail/hatim-tai: Hatim Al-Tai welcoming guests with a feast of generosity | hail_05 | 103 |  |
| jeddah/hijazi-wedding: Hijazi wedding with mizmar dancers and lanterns | jeddah_07 | 103 |  |
| najran/hima-rock-art: Hima rock-art discovery | najran_04 | 101 |  |
| tabuk/snow-mountain: Rare snow day on Jabal Al-Lawz with kids making a snowman | tabuk_06 | 100 |  |
| najran/najran-dam: Family outing at the Najran dam overlook | najran_06 | 98 |  |
| jeddah/jeddah-sculptures: Playing among the giant sculptures of the Corniche | jeddah_05 | 97 |  |
| riyadh/camel-festival: Decorated camels at a camel beauty festival | riyadh_08 | 97 |  |
| alula/old-town-alula: Old Town mud houses and the hilltop castle | alula_03 | 96 |  |
| asir/baboons-road: Baboons watching cars on the mountain road | asir_05 | 95 |  |
| hail/aarif-fort: Aarif Fort on the hill above the old town | hail_02 | 91 |  |
| tabuk/wadi-disah: Wadi Al-Disah canyon with palms and a river | tabuk_05 | 91 |  |

## Heavy outlines (4 pages)

20% or more of the page is black line. Usually many tiny shapes that were burned into the outline; the page reads as dark and busy.

| Page | Pack id |
|---|---|
| al-ahsa/ibrahim-palace: Horse riders at Ibrahim Palace | al_ahsa_07 |
| asir/flower-men: Flower-men of Rijal Almaa wearing herb crowns on a mountain path | asir_01 |
| jazan/coffee-terraces: Coffee farmers picking beans on mountain terraces | jazan_04 |
| jazan/fifa-mountains: Terraced Fifa Mountains with a village on the peak | jazan_02 |

## Small shapes drawn as ink (every page)

Every page has shapes under 1,200 px (about 40×40) that the importer fills solid black so a child can never miss-tap them: eyes, fingers, small window panes, palm-leaf tips. That is the intended behaviour, but where a page lists 40 or more, details like faces or patterns may have turned into black blobs; check those first.

| Page | Shapes inked |
|---|---|
| asir/flower-men | 93 |
| jazan/coffee-terraces | 90 |
| hail/qishlah-palace | 85 |
| jazan/fifa-mountains | 79 |
| najran/tower-houses-harvest | 77 |
| hail/hail-rally | 66 |
| jazan/sabya-market | 65 |
| tabuk/hejaz-railway | 60 |
| al-ahsa/ibrahim-palace | 58 |
| jeddah/hijazi-wedding | 53 |
| jazan/mangroves | 51 |
| jeddah/al-balad-rawashin | 51 |
| al-ahsa/palm-oasis | 50 |
| al-ahsa/hofuf-train | 49 |
| riyadh/masmak-fort | 46 |
| najran/al-aan-palace | 43 |
| jeddah/corniche-fountain | 42 |
| asir/honey-bees | 41 |
| hail/hail-farm | 40 |
| jazan/farasan-islands | 40 |
| jeddah/dhow-sail | 40 |
| najran/palm-basket-workshop | 40 |

## Not checked by the importer

The importer checks shapes and colours, not meaning. Before marking a scene `approved` in its `region.json`, look at it in the app for: two objects joined into one fillable shape, landmark and costume accuracy (the pack's README notes no reference photos were used), and the interpretive scenes the pack calls out (Tabuk future city, Hofuf steam train, Hatim Al-Tai, the Aarif Fort bell).
