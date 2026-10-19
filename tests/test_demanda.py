from __future__ import annotations

from argfx.informe.demanda import concepts, dollar_account, yearly_pace


def test_persons_and_firms_are_kept_apart() -> None:
    group = "03- Compra-venta de billetes y divisas sin fines específicos"
    assert concepts("Personas Humanas", group, "Billetes - Egresos") == ["atesoramiento_personas"]
    assert concepts("Comercio", group, "Divisas - Egresos") == ["atesoramiento_empresas"]
    assert concepts("Entidades financieras y cambiarias", group, "Divisas - Egresos") == []
    travel = "Consumos de bienes y servicios pagados con tarjetas y viajes - Egresos"
    assert concepts("Personas Humanas", "02- Servicios", travel) == ["viajes"]
    assert concepts("Sector Público", "03- Ingreso primario", "Intereses - Egresos") == []


def test_pace_is_the_monthly_average_times_twelve() -> None:
    monthly = {"2026-01": {"viajes": -6.0}, "2026-02": {"viajes": -12.0}, "2025-12": {"viajes": 1}}
    assert yearly_pace(monthly, "2026-01", "2026-02") == {"viajes": -108.0}


def test_the_account_subtracts_each_use_once() -> None:
    imf = [{"anio": "2027", "balanza_bienes_musd": "20", "servicios_musd": "-10",
            "ingreso_primario_musd": "-15", "interes_publico_musd": "-9",
            "ingreso_secundario_musd": "2"}]  # fmt: skip
    (row,) = dollar_account(imf, {2027: 12.0, 2028: 5.0}, {"a": 8.0}, 3.0)
    # 20 + 2 - 10 - (15 - 9): public interest is already in the maturities
    assert row["disponible_para_deuda"] == 6
    assert row["resultado_antes_de_atesoramiento"] == -6
    assert row["brecha_a"] == -14 and row["brecha_a_y_empresas"] == -17
