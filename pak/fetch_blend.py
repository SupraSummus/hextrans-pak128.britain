"""Fetch a single blob from the upstream Pak128.Britain-blends repo.

Thin wrapper over `pak._fetch`; see that module's docstring for the
lock-file format and validation contract.  Cache layout is
`.cache/blends/<sha>/<path>`.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from pak._fetch import Source, fetch as _fetch

SOURCE = Source(
    repo="jamespetts/Pak128.Britain-blends",
    lock_name="blends.lock",
    cache_dir="blends",
)


def fetch(path: str, sha: str | None = None) -> Path:
    return _fetch(SOURCE, path, sha)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", help="path within the blends repo, e.g. Trains/Railcars/br-350-lnr.blend")
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
