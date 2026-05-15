"""Fetch a single file from the upstream simutrans-pak128.britain repo.

SHA pinned via pak.lock at the repo root.  Anonymous HTTPS to
raw.githubusercontent.com; cache layout `.cache/pak/<sha>/<path>`.
Mirrors fetch_blend.py for the parallel `Pak128.Britain-blends` repo.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path


REPO = "jamespetts/simutrans-pak128.britain"
RAW = "https://raw.githubusercontent.com"


def repo_root() -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "pak.lock").is_file():
            return parent
    raise RuntimeError("pak.lock not found walking up from " + str(p))


def pinned_sha() -> str:
    lock = json.loads((repo_root() / "pak.lock").read_text())
    return lock[REPO]


def fetch(path: str, sha: str | None = None) -> Path:
    """Return a local cache path for `path` within the upstream pak repo,
    downloading if not already cached."""
    sha = sha or pinned_sha()
    cache = repo_root() / ".cache" / "pak" / sha / path
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
    ap.add_argument("path", help="path within the upstream pak repo, e.g. trains/carriages/4wheel-1850-first-lnwr_S.png")
    ap.add_argument("--sha", help="override pinned SHA")
    args = ap.parse_args(argv)
    print(fetch(args.path, args.sha))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
