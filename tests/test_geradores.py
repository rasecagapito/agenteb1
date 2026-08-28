# -*- coding: utf-8 -*-
"""Testes dos geradores TCD. Só stdlib + pandas/yaml (já exigidos pelos scripts).

    python -m unittest discover -s tests -v
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parent.parent
SCRIPTS = RAIZ / "scripts"
NOME = "CARGA_TESTE"


def grade(linhas):
    return pd.DataFrame(linhas)


class Base(unittest.TestCase):
    def montar(self, df: pd.DataFrame, **over) -> Path:
        self.tmp = Path(tempfile.mkdtemp(prefix="tcd_"))
        d = self.tmp / "saida" / NOME / "TCD2"
        d.mkdir(parents=True)
        df.to_excel(d / "TCD2_CARGA.xlsx", index=False)
        cfg = {
            "projeto": {"nome": NOME, "tcd_type": "MI"},
            "otcd": {"abs_id": 7},
            "saida": "saida",
            "skip_prioridades": [],
            "tcd3": {"modo_teste": True, "test_from": "2026-01-01"},
            "hana": {"batch_size": 500},
        }
        cfg.update(over)
        p = self.tmp / "config.yaml"
        p.write_text(yaml.safe_dump(cfg, allow_unicode=True), encoding="utf-8")
        return p

    def rodar(self, script: str, cfg: Path):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / script), "--config", str(cfg)],
            cwd=self.tmp, capture_output=True, text=True,
        )

    def inserts(self, camada: str, stem: str):
        d = self.tmp / "saida" / NOME / camada
        arquivos = sorted(d.glob(f"{stem}_p*.sql")) or [d / f"{stem}.sql"]
        linhas = []
        for f in arquivos:
            linhas += [l for l in f.read_text(encoding="utf-8").splitlines()
                       if l.strip().upper().startswith("INSERT")]
        return linhas


class TestSkipAlinhaCamadas(Base):
    """skip_prioridades tem de valer igual na TCD2 e na TCD3.

    Sem isso a TCD3 aponta Tcd2Id para AbsId que nunca entrou na TCD2 — e o
    erro só aparece no Q27, depois do INSERT no HANA.
    """

    def setUp(self):
        self.cfg = self.montar(
            grade([
                {"Prioridade": p, "AbsId_TCD1": 100 + p, "DispOrder": d,
                 "KeyFld_1_V": f"V{p}{d}", "KeyFld_2_V": None, "KeyFld_3_V": None,
                 "KeyFld_4_V": None, "KeyFld_5_V": None}
                for p in (1, 2, 3) for d in (1, 2)
            ]),
            skip_prioridades=[2],
        )

    def test_contagens_batem(self):
        r2 = self.rodar("gerar_tcd2.py", self.cfg)
        r3 = self.rodar("gerar_tcd3.py", self.cfg)
        self.assertEqual(r2.returncode, 0, r2.stderr)
        self.assertEqual(r3.returncode, 0, r3.stderr)
        tcd2 = self.inserts("TCD2", "TCD2_INSERT")
        tcd3 = self.inserts("TCD3", "TCD3_INSERT")
        self.assertEqual(len(tcd2), 4, "6 linhas menos a prioridade 2")
        self.assertEqual(len(tcd3), len(tcd2), "TCD3 tem de seguir o filtro da TCD2")

    def test_tcd2id_nao_ultrapassa_tcd2(self):
        self.rodar("gerar_tcd2.py", self.cfg)
        self.rodar("gerar_tcd3.py", self.cfg)
        tcd2 = self.inserts("TCD2", "TCD2_INSERT")
        ids = [int(re.search(r"VALUES \((\d+),\d+,(\d+),", l).group(2))
               for l in self.inserts("TCD3", "TCD3_INSERT")]
        self.assertEqual(max(ids), len(tcd2))
        self.assertEqual(sorted(ids), list(range(1, len(tcd2) + 1)))

    def test_prioridade_skipada_nao_gera_linha(self):
        self.rodar("gerar_tcd2.py", self.cfg)
        self.assertFalse([l for l in self.inserts("TCD2", "TCD2_INSERT") if "'V2" in l])

    def test_slot_vazio_vira_null(self):
        self.rodar("gerar_tcd2.py", self.cfg)
        primeira = self.inserts("TCD2", "TCD2_INSERT")[0]
        self.assertIn("NULL,NULL,NULL,NULL);", primeira)
        self.assertNotIn(",'0',", primeira)


class TestTcd3Producao(Base):
    LINHAS = [
        {"Prioridade": 1, "AbsId_TCD1": 101, "DispOrder": 1, "KeyFld_1_V": "A",
         "EfctFrom": "2026-01-01", "EfctTo": "2026-06-30"},
        {"Prioridade": 1, "AbsId_TCD1": 101, "DispOrder": 2, "KeyFld_1_V": "B",
         "EfctFrom": "2026-07-01", "EfctTo": None},
        {"Prioridade": 2, "AbsId_TCD1": 102, "DispOrder": 1, "KeyFld_1_V": "C",
         "EfctFrom": "2026-02-01", "EfctTo": "2099-12-31"},
    ]

    def test_usa_datas_da_grade(self):
        cfg = self.montar(grade(self.LINHAS), tcd3={"modo_teste": False})
        r = self.rodar("gerar_tcd3.py", cfg)
        self.assertEqual(r.returncode, 0, r.stderr)
        linhas = self.inserts("TCD3", "TCD3_INSERT")
        self.assertEqual(len(linhas), 3)
        self.assertIn("'2026-01-01','2026-06-30',NULL", linhas[0])

    def test_efctto_aberto_e_2099_viram_null(self):
        cfg = self.montar(grade(self.LINHAS), tcd3={"modo_teste": False})
        self.rodar("gerar_tcd3.py", cfg)
        linhas = self.inserts("TCD3", "TCD3_INSERT")
        self.assertTrue(linhas[1].endswith("'2026-07-01',NULL,NULL);"), linhas[1])
        self.assertTrue(linhas[2].endswith("'2026-02-01',NULL,NULL);"), linhas[2])

    def test_taxcode_sempre_null_no_mi(self):
        cfg = self.montar(grade(self.LINHAS), tcd3={"modo_teste": False})
        self.rodar("gerar_tcd3.py", cfg)
        for l in self.inserts("TCD3", "TCD3_INSERT"):
            self.assertTrue(l.rstrip().endswith(",NULL);"))

    def test_sem_coluna_efctfrom_para_com_mensagem(self):
        cfg = self.montar(
            grade([{"Prioridade": 1, "AbsId_TCD1": 101, "DispOrder": 1, "KeyFld_1_V": "A"}]),
            tcd3={"modo_teste": False},
        )
        r = self.rodar("gerar_tcd3.py", cfg)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("EfctFrom", r.stderr)

    def test_data_vazia_nao_gera_parcial(self):
        linhas = [dict(self.LINHAS[0]), dict(self.LINHAS[1])]
        linhas[1]["EfctFrom"] = None
        cfg = self.montar(grade(linhas), tcd3={"modo_teste": False})
        r = self.rodar("gerar_tcd3.py", cfg)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("EfctFrom vazio", r.stderr)


class TestLotes(Base):
    def test_fatia_no_batch_size(self):
        cfg = self.montar(
            grade([{"Prioridade": 1, "AbsId_TCD1": 101, "DispOrder": i, "KeyFld_1_V": f"V{i}"}
                   for i in range(1, 6)]),
            hana={"batch_size": 2},
        )
        self.rodar("gerar_tcd2.py", cfg)
        d = self.tmp / "saida" / NOME / "TCD2"
        self.assertEqual(len(list(d.glob("TCD2_INSERT_p*.sql"))), 3)
        self.assertEqual(len(self.inserts("TCD2", "TCD2_INSERT")), 5)


class TestTcd3MultiPeriodo(Base):
    """N vigências por TCD2, via TCD3_CARGA.xlsx."""

    GRADE2 = [
        {"Prioridade": 1, "AbsId_TCD1": 101, "DispOrder": 1, "KeyFld_1_V": "A"},
        {"Prioridade": 1, "AbsId_TCD1": 101, "DispOrder": 2, "KeyFld_1_V": "B"},
    ]

    def com_periodos(self, periodos, **over):
        cfg = self.montar(grade(self.GRADE2), **over)
        d = self.tmp / "saida" / NOME / "TCD3"
        d.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(periodos).to_excel(d / "TCD3_CARGA.xlsx", index=False)
        return cfg

    def test_varias_vigencias_por_tcd2(self):
        cfg = self.com_periodos([
            {"AbsId_TCD2": 1, "EfctFrom": "2026-01-01", "EfctTo": "2026-06-30"},
            {"AbsId_TCD2": 1, "EfctFrom": "2026-07-01", "EfctTo": "2026-12-31"},
            {"AbsId_TCD2": 1, "EfctFrom": "2027-01-01", "EfctTo": None},
            {"AbsId_TCD2": 2, "EfctFrom": "2026-01-01", "EfctTo": None},
        ])
        r = self.rodar("gerar_tcd3.py", cfg)
        self.assertEqual(r.returncode, 0, r.stderr)
        linhas = self.inserts("TCD3", "TCD3_INSERT")
        self.assertEqual(len(linhas), 4)
        absid = [int(re.search(r"VALUES \((\d+),", l).group(1)) for l in linhas]
        tcd2 = [int(re.search(r"VALUES \(\d+,\d+,(\d+),", l).group(1)) for l in linhas]
        self.assertEqual(absid, [1, 2, 3, 4], "AbsId da TCD3 é sequencial próprio")
        self.assertEqual(tcd2, [1, 1, 1, 2], "Tcd2Id repete na mesma combinação")

    def test_grade_tcd3_exportada_para_a_tcd5(self):
        cfg = self.com_periodos([
            {"AbsId_TCD2": 1, "EfctFrom": "2026-01-01", "EfctTo": None},
            {"AbsId_TCD2": 2, "EfctFrom": "2026-01-01", "EfctTo": None},
        ])
        self.rodar("gerar_tcd3.py", cfg)
        g = pd.read_excel(self.tmp / "saida" / NOME / "TCD3" / "TCD3_GRADE.xlsx")
        self.assertEqual(list(g["AbsId"]), [1, 2])
        self.assertEqual(list(g["AbsId_TCD2"]), [1, 2])

    def test_periodos_sobrepostos_param(self):
        cfg = self.com_periodos([
            {"AbsId_TCD2": 1, "EfctFrom": "2026-01-01", "EfctTo": "2026-08-31"},
            {"AbsId_TCD2": 1, "EfctFrom": "2026-06-01", "EfctTo": None},
            {"AbsId_TCD2": 2, "EfctFrom": "2026-01-01", "EfctTo": None},
        ])
        r = self.rodar("gerar_tcd3.py", cfg)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("sobrepostos", r.stderr)

    def test_dois_periodos_abertos_na_mesma_tcd2(self):
        cfg = self.com_periodos([
            {"AbsId_TCD2": 1, "EfctFrom": "2026-01-01", "EfctTo": None},
            {"AbsId_TCD2": 1, "EfctFrom": "2026-07-01", "EfctTo": None},
            {"AbsId_TCD2": 2, "EfctFrom": "2026-01-01", "EfctTo": None},
        ])
        r = self.rodar("gerar_tcd3.py", cfg)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("período aberto", r.stderr)

    def test_absid_tcd2_de_prioridade_skipada(self):
        cfg = self.com_periodos(
            [{"AbsId_TCD2": 1, "EfctFrom": "2026-01-01", "EfctTo": None},
             {"AbsId_TCD2": 2, "EfctFrom": "2026-01-01", "EfctTo": None},
             {"AbsId_TCD2": 9, "EfctFrom": "2026-01-01", "EfctTo": None}],
        )
        r = self.rodar("gerar_tcd3.py", cfg)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("AbsId_TCD2 inexistente", r.stderr)

    def test_tcd2_sem_vigencia_para(self):
        cfg = self.com_periodos([{"AbsId_TCD2": 1, "EfctFrom": "2026-01-01", "EfctTo": None}])
        r = self.rodar("gerar_tcd3.py", cfg)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("sem nenhuma vigência", r.stderr)


class TestGradeExportada(Base):
    def test_tcd2_grade_numerada_pos_skip(self):
        cfg = self.montar(
            grade([{"Prioridade": p, "AbsId_TCD1": 100 + p, "DispOrder": 1, "KeyFld_1_V": f"V{p}"}
                   for p in (1, 2, 3)]),
            skip_prioridades=[2],
        )
        self.rodar("gerar_tcd2.py", cfg)
        g = pd.read_excel(self.tmp / "saida" / NOME / "TCD2" / "TCD2_GRADE.xlsx")
        self.assertEqual(list(g["AbsId"]), [1, 2])
        self.assertEqual(list(g["Prioridade"]), [1, 3])


if __name__ == "__main__":
    unittest.main()
