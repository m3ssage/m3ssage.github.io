#!/usr/bin/env python3
"""Acceptatiespec: de post die in de repo staat, staat live en rendert.

Eén artefact dat specificatie én validatie is. De scenario's staan in de taal van
het probleem (een lezer opent een post), niet in de taal van de oplossing: geen
plugin, geen MkDocs-internals, geen bestandsnamen van de implementatie.

Vier lagen, van boven naar beneden:

1. testcases  `scenario_*`  — Given/When/Then, één scenario per eigenschap
2. DSL        `resolve`, `header_image`, `teaser_link` — domeinoperaties
3. drivers    `fetch`, `sitemap_paths`, `frontmatter` — praten met de echte site
4. systeem    https://pages.bommel.xyz via MkDocs + GitHub Pages

Gebruik:

    python3 tests/acceptance/publicatie.py                # nieuwste post
    python3 tests/acceptance/publicatie.py --post docs/blog/posts/<post>.md
    python3 tests/acceptance/publicatie.py --site file:///tmp/kopie --json

Exit 0 = alle scenario's groen, 1 = minstens één rood, 2 = kon niet lopen.

De verwachtingen aanpassen is een contractwijziging: dat doet de eigenaar, niet de
agent die de post schrijft. Zie tests/acceptance/README.md.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
POSTS_DIR = REPO / "docs/blog/posts"
SITE = "https://pages.bommel.xyz"
TIMEOUT = 30
HEADER_WIDTH = "250"

FRONTMATTER_IMAGE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)\s]+)\)")
H1 = re.compile(r"<h1[^>]*>(?P<title>.*?)</h1>", re.S)
IMG = re.compile(r"<img\b[^>]*>", re.S)
LOC = re.compile(r"<loc>\s*(?P<url>[^<\s]+)\s*</loc>")


# --------------------------------------------------------------------------- laag 3: drivers


class DriverError(Exception):
    """De site of de repo is niet te lezen: het scenario kan geen oordeel geven."""


@dataclass(frozen=True)
class Document:
    path: str
    status: int
    body: str
    content_type: str = ""


def fetch(base: str, path: str) -> Document:
    """GET <base><path>; een pad op een map krijgt index.html (Pages-gedrag)."""
    url = base.rstrip("/") + "/" + path.lstrip("/")
    if url.endswith("/"):
        url += "index.html"
    request = urllib.request.Request(url, headers={"User-Agent": "bommel-acceptance/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            try:
                content_type = response.headers.get_content_type()
            except AttributeError:
                content_type = ""
            # file:// (de offline kopie voor de rood-bewijs-test) levert geen HTTP-status.
            return Document(
                path=path,
                status=getattr(response, "status", None) or 200,
                body=response.read().decode(charset, "replace"),
                content_type=content_type or "",
            )
    except urllib.error.HTTPError as error:
        return Document(path=path, status=error.code, body="")
    except (urllib.error.URLError, OSError) as error:
        raise DriverError(f"{url} niet op te halen: {error}") from error


def sitemap_paths(base: str) -> list[str]:
    document = fetch(base, "/sitemap.xml")
    if document.status != 200:
        raise DriverError(f"/sitemap.xml gaf HTTP {document.status}")
    paths = []
    for url in LOC.findall(document.body):
        path = re.sub(r"^https?://[^/]+", "", html.unescape(url))
        paths.append(path if path.endswith("/") else path + "/")
    if not paths:
        raise DriverError("/sitemap.xml bevat geen <loc>-regels")
    return paths


def frontmatter(post: Path) -> dict[str, str]:
    """Lees de YAML-kop van een post zonder YAML-afhankelijkheid."""
    lines = post.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise DriverError(f"{post.name} heeft geen frontmatter")
    values: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return values
        match = re.match(r"^(?P<key>[a-z_]+):\s*(?P<value>.*)$", line)
        if match:
            values[match.group("key")] = match.group("value").strip().strip('"').strip("'")
    raise DriverError(f"{post.name} sluit de frontmatter niet af")


def post_paths() -> list[Path]:
    posts = sorted(POSTS_DIR.glob("*.md"))
    if not posts:
        raise DriverError(f"geen posts in {POSTS_DIR}")
    return posts


# --------------------------------------------------------------------------- laag 2: DSL


def post_date(post: Path) -> str:
    stamp = frontmatter(post).get("date", "")
    if not re.match(r"^\d{4}-\d{2}-\d{2}", stamp):
        raise DriverError(f"{post.name} heeft geen bruikbare date: {stamp!r}")
    return stamp[:10]


def date_path(post: Path) -> str:
    year, month, day = post_date(post).split("-")
    return f"/blog/{year}/{month}/{day}/"


def slug_tokens(text: str) -> set[str]:
    return {word for word in re.split(r"[^a-z0-9]+", text.lower()) if len(word) > 2}


def resolve(post: Path, paths: list[str]) -> str:
    """Het pad van deze post in de sitemap: zelfde datum, beste titeloverlap."""
    title = frontmatter(post).get("title", "")
    wanted = slug_tokens(title)
    candidates = [path for path in paths if path.startswith(date_path(post))]
    if not candidates:
        raise LookupError(f"geen pagina onder {date_path(post)} in de sitemap")
    scored = sorted(candidates, key=lambda p: len(wanted & slug_tokens(p)), reverse=True)
    best = scored[0]
    if len(wanted & slug_tokens(best)) < 2:
        raise LookupError(f"geen pagina onder {date_path(post)} lijkt op {title!r}")
    return best


def header_image(post: Path) -> dict[str, str]:
    body = post.read_text(encoding="utf-8").split("---", 2)[-1]
    match = FRONTMATTER_IMAGE.search(body)
    if not match:
        raise LookupError(f"{post.name} heeft geen kop-afbeelding in de markdown")
    return {"alt": match.group("alt"), "src": match.group("src")}


def rendered_header(document: Document, image: dict[str, str]) -> dict[str, str]:
    """De <img> van de kop-afbeelding zoals de browser hem krijgt, plus zijn wikkel."""
    position = H1.search(document.body)
    if not position:
        raise LookupError("de pagina heeft geen <h1>")
    start = position.end()
    for match in IMG.finditer(document.body, start):
        tag = match.group(0)
        if image["src"] not in tag:
            continue
        before = document.body[start : match.start()]
        wrapper = re.findall(r"<a\b[^>]*>", before)
        return {
            "tag": tag,
            "src": attribute(tag, "src"),
            "width": attribute(tag, "width"),
            "wrapper": wrapper[-1] if wrapper else "",
        }
    raise LookupError(f"geen <img> met {image['src']} na de <h1>")


def normalise(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", html.unescape(text).lower())


def attribute(tag: str, name: str) -> str:
    match = re.search(rf'\b{name}="([^"]*)"', tag)
    return match.group(1) if match else ""


def article_images(document: Document) -> list[str]:
    """De src's van de afbeeldingen die de postinhoud toont (geen sitechrome)."""
    start = document.body.find('class="md-content__inner md-typeset"')
    if start < 0:
        raise LookupError("de pagina heeft geen artikelinhoud")
    end = document.body.find("</article>", start)
    region = document.body[start : end if end > 0 else len(document.body)]
    sources = []
    for tag in IMG.findall(region):
        source = attribute(tag, "src")
        if source and source not in sources:
            sources.append(source)
    return sources


def asset_path(source: str) -> str:
    """Het pad op de site voor een src uit de pagina."""
    if source.startswith(("http://", "https://")):
        return re.sub(r"^https?://[^/]+", "", source)
    return source


# --------------------------------------------------------------------------- laag 1: testcases


@dataclass
class Scenario:
    given: str
    when: str
    then: str
    failures: list[str]

    @property
    def passed(self) -> bool:
        return not self.failures


@dataclass
class Case:
    """Eén post tegen één site: wat de scenario's samen delen."""

    post: Path
    base: str
    paths: list[str]
    path: str | None = None


def scenario_page_is_the_post(case: Case) -> Scenario:
    given = f"de post {case.post.name} staat in de repo"
    when = "een lezer de pagina uit de sitemap opent"
    then = "krijgt hij precies deze post: dezelfde titel in de <h1>"
    scenario = Scenario(given, when, then, [])
    try:
        path = resolve(case.post, case.paths)
    except LookupError as error:
        scenario.failures.append(f"{error} (niet gedeployd, of de datum klopt niet)")
        return scenario
    case.path = path
    document = fetch(case.base, path)
    if document.status != 200:
        scenario.failures.append(f"{path} gaf HTTP {document.status}")
        return scenario
    heading = H1.search(document.body)
    if not heading:
        scenario.failures.append(f"{path} heeft geen <h1>")
        return scenario
    title = frontmatter(case.post).get("title", "")
    if normalise(heading.group("title")) != normalise(title):
        scenario.failures.append(f"<h1> is {heading.group('title')!r}, frontmatter zegt {title!r}")
    return scenario


def scenario_header_image_renders(case: Case) -> Scenario:
    given = f"de post {case.post.name} heeft een kop-afbeelding met breedte-attribuut"
    when = "de pagina in de browser wordt geopend"
    then = "staat die afbeelding direct onder de titel, in de lightbox en op 250px"
    scenario = Scenario(given, when, then, [])
    if case.path is None:
        scenario.failures.append("niet te beoordelen: de pagina is niet gevonden (scenario 1)")
        return scenario
    try:
        image = header_image(case.post)
    except LookupError as error:
        scenario.failures.append(str(error))
        return scenario
    document = fetch(case.base, case.path)
    if document.status != 200:
        scenario.failures.append(f"{case.path} gaf HTTP {document.status}")
        return scenario
    try:
        rendered = rendered_header(document, image)
    except LookupError as error:
        scenario.failures.append(f"{error}: de afbeelding wordt niet gerenderd")
        return scenario
    if rendered["src"] != image["src"]:
        scenario.failures.append(f"src is {rendered['src']!r}, markdown zegt {image['src']!r}")
    if rendered["width"] != HEADER_WIDTH:
        scenario.failures.append(
            f"width is {rendered['width']!r} in plaats van {HEADER_WIDTH!r}: de afbeelding rendert paginabreed"
        )
    if "glightbox" not in rendered["wrapper"]:
        scenario.failures.append("de <img> zit niet in een lightbox-wrapper (<a class=\"glightbox\">)")
    return scenario


def scenario_images_load(case: Case) -> Scenario:
    given = f"de post {case.post.name} toont afbeeldingen"
    when = "een lezer de pagina opent"
    then = "laadt elke afbeelding in de postinhoud, en geen enkele geeft 404"
    scenario = Scenario(given, when, then, [])
    if case.path is None:
        scenario.failures.append("niet te beoordelen: de pagina is niet gevonden (scenario 1)")
        return scenario
    document = fetch(case.base, case.path)
    if document.status != 200:
        scenario.failures.append(f"{case.path} gaf HTTP {document.status}")
        return scenario
    try:
        sources = article_images(document)
    except LookupError as error:
        scenario.failures.append(str(error))
        return scenario
    if not sources:
        scenario.failures.append("de postinhoud toont geen enkele afbeelding")
        return scenario
    for source in sources:
        try:
            asset = fetch(case.base, asset_path(source))
        except DriverError as error:
            scenario.failures.append(f"niet op te halen: {error}")
            continue
        if asset.status != 200:
            scenario.failures.append(f"{asset_path(source)} gaf HTTP {asset.status}")
        elif asset.content_type and not asset.content_type.startswith("image/"):
            scenario.failures.append(f"{asset_path(source)} is {asset.content_type}, geen afbeelding")
        elif len(asset.body) < 1024:
            scenario.failures.append(f"{asset_path(source)} is leeg of afgekapt ({len(asset.body)} bytes)")
    return scenario


SCENARIOS = (scenario_page_is_the_post, scenario_header_image_renders, scenario_images_load)


# --------------------------------------------------------------------------- runner


def run(post: Path, base: str, as_json: bool) -> int:
    try:
        case = Case(post=post, base=base, paths=sitemap_paths(base))
    except DriverError as error:
        print(f"kan niet lopen: {error}", file=sys.stderr)
        return 2
    results = []
    for factory in SCENARIOS:
        try:
            results.append(factory(case))
        except DriverError as error:
            # Niet kunnen verifiëren is rood, geen grijs: een check die zijn eigen
            # onvermogen als groen boekt, is erger dan geen check.
            results.append(Scenario(given="de pagina is bereikbaar", when="de spec hem opvraagt",
                                    then=f"scenario {factory.__name__} kan een oordeel geven",
                                    failures=[f"niet te beoordelen: {error}"]))

    if as_json:
        print(json.dumps(
            {
                "post": str(post.relative_to(REPO)),
                "site": base,
                "path": case.path,
                "scenarios": [
                    {"then": item.then, "ok": item.passed, "failures": item.failures} for item in results
                ],
                "ok": all(item.passed for item in results),
            },
            indent=2,
            ensure_ascii=False,
        ))
    else:
        print(f"spec: {post.relative_to(REPO)} · site: {base}")
        for index, item in enumerate(results, start=1):
            status = "PASS" if item.passed else "FAIL"
            print(f"{status}  scenario {index}: {item.then}")
            print(f"        Given {item.given}")
            print(f"        When  {item.when}")
            for failure in item.failures:
                print(f"        → {failure}")
    return 0 if all(item.passed for item in results) else 1


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--post", help="pad naar de post (default: de nieuwste op datum)")
    parser.add_argument("--site", default=SITE, help=f"basis-URL van de site (default: {SITE})")
    parser.add_argument("--json", action="store_true", help="machineleesbare uitvoer")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = parse_args(argv if argv is not None else sys.argv[1:])
    try:
        if arguments.post:
            post = Path(arguments.post)
            if not post.is_absolute():
                post = (REPO / post).resolve()
            if not post.is_file():
                print(f"kan niet lopen: {post} bestaat niet", file=sys.stderr)
                return 2
        else:
            post = max(post_paths(), key=post_date)
    except DriverError as error:
        print(f"kan niet lopen: {error}", file=sys.stderr)
        return 2
    return run(post, arguments.site, arguments.json)


if __name__ == "__main__":
    sys.exit(main())
