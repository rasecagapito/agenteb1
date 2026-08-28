# -*- coding: utf-8 -*-
"""Funções compartilhadas da carga TCD. Sem CompanyDB, sem cliente fixo."""
from __future__ import annotations

import argparse
import re
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import yaml

PLACEHOLDERS_NOME = frozenset(
    {"", "NOME_DESTE_CLIENTE", "NOME_DO_PROJETO", "TODO", "xxx", "CHANGEME"}
)


def load_config(path: Path) -> dict:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("config.yaml inválido")
    return data


def require_projeto(cfg: dict) -> str:
    nome = str((cfg.get("projeto") or {}).get("nome") or "").strip()
    if nome in PLACEHOLDERS_NOME:
        raise SystemExit(
            "projeto.nome obrigatório. Copie config.example.yaml e dê o nome DESTE cliente/carga."
        )
    return nome


def saida_camada(cfg: dict, camada: str) -> Path:
    nome = require_projeto(cfg)
    root = Path(cfg.get("saida") or "saida")
    d = root / nome / camada
    d.mkdir(parents=True, exist_ok=True)
    return d


def nval(v):
    if v is None or pd.isna(v):
        return None
    if isinstance(v, pd.Timestamp):
        return v.strftime("%Y-%m-%d")
    if isinstance(v, datetime):
        return v.strftime("%Y-%m-%d")
    if isinstance(v, date):
        return v.isoformat()
    s = str(v).strip()
    if s.endswith(" 00:00:00"):
        s = s[:10]
    if s in ("nan", "NaT", "None", "#N/A", "#N/D", ""):
        return None
    return s


def sap_val(chave, val, grupo_item_map: dict | None = None):
    v = nval(val)
    if v is None:
        return None
    chave_u = (nval(chave) or "").strip()
    mp = grupo_item_map or {}
    if chave_u == "Grupo de Itens":
        return str(mp.get(v, v))
    if chave_u == "Filial":
        try:
            return str(int(float(v)))
        except Exception:
            return v
    if re.fullmatch(r"-?\d+\.0", v):
        return v[:-2]
    return v


def sql_str(v) -> str:
    if v is None:
        return "NULL"
    return "'" + str(v).replace("'", "''") + "'"


def sql_num(v) -> str:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "NULL"
    return str(int(v))


def ktuple(vals) -> tuple:
    return tuple("" if x is None else str(x) for x in vals)


def to_date(v):
    s = nval(v)
    if not s:
        return None
    if s in ("2099-12-31", "9999-12-31"):
        return None
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d").date()
    except Exception:
        return None


def covers(dfrom, dto, d) -> bool:
    if dfrom is None or dfrom > d:
        return False
    if dto is None:
        return True
    return dto >= d


def norm_uso(s: str) -> str:
    s = str(s).upper()
    s = s.translate(str.maketrans("ÁÀÃÂÉÊÍÓÔÕÚÜÇ", "AAAAEEIOOOUUC"))
    return re.sub(r"[^A-Z0-9]", "", s)


def map_uso(txt, by_exact: dict, by_norm: dict):
    if not txt:
        return None, None, "SEM_USO"
    if txt in by_exact:
        return by_exact[txt], txt, "EXATO"
    n = norm_uso(txt)
    if n in by_norm:
        sap, oid = by_norm[n]
        return oid, sap, "SINONIMO"
    return None, None, "AUSENTE"


def write_batches(inserts: list[str], out_dir: Path, stem: str, batch_size: int, header: list[str]):
    total = len(inserts)
    nlot = max(1, (total + batch_size - 1) // batch_size) if total else 0
    for old in out_dir.glob(f"{stem}_p*.sql"):
        old.unlink()
    if total == 0:
        (out_dir / f"{stem}.sql").write_text("-- nenhum INSERT\n", encoding="utf-8")
        return
    if total <= batch_size:
        lines = header + inserts + ["", "COMMIT;", ""]
        (out_dir / f"{stem}.sql").write_text("\n".join(lines), encoding="utf-8")
        return
    for i in range(nlot):
        chunk = inserts[i * batch_size : (i + 1) * batch_size]
        a1 = i * batch_size + 1
        a2 = i * batch_size + len(chunk)
        lines = [
            f"-- {stem} lote {i + 1:02d}/{nlot:02d}. linhas {a1}-{a2} de {total}.",
            "-- HANA Studio: um arquivo por vez.",
            "",
            *chunk,
            "",
            "COMMIT;",
            "",
        ]
        (out_dir / f"{stem}_p{i + 1:02d}.sql").write_text("\n".join(lines), encoding="utf-8")
    idx = header + [
        f"-- NAO executar este indice. Use {stem}_p01.sql ... p{nlot:02d}.sql",
        f"-- Total esperado = {total}",
        "",
    ]
    (out_dir / f"{stem}.sql").write_text("\n".join(idx), encoding="utf-8")


def arg_config() -> Path:
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True, help="caminho do config.yaml DESTE projeto")
    return Path(p.parse_args().config)
