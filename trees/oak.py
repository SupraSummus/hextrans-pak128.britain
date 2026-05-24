from pak.bake import bake_main
from pak.dat import Tree

# Upstream declares `seasons=5`; ours is `1` until leaf-colour
# calibration (TODO.md → tree per-season leaf-colour) makes the other
# four rows distinguishable from summer.
SPEC = Tree(
    name="EnglishOak",
    copyright="James",
    distribution_weight=180,
    climates="temperate,mediterran,tropical",
    seasons=1,
    blend="trees/oak.blend",
    upstream_dat="trees/oak.dat",
)

if __name__ == "__main__":
    bake_main(SPEC, __file__)
