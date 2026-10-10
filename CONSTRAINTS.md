# Constraints

Last reviewed: 2026-10-10 by @eelco

## Floor (altijd, blokkerend, draait al)

- Geen secrets in de source (tokens, API-keys, wachtwoorden, private keys)
- Geen lokale home-paden in tekst, config of frontmatter
- Geen post zonder header-afbeelding, `<!-- more -->`-marker of geldige frontmatter
- Geen `date` met `+HHMM` in plaats van `+HH:MM` (harde buildfout in de blog-plugin)
- Geen suppressie-comments die een check in CI of in een poort uitzetten
- Geen gegenereerde of grote bestanden in git (`/site` en `.cache` staan in `.gitignore`)
- Dit bestand wordt niet verzwakt om een wijziging groen te krijgen

Deze floor wordt al afgedwongen door twee poorten die vóór de push draaien:

| Poort | Commando | Dekt |
|-------|----------|------|
| Inhoud | `blog-axi --changed` (exit 1 = fouten, 3 = beslissing van de gebruiker nodig) | asset-paden, frontmatter/datum, bestandsnaam, header-afbeelding, more-marker, de semantische neutraliteitspoort en de categorie-audit |
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
| Aantal posts | 50 | mag groeien, niet krimpen |
| Duur strict build | 8 s (6,5 s build) | mag niet boven ~60 s komen |
| Hygiëne-waarschuwingen (dash-stijl) | 48 over 67 bestanden | stijl, geen drempel |
| Categorie-audit (`blog-axi categorie`) | 0 fouten, 21 geaccepteerde let-op-signalen | 0 fouten mag niet stijgen |
| SEO/GEO-crawl (loop 006, `seo_geo_check.py`) | 0 site-fails, 50 pagina-fails (posts delen de site-description), benchmark 27/28 — 2026-10-10, ronde 1 | pagina-fails → 0 (elke post een eigen description), benchmark → 28/28 |
| SEO/GEO-crawl, nulmeting vóór ronde 1 | 1 site-fail (robots.txt 404), 85 pagina-fails (generator-default), benchmark 27/28 — 2026-10-10 | — |

## Uitzonderingen

| ID | Regel | Pad | Reden | Eigenaar | Verloopt |
|----|-------|-----|-------|----------|----------|
| | | | nog geen | | |
