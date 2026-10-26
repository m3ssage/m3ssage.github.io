#!/usr/bin/env python3
"""Rood-bewijs: bewijst dat de acceptatiespec een fout antwoord kán vangen.

Een spec die nooit rood is geweest, is een wens. Dit script haalt de nieuwste
gepubliceerde pagina op, plant drie echte fouten in een kopie (en één schone
controle) en eist dat de spec precies het juiste scenario laat vallen:

    geval   mutatie                                   verwacht
    groen   geen                                      exit 0, 3x PASS
    a       lightbox-wrapper en width-attribuut weg   exit 1, scenario 2 rood
    b       asset-bestand weg                         exit 1, scenario 3 rood
    c       post niet in de sitemap                   exit 1, scenario 1 rood (2 en 3
                                                     kunnen niets beoordelen en tellen rood)

Gebruik: python3 tests/acceptance/rood_bewijs.py [--post <pad>]

Exit 0 = de spec reageert op alle vier de gevallen zoals verwacht, 1 = minstens
één geval reageert verkeerd (dan is de spec zelf kapot), 2 = kon niet lopen.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def load_spec():
    """De spec onder test, geladen op zijn pad (geen sys.path-manipulatie)."""
    loader = importlib.util.spec_from_file_location("publicatie", HERE / "publicatie.py")
    if loader is None or loader.loader is None:
        raise RuntimeError(f"{HERE / 'publicatie.py'} is niet te laden")
    module = importlib.util.module_from_spec(loader)
    # dataclasses zoeken hun eigen module op in sys.modules tijdens het uitvoeren.
    sys.modules["publicatie"] = module
    loader.loader.exec_module(module)
    return module


publicatie = load_spec()


@dataclass
class Case:
    name: str
    mutate: str
    expected_exit: int
    expected_failed: set[int]
    note: str


CASES = (
    Case("groen", "geen", 0, set(), "ongemuteerde kopie"),
    Case("a", "kopschijf", 1, {2}, "geen width-attribuut en geen lightbox-wrapper"),
    Case("b", "asset", 1, {3}, "het asset-bestand ontbreekt"),
    Case("c", "sitemap", 1, {1, 2, 3}, "de post staat niet in de sitemap: niets valt te beoordelen"),
)


def download(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "bommel-acceptance/1.0"})
    with urllib.request.urlopen(request, timeout=publicatie.TIMEOUT) as response:
        target.write_bytes(response.read())


def build_copy(post: Path, root: Path, base: str, site: str) -> None:
    """Kopieer sitemap, postpagina en de afbeeldingen van die pagina naar <root>."""
    paths = publicatie.sitemap_paths(base)
    path = publicatie.resolve(post, paths)
    download(base.rstrip("/") + "/sitemap.xml", root / "sitemap.xml")
    download(base.rstrip("/") + path, root / path.lstrip("/") / "index.html")
    page = publicatie.fetch(base, path)
    for source in publicatie.article_images(page):
        url = site.rstrip("/") + publicatie.asset_path(source)
        download(url, root / publicatie.asset_path(source).lstrip("/"))


def mutate(case: Case, post: Path, root: Path, base: str) -> None:
    path = publicatie.resolve(post, publicatie.sitemap_paths(base))
    page = root / path.lstrip("/") / "index.html"
    if case.mutate == "kopschijf":
        html = page.read_text(encoding="utf-8")
        html = re.sub(r'<a class="glightbox"[^>]*>', "", html, count=1)
        html = html.replace(' width="250"', "", 1)
        html = html.replace("</a></p>", "</p>", 1)
        page.write_text(html, encoding="utf-8")
    elif case.mutate == "asset":
        first = publicatie.article_images(publicatie.fetch(base, path))[0]
        (root / publicatie.asset_path(first).lstrip("/")).unlink()
    elif case.mutate == "sitemap":
        sitemap = root / "sitemap.xml"
        lines = [line for line in sitemap.read_text(encoding="utf-8").splitlines() if path.strip("/") not in line]
        sitemap.write_text("\n".join(lines) + "\n", encoding="utf-8")


def judge(case: Case, post: Path, root: Path, spec: Path) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, str(spec), "--post", str(post), "--site", root.as_uri(), "--json"],
        capture_output=True,
        text=True,
        timeout=180,
    )
    if result.returncode not in (0, 1):
        return False, f"spec gaf exit {result.returncode}: {result.stderr.strip()[:200]}"
    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError:
        return False, f"geen JSON van de spec: {result.stdout[:200]!r}"
    failed = {index for index, item in enumerate(report["scenarios"], start=1) if not item["ok"]}
    if result.returncode != case.expected_exit:
        return False, f"exit {result.returncode}, verwacht {case.expected_exit}"
    if failed != case.expected_failed:
        return False, f"rode scenario's {sorted(failed) or 'geen'}, verwacht {sorted(case.expected_failed) or 'geen'}"
    return True, "zoals verwacht"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--post", help="pad naar de post (default: de nieuwste op datum)")
    arguments = parser.parse_args(argv)
    try:
        post = Path(arguments.post).resolve() if arguments.post else max(publicatie.post_paths(), key=publicatie.post_date)
        base = publicatie.SITE
        publicatie.sitemap_paths(base)
    except (publicatie.DriverError, OSError) as error:
        print(f"kan niet lopen: {error}", file=sys.stderr)
        return 2

    spec = HERE / "publicatie.py"
    workdir = Path(tempfile.mkdtemp(prefix="rood-bewijs-"))
    print(f"rood-bewijs · {post.name} · {base}")
    ok = True
    try:
        for case in CASES:
            root = workdir / case.name
            try:
                build_copy(post, root, base, base)
                mutate(case, post, root, base)
                passed, detail = judge(case, post, root, spec)
            except (publicatie.DriverError, OSError) as error:
                passed, detail = False, f"kon het geval niet planten: {error}"
            ok = ok and passed
            print(f"{'PASS' if passed else 'FAIL'}  geval {case.name:<5} {case.note}: {detail}")
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
