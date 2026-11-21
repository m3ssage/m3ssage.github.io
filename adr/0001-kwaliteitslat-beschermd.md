# ADR-0001 — De kwaliteitslat staat in een bestand van de eigenaar, en dat wordt niet verzwakt

**Status:** aangenomen
**Datum:** 2026-11-21 (vastgelegd; de werkwijze bestaat sinds de invoering van `CONSTRAINTS.md`)

## Context

Een agent onder druk doet wat het snelst groen maakt. Zonder bescherming verdwijnt een regel die in de
weg zit, of wordt een drempel net zo lang verlaagd tot de wijziging erdoor is. Dan is de poort geen
lat meer maar een formaliteit, en is de kwaliteit van de site een optelsom van wat elke sessie
toevallig toestond.

## Beslissing

De blokkerende regels staan in `CONSTRAINTS.md`, een bestand van de eigenaar, en dat bestand is met de
gate `spec-guard` beschermd tegen stilzwijgende wijziging. De regel staat er letterlijk: *dit bestand
wordt niet verzwakt om een wijziging groen te krijgen*. Een te strenge poort is een gesprek, geen
wijziging.

Waar een uitzondering toch nodig is, krijgt hij een eigen plek met bewijs: in
`scripts/complexity-baseline.json` staat per uitzondering de reden én de gemeten waarde, en een bekend
blok mag niet boven zijn eigen waarde groeien. In `CONSTRAINTS.md` staat een tabel `Uitzonderingen`
met ID, regel, pad, reden, eigenaar en vervaldatum.

## Gevolgen

- Een agent die een poort in de weg vindt, meldt dat en gaat niet edits plegen op de lat. Dat is
  langzamer voor de agent en sneller voor de eigenaar.
- Elke uitzondering is zichtbaar en meetbaar, dus een uitzondering die veroudert valt op in plaats van
  te verdwijnen.
- Er is geen suppressie-comment in de code die een check uitzet; dat is een aparte floor-regel, om
  dezelfde reden: een uitzondering hoort op één plek te staan waar je hem allemaal ziet.
