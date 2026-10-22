# Acceptatiespec: de post staat live en rendert

Eén artefact dat specificatie én validatie is. De scenario's staan in de taal van het probleem (een lezer
opent een post), niet in de taal van de oplossing — geen plugin, geen MkDocs-internals, geen bestandsnamen
van de implementatie. Daarom kan de site anders gebouwd worden zonder dat deze spec verandert, en kan een
scenario alleen rood worden als de lezer iets mist.

## Draaien

```bash
python3 tests/acceptance/publicatie.py                    # de nieuwste post
python3 tests/acceptance/publicatie.py --post docs/blog/posts/<post>.md
python3 tests/acceptance/publicatie.py --json             # machineleesbaar
python3 tests/acceptance/publicatie.py --site file:///tmp/kopie   # offline tegen een kopie
python3 tests/acceptance/rood_bewijs.py                   # bewijst dat de spec kán falen
```

Exit **0** = groen, **1** = minstens één scenario rood, **2** = kon niet lopen (geen sitemap, geen posts).
Een scenario dat zijn eigen onvermogen niet kan meten (pagina onbereikbaar) telt **rood**, niet grijs.

## De vier lagen

| Laag | In dit bestand | Wat het doet |
|---|---|---|
| testcases | `scenario_*` | Given/When/Then, één eigenschap per scenario |
| DSL | `resolve`, `header_image`, `rendered_header`, `article_images` | domeinoperaties: "de pagina is deze post", "de kop-afbeelding rendert" |
| protocol-drivers | `fetch`, `sitemap_paths`, `frontmatter` | praten met de echte site en de echte repo |
| systeem onder test | `https://pages.bommel.xyz` | MkDocs + GitHub Pages |

De URL komt uit `sitemap.xml`, niet uit de bestandsnaam: de slug is een eigenschap van de plugin, en een
spec die de plugin nabouwt breekt zodra de plugin verandert.

## De drie scenario's, en wat elk als enige vangt

1. **De pagina is deze post** — de sitemap heeft een pagina onder de datum van de post en de `<h1>` is de
   titelfrontmatter. Vangt: niet gedeployd, een mislukte build, een verkeerde slug, een pagina die een
   andere post toont.
2. **De kop-afbeelding rendert** — direct onder de `<h1>`, met het pad uit de markdown, `width="250"` en in
   de lightbox-wrapper. Vangt: de dependency-regressie uit `CONSTRAINTS.md` (`selectolax` 1.0.1 liet het
   `<img>` verdwijnen), een ontbrekend breedte-attribuut (beeld rendert paginabreed), een omgezet pad.
3. **Elke afbeelding in de postinhoud laadt** — per `src` in het artikelgebied een echte GET: status 200,
   content-type `image/*` en niet leeg. Vangt: een hernoemd of niet-geüpload asset, een afgekapt bestand.
   Scenario 2 kan hier niet bij: de `<img>`-tag kan perfect zijn terwijl het bestand 404 geeft.

Wat de spec **niet** dekt: of de tekst klopt (dat is `blog-axi` plus de leesbaarheidspas), of de index de
post toont (die toont 10 posts per pagina, dus een index-check wordt om de verkeerde reden rood), en of de
post inhoudelijk neutraal is (Jev-poort in `blog-axi`).

## Het rood-bewijs

`rood_bewijs.py` haalt de nieuwste pagina op, plant drie echte fouten in een wegwerpkopie en eist dat de
spec precies het juiste scenario laat vallen:

| geval | mutatie | verwacht |
|---|---|---|
| groen | geen | exit 0, 3× PASS |
| a | lightbox-wrapper en `width` weg | exit 1, scenario 2 rood |
| b | asset-bestand weg | exit 1, scenario 3 rood |
| c | post niet in de sitemap | exit 1, scenario 1 rood (2 en 3 kunnen niets beoordelen) |

Exit 0 betekent: de spec is in staat een fout antwoord te vangen. Zonder die stap is een groene spec een
wens. Draai hem na elke wijziging aan de spec zelf.

## Contractwijziging

De scenario's en hun drempels zijn het contract. Wie ze aanpast omdat een post ze niet haalt, verzwakt de
spec om groen te worden — precies wat `CONSTRAINTS.md` verbiedt. Een verwachting aanpassen (een extra
scenario, een strengere drempel) is een beslissing van de eigenaar, met de reden in de commit.
