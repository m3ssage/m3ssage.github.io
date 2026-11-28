#!/usr/bin/env python3
"""Genereert docs/llms.txt uit de frontmatter van de blogposts.

`llms.txt` is de ingang voor AI-assistenten die deze site bezoeken: geen crawl van 61 losse
pagina's, maar één bestand dat zegt wat er staat en waar het staat. Het bestand werd met de hand
onderhouden en bevatte alleen pointers naar de blog en de sitemap; deze generator maakt er een echte
index van (per categorie, nieuwste eerst).

Draaien na een nieuwe post, of vóór het publiceren:

    python3 scripts/gen_llms.py            # schrijft docs/llms.txt
    python3 scripts/gen_llms.py --check    # exit 1 als het bestand verouderd is (voor CI)

Twee dingen die dit script bewust doet:

  - posts met een datum in de toekomst overslaan, want `draft_if_future_date: true` in mkdocs.yml
    publiceert ze niet — een index die naar 404's linkt is erger dan geen index;
  - de taalaanduiding (`Dutch`) niet als categorie gebruiken, anders belandt elke Nederlandse post
    in een categorie "Dutch" in plaats van bij zijn onderwerp.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from datetime import date, datetime
from urllib.parse import quote

import yaml

try:
    # Exact de functie die de blogplugin gebruikt (MkDocs Material: post_slugify).
    # Niet nagebootst, want dat ging mis: PyMdown bewaart unicode (é) en maakt van een em-dash "--".
    from pymdownx.slugs import slugify as _pymdown_slugify
except ImportError:  # pragma: no cover
    sys.exit(
        "gen_llms.py heeft pymdownx nodig (MkDocs Material). Draai het met de blog-omgeving:\n"
        "  ~/.venvs/blog/bin/python scripts/gen_llms.py"
    )

_SLUG = _pymdown_slugify(case="lower")

SITE = "https://pages.bommel.xyz"
HIER = pathlib.Path(__file__).resolve().parent.parent
POSTS = HIER / "docs" / "blog" / "posts"
DOEL = HIER / "docs" / "llms.txt"

TAALMARKERING = {"Dutch"}
CATEGORIE_ORDE = [
    "AI",
    "Science",
    "Technology",
    "Software Development",
    "Economics",
    "Society",
    "Culture",
    "Nature",
    "Lifestyle",
    "Sport",
    "Travel",
    "YouTube",
]
KOP = (
    "# bommel.xyz\n\n"
    "> Personal site and blog of Eelco van Bommel: long-form articles on AI, technology, science, "
    "culture and society.\n\n"
    "Every post is listed below with its date, category and one-line summary, newest first per "
    "category. Posts are written in English or Dutch; the language is visible from the title.\n\n"
    "## Main pages\n\n"
    f"- [Blog]({SITE}/blog/): all posts, newest first\n"
    f"- [About]({SITE}/about/): how this site is built\n"
    f"- [Sitemap]({SITE}/sitemap.xml): every URL with a lastmod date\n"
)


def lees_meta(pad: pathlib.Path) -> dict | None:
    """De YAML-frontmatter van een post, of None als die er niet is."""
    tekst = pad.read_text(encoding="utf-8")
    if not tekst.startswith("---"):
        return None
    delen = tekst.split("---", 2)
    if len(delen) < 3:
        return None
    try:
        meta = yaml.safe_load(delen[1])
    except yaml.YAMLError:
        return None
    return meta if isinstance(meta, dict) else None


def datum_van(meta: dict, pad: pathlib.Path) -> date | None:
    ruw = meta.get("date")
    if isinstance(ruw, datetime):
        return ruw.date()
    if isinstance(ruw, date):
        return ruw
    match = re.match(r"^(\d{4})-(\d{2})-(\d{2})-", pad.name)
    if not match:
        return None
    try:
        return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    except ValueError:
        return None


def slug_van(pad: pathlib.Path, meta: dict) -> str:
    """Het `slug`-veld als het er is, anders de geslugde titel.

    De blogplugin bouwt de URL uit de *titel*, niet uit de bestandsnaam: een post zonder `slug`-veld
    landt op /blog/<datum>/<geslugde titel>/. Wie hier een andere regel gebruikt, schrijft een index
    vol 404's — daarom dezelfde functie als de plugin en geen eigen variant.
    """
    eigen = meta.get("slug")
    if isinstance(eigen, str) and eigen.strip():
        return eigen.strip()
    titel = str(meta.get("title") or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", pad.stem))
    return _SLUG(titel, "-")


def url_van(dag: date, slug: str) -> str:
    # Percent-encoding zoals in de sitemap: /blog/2026/11/11/van-%C3%A9%C3%A9n-bedrag-.../
    return f"{SITE}/blog/{dag.year:04d}/{dag.month:02d}/{dag.day:02d}/{quote(slug)}/"


def categorie_van(meta: dict) -> str:
    """De eerste categorie die geen taalaanduiding is."""
    categorien = [k for k in (meta.get("categories") or []) if isinstance(k, str)]
    for naam in categorien:
        if naam not in TAALMARKERING:
            return naam
    return categorien[0] if categorien else "Other"


def verzamel(vandaag: date) -> tuple[dict[str, list[tuple[date, str, str, str]]], int]:
    """{categorie: [(datum, titel, url, samenvatting)]}, en hoeveel posts zijn overgeslagen."""
    per_categorie: dict[str, list[tuple[date, str, str, str]]] = {}
    overgeslagen = 0
    for pad in sorted(POSTS.glob("*.md")):
        meta = lees_meta(pad)
        if not meta:
            overgeslagen += 1
            continue
        dag = datum_van(meta, pad)
        titel = (meta.get("title") or "").strip()
        if not dag or not titel or dag > vandaag:
            overgeslagen += 1
            continue
        samenvatting = re.sub(r"\s+", " ", (meta.get("description") or "")).strip()
        regel = (dag, titel, url_van(dag, slug_van(pad, meta)), samenvatting)
        per_categorie.setdefault(categorie_van(meta), []).append(regel)
    return per_categorie, overgeslagen


def render(per_categorie: dict[str, list[tuple[date, str, str, str]]]) -> str:
    volgorde = [c for c in CATEGORIE_ORDE if c in per_categorie]
    volgorde += sorted(c for c in per_categorie if c not in CATEGORIE_ORDE)
    blokken = [KOP]
    for categorie in volgorde:
        regels = sorted(per_categorie[categorie], key=lambda r: r[0], reverse=True)
        blokken.append(f"\n## {categorie} ({len(regels)})\n")
        for dag, titel, url, samenvatting in regels:
            staart = f": {samenvatting}" if samenvatting else ""
            blokken.append(f"- [{titel}]({url}){staart} ({dag.isoformat()})")
    return "\n".join(blokken) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="niet schrijven; exit 1 als het verouderd is")
    args = ap.parse_args()

    per_categorie, overgeslagen = verzamel(date.today())
    inhoud = render(per_categorie)
    aantal = sum(len(v) for v in per_categorie.values())
    huidig = DOEL.read_text(encoding="utf-8") if DOEL.exists() else ""

    if inhoud == huidig:
        print(f"llms.txt is bij: {aantal} posts in {len(per_categorie)} categorieën")
        return 0

    if args.check:
        print(
            f"llms.txt is verouderd: {aantal} posts in {len(per_categorie)} categorieën "
            f"({overgeslagen} overgeslagen) — draai: python3 scripts/gen_llms.py",
            file=sys.stderr,
        )
        return 1

    DOEL.write_text(inhoud, encoding="utf-8")
    print(f"llms.txt geschreven: {aantal} posts in {len(per_categorie)} categorieën, {len(inhoud)} bytes")
    if overgeslagen:
        print(f"  {overgeslagen} bestand(en) overgeslagen (geen frontmatter, geen titel of toekomstdatum)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
