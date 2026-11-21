"""fnv_where.py - what is at this address in FalloutNV.exe? Answered from momusdigital's fnv_decomp.

Made 2026-11-21 (Tefa: "please look at this pile of gold and use it when we mod our version of tales of two
wastelands modlist"). fnv_decomp is a matching decompilation of FalloutNV.exe 1.4.0.525 (CC0): every function at its
original address, with a name and its rebuilt C++ source. It matches the list's game program byte for byte in code
(the FNV4GB patch only touches 188 bytes outside the code, checked 2026-11-21), so an address from a crash, from
x64dbg or from TTWVR's hooks can be turned into a function name and the source that explains it.

    python tools/fnv_where.py addr 0x00A24660 0x0070F6E0 ...   the function each address falls in, its source file
                                                              and line
    python tools/fnv_where.py find Water [--limit 40]          functions whose name contains the text
    python tools/fnv_where.py src 0x00A24660                   print that function's rebuilt source
    --game f3                                                  use f3_decomp (Fallout3.exe 1.7.0.3) instead; NOT
                                                              the program TTW runs, only for comparing with FO3

Where the decompilations are: FNV_DECOMP / F3_DECOMP, else D:\\claude video game stuff\\decomps\\<name>. Read-only.
Data addresses (globals) are only found when a unit names them; a miss says so.
"""
import argparse
import bisect
import json
import os
import re
import sys

DEFAULT_ROOT = r"D:\claude video game stuff\decomps"
GAMES = {"fnv": ("FNV_DECOMP", "fnv_decomp"), "f3": ("F3_DECOMP", "f3_decomp")}


def root_for(game):
    env, name = GAMES[game]
    return os.environ.get(env) or os.path.join(DEFAULT_ROOT, name)


def demangle(sym):
    """Readable name from an MSVC symbol, good enough to read (not a full undname)."""
    if not sym.startswith("?"):
        return sym.lstrip("_")
    special = {"??0": "{cls}::{cls}", "??1": "{cls}::~{cls}", "??_G": "{cls}::`scalar deleting destructor'",
               "??_E": "{cls}::`vector deleting destructor'"}
    for pre, fmt in special.items():
        if sym.startswith(pre):
            parts = sym[len(pre):].split("@@")[0].split("@")
            cls = "::".join(reversed([p for p in parts if p]))
            return fmt.format(cls=cls.split("::")[-1]) if "::" not in cls else \
                cls + "::" + fmt.format(cls=cls.split("::")[-1]).split("::", 1)[1]
    body = sym[1:].split("@@")[0]
    parts = [p for p in body.split("@") if p]
    return "::".join(reversed(parts)) if parts else sym


def load(game):
    root = root_for(game)
    path = os.path.join(root, "build", "units.json")
    if not os.path.exists(path):
        sys.exit(f"fnv_where: no decompilation at {root} (clone https://github.com/momusdigital/{GAMES[game][1]})")
    units = json.load(open(path, encoding="utf-8"))["units"]
    funcs = []
    data = {}
    for u in units:
        for f in u.get("functions", []):
            funcs.append((int(f["address"], 16), int(f.get("size", 0)), f["symbol"], u["source"]))
        for sym, addr in (u.get("symbols") or {}).items():
            try:
                data.setdefault(int(addr, 16), sym)
            except (TypeError, ValueError):
                pass
    funcs.sort()
    return root, funcs, data


def source_line(root, src, addr, sym):
    """Line of the function in its source: the 'src:' address marker first, then the plain name."""
    path = os.path.join(root, src)
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
    except OSError:
        return None
    hexa = f"{addr:08x}"
    name = demangle(sym).split("::")[-1]
    pat = re.compile(r"\b" + re.escape(name) + r"\s*\(")
    marker = next((i for i, l in enumerate(lines) if hexa in l.lower()), None)
    # The definition itself: the first non-declaration line naming the function, after the address marker if any
    # (a marker can sit on a namespace wrapper that declares helper structs first).
    for i in range(marker or 0, len(lines)):
        if pat.search(lines[i]) and not lines[i].rstrip().endswith(";"):
            return i + 1
    return marker + 1 if marker is not None else None


def find_func(funcs, addr):
    i = bisect.bisect_right([f[0] for f in funcs], addr) - 1
    if i >= 0:
        start, size, sym, src = funcs[i]
        if start <= addr < start + max(size, 1):
            return funcs[i]
    return None


def cmd_addr(game, addrs):
    root, funcs, data = load(game)
    for a in addrs:
        addr = int(a, 16)
        f = find_func(funcs, addr)
        if f:
            start, size, sym, src = f
            line = source_line(root, src, start, sym)
            off = f"+0x{addr - start:x}" if addr != start else ""
            print(f"0x{addr:08X}  {demangle(sym)}{off}  ({size} bytes)  {src}{':' + str(line) if line else ''}")
        elif addr in data:
            print(f"0x{addr:08X}  data: {demangle(data[addr])}")
        else:
            print(f"0x{addr:08X}  not in a listed function (data, a thunk, or outside the decompiled code)")


def cmd_find(game, text, limit):
    root, funcs, _ = load(game)
    t = text.lower()
    hits = [f for f in funcs if t in demangle(f[2]).lower()]
    for start, size, sym, src in hits[:limit]:
        print(f"0x{start:08X}  {demangle(sym)}  ({size} bytes)  {src}")
    if len(hits) > limit:
        print(f"... {len(hits) - limit} more (raise --limit)")
    if not hits:
        print("no function name contains that")


def cmd_src(game, a):
    root, funcs, _ = load(game)
    f = find_func(funcs, int(a, 16))
    if not f:
        sys.exit("not in a listed function")
    start, size, sym, src = f
    line = source_line(root, src, start, sym)
    lines = open(os.path.join(root, src), encoding="utf-8", errors="replace").read().split("\n")
    if not line:
        sys.exit(f"{demangle(sym)} is in {src}, but its line was not found")
    i = line - 1
    while i > 0 and lines[i - 1].lstrip().startswith("//"):
        i -= 1
    depth, seen, out = 0, False, []
    for l in lines[i:]:
        out.append(l)
        depth += l.count("{") - l.count("}")
        seen = seen or "{" in l
        if seen and depth <= 0:
            break
        if len(out) > 400:
            out.append("... (cut at 400 lines)")
            break
    print(f"// {src}:{line}\n" + "\n".join(out))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", choices=GAMES, default="fnv")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("addr"); p.add_argument("addresses", nargs="+")
    p = sub.add_parser("find"); p.add_argument("text"); p.add_argument("--limit", type=int, default=40)
    p = sub.add_parser("src"); p.add_argument("address")
    a = ap.parse_args()
    if a.cmd == "addr":
        cmd_addr(a.game, a.addresses)
    elif a.cmd == "find":
        cmd_find(a.game, a.text, a.limit)
    else:
        cmd_src(a.game, a.address)


if __name__ == "__main__":
    main()
