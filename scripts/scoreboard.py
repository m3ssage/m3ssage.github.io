#!/usr/bin/env python3
"""Scoreboard: cyclomatic complexity van de code die wij zelf onderhouden.

Aanleiding (2026-10-23): Beningo's metrics scoreboard in de Steppe School-video —
een functie boven cyclomatic complexity 10 is aantoonbaar bug-gevoeliger én duurder
om te wijzigen, dus dat cijfer hoort in een poort en niet in een gevoel.

Scope: standaard de Python-bestanden van deze repo (tests/). `--path` meet een andere
boom, bijvoorbeeld een checkout: `--path ~/.hermes/hermes-agent/agent`.

Gebruik:
    python3 scripts/scoreboard.py                    # compact
    python3 scripts/scoreboard.py --full             # elke functie boven de drempel
    python3 scripts/scoreboard.py --json             # machineleesbaar
    python3 scripts/scoreboard.py --path <dir> --top 5
    python3 scripts/scoreboard.py --baseline scripts/complexity-baseline.json

Zonder baseline faalt elk blok boven de drempel. Met een baseline (JSON met `getolereerd`:
pad, naam, gemeten waarde en een reden) blijven bestaande blokken staan als "bekend", maar
faalt elk nieuw blok én elk blok dat boven zijn eigen gemeten waarde groeit. Dat is een ratel:
de schuld mag niet groeien, en een regel die niet meer nodig is meldt de tool zelf.

Exit 0 = alles onder de drempel, 1 = minstens één blok erover, 2 = kon niet meten
(geen radon, geen Python-bestanden, onbruikbaar pad). Meten dat niet lukt is nooit
groen: een poort die zijn eigen onvermogen als pass wegschrijft, is geen poort.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_SCOPE = ["tests"]
DEFAULT_MAX = 10.0  # Beningo's drempel, en de gangbare grens uit de literatuur
HIGH = 20.0  # D/E/F-rank: herschrijven, niet meer aanpassen


def find_radon() -> list[str] | None:
    """Het meetinstrument. Lokaal via uvx, in CI via pip; nooit stilzwijgend overslaan."""
    if importlib.util.find_spec("radon") is not None:
        return [sys.executable, "-m", "radon"]
    uvx = shutil.which("uvx")
    if not uvx:
        candidate = Path.home() / ".hermes" / "bin" / "uvx"
        if candidate.exists():
            uvx = str(candidate)
    if uvx:
        return [uvx, "--quiet", "radon"]
    return None


def measure(cmd: list[str], paths: list[str]) -> tuple[dict, str]:
    proc = subprocess.run(
        [*cmd, "cc", "-s", "-j", *paths],
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=600,
    )
    if proc.returncode != 0 and not proc.stdout.strip():
        return {}, (proc.stderr or "radon gaf geen uitvoer").strip()
    try:
        return json.loads(proc.stdout or "{}"), ""
    except json.JSONDecodeError as exc:  # pragma: no cover - radon's JSON is stabiel
        return {}, f"kon radon-uitvoer niet lezen: {exc}"


def collect(data: dict) -> tuple[list[dict], list[str]]:
    blocks: list[dict] = []
    for rel, items in data.items():
        for b in items:
            try:
                shown = str(Path(rel).resolve().relative_to(Path.cwd()))
            except ValueError:
                shown = rel
            blocks.append(
                {
                    "path": shown,
                    "line": b["lineno"],
                    "name": b["name"],
                    "type": b["type"],
                    "complexity": float(b["complexity"]),
                    "rank": b["rank"],
                }
            )
    blocks.sort(key=lambda b: (-b["complexity"], b["path"], b["line"]))
    return blocks, sorted({b["path"] for b in blocks})


def load_baseline(path: str) -> tuple[dict[str, float], str]:
    """Bekende uitzonderingen: {"getolereerd": [{"path", "name", "complexity", "reden"}]}.

    Een ratel, geen vrijbrief: de baseline houdt bestaande schuld tegen met een reden en een
    gemeten waarde, en laat elk nieuw of gegroeid blok alsnog falen. Zonder baseline faalt
    alles boven de drempel.
    """
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
    except OSError as exc:
        return {}, f"kan {path} niet lezen: {exc}"
    except json.JSONDecodeError as exc:
        return {}, f"{path} is geen geldige JSON: {exc}"
    rows = raw.get("getolereerd") if isinstance(raw, dict) else raw
    if not isinstance(rows, list):
        return {}, f"{path} mist een 'getolereerd'-lijst"
    out: dict[str, float] = {}
    for row in rows:
        if not isinstance(row, dict) or "path" not in row or "name" not in row:
            return {}, f"{path}: elke regel heeft 'path' en 'name' nodig"
        if not str(row.get("reden", "")).strip():
            return {}, f"{path}: {row['path']}:{row['name']} mist een 'reden'"
        try:
            out[f"{row['path']}:{row['name']}"] = float(row.get("complexity", DEFAULT_MAX))
        except (TypeError, ValueError):
            return {}, f"{path}: {row['path']}:{row['name']} heeft geen numerieke 'complexity'"
    return out, ""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Cyclomatic-complexity scoreboard.")
    ap.add_argument(
        "--path",
        action="append",
        default=None,
        help="te meten pad (herhaalbaar); standaard: tests/ in deze repo",
    )
    ap.add_argument(
        "--max",
        type=float,
        default=DEFAULT_MAX,
        help=f"drempel per blok (standaard {DEFAULT_MAX:g})",
    )
    ap.add_argument("--top", type=int, default=5, help="hoeveel hoogste scores tonen (standaard 5)")
    ap.add_argument("--full", action="store_true", help="alle blokken boven de drempel")
    ap.add_argument("--json", action="store_true", help="machineleesbare uitvoer")
    ap.add_argument(
        "--baseline",
        default=None,
        help="JSON met bekende, geaccepteerde uitzonderingen; nieuwe of gegroeide blokken falen alsnog",
    )
    args = ap.parse_args(argv)

    scope = args.path or DEFAULT_SCOPE
    paths = [p for p in scope if (REPO / p).exists() or Path(p).exists()]
    missing = [p for p in scope if p not in paths]
    if not paths:
        print(f"scoreboard: geen van de paden bestaat: {', '.join(scope)}", file=sys.stderr)
        return 2

    cmd = find_radon()
    if cmd is None:
        print(
            "scoreboard: radon niet gevonden (pip install radon==6.0.1 of uvx beschikbaar maken)",
            file=sys.stderr,
        )
        return 2

    data, err = measure(cmd, paths)
    if err:
        print(f"scoreboard: meten mislukt: {err}", file=sys.stderr)
        return 2

    blocks, files = collect(data)
    if not blocks:
        print(f"scoreboard: geen Python-blokken gevonden in {', '.join(paths)}", file=sys.stderr)
        return 2

    over = [b for b in blocks if b["complexity"] > args.max]
    heavy = [b for b in blocks if b["complexity"] > HIGH]
    worst = blocks[0]

    known: list[dict] = []
    grew: list[dict] = []
    new: list[dict] = []
    stale: list[str] = []
    if args.baseline:
        tolerated, err = load_baseline(args.baseline)
        if err:
            print(f"scoreboard: baseline onbruikbaar: {err}", file=sys.stderr)
            return 2
        seen: set[str] = set()
        for b in over:
            key = f"{b['path']}:{b['name']}"
            if key not in tolerated:
                new.append(b)
            elif b["complexity"] <= tolerated[key]:
                known.append(b)
                seen.add(key)
            else:
                grew.append(b)  # schuld mag niet groeien, ook niet met een bekende uitzondering
                seen.add(key)
        stale = sorted(k for k in tolerated if k not in seen)
        failing = new + grew
    else:
        failing = over
    ok = not failing

    if args.json:
        print(
            json.dumps(
                {
                    "status": "ok" if ok else "fail",
                    "paths": paths,
                    "missing_paths": missing,
                    "threshold": args.max,
                    "blocks": len(blocks),
                    "files": len(files),
                    "max": worst["complexity"],
                    "max_at": f"{worst['path']}:{worst['line']} {worst['name']}",
                    "over_threshold": len(over),
                    "over_high": len(heavy),
                    "known": known,
                    "new": new,
                    "grown": grew,
                    "stale_baseline": stale,
                    "offenders": failing if args.full else failing[: args.top],
                },
                indent=2,
            )
        )
        return 0 if ok else 1

    print(
        f"complexity  blocks={len(blocks)}  files={len(files)}  "
        f"max={worst['complexity']:g}  over{args.max:g}={len(over)}  over{HIGH:g}={len(heavy)}"
        + (f"  bekend={len(known)}" if args.baseline else "")
    )
    print(f"  hoogste: {worst['path']}:{worst['line']} {worst['name']} ({worst['complexity']:g})")
    for b in known:
        print(f"  bekend: {b['path']}:{b['line']} {b['name']} ({b['complexity']:g}, {b['rank']})")
    if stale:
        print(f"  let-op: baseline-regel niet meer nodig (mag eruit): {', '.join(stale)}")
    if failing:
        shown = failing if args.full else failing[: args.top]
        for b in shown:
            mark = "gegroeid" if b in grew else "nieuw"
            print(f"  {mark}: {b['path']}:{b['line']} {b['name']} ({b['complexity']:g}, {b['rank']})")
        rest = len(failing) - len(shown)
        if rest > 0:
            print(f"  ... {rest} meer (--full)")
        print(
            f"FAIL: {len(failing)} blok(ken) boven {args.max:g} zonder geldige uitzondering; "
            "splits de functie of leg de uitzondering met reden vast in de baseline",
            file=sys.stderr,
        )
        return 1
    if heavy:
        print(
            f"let-op: {len(heavy)} blok(ken) boven {HIGH:g} — kandidaat voor herschrijven, niet blokkerend",
            file=sys.stderr,
        )
    print("OK: geen nieuw of gegroeid blok boven de drempel")
    return 0


if __name__ == "__main__":
    sys.exit(main())
