# AGENTS.md — hoe we aan deze site werken

Dit bestand gaat over **samenwerken**, niet over de site. Wat er technisch moet kloppen staat in
`CONSTRAINTS.md` (harde vloer, poorten, gemeten cijfers) en in de skill `mkdocs-blog-publishing`
(werkwijze per taak). Hier staat wat je niet uit de code kunt afleiden: hoe je je gedraagt als je eraan
werkt.

Er schrijven hier meerdere partijen: Hermes, het blog-profiel met zijn workers, en de eigenaar zelf. Deze
afspraken gelden voor allemaal, ook voor een agent die hier over drie maanden voor het eerst komt.

## Rapportage

- Meld de **uitkomst in één regel**, met bewijs: commit-SHA, CI-run, live URL, exit-code.
- Meld ook wat je **niet** hebt gedaan of niet kon verifiëren. Een half rapport is erger dan een kort.
- Geen procescommentaar ("ik ga nu kijken...") en geen statusupdate zonder verandering. Stilte is een
  geldig antwoord als er niets te melden is.
- Cijfers, paden en commando's letterlijk overnemen; een lange URL blijft één ononderbroken regel.
- Vraag alleen bij een echte beslissing (geld, toegang, intentie, koers) — zie de skill
  `attention-contract`. Techniek los je zelf op.

## Klaar

- **"Klaar" is een bewezen eindstand**: gepusht, CI groen, en de acceptatiespec groen — niet
  "de build zou moeten slagen". Dat laatste is een commando, geen indruk:
  `python3 tests/acceptance/publicatie.py --post docs/blog/posts/<post>.md` → exit 0.
- Een groene build bewijst de build, niet de post. De acceptatiespec beoordeelt het artefact dat de lezer
  krijgt: de pagina is deze post, de kop-afbeelding rendert op 250px in de lightbox, en elk beeld in de
  postinhoud laadt. Zie `tests/acceptance/README.md`.
- Een post is pas af als `blog-axi --changed` **exit 0** gaf. Exit 3 betekent een beslissing voor de
  eigenaar: leg hem voor, werk hem niet weg.
- Een halve wijziging laat je niet achter. Of je maakt het af en pusht, of je parkeert het met een
  expliciete reden buiten de gepubliceerde map.

## Eigendom

- **Trek altijd eerst** (`git pull --ff-only origin main`): andere agents pushen hier ook, en een
  verouderde `main` is de meest voorkomende bron van conflicten.
- **Eén schrijver per bestand tegelijk.** Werk je aan een post die een ander ook raakt, claim het bestand
  in je commit- of kaartboodschap voordat je begint.
- Committen op `main` is de normale route; er is geen PR-flow. **Nooit `git add .`** — altijd het
  specifieke bestand, na `git status` en `git diff`.
- De pre-push-poorten en de CI-strict-build zijn niet te omzeilen, niet te verzwakken en niet met een
  suppressie-comment uit te zetten. `CONSTRAINTS.md` verzwakken om iets groen te krijgen is verboden.
- **Alleen de eigenaar** beslist over merges, force-push, het verwijderen van pagina's, het aanpassen van
  `CONSTRAINTS.md` en het goedkeuren van een let-op-signaal.
- `CONSTRAINTS.md` en `tests/acceptance/*.py` zijn beschermd door de Hermes-hook `spec-guard`: een agent
  kan er geen bestaand bestand in wijzigen, ook niet om een rode check groen te krijgen. Een nieuw
  scenario toevoegen mag wel. Wil je een verwachting aanpassen, dan doe je dat zelf of met een expliciet
  akkoord per pad (`~/.hermes/state/spec-goedkeuring.txt`).

## Overdracht

- Alles wat een opvolger nodig heeft, staat in de commit, de kaart of een bestand — **niet in het
  gesprek**. Een sessie kan gecompacteerd of vervangen zijn voordat iemand verder leest.
- Een commit-boodschap zegt *wat* en *waarom* in conventional-commit-vorm (`content:`, `fix:`, `feat:`),
  niet *hoe lang je hebt gezocht*.
- Verwijs naar de skill of het script in plaats van commando's te herhalen; gedupliceerde commando's
  verouderen en dan liegt de documentatie.
- Laat de repo schoon achter: geen `site/`, geen `.cache`, geen losse probeerbestanden.

## Toon

- De site is **Engelstalig**; Nederlandstalig is gereserveerd voor posts die primair over Nederland gaan
  (zie `CONSTRAINTS.md`).
- **Neutraal, niet partijdig.** Geen politieke stellingname, geen campagne-retoriek, geen oordeel dat de
  eigenaar niet zelf zou onderschrijven. Twijfel je, dan is dat een beslissing voor hem.
- Feiten met bron, citaten letterlijk, en geen sfeertekst die een oordeel binnenbrengt.
- Schrijf voor een lezer, niet voor een zoekmachine of een reviewer.

## Poorten

Vóór de push, in deze volgorde — een rode poort betekent: niet pushen, eerst oplossen.

1. **Inhoud** (`blog-axi --changed`): frontmatter, datum, bestandsnaam, kop-afbeelding, more-marker,
   categorie-audit, taalregel en de neutraliteitspoort.
2. **Hygiëne** (`.git/hooks/pre-push`): secrets en lokale home-paden.
3. **CI** (`mkdocs build --strict` → `gh-deploy`): een waarschuwing publiceert niets.
4. **Publicatie** (`tests/acceptance/publicatie.py`, ná de deploy): de pagina die de lezer krijgt is deze
   post. Deze poort kan niet vóór de push, want hij leest de live site; hij bepaalt of je "klaar" mag
   zeggen. Rood = de post is niet (goed) gepubliceerd, dus eerst oplossen en opnieuw deployen.

Een poort die te streng lijkt, is een gesprek met de eigenaar — geen wijziging in de poort.
