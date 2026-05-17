"""Fetch a single file from the upstream simutrans-pak128.britain repo.

Thin wrapper over `pak._fetch`; see that module's docstring for the
lock-file format and validation contract.  Cache layout is
`.cache/pak/<sha>/<path>`.  Mirrors `fetch_blend` for the parallel
blends repo.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pak._fetch import Source, fetch as _fetch, load_lock

SOURCE = Source(
    repo="jamespetts/simutrans-pak128.britain",
    lock_name="pak.lock",
    cache_dir="pak",
)


def fetch(path: str, sha: str | None = None) -> Path:
    return _fetch(SOURCE, path, sha)


def pinned_sha() -> str:
    return load_lock(SOURCE)[0]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", help="path within the upstream pak repo, e.g. trains/carriages/4wheel-1850-first-lnwr_S.png")
    ap.add_argument("--sha", help="override pinned SHA")
    args = ap.parse_args(argv)
    print(fetch(args.path, args.sha))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
