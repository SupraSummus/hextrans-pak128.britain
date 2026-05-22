# Special colours and reserved-palette PIXVALs

Companion to `CLAUDE.md` (engine facts, bake-unit conventions).
Authoritative reference: the Simutrans wiki page
[`en_SpecialColors`](https://simutrans-germany.com/wiki/wiki/en_SpecialColors).
This doc captures the four categories described there, how the
hex Britain port handles each, and the empirical state of the
catalog as of May 2026.

## Mechanism

Simutrans reserves 31 specific RGB888 triples (plus one
transparency key) that get **special handling** during pakset
encoding and at runtime:

  * `makeobj` (`descriptor/writer/image_writer.cc::pixrgb_to_pixval`)
    scans every opaque pixel of every input PNG.  Any pixel
    whose RGB matches an entry in the engine's `rgbtab[]` table
    is encoded as a **special-PIXVAL** `0x8000 + i`, *not* as a
    normal RGB555 pack.
  * At runtime the engine treats those PIXVALs as **palette
    indices** rather than direct colour data: the actual on-
    screen colour depends on the player (P1/P2), the time of
    day (day-night), or stays fixed (menu-gray, signal lamps).
  * The transparency key (`0xE7FFFF`) is handled separately at
    image load time via `image_writer.cc::SPECIAL`, not by
    PIXVAL substitution.  Pixels matching it become alpha-zero.

The encoding lives in the **main atlas**.  There is no separate
`_mask.png` on the engine side, even though pak128.Britain's
authoring workflow (the upstream `-65.py` "Make Masks" path)
emits one — that's authoring scaffolding, not what makeobj /
the runtime read.

The full 31-entry set sits in `pak/lightmap.py::
RGBTAB_RESERVED` (a frozenset; the source literal is laid out
in `rgbtab[]` order, the runtime type isn't ordered).  By
category:

### Player 1 (rgbtab indices 0–7)

Eight blue shades `0x244B67` (darkest) → `0xB0D2FF` (lightest),
runtime-substituted with the owning player's primary colour.
The eight shades form a brightness gradient — authoring a panel
that uses all eight (e.g. at different Lambert levels of one
surface) produces a single material that recolours coherently
when the player picks a new colour.

### Player 2 (rgbtab indices 8–15)

Eight yellow / brown shades `0x7B5803` → `0xFFF90D`, same
gradient structure as P1.  Substituted with the player's
secondary colour.

### Day-and-night entries (10 entries)

Two functional sub-groups:

  * **Constant-colour lamps** — read as the same RGB day or
    night: `0xFFFF53` (yellow), `0xFF211D` (red), `0x01DD01`
    (green), `0xFF017F` (magenta), `0x0101FF` (blue).  Used
    for signal aspects and lamp glows.
  * **Day-night shifts** — pixels recolour after dusk:
    `0x7F9BF1` (cool blue → cyan, brightens at night),
    `0x57656F` / `0x4D4D4D` / `0xC1B1D1` (greys → warm amber
    `0xD3C380`), `0xE3E3FF` (lavender-white → warm white
    `0xFFFFE3`).  Used on building facades for the "windows
    light up at night" effect.

### Menu gray (rgbtab indices 21–25)

Five fixed neutrals `0x6B6B6B`..`0xDFDFDF` that do **not**
darken at night — intended for UI cursors, marker overlays,
and other elements that need to stay legible regardless of
the in-game time.

### Transparency

`0xE7FFFF` (very pale cyan).  Engine treats matching opaque
pixels as fully transparent at load time.  Our pipeline uses
`MAGIC_PINK = (255, 0, 255)` internally and relies on the
final PNG's alpha channel, so we don't intersect this key
accidentally.

## Empirical state of the Britain port

Measured by counting reserved-palette opaque pixels in our
re-baked PNGs vs the matching upstream PNGs:

  * **Vehicles** — 0 P1/P2 pixels in any of 606 ported train
    PNGs.  Upstream PNGs spot-checked for two assets (vulcan,
    4wheel-1850s-first) likewise carry ~0 P1/P2 — consistent
    with Britain-Extended handling vehicle branding through
    the **livery system** (`livery_image[<name>][<facing>]=...`)
    rather than runtime-recolour.  See `CLAUDE.md` → "What to
    carry from upstream, tiered" for livery-system context.
    No regression from our re-bake on the vehicle side.
  * **Buildings (signalboxes, sampled)** — upstream uses player
    colours heavily.  `mechanical-signalbox-large.png` carries
    4090 P1 pixels using all 8 P1 shades, distributed ≥45/cell
    across the 16-cell 4×4 atlas; small and power-large
    variants carry 1120 / 586 px (6 / 2 distinct P1 shades).
    Our re-bake of `mechanical_signalbox_large.png` has 0
    deliberate P1 + 3 stray `DN.lampdark` pixels (AA noise —
    see below).  **Shipped regression**: in-game you can't
    tell whose signalbox it is.  Likely extends to other
    player-owned buildings (depots, stations, HQs); not
    measured.
  * **Day-night lighting** — not measured.

## Why `Make Masks` doesn't apply

`render_SimutransRender_pak128Britain-65.py` (jamespetts/Pak128.
Britain-blends) carries a "Make Masks" Blender operator that
iterates `bpy.data.materials`, finds names starting with `sp_`,
swaps window-glass colours to magenta and enables `use_shadeless`
on the rest.  The `sp_*` convention is documented in `CLAUDE.md`
→ "Don't bake the answer".

In practice, none of the three signalbox blends we have
(`signals/mechanical-signalbox-{large,small}.blend`,
`signals/power-signalbox-large.blend`) contain a single `sp_*`
material.  Porting the `-65` material-swap into our `render.py`
would do nothing on the current building catalog.  Upstream's
signalbox masks must come from one of:

  1. Hand-painting post-render — plausible for the small panels
     observed (lettering area, window frames).
  2. A `sp_*`-bearing blend revision in upstream history,
     subsequently refactored out.
  3. An alternate blend from the JamesHood repo or pre-`.blend`-
     era vendored PNGs.

Not investigated which.  Whichever the answer, the path forward
for the hex port is to **author the masks ourselves** rather
than try to port upstream's.

## Cycles AA into the reserved palette

Cycles anti-aliasing dither randomly produces opaque pixels
whose RGB lands exactly on a reserved triple even when no
`sp_*` material is involved.  Observed: 3 px of `DN.lampdark`
(`0x4D4D4D`) on `mechanical_signalbox_large.png`, 1–2 px of
the same triple scattered across train atlases.  makeobj
encodes them as special-PIXVAL `0x8000 + 28` and the runtime
animates them at dusk — flickering pixels with no apparent
cause.  Tiny per asset, but it accumulates and triggers from
ordinary rendering rather than authored intent.

The matching defensive primitive already exists for the **ground**
side: `pak/lightmap.py::safe_face_rgb` nudges a Lambert grey
that lands on a reserved triple by ±1 RGB unit so makeobj falls
into the normal-RGB555 path.  Same trick applies inverted for
the **sprite** side — snap any opaque pixel in `RGBTAB_RESERVED`
*away* from the palette unless we put it there on purpose.

## What's wired up today

`pak/lightmap.py::RGBTAB_RESERVED` carries all 31 triples and is
consumed by `safe_face_rgb` to keep the ground-Lambert encoding
off the reserved palette.  Nothing on the sprite side touches
the mechanism yet — the defensive snap and per-asset mask
mechanisms in TODO.md are both unimplemented.

Note: `RGBTAB_RESERVED` currently lives in `lightmap.py` because
that's the file with the only consumer.  Adding a sprite-side
consumer would be a reasonable trigger to move the constant to
a dedicated `pak/special_colors.py` and have `lightmap.py`
import it — mechanical move, deferrable.

## Open work

See `TODO.md` → "Special-colour PIXVAL handling" for the two
concrete passes: catalog-wide defensive snap (no trigger), and
per-asset mask authoring (per-asset trigger).
