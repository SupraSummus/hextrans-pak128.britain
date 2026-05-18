"""Diagnose why a freshly-baked PNG differs from its committed version.

Run as `python3 -m pak.diag_png_drift <path1> [<path2> ...]`.  For each
path, compares the working-tree bytes against `git show HEAD:<path>` and
prints:

  * file sizes
  * PNG chunk list side by side (which chunk types / lengths differ)
  * raw bitmap hash (sha256 over decoded pixel array) -- equal here
    means it's a PNG-encoding-only difference (zlib / chunk layout)
  * if the bitmaps differ: differing-pixel count, max per-channel delta,
    coordinates of the first few differing pixels.

Not used inside Blender -- PIL is fine.
"""
from __future__ import annotations

import hashlib
import io
import struct
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def _iter_chunks(data: bytes):
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    i = 8
    while i < len(data):
        n = struct.unpack(">I", data[i:i + 4])[0]
        t = data[i + 4:i + 8].decode("ascii", errors="replace")
        yield t, n
        if t == "IEND":
            return
        i += 12 + n


def _decode(data: bytes) -> np.ndarray:
    return np.asarray(Image.open(io.BytesIO(data)).convert("RGBA"))


def _diag_one(path: Path) -> None:
    print(f"=== {path} ===")
    wt = path.read_bytes()
    head = subprocess.check_output(["git", "show", f"HEAD:{path}"])
    print(f"sizes: HEAD={len(head)} working={len(wt)}  "
          f"({'same' if len(head) == len(wt) else 'DIFFER'})")
    if wt == head:
        print("bytes identical -- nothing to diagnose")
        return

    head_chunks = list(_iter_chunks(head))
    wt_chunks = list(_iter_chunks(wt))
    print("chunks (HEAD vs working; ** = differ):")
    for (th, lh), (tw, lw) in zip(head_chunks, wt_chunks, strict=False):
        mark = "**" if (th, lh) != (tw, lw) else "  "
        print(f"  {mark} {th} {lh:>8}    {tw} {lw:>8}")
    if len(head_chunks) != len(wt_chunks):
        print(f"  ** chunk count differs: HEAD={len(head_chunks)} "
              f"working={len(wt_chunks)}")

    head_px = _decode(head)
    wt_px = _decode(wt)
    head_hash = hashlib.sha256(head_px.tobytes()).hexdigest()[:16]
    wt_hash = hashlib.sha256(wt_px.tobytes()).hexdigest()[:16]
    print(f"bitmap sha256 (16-prefix): HEAD={head_hash} working={wt_hash}")
    if head_px.shape != wt_px.shape:
        print(f"shape differs: HEAD={head_px.shape} working={wt_px.shape}")
        return
    if head_hash == wt_hash:
        print("PIXEL DATA IDENTICAL -- PNG-encoding-only difference "
              "(zlib / chunk layout / filter choice)")
        return
    diff = head_px.astype(np.int16) - wt_px.astype(np.int16)
    nonzero = np.any(diff != 0, axis=-1)
    n_diff = int(nonzero.sum())
    print(f"PIXEL DATA DIFFERS: {n_diff}/{nonzero.size} pixels "
          f"({100.0 * n_diff / nonzero.size:.4f}%)")
    print(f"max abs per-channel delta: {int(np.abs(diff).max())}")
    print(f"mean abs per-channel delta (over differing pixels): "
          f"{float(np.abs(diff[nonzero]).mean()):.3f}")
    ys, xs = np.where(nonzero)
    for y, x in list(zip(ys, xs, strict=True))[:8]:
        print(f"  pixel ({x},{y}): HEAD={tuple(head_px[y, x])} "
              f"working={tuple(wt_px[y, x])}")


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python3 -m pak.diag_png_drift <png> [<png> ...]",
              file=sys.stderr)
        return 2
    for arg in sys.argv[1:]:
        _diag_one(Path(arg))
    return 0


if __name__ == "__main__":
    sys.exit(main())
