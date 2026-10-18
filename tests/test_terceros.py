from __future__ import annotations

from pathlib import Path

import pytest

from argfx.informe.terceros import read_structure, third_party_debt


def _files(tmp_path: Path, private: str = "110") -> tuple[Path, Path, Path]:
    s = tmp_path / "s.csv"
    s.write_text(
        "corte,concepto,valor,unidad,source_id,nota\n"
        "2023-12-31,base_privados_sin_holdouts,100,,,\n"
        "2023-12-31,holdouts,10,,,\n"
        "2023-12-31,pct_dolares,50,,,\n"
        "2023-12-31,pct_euros_y_otros,10,,,\n"
        "2023-12-31,pct_dolar_linked,10,,,\n"
        "2023-12-31,pct_cer,20,,,\n"
        "2023-12-31,pct_pesos,10,,,\n"
        "2023-12-31,divisas_pago_normal_total,300,,,\n"
    )
    h = tmp_path / "h.csv"
    h.write_text(
        "corte,deuda_en_poder_del_sector_privado_usd_millones,multilaterales_y_bilaterales_usd_millones\n"
        f"2023-12-31,{private},80\n"
    )
    r = tmp_path / "r.csv"
    r.write_text("mes,total_pasivos_remunerados_pases_leliq_lefi_otros_mm_ars\n2023-12,2000000\n")
    return s, h, r


def test_private_debt_splits_by_currency_and_pesos_add_the_bcra(tmp_path: Path) -> None:
    s, h, r = _files(tmp_path)
    [row] = third_party_debt(
        read_structure(s), h, r, {"2023-12": 1e4}, {"2023-12": 1.0, "2026-08": 2.0}, "2026-08"
    )
    assert row["divisas_privados_usd"] == 60 and row["divisas_terceros_usd"] == 140
    # Foreign currency of the public sector is what is left of the total.
    assert row["divisas_sector_publico_usd"] == 300 - 60 - 80
    # 40 million USD in pesos at 10.000 per dollar: 0,4 trillion; plus 2 of the BCRA.
    assert row["pesos_terceros_consolidado_corrientes"] == 2.4
    assert row["pesos_terceros_consolidado_constantes"] == 4.8


def test_the_pie_must_add_up_to_the_published_holding(tmp_path: Path) -> None:
    s, h, r = _files(tmp_path, private="200")
    with pytest.raises(ValueError):
        third_party_debt(read_structure(s), h, r, {"2023-12": 1.0}, {"2023-12": 1.0}, "2023-12")
