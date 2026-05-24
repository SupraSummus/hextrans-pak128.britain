# Tunnel-bake architecture

Companion to `CLAUDE.md` (engine facts, calibration contract,
bake-unit conventions).

Tunnels (`Obj=tunnel`) port via a `Tunnel` SPEC with inline
`blend=` / `upstream_dat=` bake-meta and a `bake_main(SPEC,
__file__)` call.  Six hex-edge portal facings render through
`tunnel_hex_viewpoint()` into a single-row 6-cell atlas.  Facing
labels are `n, ne, se, s, sw, nw` matching `hex_keys::edge_names`
in the engine writer; `emit_tunnel` ships lowercase
`frontimage[<edge>][0]=` only.

**Two opposite key conventions live in this codebase.**  The hex
engine uses **low-edge** naming -- `frontimage[<edge>]` = portal
whose mouth faces `<edge>` (the direction a train exits) -- so
`_HEX_TUNNEL_MODEL_ROT_DEG`'s rotation table is just
`θ(e) = world_angle_of(e)`.  Upstream pak128.Britain inherits
pak64's **high-edge** naming -- key names the edge the mountain
rises against, mouth points opposite -- so `FrontImage[S]` shows
mouth-points-north.  `tunnel_desc.cc:9-34` documents the engine's
N↔S, E↔W permutation between the two ("pre-port pak64 tunnel
images load at slots with N↔S and E↔W permuted; new hex art needs
to follow the low-edge convention").  Production hex stays
low-edge; `tunnel_square_viewpoint`'s calibration rotation table
goes high-edge so a label-to-label diff against upstream cells
aligns cell-for-cell.

**Diff stitch.**  `diff_tunnel` alpha-composites upstream's
`BackImage` under `FrontImage` per facing -- same pattern as
`diff_buildings._stitch_upstream_layout` specialised to the
tunnel case where both layers land on the same 128² cell.
Stone-tunnel ships Back only for N/W, so S/E rows fall back to
Front-only and carry an XOR contribution from our whole-portal
silhouette (worst IoU ~0.72 on those rows, ~0.81 on Back-present
rows; `FAIL_IOU=0.65`).  Future variants (e.g. brick-face) that
ship Back on all four cardinals will test the apples-to-apples
Back+Front path directly.
