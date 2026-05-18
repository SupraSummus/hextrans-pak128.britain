"""Fetch a single blob from JamesHood's pak128.Britain blend mirror.

The canonical `jamespetts/Pak128.Britain-blends` repo doesn't carry
bridge / viaduct blends; `JamesHood/pak128.Britain-blend-files` does.
Same fetch contract as `pak.fetch_blend` — `Source`-declared, lock-pinned
via `jh_blends.lock`, cached under `.cache/jh_blends/<sha>/<path>`.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from pak._fetch import Source, fetch as _fetch, load_lock

SOURCE = Source(
    repo="JamesHood/pak128.Britain-blend-files",
    lock_name="jh_blends.lock",
    cache_dir="jh_blends",
)


def fetch(path: str, sha: str | None = None) -> Path:
    return _fetch(SOURCE, path, sha)


def pinned_sha() -> str:
    return load_lock(SOURCE)[0]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", help="path within the JH blend repo, e.g. ways/plate_girder/straight.blend")
    ap.add_argument("--sha", help="override pinned SHA")
    ap.add_argument("--print-sha256", action="store_true", help="also print sha256 of fetched bytes")
    args = ap.parse_args(argv)
    out = fetch(args.path, args.sha)
    print(out)
    if args.print_sha256:
        print(hashlib.sha256(out.read_bytes()).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
