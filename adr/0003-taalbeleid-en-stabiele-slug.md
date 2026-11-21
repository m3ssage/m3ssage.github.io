# ADR-0003 — De site is Engelstalig, met een uitzondering die aan het onderwerp hangt

**Status:** aangenomen (gebruikersbesluit 2026-10-12)
**Datum:** 2026-11-21 (vastgelegd)

## Context

De site is in het Engels geschreven, maar een deel van de onderwerpen is Nederlands: wetgeving,
beleid, een Nederlands onderwerp waar de bronnen Nederlandstalig zijn. Een post daarover in het Engels
schrijven maakt hem slechter leesbaar voor de mensen over wie hij gaat; alles in het Nederlands
schrijven breekt de eenheid van de site. Er moest dus een regel komen, en een regel die te toetsen is
zonder smaakoordeel.

## Beslissing

De site is Engelstalig. Nederlands mag alleen als de post **primair over Nederland gaat**; in dat geval
volgen **titel en description** de taal van de post, draagt de post de categorie `Dutch`, en houdt hij
een **expliciete Engelse `slug:`** zodat de URL niet verandert.

Bestandsnaam, categorieën en tags blijven Engels. De taal van de body wordt deterministisch getoetst
(poort `taal`, rubriek `blog-taal`); een post over Nederland die in het Engels blijft mag, maar levert
bewust een let-op-signaal op.

## Gevolgen

- URL's zijn stabiel ongeacht de taal van de titel: de slug is Engels en expliciet, dus een latere
  vertaling of titelwijziging verschuift de URL niet en breekt geen links of zoekresultaten.
- `Dutch` is een taallabel náást de onderwerpscategorieën, geen vervanging: een Nederlandse post over
  beleid houdt zijn beleidscategorie en krijgt `Dutch` erbij.
- De grens "primair over Nederland" blijft een menselijk oordeel; de poort toetst de gevolgen
  (taal van de body, label, slug), niet de vraag of het onderwerp Nederlands genoeg is. Dat is de
  bedoelde verdeling: de machine toetst wat hij kan toetsen, de rest is een let-op-signaal.
