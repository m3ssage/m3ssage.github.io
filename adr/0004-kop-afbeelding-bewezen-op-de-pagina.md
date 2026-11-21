# ADR-0004 — De kop-afbeelding wordt bewezen op de gerenderde pagina, niet met een grep

**Status:** aangenomen
**Datum:** 2026-11-21 (vastgelegd; de correctie dateert van 2026-10-22)

## Context

Elke post heeft een kop-afbeelding nodig, en die moet met een breedte-attribuut
(`{ align=right width="250" loading=lazy }`) in de pagina staan: een vierkant beeld van 1024 px zonder
attribuut rendert paginabreed en verpest de layout.

Het oorspronkelijke bewijs was `curl -s <post-url> | grep -c glightbox ≥ 1`. Dat kon **niet falen**:
`glightbox.min.css` staat in de `<head>` van élke pagina, dus de controle gaf altijd minstens 1, ook
als de afbeelding helemaal niet gerenderd werd. Een groene check die niet kan falen is erger dan geen
check, want hij vervangt een echte meting door een geruststelling.

## Beslissing

Het bewijs is de **acceptatiespec** `tests/acceptance/publicatie.py`: die haalt de gepubliceerde pagina
op en controleert wat de lezer krijgt — titel in de `<h1>`, kop-afbeelding op `width="250"` in de
lightbox, en elk beeld in de postinhoud dat laadt (200, `image/*`). Exit 0/1/2, en de uitslag blokkeert
de "klaar"-claim.

Daarnaast zijn de dependencies in `requirements.txt` gepind op versies die dit gedrag vertonen
(`selectolax==1.0.0`); 1.0.1 laat het `<img>` op elke postpagina verdwijnen en levert een lege `<p></p>`.
Een pin hier is geen bureaucratie maar een gemeten eigenschap van de output.

## Gevolgen

- De controle meet de output, niet een naam die toevallig in de HTML voorkomt. Ze kan dus falen, en
  dat is precies de bedoeling.
- De acceptatiespec draait **ná** de deploy: een post is pas bewezen als hij live staat. Vóór de push
  dekt de inhoudspoort de frontmatter en het bestand, niet het resultaat.
- Een dependency-update in deze keten is een wijziging met bewijsplicht: eerst de spec groen, dan pas
  de versie.
