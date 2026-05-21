# Porting process

Notes for porting upstream pak128.Britain assets to hex bake
units.  Companion to `CLAUDE.md` (engine facts, bake-unit shape,
schema contract).

Validated empirically: ~600 train ports run unsupervised in one
session under the workflow below.  Acceptance ~70 % overall;
rejected assets are catastrophic-IoU (matcher picked wrong
blend) or upstream stubs (no image refs, 404 PNGs).

## Workflow

The end-to-end shape per asset (driven by `/tmp/autoport.py`-
style tooling in unsupervised runs, manual for tricky cases):

1. **Pick** an unported dat + candidate blend.
   `python3 -m pak.bake_units --unported trains` lists unported;
   `python3 -m pak.blend_index trains` groups by candidate blend
   (token-subseq match against both upstream blend repos).
2. **Seed** the SPEC.  `pak.dat.parse(dat) | pak.dat.port_vehicle`
   gives a populated `Vehicle`; `seed_python` renders the non-
   default fields.  Add `blend=` and `upstream_dat=` (bake-meta).
3. **Bake.**  `python3 -m <category>.<module>` (Cycles backend,
   ~5-15 s per facing).
4. **Check.**  `python3 -m pak.check <path>` runs `diff_upstream`,
   prints per-facing IoU/XOR/dRGB.  Exit code uses the strict
   FAIL_IOU=0.90 threshold; for unsupervised porting, parse the
   table and use the soft floor (below).
5. **Ship** if soft acceptance holds: `git rm` the upstream dat,
   `git add` the new triple + `blends.lock` + `pak.lock`, commit.
6. **Push** every few ports so partial progress survives.

## Soft acceptance

Hard structural floor (must pass):

- Atlas exists with all 8 facings; bbox non-empty per facing.
- Dat round-trips (`pak.reemit_dats` clean).
- `ruff check` clean.
- The autoport script's `_cleanup_failed` reverts `blends.lock`
  / `pak.lock` on skip to avoid TOFU drift on assets we don't
  ship.

Calibration floor: **worst-facing IoU ≥ 0.5**.  Below that the
visual is unrecognizable (rotated, mis-scaled, wrong model).  At
0.5-0.93, ship anyway — the asset is close enough to be playable
and the polish gap is human-vision work, not auto-tunable.  At
≥ 0.93 it's near-calibration-grade.

Empirical distribution from the train trial (n=595):

- ≥ 0.90: 62 %.  Matcher picked the right blend or a close
  visual variant; bake pipeline produced the same render upstream
  did.  Median IoU across all shipped ports is 0.92.
- 0.50-0.90: 38 %.  Usually a livery mismatch — matcher picked
  a livery-specific blend (e.g. `br-cl30-green`) for a dat with
  generic livery refs; silhouette is right, colour is wrong.
  Ships with a low IoU note for later polish.
- < 0.50: skipped, not part of the 595.  Wrong asset entirely
  (matcher picked the wrong upstream blend); autoport's
  `_cleanup_failed` reverts the triple + lock entries.

70 % overall acceptance against the full attempt set; the other
30 % split between catastrophic-IoU (skipped + cleaned) and
upstream stub dats (no image refs / 404 PNG fetches — see below).

## Failure modes seen in the wild

**Upstream dat is a stub** — `EmptyImage[…]=` references missing
or pointing at nonexistent PNGs.  `pak.check` fails fetch
(HTTP 404) or reports no image refs.  Not portable; the upstream
dat itself needs maintenance.  Skip.

**Module-name collision** — when a dat has no hyphens
(`vulcan.dat`), the naive `dat.stem.replace('-','_')` produces
the same stem as upstream and the bake overwrites the upstream
dat before `git rm` runs.  Fix: prepend `_` when the renamed
stem equals the original.

**Nested-dir categories** — `boats/boats192/<asset>.dat` and
`air/air192/<asset>.dat` break the flat `<category>/<module>.py`
assumption.  Autoport doesn't currently handle these; manual
ports work but need a `__init__.py` in the subdir.

**Multi-object dats with distinct blends** — loco + tender, EMU
sets.  Each object renders from its own blend.  The current
autoport pattern (`SPECS = [...]` sharing one blend via
`_BLEND`) handles only shared-blend multi-object dats.  Distinct
blends need separate bake calls per object — see CLAUDE.md →
"Bake unit shape".

**Wrong-livery match** — matcher picks `br-cl30-green.blend` for
`br-cl30.dat` because that's the only `br-cl30-*` blend in
upstream, but the dat's image refs are for a different livery
(say BR-blue).  IoU lands in the 0.6-0.85 band; silhouette
matches, colour doesn't.  Ships with the note; needs manual
material recolour for full calibration.

**Token-mismatch orphans** — dats with bracketed suffixes
(`br-410[cep].dat`), trailing -0/-2 variants (`br-172-0.dat`),
or special chars (`l&s-…`) don't tokenize cleanly.  Loose
matching (first 2 dat tokens as prefix) recovers some at the
cost of higher false-positive rate.

## What not to do

- **Don't tune `materials=` to match upstream pixels** in
  unsupervised runs.  That requires vision-supervised iteration
  the agent doesn't have.  Material polish is a separate later
  pass over the shipped pool.
- **Don't edit `pak/` infrastructure or `CLAUDE.md`** during an
  asset port.  Real bugs in shared code need their own PR.
  Stowaway edits inside batch port commits are hard to review.
- **Don't extend the matcher to chase orphans aggressively.**
  False positives are worse than orphans — agents pick the
  wrong blend, the bake passes structural checks at low IoU,
  and ships visual garbage.  Better to skip and write a TODO
  entry naming the dat.

## Catalog-wide checks after a batch

- `python3 -m pak.reemit_dats` — every bake script's SPEC
  re-emits the committed dat (`git diff --exit-code -- '*.dat'`
  must be clean).
- `ruff check .` — top-of-file extracted upstream comments
  often have trailing whitespace; `ruff check . --fix` handles
  it mechanically.
- `python3 -m unittest discover tests/` — should pass before
  pushing a batch.
