"""Shared infrastructure for the per-upstream-repo fetchers.

Each fetcher (`fetch_blend`, `fetch_pak`, …) is a thin wrapper that
declares a `Source` — repo slug, lock-file name, cache subdir —
and delegates here.  The lock file is plain text:

    commit <sha>

    <sha256>  <path>
    <sha256>  <path>
    …

Lines are sha256sum format (`<hex>  <path>`), sorted by path so
inserts and removes diff as single-line changes.  The fetcher
validates downloaded bytes against the manifest; unknown paths are
recorded on first fetch (TOFU) and `git diff --exit-code` surfaces
them.  Cache hits are trusted (the bytes were validated when
written).

The format is `sha256sum -c`-compatible once the header is
stripped — useful for ad-hoc verification of a populated cache.
"""

from __future__ import annotations

import hashlib
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

RAW = "https://raw.githubusercontent.com"


@dataclass(frozen=True)
class Source:
    """Pins one upstream repo: GitHub slug, on-disk lock filename, and
    cache subdir under `.cache/`."""
    repo: str        # "jamespetts/Pak128.Britain-blends"
    lock_name: str   # "blends.lock"
    cache_dir: str   # "blends" -> .cache/blends/<sha>/<path>


def repo_root(lock_name: str) -> Path:
    """The checkout root, located by walking up to find `lock_name`."""
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / lock_name).is_file():
            return parent
    raise RuntimeError(f"{lock_name} not found walking up from {p}")


def parse_lock(text: str, *, source: str = "<lock>") -> tuple[str, dict[str, str]]:
    """Parse a lock-file string into (commit, {path: sha256}).

    `source` is used only in the error message when a line can't be
    parsed."""
    commit = ""
    files: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("commit "):
            commit = line.split(None, 1)[1]
            continue
        sha, sep, path = line.partition("  ")
        if not sep:
            raise RuntimeError(f"{source}: cannot parse line {raw!r}")
        files[path] = sha
    return commit, files


def emit_lock(commit: str, files: dict[str, str]) -> str:
    """Render (commit, files) back to lock-file text, sorted by path."""
    lines = [f"commit {commit}", ""]
    lines.extend(f"{files[p]}  {p}" for p in sorted(files))
    return "\n".join(lines) + "\n"


def load_lock(src: Source) -> tuple[str, dict[str, str]]:
    lock = repo_root(src.lock_name) / src.lock_name
    return parse_lock(lock.read_text(), source=src.lock_name)


def write_lock(src: Source, commit: str, files: dict[str, str]) -> None:
    lock = repo_root(src.lock_name) / src.lock_name
    tmp = lock.with_suffix(lock.suffix + ".part")
    tmp.write_text(emit_lock(commit, files))
    tmp.replace(lock)


def validate_or_record(
    files: dict[str, str], path: str, digest: str
) -> bool:
    """Decide what to do about a newly-hashed download.

    - If `path` is absent from `files`, record it (mutates `files`) and
      return True to signal the caller should write the lock back.
    - If `path` matches, return False.
    - If `path` mismatches, raise SystemExit.
    """
    expected = files.get(path)
    if expected is None:
        files[path] = digest
        return True
    if expected != digest:
        raise SystemExit(
            f"sha256 mismatch for {path!r}\n"
            f"  expected: {expected}\n"
            f"  got:      {digest}"
        )
    return False


def fetch(src: Source, path: str, sha: str | None = None) -> Path:
    """Return a local cache path for `path` within `src`'s upstream
    repo, downloading if not already cached.  Validates downloaded
    bytes against the per-file sha256 in the lock file; records
    unknown paths on first fetch.  An explicit `sha` override skips
    the manifest check — the manifest is a contract for the pinned
    commit only, and recording an off-pin digest under that contract
    would pollute it."""
    commit, files = load_lock(src)
    pinned = sha is None or sha == commit
    sha = sha or commit
    cache = repo_root(src.lock_name) / ".cache" / src.cache_dir / sha / path
    if cache.is_file():
        return cache
    url = f"{RAW}/{src.repo}/{sha}/{path}"
    cache.parent.mkdir(parents=True, exist_ok=True)
    tmp = cache.with_suffix(cache.suffix + ".part")
    hasher = hashlib.sha256()
    try:
        with urllib.request.urlopen(url) as resp, tmp.open("wb") as f:
            while chunk := resp.read(1 << 16):
                hasher.update(chunk)
                f.write(chunk)
    except urllib.error.HTTPError as e:
        tmp.unlink(missing_ok=True)
        raise SystemExit(f"fetch {url}: HTTP {e.code}") from e
    if pinned:
        try:
            if validate_or_record(files, path, hasher.hexdigest()):
                write_lock(src, commit, files)
        except SystemExit as e:
            tmp.unlink(missing_ok=True)
            raise SystemExit(f"fetch {url}: {e}") from e
    tmp.rename(cache)
    return cache
