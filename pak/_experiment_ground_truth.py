"""Ground-truth experiment: perturb a known-converged Building's pin
by a synthetic offset, re-render, and check `diag_centroid_align`
recovers the perturbation's negation.

If the renderer applies `Translation(-pin)` and the solver inverts that
correctly, then setting `pin = baseline + delta` should produce a fit
that says `-delta` (modulo the unfittable per-facing residual already
present at baseline).  Sign error, rotation direction error, axis swap,
or magnitude error all surface as a mismatch between expected and
recovered.

This is a one-shot validation script, not part of the regression suite
(needs Blender + blend fetch).  Run from the repo root::

    python3.12 -m pak._experiment_ground_truth
"""
from __future__ import annotations

import re
import subprocess
import sys

from pak import REPO_ROOT

SCRIPT = REPO_ROOT / "signalboxes" / "mechanical_signalbox_large.py"
BASELINE = (0.0, 0.0, 2.14)  # pinned value that converged at R²=35 % residual
PERTURBATIONS = [
    (0.0, 0.0, +1.0),
    (0.0, 0.0, -1.0),
    (+1.0, 0.0, 0.0),
    (0.0, +1.0, 0.0),
    (+0.5, -0.3, +0.5),
]

_PIN_RE = re.compile(
    r"blend_model_offset_xyz=\([^)]*\)"
)
_FIT_RE = re.compile(
    r"^\s*xyz\s+([+-]?\d+\.\d+)\s+([+-]?\d+\.\d+)\s+([+-]?\d+\.\d+)\s+"
    r"([+-]?\d+\.\d+)",
    re.M,
)


def _set_pin(pin: tuple[float, float, float]) -> str:
    text = SCRIPT.read_text()
    new = f"blend_model_offset_xyz=({pin[0]:+.2f}, {pin[1]:+.2f}, {pin[2]:+.2f})"
    patched, n = _PIN_RE.subn(new, text)
    if n != 1:
        raise SystemExit(f"expected 1 pin line in {SCRIPT}, found {n}")
    SCRIPT.write_text(patched)
    return text  # original, for restore


def _run(cmd: list[str], *, allow_nonzero: bool = False) -> str:
    """Run a command and capture stdout.  `pak.check` exits non-zero when
    IoU is below `FAIL_IOU` (signalbox at ~0.7 < 0.88 floor), which we
    don't care about here -- we just need the diff artefacts written."""
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0 and not allow_nonzero:
        sys.stderr.write(res.stderr)
        raise SystemExit(f"command failed: {' '.join(cmd)}")
    return res.stdout


def _measure(pin: tuple[float, float, float]) -> tuple[float, float, float, float]:
    original = _set_pin(pin)
    try:
        _run(["python3.12", "-m", "pak.check", str(SCRIPT)], allow_nonzero=True)
        out = _run(["python3.12", "-m", "pak.diag_centroid_align", str(SCRIPT)])
    finally:
        SCRIPT.write_text(original)
    m = _FIT_RE.search(out)
    if not m:
        raise SystemExit(f"no xyz row in diag output:\n{out}")
    return tuple(float(g) for g in m.groups())  # (mx, my, mz, r2)


def main() -> int:
    print(f"baseline pin: {BASELINE}")
    base_mx, base_my, base_mz, base_r2 = _measure(BASELINE)
    print(f"  baseline residual fit: ({base_mx:+.2f}, {base_my:+.2f}, "
          f"{base_mz:+.2f}) R²={base_r2:.2f}\n")

    print(f"  {'delta':<22} {'expected (-delta)':<22} "
          f"{'recovered':<22} {'err':<6}  R²")
    for delta in PERTURBATIONS:
        pin = tuple(BASELINE[i] + delta[i] for i in range(3))
        mx, my, mz, r2 = _measure(pin)
        # The recovered fit reports the residual from baseline drift plus
        # the negation of our perturbation.  Subtract baseline residual to
        # isolate the perturbation response.
        rec = (mx - base_mx, my - base_my, mz - base_mz)
        expected = tuple(-d for d in delta)
        err = max(abs(rec[i] - expected[i]) for i in range(3))
        d = f"({delta[0]:+.2f},{delta[1]:+.2f},{delta[2]:+.2f})"
        e = f"({expected[0]:+.2f},{expected[1]:+.2f},{expected[2]:+.2f})"
        r = f"({rec[0]:+.2f},{rec[1]:+.2f},{rec[2]:+.2f})"
        flag = "  OK" if err < 0.3 else "  ⚠"
        print(f"  {d:<22} {e:<22} {r:<22} {err:<5.2f} {r2:.2f}{flag}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
