# AGENTS.md — hoe we hier samenwerken

Dit bestand gaat over gedrag, niet over de site. De technische vloer staat in `CONSTRAINTS.md`
(poorten, drempels, gemeten cijfers), de werkwijze per taak in de skill `mkdocs-blog-publishing`.
Hier staat alleen wat je uit geen van beide kunt afleiden — en het geldt voor iedereen die hier
schrijft: Hermes, het blog-profiel met zijn workers en de eigenaar.

## Altijd

- **Trek eerst** (`git pull --ff-only origin main`). Andere agents pushen hier ook; een oude `main`
  is de meest voorkomende bron van conflicten.
- **Één schrijver per bestand.** Claim het bestand in je commit- of kaartboodschap voordat je begint.
- **Stage per bestand**, na `git status` en `git diff` — nooit `git add .`.
- **Verzwak de lat niet.** `CONSTRAINTS.md` en `tests/acceptance/*.py` zijn van de eigenaar en met
  `spec-guard` beschermd; een te strenge poort is een gesprek, geen wijziging.
- **Klaar is bewezen**: gepusht, CI groen, `python3 tests/acceptance/publicatie.py --post <pad>` exit 0
  en `blog-axi --changed` exit 0. Exit 3 is een beslissing voor de eigenaar, geen hindernis.
- **Laat de repo schoon achter**: geen `site/`, geen `.cache`, geen probeerbestanden.

## Waar de rest staat

| Nodig | Ga naar |
|---|---|
| Een post schrijven, aanpassen of vertalen | skill `mkdocs-blog-publishing` (schrijven, humanizer-pass, taalregel) |
| Een drempel, poort of uitzondering bekijken | `CONSTRAINTS.md`; een nieuwe uitzondering hoort met reden in `scripts/complexity-baseline.json` |
| Bulk-, onbeheerd of meerstaps werk | skill `hermes-kanban-project-setup` (kaart in een worktree, push na jouw akkoord) |
| Na een push: staat het live? | skill `mkdocs-blog-publishing` §4 (`blog-axi deploy`, sitemap, acceptatiespec) |

De poortvolgorde en wat elke poort dekt staan in `CONSTRAINTS.md`; herhaal ze hier niet, dan lopen er
twee versies uiteen.

## Toon

- **Neutraal, niet partijdig.** Geen politieke stellingname, geen campagne-retoriek, geen oordeel dat de
  eigenaar niet zelf zou onderschrijven. Twijfel je, dan is dat een beslissing voor hem.
- Feiten met bron, citaten letterlijk, en geen sfeertekst die een oordeel binnenbrengt.
- Schrijf voor een lezer, niet voor een zoekmachine of een reviewer.
- De taal van een post volgt het onderwerp (de site is Engelstalig); de regel zelf staat in
  `CONSTRAINTS.md` en wordt door de poort getoetst.

## Rapportage

- **Uitkomst in één regel, met bewijs**: commit-SHA, CI-run, live URL of exit-code.
- **Meld wat je niet deed of niet kon verifiëren.** Een half rapport is erger dan een kort.
- **Geen procescommentaar** ("ik ga nu kijken…") en geen statusupdate zonder verandering; stilte is
  een geldig antwoord.
- **Cijfers, paden en commando's letterlijk** overnemen; een lange URL blijft één ononderbroken regel.
- **Vraag alleen bij een echte beslissing** (geld, toegang, intentie, koers) — zie skill
  `attention-contract`. Techniek los je zelf op.

## Eigendom en overdracht

- **Alleen de eigenaar** beslist over merges, force-push, pagina's verwijderen, het aanpassen van
  `CONSTRAINTS.md` en het goedkeuren van een let-op-signaal.
- **Committen op `main` is de normale route**; er is geen PR-flow. De commitvorm zegt *wat* en *waarom*
  (`content:`, `fix:`, `feat:`), niet hoe lang je hebt gezocht.
- **Een halve wijziging laat je niet achter**: afmaken en pushen, of parkeren met een expliciete reden
  buiten de gepubliceerde map.
- **Overdracht staat in de commit, de kaart of een bestand**, niet in het gesprek — een sessie kan
  gecompacteerd zijn voordat iemand verder leest. Verwijs naar de skill of het script in plaats van
  commando's te herhalen; gedupliceerde commando's verouderen en dan liegt de documentatie.
