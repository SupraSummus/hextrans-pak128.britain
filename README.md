# pak128.Britain (hex port)

A port of the [pak128.Britain][upstream-pak] pakset to the hex-grid
engine [`SupraSummus/hextrans`][engine].  Forked from the
Simutrans-Extended flavour at `jamespetts/simutrans-pak128.britain`;
sprites are re-rendered from the upstream
[blends repo][blends] through a hex camera.

## Status

Work in progress and **unplayable** until a critical mass of
ground, way and vehicle assets has been baked.  The engine itself
is not yet shipping either.  `TODO.md` tracks which assets have
crossed the line; `CLAUDE.md` documents the porting conventions
and bake pipeline.

## Building

```
make MAKEOBJ=<path to makeobj from hextrans> clean all archives
```

`makeobj` is built from the [`SupraSummus/hextrans`][engine] tree;
it diverges from upstream Simutrans `makeobj` for hex schema
support.  Sound effects and the boot-screen deliverables are
fetched at build time from the SHA-pinned upstream pak via
`pak.lock`; sprite blends are fetched at bake time via
`blends.lock`.  `.github/workflows/build.yml` publishes nightly
archives to the repo's `Nightly` GitHub release.

## Documentation

* `CLAUDE.md` — porting conventions, bake pipeline, repo strategy.
* `TODO.md` — open work, blockers, suspected bugs.
* `docs/` — per-class bake architecture notes (`bake-building.md`,
  `bake-tree.md`, `bake-way.md`).
* `CHANGELOG.md` — upstream 2009–2011 release history (pre-fork);
  this fork's history is in `git log`.

## Licence

Released open source under the Artistic License.  See
[`licence.txt`](licence.txt).  Sprite source blends and the
upstream `.dat` catalog inherit their licences from the upstream
repos linked above.

[upstream-pak]: https://github.com/jamespetts/simutrans-pak128.britain
[engine]: https://github.com/SupraSummus/hextrans
[blends]: https://github.com/jamespetts/Pak128.Britain-blends
