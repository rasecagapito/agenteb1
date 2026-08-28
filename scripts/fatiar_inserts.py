# -*- coding: utf-8 -*-
"""Fatiar arquivo de INSERTs para o HANA Studio (console too large)."""
from __future__ import annotations

import argparse
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--arquivo", required=True)
    p.add_argument("--lote", type=int, default=500)
    args = p.parse_args()
    path = Path(args.arquivo)
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip().upper().startswith("INSERT")]
    if not lines:
        raise SystemExit("nenhum INSERT")
    stem = path.stem
    out = path.parent
    nlot = (len(lines) + args.lote - 1) // args.lote
    for i in range(nlot):
        chunk = lines[i * args.lote : (i + 1) * args.lote]
        dest = out / f"{stem}_p{i + 1:02d}.sql"
        dest.write_text(
            f"-- lote {i + 1:02d}/{nlot:02d} ({len(chunk)} INSERT)\n\n"
            + "\n".join(chunk)
            + "\n\nCOMMIT;\n",
            encoding="utf-8",
        )
    print(len(lines), "INSERT ->", nlot, "lotes em", out)


if __name__ == "__main__":
    main()
