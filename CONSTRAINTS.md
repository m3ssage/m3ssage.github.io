# Constraints

Last reviewed: 2026-10-12 by @eelco

## Floor (altijd, blokkerend, draait al)

- Geen secrets in de source (tokens, API-keys, wachtwoorden, private keys)
- Geen lokale home-paden in tekst, config of frontmatter
- Geen post zonder header-afbeelding, `<!-- more -->`-marker of geldige frontmatter
- Geen `date` met `+HHMM` in plaats van `+HH:MM` (harde buildfout in de blog-plugin)
- Geen suppressie-comments die een check in CI of in een poort uitzetten
- Geen Nederlandstalige post zonder Nederlands onderwerp: de site is Engelstalig, Nederlands mag
  alleen als de post primair over Nederland gaat (poort `taal`, rubriek `blog-taal`)
- Categorieën komen uit `categories_allowed` in `mkdocs.yml`, en categorieën en tags blijven Engels
  ook als de post Nederlands is (de `frontmatter`-poort controleert de categorielijst)
- Een post in het Nederlands draagt de categorie `Dutch`, een Engelse post niet: `Dutch` is een
  taallabel naast de onderwerpscategorieën, deterministisch getoetst op de taal van de body in de
  `categorie`-poort (`blog-axi`, net als het bronlabel `YouTube` bij de videolink)
- Van een Nederlandse post volgen **titel** en **description** de taal van de post; een Nederlandse
  titel gaat samen met een expliciete Engelse `slug:` in de frontmatter, zodat de URL niet verandert
  (gebruikersbesluit 2026-10-12). Bestandsnaam, categorieën en tags blijven Engels
- Geen gegenereerde of grote bestanden in git (`/site` en `.cache` staan in `.gitignore`)
- Dit bestand wordt niet verzwakt om een wijziging groen te krijgen

Deze floor wordt al afgedwongen door twee poorten die vóór de push draaien:

| Poort | Commando | Dekt |
|-------|----------|------|
| Inhoud | `blog-axi --changed` (exit 1 = fouten, 3 = beslissing van de gebruiker nodig) | asset-paden, frontmatter/datum, bestandsnaam, header-afbeelding, more-marker, de semantische neutraliteitspoort, de categorie-audit en de taalregel |
| Hygiëne | `.git/hooks/pre-push` → `python3 ~/.hermes/scripts/publicatie_hygiene.py --quiet --dashes=off` | secrets en lokale home-paden |

Em/en-dashes zijn schrijfstijl, geen fout: daarom `--dashes=off` (gemeten 2026-10-07: 349 in `docs/`).

## Afgedwongen met getallen

| Dimensie | Regel | Gecontroleerd door | Loopt bij |
|----------|-------|--------------------|-----------|
| Build | 0 warnings en een geslaagde build | `mkdocs build --strict` | CI, vóór de deploy (blokkerend) |
| Publiceren | Alleen een groene build komt op de site | `mkdocs gh-deploy --force` na de strict-stap | CI |

Faalt de strict-stap, dan stopt de CI-job en draait `gh-deploy` niet meer: een gewaarschuwde build
publiceert dus niets. Lokaal is diezelfde build een waarschuwing en geen poort:
`~/.venvs/blog/bin/mkdocs build --strict --site-dir ~/.hermes/cache/scratch/site-strict-$(date +%H%M%S)`
(bouw buiten de repo, of naar de gitignorde `site/`). De twee poorten hierboven blijven de enige
blokkerende checks op deze host.

## Gemeten, nog niet afgedwongen

| Metriek | Vandaag | Richting |
|---------|---------|----------|
| Aantal posts | 52 | mag groeien, niet krimpen |
| Duur strict build | 8 s (6,5 s build) | mag niet boven ~60 s komen |
| Hygiëne-waarschuwingen (dash-stijl) | 48 over 67 bestanden | stijl, geen drempel |
| Categorie-audit (`blog-axi categorie`) | 0 fouten, 24 let-op-signalen over 52 posts (gemeten 2026-10-12, met het 13e label `Dutch` en de fail-drempel op **0,049**) | 0 fouten houden; de 0,05–0,30-band en de twee `bronlabel_ontbreekt`-gevallen blijven geaccepteerde keuzes |
| SEO/GEO-crawl (loop 006, `seo_geo_check.py`) | 0 fails (0 site, 0 pagina), benchmark 27/28 — 2026-10-10, ronde 2 (50 post-descriptions + `llms.txt`) | 0 fails houden; volgende notes: JSON-LD, `og:type=article`, de "Index"-titels van lijstpagina's |
| SEO/GEO-crawl, ronde 1 | 0 site-fails, 50 pagina-fails (posts deelden de site-description), benchmark 27/28 — 2026-10-10 (`6fd6a0e`) | — |
| SEO/GEO-crawl, nulmeting | 1 site-fail (`robots.txt` 404), 85 pagina-fails (generator-default), benchmark 27/28 — 2026-10-10 | — |
| Neutraliteitspoort | 2× let-op, 0 fouten (`2025-07-19-184.md`, `2025-07-28-276.md`), beide **goedgekeurd door de gebruiker op 2026-10-10** (`.blog-poort.yaml`) — gemeten over alle 50 posts | nieuwe let-op-signalen blijven een keuze van de gebruiker: `blog-axi keur-goed <post> --reden "..."` of de post aanpassen |
| Taalregel (`blog-axi taal`) | 0 fouten, 3 let-op-signalen; 10 van de 52 posts gaan over Nederland en die 10 staan in het Nederlands (gemeten 2026-10-12 na de vertaalronde, ≈$0,005) | 0 fouten houden; een post over Nederland mag in het Engels blijven, maar dan staat er bewust een let-op-signaal |

## Uitzonderingen

| ID | Regel | Pad | Reden | Eigenaar | Verloopt |
|----|-------|-----|-------|----------|----------|
| | | | nog geen | | |
