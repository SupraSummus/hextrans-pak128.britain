"""Minimal .blend parser for the BI texture-slot data the modern API drops.

The Britain pak's blends are all saved by Blender 2.42 or 2.48 (BI-era),
and their binary still carries the full pre-2.5 Material struct -- including
`MTex *mtex[10]` slot pointers and per-material `alpha`.  Blender 4.0 drops
this on load (Material has no `texture_slots` since 2.80), but the data
is intact in the file.  This module reads it directly.

Status: foundation + diagnostic.  No production consumer yet.  Designed to
unblock the slot-driven material binding described in TODO.md ("Building
material->texture binding can read from .blend binary").  Until that lands,
run `python3 -m pak.blend_slots <blend_path>` to inspect what the binary
carries for a given asset.

Targets pre-2.5 blends specifically -- BAT (blender-asset-tracer) doesn't
support these (looks for `DNA1` block in the wrong position; pre-2.5
files have it but with the older block-header size).  Not a general
parser; only the structs the future renderer needs.
"""
from __future__ import annotations

import gzip
import io
import struct
from dataclasses import dataclass, field
from pathlib import Path

# DNA_texture_types.h constants.  TEXCO_ORCO/_GLOB/_UV are the three the
# Britain blends actually use; full enum is wider.
TEXCO_ORCO = 1
TEXCO_GLOB = 8
TEXCO_UV = 16

# Tex.flag bit 0: when set, the Tex's `coba` ColorBand maps the
# texture's intensity to RGB at render time; otherwise BI falls back
# to the MTex slot's per-slot RGB.
TEX_COLORBAND = 1

# The Britain blends only use these subset of Tex.type values; rest are
# present in the format but irrelevant to this pak.
_TEX_TYPE = {
    1: "CLOUDS", 2: "WOOD", 6: "STUCCI", 7: "NOISE",
    8: "IMAGE", 11: "MUSGRAVE",
}


@dataclass
class TextureSlot:
    slot_idx: int
    tex_type: str           # "IMAGE", "CLOUDS", "NOISE", "MUSGRAVE", "STUCCI", "WOOD", or "OTHER"
    image_name: str         # "" if not IMAGE
    size: tuple[float, float, float]
    ofs: tuple[float, float, float]
    texco: int              # 1=ORCO 8=GLOBAL 16=UV
    blendtype: int          # 0=MIX 1=MUL 2=ADD ...
    colfac: float
    # MTex per-slot RGB (`MTex.r/g/b`).  BI uses this as the slot's
    # texture-output colour when the Tex itself doesn't supply RGB --
    # i.e. for procedural textures without `TEX_COLORBAND` set, or
    # without `stype = TEX_COLOR`.  Default for unused IMAGE slots
    # is the magenta sentinel `(1.0, 0.0, 1.0)`; meaningful only for
    # procedural slots that the renderer composites as a flat colour.
    color: tuple[float, float, float] = (1.0, 1.0, 1.0)
    # ColorBand entries from the Tex datablock when `TEX_COLORBAND`
    # (`Tex.flag & 1`) is set.  None if the flag is unset, in which
    # case BI falls back to `color` (above).  Each entry is
    # `(pos, r, g, b, a)`.
    color_band: list[tuple[float, float, float, float, float]] | None = None


@dataclass
class MaterialSlots:
    name: str               # ID name without the "MA" prefix
    rgb: tuple[float, float, float]
    alpha: float
    slots: list[TextureSlot] = field(default_factory=list)


@dataclass
class _StructDef:
    fields: list[tuple[str, str, int]]  # (type_name, raw_field_name, offset)


def _read_data(path: Path) -> bytes:
    with open(path, "rb") as f:
        if f.read(2) == b"\x1f\x8b":
            return gzip.open(path, "rb").read()
    return open(path, "rb").read()


def _array_count(raw_name: str) -> int:
    """Number of array elements encoded in a DNA field name like `mtex[10]`
    or `ofs[3][4]`; 1 if there are no brackets."""
    n = 1
    s = raw_name
    while "[" in s:
        lb = s.index("["); rb = s.index("]", lb)
        n *= int(s[lb + 1:rb])
        s = s[rb + 1:]
    return n


def _is_pointer(raw_name: str) -> bool:
    return raw_name.startswith("*") or raw_name.startswith("(*")


def _read_cstr_array(buf: io.BytesIO, count: int) -> list[str]:
    out = []
    for _ in range(count):
        chars = bytearray()
        while True:
            ch = buf.read(1)
            if ch == b"\x00":
                break
            chars.extend(ch)
        out.append(chars.decode("ascii", errors="replace"))
    return out


def _align(buf: io.BytesIO, n: int) -> None:
    pad = (-buf.tell()) % n
    if pad:
        buf.read(pad)


class _Parser:
    """One-shot parser; not reusable across files."""

    def __init__(self, path: Path):
        data = _read_data(path)
        if not data.startswith(b"BLENDER"):
            raise ValueError(f"not a blend file: {path}")
        self.ptr_size = 4 if data[7:8] == b"_" else 8
        self.endian = "<" if data[8:9] == b"v" else ">"
        self.ptr_fmt = self.endian + ("I" if self.ptr_size == 4 else "Q")

        self.blocks: list[tuple[bytes, bytes]] = []  # (code, body)
        self.by_addr: dict[int, int] = {}
        off = 12
        while off < len(data):
            code = data[off:off + 4]
            size = struct.unpack(self.endian + "I", data[off + 4:off + 8])[0]
            addr = struct.unpack(self.ptr_fmt, data[off + 8:off + 8 + self.ptr_size])[0]
            hdr = 16 + self.ptr_size
            body = data[off + hdr:off + hdr + size]
            if addr:
                self.by_addr[addr] = len(self.blocks)
            self.blocks.append((code, body))
            off += hdr + size
            if code == b"ENDB":
                break

        dna = next(b for code, b in self.blocks if code == b"DNA1")
        self._parse_dna(dna)

    def _parse_dna(self, dna: bytes) -> None:
        b = io.BytesIO(dna)
        assert b.read(4) == b"SDNA"
        assert b.read(4) == b"NAME"
        names = _read_cstr_array(b, struct.unpack(self.endian + "I", b.read(4))[0])
        _align(b, 4)
        assert b.read(4) == b"TYPE"
        nt = struct.unpack(self.endian + "I", b.read(4))[0]
        types = _read_cstr_array(b, nt)
        _align(b, 4)
        assert b.read(4) == b"TLEN"
        type_sizes = list(struct.unpack(self.endian + ("H" * nt), b.read(2 * nt)))
        _align(b, 4)
        assert b.read(4) == b"STRC"
        ns = struct.unpack(self.endian + "I", b.read(4))[0]
        self.structs: dict[str, _StructDef] = {}
        for _ in range(ns):
            type_idx, n_fields = struct.unpack(self.endian + "HH", b.read(4))
            type_name = types[type_idx]
            fields = []
            offset = 0
            for _ in range(n_fields):
                ft_idx, fn_idx = struct.unpack(self.endian + "HH", b.read(4))
                ft = types[ft_idx]
                fn = names[fn_idx]
                fields.append((ft, fn, offset))
                base = self.ptr_size if _is_pointer(fn) else type_sizes[ft_idx]
                offset += base * _array_count(fn)
            self.structs[type_name] = _StructDef(fields)

    def _field(self, struct_name: str, body: bytes, field_name: str):
        for ft, fn, off in self.structs[struct_name].fields:
            if fn.lstrip("*").split("[")[0] != field_name:
                continue
            arr = _array_count(fn)
            if _is_pointer(fn):
                if arr == 1:
                    return struct.unpack(self.ptr_fmt, body[off:off + self.ptr_size])[0]
                return list(struct.unpack(
                    self.endian + ("I" if self.ptr_size == 4 else "Q") * arr,
                    body[off:off + self.ptr_size * arr]
                ))
            if ft == "float":
                if arr == 1:
                    return struct.unpack(self.endian + "f", body[off:off + 4])[0]
                return list(struct.unpack(self.endian + "f" * arr, body[off:off + 4 * arr]))
            if ft == "short":
                return struct.unpack(self.endian + "h", body[off:off + 2])[0]
            if ft == "int":
                return struct.unpack(self.endian + "i", body[off:off + 4])[0]
            if ft == "char" and arr > 1:
                raw = body[off:off + arr]
                end = raw.find(b"\x00")
                return (raw[:end] if end >= 0 else raw).decode("ascii", errors="replace")
            return None
        raise KeyError(f"{struct_name}.{field_name}")

    def _id_name(self, body: bytes) -> str:
        """ID-named struct's `name[N]` field, stripped of the 2-char type prefix
        (e.g. `MA` for Material, `TE` for Texture, `IM` for Image)."""
        name_off = next(o for t, n, o in self.structs["ID"].fields
                        if n.startswith("name"))
        raw = body[name_off:name_off + 64]
        end = raw.find(b"\x00")
        s = (raw[:end] if end >= 0 else raw).decode("ascii", errors="replace")
        return s[2:] if len(s) > 2 else s

    def _maybe_field(self, struct_name: str, body: bytes, field_name: str, default):
        try:
            return self._field(struct_name, body, field_name)
        except KeyError:
            return default


def extract(path: Path) -> dict[str, MaterialSlots]:
    """Returns {material_name -> MaterialSlots} for every Material in the
    blend.  Material names have the "MA" ID prefix stripped (i.e. they match
    what `bpy.data.materials[name]` uses in Blender 4.0)."""
    P = _Parser(path)
    out: dict[str, MaterialSlots] = {}

    for code, body in P.blocks:
        if code != b"MA\x00\x00":
            continue
        ms = MaterialSlots(
            name=P._id_name(body),
            rgb=(
                P._maybe_field("Material", body, "r", 0.5),
                P._maybe_field("Material", body, "g", 0.5),
                P._maybe_field("Material", body, "b", 0.5),
            ),
            alpha=P._maybe_field("Material", body, "alpha", 1.0),
        )
        mtex_ptrs = P._field("Material", body, "mtex")
        if not isinstance(mtex_ptrs, list):
            mtex_ptrs = [mtex_ptrs]
        for slot_i, ptr in enumerate(mtex_ptrs):
            if ptr == 0:
                continue
            mt_idx = P.by_addr.get(ptr)
            if mt_idx is None:
                continue
            ms.slots.append(_read_slot(P, slot_i, P.blocks[mt_idx][1]))
        out[ms.name] = ms
    return out


def _read_slot(P: _Parser, slot_i: int, mt: bytes) -> TextureSlot:
    """Decode one MTex block into a TextureSlot."""
    tex_type = "OTHER"
    image_name = ""
    color_band = None
    tex_ptr = P._field("MTex", mt, "tex")
    if tex_ptr:
        tex_blk_i = P.by_addr.get(tex_ptr)
        if tex_blk_i is not None:
            tex_body = P.blocks[tex_blk_i][1]
            tex_type = _TEX_TYPE.get(
                P._maybe_field("Tex", tex_body, "type", 0), "OTHER"
            )
            tex_flag = P._maybe_field("Tex", tex_body, "flag", 0)
            if tex_type == "IMAGE":
                ima_ptr = P._maybe_field("Tex", tex_body, "ima", 0)
                if ima_ptr:
                    ima_idx = P.by_addr.get(ima_ptr)
                    if ima_idx is not None:
                        image_name = P._id_name(P.blocks[ima_idx][1])
            if tex_flag & TEX_COLORBAND:
                coba_ptr = P._maybe_field("Tex", tex_body, "coba", 0)
                if coba_ptr:
                    coba_idx = P.by_addr.get(coba_ptr)
                    if coba_idx is not None:
                        color_band = _read_color_band(P, P.blocks[coba_idx][1])

    size_xyz = P._field("MTex", mt, "size") or [1.0, 1.0, 1.0]
    ofs_xyz = P._field("MTex", mt, "ofs") or [0.0, 0.0, 0.0]
    return TextureSlot(
        slot_idx=slot_i,
        tex_type=tex_type,
        image_name=image_name,
        size=tuple(size_xyz),
        ofs=tuple(ofs_xyz),
        texco=P._field("MTex", mt, "texco") or 0,
        blendtype=P._field("MTex", mt, "blendtype") or 0,
        colfac=P._maybe_field("MTex", mt, "colfac", 1.0),
        color=(
            P._maybe_field("MTex", mt, "r", 1.0),
            P._maybe_field("MTex", mt, "g", 1.0),
            P._maybe_field("MTex", mt, "b", 1.0),
        ),
        color_band=color_band,
    )


def _read_color_band(
    P: _Parser, body: bytes,
) -> list[tuple[float, float, float, float, float]]:
    """Decode a ColorBand block into its `(pos, r, g, b, a)` stops.

    Layout (from `DNA_color_types.h`, stable across BI-era files):
    `short flag, tot, cur, ipotype` then `CBData data[16]`, where each
    `CBData` is `float r, g, b, a, pos; int cur` (24 bytes)."""
    tot = struct.unpack(P.endian + "h", body[2:4])[0]
    stops: list[tuple[float, float, float, float, float]] = []
    for i in range(tot):
        off = 8 + i * 24
        r, g, b, a, pos = struct.unpack(P.endian + "fffff", body[off:off + 20])
        stops.append((pos, r, g, b, a))
    return stops


def _main():
    import sys
    path = Path(sys.argv[1])
    for name, ms in extract(path).items():
        print(f"\n{name}  rgb={tuple(round(c, 3) for c in ms.rgb)} alpha={ms.alpha:.3f}")
        for s in ms.slots:
            print(f"  slot[{s.slot_idx}]: {s.tex_type:<7s} img={s.image_name!r:<28s} "
                  f"size={tuple(round(v, 3) for v in s.size)} "
                  f"ofs={tuple(round(v, 3) for v in s.ofs)} "
                  f"texco={s.texco} blend={s.blendtype} fac={s.colfac:.2f} "
                  f"color={tuple(round(v, 3) for v in s.color)}"
                  + (f" band={s.color_band}" if s.color_band else ""))


if __name__ == "__main__":
    _main()
