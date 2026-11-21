# GLOSSARY — m3ssage.github.io

De termen zoals ze in deze repo bedoeld zijn. Bedoeld voor iedereen die hier schrijft of een poort
aanpast: Hermes, het blog-profiel met zijn workers, en de eigenaar. De regels zelf staan in
`CONSTRAINTS.md`; beslissingen met een langere adem staan in `adr/`. Dit bestand herhaalt geen
drempels — het zegt alleen wat een woord betekent.

| Term | Betekenis | Waar |
|---|---|---|
| **floor** | De blokkerende regels van deze repo. Ze zijn van de eigenaar, worden door `spec-guard` beschermd en worden niet verzwakt om een wijziging groen te krijgen. | `CONSTRAINTS.md` |
| **poort** | Een geautomatiseerde controle met een exit code. Er zijn er drie soorten: vóór de push (inhoud, hygiëne), in CI (complexiteit, strict build) en ná de deploy (de acceptatiespec). | `CONSTRAINTS.md` |
| **`blog-axi`** | De AXI-poortwachter van deze repo: één commando met subcommando's `gates`, `deploy`, `klaar`, `keur-goed`, `trek-in`, `categorie` en `taal`. | `blog-axi --help` |
| **`klaar`** | Het enige eindoordeel: CI van deze commit, hygiëne, de poorten en de acceptatiespec in één uitslag. Exit **0** = klaar, **1** = fouten, **2** = onbeslist (kon niet meten), **3** = beslissing voor de eigenaar. Exit 2 is geen succes. | `blog-axi klaar` |
| **fout vs let-op-signaal** | Twee niveaus. Een **fout** blokkeert. Een **let-op-signaal** is een keuze die de eigenaar bewust accepteert, en die blijft staan tot iemand hem intrekt. | `CONSTRAINTS.md` |
| **`keur-goed`** | Een let-op-signaal accepteren met een verplichte reden; de uitslag wordt vastgelegd in `.blog-poort.yaml`. Intrekken kan met `trek-in`. | `blog-axi keur-goed <post> --reden "..."` |
| **neutraliteitspoort** | De semantische controle op partijdigheid in een post. Levert een oordeel met een drempel, en mag alleen met een expliciete reden gepasseerd worden. | poort `Inhoud` |
| **taalregel** | De deterministische controle of een post in de juiste taal staat: de site is Engelstalig, Nederlands mag alleen als de post primair over Nederland gaat. | `blog-axi taal`, rubriek `blog-taal` |
| **rubriek** | Een semantische poort in de Jev-bibliotheek (`~/.hermes/jev-rubrieken/`) met eigen voorbeelden en een drempel. `blog-taal` is er één van deze repo. | `~/.hermes/jev-rubrieken/` |
| **categorie-audit** | De controle op de categorielabels van de posts, met een fail-drempel onder 0,049; de band daarboven is een let-op-signaal. | `blog-axi categorie` |
| **`categories_allowed`** | De enige bron van toegestane categorieën, in de siteconfiguratie. Een categorie die daar niet in staat is een fout. | `mkdocs.yml` |
| **taallabel `Dutch`** | Een label náást de onderwerpscategorieën: een Nederlandse post draagt `Dutch`, een Engelse post niet. Categorieën en tags blijven verder Engels, ook bij een Nederlandse post. | `CONSTRAINTS.md`, poort `categorie` |
| **bronlabel `YouTube`** | Hetzelfde idee voor de herkomst: een post bij een videolink draagt `YouTube`. | poort `categorie` |
| **slug** | Het stabiele, Engelse stuk URL van een post. Een Nederlandse titel gaat samen met een expliciete Engelse `slug:`, zodat bestaande URL's niet verschuiven. | frontmatter, gebruikersbesluit 2026-10-12 |
| **kop-afbeelding** | De verplichte header-afbeelding van een post, altijd met breedte-attribuut (`{ align=right width="250" loading=lazy }`). Zonder attribuut rendert een vierkant beeld paginabreed. | poort `header_image`, sinds v0.7.1 |
| **more-marker** | `<!-- more -->`: de grens tussen samenvatting en body, verplicht in elke post. | poort `frontmatter` |
| **strict build** | `mkdocs build --strict`: elke waarschuwing is een fout. Blokkeert in CI vóór de deploy; lokaal is het een waarschuwing, geen poort. | CI |
| **`gh-deploy`** | `mkdocs gh-deploy --force`, de daadwerkelijke publicatie. Draait alleen als de strict-stap groen is: een gewaarschuwde build publiceert niets. | CI |
| **acceptatiespec** | De controle **ná** de deploy op wat de lezer echt krijgt: titel in de `<h1>`, kop-afbeelding op `width="250"` in de lightbox, en elk beeld in de postinhoud laadt (200, `image/*`). Exit 0/1/2. | `tests/acceptance/publicatie.py` |
| **lightbox** | De beeldvergroter van het thema (glightbox). Een postpagina hoort zijn kop-afbeelding in de lightbox te tonen; dat is meetbaar, in tegenstelling tot het aantal keren dat de CSS-naam in de pagina voorkomt. | acceptatiespec |
| **scoreboard / complexity-baseline** | De complexiteitspoort: cyclomatic complexity per blok via radon, met 10 als grens. Een bekend blok mag niet boven zijn eigen gemeten waarde groeien; een uitzondering staat met reden en getal in de baseline. | `scripts/scoreboard.py`, `scripts/complexity-baseline.json` |
| **hygiëne-poort** | De pre-push hook die zoekt naar secrets en lokale home-paden. `--dashes=off`, want streepjesgebruik is schrijfstijl en geen fout. | `.git/hooks/pre-push` |
| **`overrides/`** | De eigen aanpassingen op het Material-thema (`custom_dir`). Hier staat hoe de site rendert, niet wat erin staat. | `mkdocs.yml` |
| **gepinde dependency** | `requirements.txt` staat op versies die de site heel laten (`selectolax==1.0.0`; 1.0.1 laat het `<img>` op elke postpagina verdwijnen). Niet losjes ophogen. | `requirements.txt` |
| **`site/` en `.cache`** | Bouwuitvoer. Staan in `.gitignore` en horen nooit in een commit; bouw lokaal buiten de repo of in de gitignorde map. | `.gitignore` |

Waarom `adr/` en niet `docs/adr/`: `docs/` is de **gepubliceerde** content van de site. Een ADR hoort
in de repo, niet op het publieke blog.
