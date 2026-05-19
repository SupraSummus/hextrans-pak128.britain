# Tree-bake architecture

Companion to `CLAUDE.md` (engine facts, calibration contract,
bake-unit conventions).

Trees (`Obj=tree`) port via a `Tree` SPEC with inline
`blend=` / `upstream_dat=` bake-meta and a `bake_tree_main(SPEC,
__file__)` call, same per-asset shape as vehicles/ways/buildings.
The render side is a single-facing billboard expanded over an
`ages × seasons` grid -- one cell per (age, season) tuple.

**Engine schema** (`descriptor/writer/tree_writer.cc`).  Five ages
(0..4) and 1/2/4/5 seasonal variants -- writer hardcodes the age loop
bound, fatals on a missing `image[age][season]` key.  `TREE_AGE_COUNT`
in `pak.dat` exposes the constant; `clamp_age_overrides` (`pak.bake`)
builds the fallback dict for the typical case where the bake renders
fewer ages than the engine reads.

**Atlas layout.**  `seasons` rows × `ages` cols.  Row = season (top
= summer = 0), col = age (left = youngest = 0).  Dat refs follow
`image[age][season]=./<basename>.<season>.<age>`.

**Age stages.**  Upstream pak128.Britain renders the same model at
four successive scales (`_TREE_AGE_SCALES` = 0.375 / 0.5 / 0.76 / 1.0,
sampled from upstream PNG bbox heights) and points engine age 4 (the
dormant / dying stage) at the bare `winter-3` cell.  Our bake mirrors
this via `Facing.model_scale` (one Facing per age in
`_tree_facings`) and `clamp_age_overrides` (fallback at dat-emit
time).  Age-0 silhouette doesn't match upstream under uniform scaling
-- see TODO.md "Tree age-0 silhouette" for the working theory
(upstream uses a per-age model variant we haven't located).

**Lighting calibration.**  Britain tree blends ship a SPOT lamp
rather than a SUN; `_strip_scene`'s authored-SUN extraction returns
None and `tree_*_viewpoint` pins `sun_energy=2.0` directly, matching
the post-scale value the building viewpoints resolve to under EEVEE.
EEVEE engine, normal-alignment camera (the blend's authored
`(10, -10, 11.6)` is the S-cardinal normal-alignment position) at
the blend's authored ortho_scale (12, half the vehicle convention).

**Landmines specific to trees:**

* **`Plane` ground reference.**  Britain tree blends ship a ~8×8
  grey ground plane (material `Material.003`, diffuse 0.8 white) at
  `z ≈ 0.29` with `hide_render=False` in a non-hidden collection,
  but upstream's published PNGs don't show it -- upstream's render
  workflow hides it via a step that doesn't ship with the blend.
  `tree_*_viewpoint` adds `"Plane"` to `Viewpoint.strip_meshes`
  alongside the default `"Sphere"`.

* **Per-season leaf-colour calibration.**  The engine's seasons
  axis is the .blend material's diffuse-colour swap upstream paints
  manually before each per-season render.  Phase 1 ships `seasons=1`
  (summer only) honestly; the autumn / winter / spring / winter-snow
  rows are a Phase 2 calibration pass (TODO.md → tree per-season
  leaf-colour).  Avoid the temptation to ship `seasons=5` with
  every row redirecting to summer -- the dat would lie about what
  in-engine behaviour we deliver.

* **Hex projection has no ground truth.**  `tree_square_viewpoint`
  diffs against upstream's published `<stem>-<season>-<age>_S.png`;
  hex applies `_hex_fit()` against blend coords (intra-tile scale
  = `2R/blend_ortho`) and is validated only against the matching
  square render.  A future hex regression that doesn't affect the
  square diff has no automated catch -- see TODO.md.
