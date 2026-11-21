# ADR-0005 — Alleen een build zonder waarschuwingen publiceert

**Status:** aangenomen
**Datum:** 2026-11-21 (vastgelegd; de CI-volgorde bestaat sinds de eerste deploy-pijplijn)

## Context

MkDocs waarschuwt bij een ontbrekende link, een onbekende categorie, een verkeerde datumopmaak of een
niet-bestaand bestand. Die waarschuwingen zijn zichtbaar in het log en verdwijnen in de ruis zodra er
veel staan. Een deploy die "toch doorloopt" publiceert dan een pagina met een dode link, en niemand
merkt het tot een lezer erop stuit.

## Beslissing

In CI staat de volgorde vast: eerst `mkdocs build --strict` (elke waarschuwing is een fout), en pas
daarna `mkdocs gh-deploy --force`. Faalt de strict-stap, dan stopt de job en draait de deploy niet.

Lokaal is diezelfde build **geen poort** maar een waarschuwing. Wie lokaal strict wil draaien, bouwt
buiten de repo:

```bash
~/.venvs/blog/bin/mkdocs build --strict --site-dir ~/.hermes/cache/scratch/site-strict-$(date +%H%M%S)
```

## Gevolgen

- Een gewaarschuwde build publiceert niets. De site kan daardoor tijdelijk achterlopen op `main`; dat
  is de bedoeling: achterlopen is zichtbaar, een stille kapotte pagina niet.
- De lokale route blijft licht, zodat schrijven niet elke keer een blokkerende build vereist. Het
  verschil tussen lokaal en CI is bewust en staat in `CONSTRAINTS.md`, zodat niemand denkt dat een
  lokale groene build genoeg is.
- De build schrijft nooit in de repo: `site/` staat in `.gitignore` en de lokale strict-build gaat naar
  de scratch-map. Een repo met bouwuitvoer erin maakt elke diff onleesbaar.
