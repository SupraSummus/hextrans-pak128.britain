"""Fetch a single blob from the upstream Pak128.Britain-blends repo.

SHA pinned via blends.lock at the repo root. Anonymous HTTPS to
raw.githubusercontent.com; cache layout `.cache/blends/<sha>/<path>`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path


REPO = "jamespetts/Pak128.Britain-blends"
RAW = "https://raw.githubusercontent.com"


def repo_root() -> Path:
    """The hextrans-pak128.britain checkout root (where blends.lock lives)."""
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "blends.lock").is_file():
            return parent
    raise RuntimeError("blends.lock not found walking up from " + str(p))


def pinned_sha() -> str:
    lock = json.loads((repo_root() / "blends.lock").read_text())
    return lock[REPO]


def fetch(path: str, sha: str | None = None) -> Path:
    """Return a local cache path for `path` within the blends repo,
    downloading if not already cached."""
    sha = sha or pinned_sha()
    cache = repo_root() / ".cache" / "blends" / sha / path
    if cache.is_file():
        return cache
    url = f"{RAW}/{REPO}/{sha}/{path}"
    cache.parent.mkdir(parents=True, exist_ok=True)
    tmp = cache.with_suffix(cache.suffix + ".part")
    try:
        with urllib.request.urlopen(url) as resp, tmp.open("wb") as f:
            while chunk := resp.read(1 << 16):
                f.write(chunk)
    except urllib.error.HTTPError as e:
        tmp.unlink(missing_ok=True)
        raise SystemExit(f"fetch {url}: HTTP {e.code}") from e
    tmp.rename(cache)
    return cache


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
