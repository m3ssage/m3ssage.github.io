# ADR-0002 — Eén eindoordeel met vier exit-codes, in plaats van losse checks

**Status:** aangenomen
**Datum:** 2026-11-21 (vastgelegd; de werkwijze bestaat sinds de introductie van `blog-axi`)

## Context

Deze repo heeft veel controles: inhoud, hygiëne, complexiteit, strict build, de acceptatiespec. Los
afroepen werkt niet, want dan kiest de melder de controle die toevallig groen is en noemt de rest
"bekend" of "bestaand probleem". De werkelijkheid is bovendien soms onbeslist: CI loopt nog, de deploy
is nog niet zichtbaar, een semantische poort kan de dienst niet bereiken. Dat is iets anders dan goed
of fout, en het mag niet als succes gelezen worden.

## Beslissing

Er is één commando dat alles samenvoegt tot één oordeel over **deze** commit: `blog-axi klaar`. Het
draait de CI van de commit, de hygiëne, de poorten en de acceptatiespec, en kent vier uitkomsten:

| Exit | Betekenis | Wat je doet |
|---|---|---|
| 0 | Klaar | Melden dat het af is |
| 1 | Fouten | Repareren |
| 2 | Onbeslist: CI loopt nog, of de meting kon niet | **Opnieuw meten**, niet "klaar" melden |
| 3 | Beslissing voor de eigenaar | Voorleggen, niet zelf invullen |

Opties als `--sha`, `--wait`, `--interval`, `--spec-wacht` en `--spec-pogingen` bestaan om op een
lopende CI of een nog niet zichtbare deploy te wachten in plaats van te gokken.

## Gevolgen

- "Klaar" is een exit code, geen indruk. Wie 2 of 3 rapporteert als 0, liegt tegen de eigenaar zonder
  dat te willen.
- Een onbesliste meting is zichtbaar werk: het kost een tweede ronde, en dat is eerlijker dan een
  groene claim op een meting die niet is afgerond.
- Omdat het oordeel per commit is, is het antwoord reproduceerbaar: dezelfde `--sha` geeft hetzelfde
  antwoord.
