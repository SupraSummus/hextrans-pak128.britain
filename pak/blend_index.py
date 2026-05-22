"""Enumerate upstream blend repos and suggest blends for unported dats.

The two upstream blend repos (`jamespetts/Pak128.Britain-blends`,
`JamesHood/pak128.Britain-blend-files`) aren't tree-indexed in any
manifest we commit -- `blends.lock` is per-blob TOFU and only knows
the blends we've already fetched.  This module fills the gap with a
blob-less clone of each repo cached under `.cache/blend_index/`,
walks the tree for `.blend` paths, and suggests candidates for the
unported dats listed by `pak.bake_units --unported`.

Candidate matching is filename-only: token-subseq in either
direction between dat-stem and blend-stem, restricted to the
category subtree.  Coverage is good for trains/boats/trams (flat
per-asset blend layout, ~85-90% of unported dats get a candidate)
and weak for air/citybuildings (upstream organises blends by
livery folder rather than per-asset, and citybuildings dats are
multi-`Obj=building` packs whose internal `Name=` fields are what
matches blend stems, not the dat filename — parsing the dats to
extract those names would extend coverage but isn't done yet).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from pak import REPO_ROOT
from pak.bake_units import unported

CACHE = REPO_ROOT / ".cache" / "blend_index"

SOURCES = {
    "jamespetts": "https://github.com/jamespetts/Pak128.Britain-blends",
    "jh": "https://github.com/JamesHood/pak128.Britain-blend-files",
}


def _ensure_clone(slug: str, url: str) -> Path:
    dst = CACHE / slug
    if (dst / ".git").exists():
        return dst
    CACHE.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "clone", "--filter=blob:none", "--no-checkout",
         "--depth=1", url, str(dst)],
        check=True,
    )
    return dst


def index() -> dict[str, list[str]]:
    """Per-source list of `.blend` paths in each upstream repo."""
    out: dict[str, list[str]] = {}
    for slug, url in SOURCES.items():
        dst = _ensure_clone(slug, url)
        ls = subprocess.run(
            ["git", "-C", str(dst), "ls-tree", "-r", "--name-only", "HEAD"],
            check=True, capture_output=True, text=True,
        )
        out[slug] = sorted(p for p in ls.stdout.splitlines() if p.endswith(".blend"))
    return out


_VARIANT_SUFFIXES = re.compile(
    r"-(first|second|third|fourth|brake|mail|composite|sub|tender|loco|trailer|"
    r"diag|sup\d*|heavy|thin|early|late|snow)$"
)


def _split(s: str) -> list[str]:
    return [t for t in s.lower().replace("_", "-").split("-") if t]


def _join_digit_letter(toks: list[str]) -> list[str]:
    """Fold `[4, wheel]` → `[4wheel]` to match upstream's mixed convention.

    Some upstream files hyphenate (`4-wheel-1860s.dat`), others don't
    (`4wheel-1860s.blend`).  Adjacent (single-digit, letter-prefix)
    pairs get merged; longer numeric tokens (`1860`) are preserved.
    """
    out: list[str] = []
    i = 0
    while i < len(toks):
        if (i + 1 < len(toks) and toks[i].isdigit() and len(toks[i]) == 1
                and toks[i + 1] and toks[i + 1][0].isalpha()):
            out.append(toks[i] + toks[i + 1])
            i += 2
        else:
            out.append(toks[i])
            i += 1
    return out


def _blend_tokens(stem: str) -> list[str]:
    """Blend stems are atomic identifiers — no suffix or `s` stripping.

    Stripping `-first` from `4wheel-first.blend` would leave `4wheel`,
    which then matches every 4-wheel dat instead of just first-class.
    """
    return _join_digit_letter(_split(stem))


def _dat_tokens(stem: str) -> list[str]:
    """Dat stems span variants — strip variant suffixes + trailing `s`.

    Folds `4wheel-1850s-brake/composite/first/mail/second/third` onto
    `4wheel-1850.blend`, the N:1 fanout pattern Britain carriage blends
    follow.  Token-boundary matching downstream rejects the
    `tea ⊂ steam` substring false positive `in`-matching produced.
    """
    s = stem.lower().replace("_", "-")
    while True:
        new = _VARIANT_SUFFIXES.sub("", s)
        if new == s:
            break
        s = new
    toks = _join_digit_letter(_split(s))
    if toks and toks[-1].endswith("s") and len(toks[-1]) > 1:
        toks[-1] = toks[-1][:-1]
    return toks


def _contains(haystack: list[str], needle: list[str]) -> bool:
    if not needle or len(needle) > len(haystack):
        return False
    for i in range(len(haystack) - len(needle) + 1):
        if haystack[i:i + len(needle)] == needle:
            return True
    return False


_CATEGORY_ALIAS = {"industry": "industries"}


def candidates_for(dat: Path, blend_paths: dict[str, list[str]]) -> list[tuple[str, str]]:
    """`(source, blend_path)` pairs matching `dat` by category + token-subseq.

    Category match: dat's top-level dir (`trains`, `air`, …) must equal
    the blend's top-level dir, case-insensitive (upstream uses `Trains/`
    in jamespetts vs `trains/` in ours).  One alias: our singular
    `industry/` maps onto upstream's plural `industries/`.  Two-direction
    token match, both legitimate fanout patterns:

    - Blend ⊂ dat: one blend backs many dat variants (carriages —
      `4wheel-1850.blend` covers `4wheel-1850s-{brake,composite,…}`).
    - Dat ⊂ blend: one dat has many livery-specific blends (locos /
      DMUs — `br-101.dat` covers `BR-101-dmbs-{b,bg,g,nse-…}.blend`).

    Reports all hits; agent disambiguates when N > 1.
    """
    category = dat.relative_to(REPO_ROOT).parts[0].lower()
    category = _CATEGORY_ALIAS.get(category, category)
    dat_toks = _dat_tokens(dat.stem)
    hits: list[tuple[str, str]] = []
    for slug, paths in blend_paths.items():
        for bp in paths:
            parts = bp.split("/")
            if len(parts) < 2 or parts[0].lower() != category:
                continue
            blend_toks = _blend_tokens(Path(bp).stem)
            if _contains(dat_toks, blend_toks) or _contains(blend_toks, dat_toks):
                hits.append((slug, bp))
    return hits


def group_by_blend(category: str | None = None) -> tuple[
    dict[tuple[str, str], list[Path]],
    list[Path],
]:
    """Group unported dats by candidate blend; return groups + orphans.

    Multi-candidate dats land in every group they hit (the agent picks
    one); dats with no candidate go to orphans.
    """
    blend_paths = index()
    groups: dict[tuple[str, str], list[Path]] = defaultdict(list)
    orphans: list[Path] = []
    for dat in unported(category):
        hits = candidates_for(dat, blend_paths)
        if not hits:
            orphans.append(dat)
            continue
        for hit in hits:
            groups[hit].append(dat)
    return dict(groups), orphans


def _main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("category", nargs="?",
                    help="restrict to one top-level dir (e.g. 'trains')")
    ap.add_argument("--orphans", action="store_true",
                    help="list only the no-candidate dats")
    args = ap.parse_args(argv)
    groups, orphans = group_by_blend(args.category)
    if args.orphans:
        for dat in orphans:
            print(dat.relative_to(REPO_ROOT))
        return 0
    for (slug, bp), dats in sorted(groups.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        print(f"{slug}:{bp}")
        for d in sorted(dats):
            print(f"  {d.relative_to(REPO_ROOT)}")
    print(f"# {len(groups)} candidate blends, "
          f"{sum(len(v) for v in groups.values())} dat hits, "
          f"{len(orphans)} orphans")
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
