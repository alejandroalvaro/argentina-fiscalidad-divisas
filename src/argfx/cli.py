"""Command line entry point: `argfx <command>`."""

from __future__ import annotations

import argparse
import sys
import tempfile
import uuid
from pathlib import Path

from argfx.config import get_settings
from argfx.fetch import fetch_sources
from argfx.manifest import ingest_file
from argfx.storage import fetch_verified, get_store


def cmd_config(_: argparse.Namespace) -> int:
    for key, value in get_settings().public_summary().items():
        print(f"{key:22} {value}")
    return 0


def cmd_storage_check(_: argparse.Namespace) -> int:
    """Round-trip a throwaway object (write, list, read, delete) against the active store."""
    settings = get_settings()
    store = get_store(settings)
    key = f"_healthcheck/{uuid.uuid4()}.txt"
    payload = b"argfx storage check"
    backend = settings.resolved_storage
    target = settings.r2_bucket if backend == "r2" else settings.local_objects_dir
    print(f"backend: {backend} ({target})")
    with tempfile.TemporaryDirectory() as tmp:
        src, back = Path(tmp) / "src.txt", Path(tmp) / "back.txt"
        src.write_bytes(payload)
        store.upload(src, key, "text/plain")
        listed = key in store.list_keys("_healthcheck/")
        store.download(key, back)
        store.delete(key)
        ok = listed and back.read_bytes() == payload and not store.exists(key)
    print("write/list/read/delete:", "OK" if ok else "FAILED")
    return 0 if ok else 1


def cmd_ingest(args: argparse.Namespace) -> int:
    settings = get_settings()
    store = get_store(settings)
    status = 0
    for path in args.files:
        if not path.is_file():
            print(f"skip (not a file): {path}", file=sys.stderr)
            status = 1
            continue
        record, created = ingest_file(path, store, settings.manifests_dir, args.source_id)
        print(f"{'stored ' if created else 'present'} {record.sha256}  {path.name}")
    return status


def cmd_fetch(args: argparse.Namespace) -> int:
    settings = get_settings()
    dest = fetch_verified(get_store(settings), args.sha256, args.dest, settings.cache_dir)
    print(f"verified {args.sha256} -> {dest}")
    return 0


def cmd_fetch_sources(args: argparse.Namespace) -> int:
    from functools import partial

    from argfx.fetch import http_fetch

    settings = get_settings()
    store = get_store(settings)
    fetcher = partial(http_fetch, user_agent=settings.user_agent)
    failed = 0
    for csv_path in args.sources:
        for r in fetch_sources(csv_path, store, settings.manifests_dir, fetcher, args.delay):
            if r.error:
                failed += 1
                print(f"FAIL    {r.source_id}  {r.error}")
                continue
            match = {True: "hash=grok", False: "hash≠grok", None: "no grok hash"}[r.hash_match]
            state = "stored " if r.created else "present"
            print(f"{state} {r.source_id}  {r.size_bytes:>10,} B  {match}  {r.sha256[:12]}")
    return 1 if failed else 0


def cmd_validate(args: argparse.Namespace) -> int:
    from argfx.validate import validate_inbox, write_report

    report = validate_inbox(args.inbox)
    print(
        f"{len(report.files)} files, {report.rows_read:,} rows: "
        f"{report.errors:,} errors, {report.warnings:,} warnings"
    )
    for i in report.issues:
        where = f"{i.lote}/{i.file}" + (f":{i.line}" if i.line else "")
        print(f"  {i.severity:7} {i.code:24} x{i.count:<5} {where}  [{i.column}] {i.message}")
    if args.out:
        csv_path, md_path = write_report(report, args.out)
        print(f"report: {md_path} and {csv_path}")
    return 1 if report.errors else 0


def cmd_calendario(args: argparse.Namespace) -> int:
    from datetime import date

    from argfx.contracts.calendar import build_calendar

    counts = build_calendar(
        args.terminos,
        args.sigade,
        args.instrumentos,
        date.fromisoformat(args.corte),
        args.out,
        args.series,
    )
    for k, v in counts.items():
        print(f"{k}: {v:,}")
    print(f"tablas en {args.out}/")
    return 0


# Finanzas quarterly debt workbook at 2026-06-30 (SRC-0103, also SRC-1005).
FINANZAS_2026_06_30 = "e481f24585ef40b8ce7c2b515e66235c8b8ebcb4001a769091cb531a6373922e"


def cmd_conciliacion(args: argparse.Namespace) -> int:
    from datetime import date

    from argfx.reconcile.conciliacion import Materiality, build_reconciliation
    from argfx.reconcile.consolidacion import build_consolidation

    xlsx = args.finanzas
    if xlsx is None:
        settings = get_settings()
        xlsx = settings.cache_dir / "finanzas" / f"{args.finanzas_sha}.xlsx"
        if not xlsx.is_file():
            fetch_verified(get_store(settings), args.finanzas_sha, xlsx, settings.cache_dir)
    counts = build_reconciliation(
        xlsx,
        args.instrumentos,
        args.calendario,
        args.terminos,
        date.fromisoformat(args.corte),
        args.out,
        Materiality(args.umbral_abs, args.umbral_rel),
    )
    for k, v in counts.items():
        print(f"{k}: {v:,}")
    consolidated = build_consolidation(
        args.tenencias / f"composicion_acreedor_{args.corte}.csv",
        args.tenencias / f"tenencias_identificadas_{args.corte}.csv",
        args.instrumentos,
        args.calendario / "flujos.csv",
        args.terminos,
        date.fromisoformat(args.corte),
        args.out,
    )
    for k, v in consolidated.items():
        print(f"{k}: {v:,}")
    pesos_csv = args.tenencias / f"tenencias_pesos_{args.corte}.csv"
    if pesos_csv.exists():
        from argfx.reconcile.finanzas import find, lines
        from argfx.reconcile.pesos import build_peso_consolidation

        iii = find(lines(xlsx, "A.1.1"), "III-").values
        pesos = build_peso_consolidation(
            args.tenencias / f"composicion_acreedor_{args.corte}.csv",
            pesos_csv,
            args.instrumentos,
            iii[1] / iii[0],
            args.out,
        )
        for k, v in pesos.items():
            print(f"{k}: {v:,}")
    print(f"tablas en {args.out}/")
    return 0


def _cached_object(sha256: str, folder: str) -> Path:
    settings = get_settings()
    dest = settings.cache_dir / folder / f"{sha256}.xlsx"
    if not dest.is_file():
        fetch_verified(get_store(settings), sha256, dest, settings.cache_dir)
    return dest


def cmd_devengados(args: argparse.Namespace) -> int:
    import csv
    from datetime import date

    from argfx.reconcile.devengados import build_accrual_table

    with args.planillas.open(newline="", encoding="utf-8") as fh:
        quarterly = [
            (date.fromisoformat(r["corte"]), _cached_object(r["sha256"], "finanzas"))
            for r in csv.DictReader(fh)
        ]
    with args.colocaciones.open(newline="", encoding="utf-8") as fh:
        placements = [_cached_object(r["sha256"], "oncp") for r in csv.DictReader(fh)]
    rows = build_accrual_table(quarterly, placements, args.spn, args.out, args.fgs)
    for r in rows:
        print(
            f"{r['trimestre']}: capitalizado devengado {r['interes_capitalizado_devengado']:>9,.1f}"
            f"  (línea A.2.2 {r['capitalizacion_a22']:>9,.1f})"
            f"  descuentos {r['descuento_colocacion_devengado']:>7,.1f}"
            + (
                f"  FGS {r['fgs_participacion_min_pct']}-{r['fgs_participacion_max_pct']}%"
                if r["fgs_participacion_min_pct"] is not None
                else ""
            )
        )
    print(f"tabla en {args.out}/devengados_trimestral.csv (miles de millones de pesos)")
    return 0


def cmd_derechos(args: argparse.Namespace) -> int:
    import csv

    from argfx.simulation.alicuotas import load_book
    from argfx.simulation.exportaciones import (
        build_duty_table,
        crude_prices,
        monthly_average,
        observed_duties_usd,
        read_month_detail,
        screen_unit_values,
    )

    settings = get_settings()
    store = get_store(settings)

    def cached(sha256: str, suffix: str) -> Path:
        dest = settings.cache_dir / "arca" / f"{sha256}{suffix}"
        if not dest.is_file():
            fetch_verified(store, sha256, dest, settings.cache_dir)
        return dest

    with args.descargas.open(newline="", encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if r["sha256"]]
    latest = {r["source_id"]: r["sha256"] for r in rows}
    zips = [latest[s] for s in sorted(latest) if args.desde <= s <= args.hasta]
    detail = [read_month_detail(cached(h, ".zip")) for h in zips]
    # Unit values are screened over every month read, so the medians use the whole series.
    months, removed = screen_unit_values(detail)
    months = [(m, f) for m, f in months if m >= args.mes_desde]
    removed = [r for r in removed if str(r["mes"]) >= args.mes_desde]
    rows_out = build_duty_table(
        months,
        load_book(args.alicuotas),
        crude_prices(cached(latest[args.pi], ".xlsx")),
        observed_duties_usd(args.recaudacion, monthly_average(args.a3500)),
        args.out,
    )
    for r in rows_out:
        cobrado = r["derecho_cobrado_musd"] or 0
        print(
            f"{r['mes']}: FOB {r['fob_musd']:>8,.0f}"
            f"  con alícuota {r['fob_con_alicuota_musd']:>8,.0f}"
            f"  estimado {r['derecho_estimado_musd']:>6,.0f}  cobrado {cobrado:>6,.0f}"
        )
    from argfx.contracts.calendar import _write

    _write(args.out / "exportaciones_valores_anomalos.csv", removed)
    lost = sum(float(r["fob_musd"]) for r in removed)  # type: ignore[arg-type]
    print(
        f"{len(removed)} posiciones-mes apartadas por valor unitario: {lost:,.0f} millones de FOB"
    )
    print(f"tablas en {args.out}/ (millones de USD)")
    return 0


# Secretaría de Finanzas monthly boletín through 2026-09 (SRC-9002): debt payments by currency.
BOLETIN_FINANZAS_SHA = "4f172f544df60ee73c325e2e3186f3091db87cd65e48132647fb25fd053cc7fd"
# BCRA Series.xlsm through 2026-10-13 (SRC-1625): factors of the monetary base.
BCRA_SERIES_SHA = "c9152a99361349604b9377d5db96466cd123e572280673f0e7356dc7bfa03c9b"
# BCRA balance cambiario workbook through 2026-08 (lote AH, SRC-1604).
BALANCE_CAMBIARIO_SHA = "fda73048a4e09a8ef4a1cd7998920e0a4862e41c137e8a158ebf66b19c0ef5b2"


def cmd_flujos(args: argparse.Namespace) -> int:
    from argfx.informe.flujos import (
        ars_flows,
        bcra_flows,
        fx_months,
        read_a3500,
        read_balance_cambiario,
        read_base_factors,
        read_cpi,
        read_csv,
        read_fx_interest,
        read_paid_in_pesos,
        read_purchases,
        sankey_html,
        treasury_usd_flows,
        usd_flows,
        write_flows,
    )

    t = args.aif
    financing = read_csv(args.financiamiento)
    fx = fx_months(
        read_a3500(args.a3500),
        read_fx_interest(_cached_object(args.boletin_sha, "finanzas")),
        read_csv(args.depositos),
        read_purchases(args.compras),
        read_paid_in_pesos(args.pagados_en_pesos, args.colocados_por_pesos),
    )
    ars = ars_flows(
        read_csv(t / "aif_base_caja_mensual_resultados.csv"),
        financing,
        read_cpi(t / "indec_ipc_nacional_nivel_general_mensual.csv"),
        fx,
        args.desde,
        args.hasta,
    )
    flows = [
        usd_flows(
            read_balance_cambiario(_cached_object(args.balance_sha, "bcra")), args.desde, args.hasta
        ),
        # Same months as the peso table: a month without the fiscal result has no financing yet.
        treasury_usd_flows(financing, fx, ars.desde, ars.hasta),
        ars,
        bcra_flows(
            read_base_factors(_cached_object(args.series_sha, "bcra")),
            read_cpi(t / "indec_ipc_nacional_nivel_general_mensual.csv"),
            ars.desde,
            ars.hasta,
        ),
    ]
    for f in flows:
        path = write_flows(f, args.out)
        title = f"{f.hub}: por dónde entraron y salieron, {f.desde} a {f.hasta} ({f.unidad})"
        path.with_suffix(".html").write_text(sankey_html(f, title), encoding="utf-8")
        total = sum(f.entradas.values())
        print(
            f"{f.clave or f.moneda} {f.desde} a {f.hasta}: entradas {total:,.0f} {f.unidad},"
            f" sin identificar {-f.descuadre:,.0f} -> {path}"
        )
    return 0


def cmd_simular(args: argparse.Namespace) -> int:
    import csv
    import json

    from argfx.contracts.calendar import _write
    from argfx.informe.flujos import (
        fx_months,
        read_a3500,
        read_balance_cambiario,
        read_base_factors,
        read_csv,
        read_fx_interest,
        read_paid_in_pesos,
        read_purchases,
        treasury_usd_months,
    )
    from argfx.simulation import corrida as cr
    from argfx.simulation.alicuotas import load_book
    from argfx.simulation.exportaciones import (
        crude_prices,
        read_month_detail,
        screen_unit_values,
    )
    from argfx.simulation.regimes import Opening

    out: Path = args.out
    out.mkdir(parents=True, exist_ok=True)

    # 1. The mandate.
    a3500 = read_a3500(args.a3500)
    fx = fx_months(
        a3500,
        read_fx_interest(_cached_object(BOLETIN_FINANZAS_SHA, "finanzas")),
        read_csv(args.depositos),
        read_purchases(args.compras),
        read_paid_in_pesos(args.pagados_en_pesos, args.colocados_por_pesos),
    )
    treasury = treasury_usd_months(read_csv(args.financiamiento), fx, args.desde, args.hasta)
    market = {
        r["mes"]: float(r["compras_netas_tesoro_en_mercado_usd_millones_informe_bcra"])
        for r in read_csv(args.compras)
        if r["compras_netas_tesoro_en_mercado_usd_millones_informe_bcra"] not in ("", "n/d")
    }
    factors = read_base_factors(_cached_object(BCRA_SERIES_SHA, "bcra"))
    balance = read_balance_cambiario(_cached_object(BALANCE_CAMBIARIO_SHA, "bcra"))
    duties = cr.observed_duties(args.derechos / "derechos_estimados.csv")
    badlar = cr.monthly_rate(args.tasa_pesos)
    first_rate = badlar[min(badlar)]
    mandate = []
    for m in sorted(treasury):
        e = a3500[0][m]
        x = treasury[m]
        mandate.append(
            cr.MandateMonth(
                mes=m,
                tipo_de_cambio=e,
                derecho_usd=duties.get(m, 0.0),
                exportaciones_mlc_usd=balance[m]["bal003"],
                compras_bcra_usd=factors[m]["Compra de divisas al sector privado"] / e,
                compras_tesoro_usd=x["compras"],
                compras_tesoro_mercado_usd=min(x["compras"], max(0.0, market.get(m, 0.0))),
                deuda_desembolsada_usd=x["desembolsada"],
                tasa_pesos=badlar.get(m, first_rate),
            )
        )
    _write(out / "mandato_insumos.csv", [vars(m) | {"proporcion_compra_bcra": round(
        m.bcra_share, 3)} for m in mandate])  # fmt: skip
    mandate_summary = []
    for uso in ("compras", "deuda"):
        for usd_rate in args.tasas_divisas:
            rows, s = cr.mandate_counterfactual(mandate, uso, usd_rate)
            mandate_summary.append(s)
            if usd_rate == args.tasas_divisas[0]:
                _write(out / f"mandato_contrafactico_{uso}.csv", rows)
    bcra = cr.bcra_interest_on_purchases(factors, args.desde, args.hasta)
    (out / "mandato_resumen.json").write_text(
        json.dumps({"contrafactico": mandate_summary, "bcra_intereses": bcra}, indent=1,
                   ensure_ascii=False), encoding="utf-8")  # fmt: skip

    # 2. The years ahead.
    settings = get_settings()
    store = get_store(settings)

    def cached(sha256: str, suffix: str) -> Path:
        dest = settings.cache_dir / "arca" / f"{sha256}{suffix}"
        if not dest.is_file():
            fetch_verified(store, sha256, dest, settings.cache_dir)
        return dest

    with args.descargas.open(newline="", encoding="utf-8") as fh:
        latest = {r["source_id"]: r["sha256"] for r in csv.DictReader(fh) if r["sha256"]}
    zips = [latest[s] for s in sorted(latest) if args.zip_desde <= s <= args.zip_hasta]
    months, _ = screen_unit_values([read_month_detail(cached(h, ".zip")) for h in zips])
    base_months = sorted(m for m, _ in months)[-12:]
    base = {int(m[5:]): fob for m, fob in months if m in base_months}
    # The ratio skips the months after the 0% window of September 2025 (Decreto 682/2025),
    # when duties paid in advance left October to December with a quarter of the estimate.
    ratio_months = [m for m in base_months if m >= args.cobro_desde]
    ratio = cr.collection_ratio(args.derechos / "derechos_estimados.csv", ratio_months)
    rate_of = cr.rate_lookup(load_book(args.alicuotas), crude_prices(cached(latest[args.pi],
                                                                           ".xlsx")))  # fmt: skip
    horizon = cr.month_range(cr.month_range(base_months[-1], "2099-12")[1], args.horizonte)
    shocks = {
        "base": None,
        "sequia_2027": cr.drought(horizon, "2027"),
        "precios_-20%": cr.price_fall(horizon),
    }
    projected = {k: cr.project_duties(base, rate_of, horizon, ratio, v) for k, v in shocks.items()}
    projected["cobro_pleno"] = cr.project_duties(base, rate_of, horizon, 1.0)
    payments = {
        renew: cr.projected_payments(
            args.calendario / "flujos.csv",
            args.conciliacion / "participacion_sector_publico.csv",
            args.instrumentos,
            horizon,
            renew,
        )
        for renew in (False, True)
    }
    scenarios = [
        cr.Scenario("base", {}, False, 1.0),
        cr.Scenario("base", {}, True, 1.0),
        cr.Scenario("cobro_pleno", {}, False, 1.0),
        cr.Scenario("sequia_2027", {}, False, 1.0),
        cr.Scenario("precios_-20%", {}, False, 1.0),
    ]
    monthly, summaries = cr.run_projection(
        horizon,
        projected,
        payments,
        a3500[0][max(a3500[0])],
        scenarios,
        Opening(reserves_usd=args.reservas, treasury_usd=args.depositos_tesoro),
    )
    _write(out / "proyeccion_mensual.csv", monthly)
    _write(out / "proyeccion_derechos.csv", [
        {"mes": m, **{f"derecho_{k}_usd": round(v[0][m], 1) for k, v in projected.items()},
         "fob_base_usd": round(projected["base"][1][m], 1),
         "servicio_consolidado_usd": round(payments[False][m], 1),
         "servicio_si_renuevan_organismos_usd": round(payments[True][m], 1)}
        for m in horizon
    ])  # fmt: skip
    (out / "proyeccion_resumen.json").write_text(
        json.dumps({"base": base_months, "meses_del_cobro": ratio_months,
                    "cobrado_sobre_estimado": round(ratio, 3),
                    "resumen": summaries}, indent=1, ensure_ascii=False),
        encoding="utf-8")  # fmt: skip

    for s in mandate_summary:
        print(json.dumps(s, ensure_ascii=False))
    print(json.dumps(bcra, ensure_ascii=False))
    print(
        f"base de exportaciones {base_months[0]} a {base_months[-1]}, cobrado/estimado {ratio:.3f}"
    )
    for s in summaries:
        print({k: v for k, v in s.items() if k != "por_anio"})
    print(f"tablas en {out}/")
    return 0


def cmd_graficos(args: argparse.Namespace) -> int:
    from argfx.informe import graficos as gr
    from argfx.informe.flujos import read_a3500

    _, eom = read_a3500(args.a3500)
    normal = next(
        float(r["propio_musd"])
        for r in gr._read(args.conciliacion / "stock.csv")
        if r["partida"].startswith("Deuda en situación de pago normal")
    )
    years = [str(y) for y in range(2027, 2037)]
    charts = [
        gr.debt_by_holder(
            args.conciliacion / "sector_publico.csv",
            args.conciliacion / "pesos_sector_publico.csv",
            normal,
            eom[args.corte[:7]],
        ),
        gr.maturities_by_creditor(args.calendario / "flujos.csv", args.instrumentos, years),
        gr.trade_vs_service(args.fmi, args.simulacion / "proyeccion_derechos.csv"),
        gr.accrued_result(args.conciliacion / "devengados_trimestral.csv"),
        gr.duties_vs_service(args.simulacion / "proyeccion_derechos.csv"),
        gr.fund_smoothing(args.simulacion / "proyeccion_mensual.csv", "2027-01", "2028-12"),
    ]
    for g in charts:
        print(gr.write_chart(g, args.out))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="argfx")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("config", help="show resolved configuration (no secrets)").set_defaults(
        func=cmd_config
    )
    sub.add_parser("storage-check", help="round-trip a test object").set_defaults(
        func=cmd_storage_check
    )

    ingest = sub.add_parser("ingest", help="store files by SHA-256 and register them")
    ingest.add_argument("files", nargs="+", type=Path)
    ingest.add_argument("--source-id", help="source_id from the Grok sources.csv")
    ingest.set_defaults(func=cmd_ingest)

    fetch = sub.add_parser("fetch", help="download an object by hash and verify it")
    fetch.add_argument("sha256")
    fetch.add_argument("dest", type=Path)
    fetch.set_defaults(func=cmd_fetch)

    fs = sub.add_parser("fetch-sources", help="download every url in Grok sources.csv into storage")
    fs.add_argument("sources", nargs="+", type=Path)
    fs.add_argument("--delay", type=float, default=1.0, help="seconds between requests")
    fs.set_defaults(func=cmd_fetch_sources)

    val = sub.add_parser("validate", help="validate Grok batches under an inbox directory")
    val.add_argument("inbox", type=Path, help="directory containing lote-*/ folders")
    val.add_argument("--out", type=Path, help="write resumen.md and issues.csv here")
    val.set_defaults(func=cmd_validate)

    cal = sub.add_parser("calendario", help="contract engine: obligations calendar by bucket")
    cal.add_argument("--corte", default="2026-06-30", help="cut-off date (YYYY-MM-DD)")
    cal.add_argument("--terminos", type=Path, default=Path("contratos"))
    cal.add_argument("--sigade", type=Path, default=Path("inbox/lote-c/tablas_sigade"))
    cal.add_argument("--instrumentos", type=Path, default=Path("inbox/lote-c/instruments.csv"))
    cal.add_argument("--out", type=Path, default=Path("data/calendario"))
    cal.add_argument("--series", type=Path, default=Path("series"), help="observed BCRA series")
    cal.set_defaults(func=cmd_calendario)

    con = sub.add_parser("conciliacion", help="phase 3: reconcile with the Finanzas workbook")
    con.add_argument("--corte", default="2026-06-30")
    con.add_argument("--finanzas", type=Path, help="local copy of the Finanzas workbook")
    con.add_argument("--finanzas-sha", default=FINANZAS_2026_06_30, help="R2 object to use")
    con.add_argument("--instrumentos", type=Path, default=Path("inbox/lote-c/instruments.csv"))
    con.add_argument("--calendario", type=Path, default=Path("data/calendario"))
    con.add_argument("--terminos", type=Path, default=Path("contratos"))
    con.add_argument("--tenencias", type=Path, default=Path("tenencias"))
    con.add_argument("--out", type=Path, default=Path("data/conciliacion"))
    con.add_argument("--umbral-abs", type=float, default=10.0, help="millions of USD")
    con.add_argument("--umbral-rel", type=float, default=0.001)
    con.set_defaults(func=cmd_conciliacion)

    dev = sub.add_parser("devengados", help="phase 3: capitalized interest accrued (D-009)")
    dev.add_argument(
        "--planillas", type=Path, default=Path("series/finanzas_planillas_trimestrales.csv")
    )
    dev.add_argument("--colocaciones", type=Path, default=Path("series/oncp_colocaciones.csv"))
    dev.add_argument(
        "--spn", type=Path, default=Path("inbox/lote-i/tablas/series_spn_base_caja.csv")
    )
    dev.add_argument("--fgs", type=Path, default=Path("tenencias/fgs_cartera_categorias.csv"))
    dev.add_argument("--out", type=Path, default=Path("data/conciliacion"))
    dev.set_defaults(func=cmd_devengados)

    der = sub.add_parser("derechos", help="phase 4: export duties estimated by NCM position")
    der.add_argument("--descargas", type=Path, default=Path("manifests/downloads.csv"))
    der.add_argument("--desde", default="SRC-1375", help="first ARCA monthly zip")
    der.add_argument("--hasta", default="SRC-1491", help="last ARCA monthly zip")
    der.add_argument("--mes-desde", default="2020-03", help="first month (rates start 2020-03)")
    der.add_argument("--pi", default="SRC-1566", help="international crude price workbook")
    der.add_argument("--alicuotas", type=Path, default=Path("alicuotas/eventos.csv"))
    der.add_argument("--a3500", type=Path, default=Path("series/bcra_a3500.csv"))
    der.add_argument(
        "--recaudacion", type=Path, default=Path("inbox/lote-d/tablas/series_lote_d.csv")
    )
    der.add_argument("--out", type=Path, default=Path("data/simulacion"))
    der.set_defaults(func=cmd_derechos)

    flu = sub.add_parser("flujos", help="report: peso and dollar flows of the mandate (Sankey)")
    flu.add_argument("--balance-sha", default=BALANCE_CAMBIARIO_SHA)
    flu.add_argument("--series-sha", default=BCRA_SERIES_SHA, help="BCRA Series.xlsm (SRC-1625)")
    flu.add_argument("--aif", type=Path, default=Path("inbox/lote-am/tablas"))
    flu.add_argument(
        "--financiamiento",
        type=Path,
        default=Path(
            "inbox/lote-an/tablas/aif_base_caja_fuentes_y_aplicaciones_financieras_corregida.csv"
        ),
    )
    flu.add_argument(
        "--boletin-sha", default=BOLETIN_FINANZAS_SHA, help="boletín with sheet A.5 (SRC-9002)"
    )
    flu.add_argument(
        "--depositos",
        type=Path,
        default=Path("inbox/lote-am/tablas/bcra_depositos_gobierno_nacional_fin_de_mes.csv"),
    )
    flu.add_argument("--a3500", type=Path, default=Path("series/bcra_a3500.csv"))
    flu.add_argument(
        "--compras",
        type=Path,
        default=Path("inbox/lote-ai/tablas/tesoro_compras_divisas_mensual.csv"),
        help="Treasury purchases of dollars by month (lote AI)",
    )
    flu.add_argument(
        "--pagados-en-pesos",
        type=Path,
        default=Path("inbox/lote-ar/tablas/amortizacion_caja_resumen_mensual_2023-12_2026-09.csv"),
        help="debt written in dollars and paid in pesos, amortized in cash (lote AR)",
    )
    flu.add_argument(
        "--colocados-por-pesos",
        type=Path,
        default=Path(
            "inbox/lote-ar/tablas/colocaciones_licitacion_efectivo_total_mensual_vs_aif_me.csv"
        ),
        help="debt written in dollars and paid in pesos, placed for cash (lote AR)",
    )
    flu.add_argument("--desde", default="2023-12")
    flu.add_argument("--hasta", default="2026-09")
    flu.add_argument("--out", type=Path, default=Path("data/informe"))
    flu.set_defaults(func=cmd_flujos)

    sim = sub.add_parser("simular", help="phase 4: run the regimes on the mandate and ahead")
    sim.add_argument("--desde", default="2023-12")
    sim.add_argument("--hasta", default="2026-08")
    sim.add_argument("--horizonte", default="2036-12")
    sim.add_argument("--a3500", type=Path, default=Path("series/bcra_a3500.csv"))
    sim.add_argument("--tasa-pesos", type=Path, default=Path("series/bcra_badlar.csv"))
    sim.add_argument("--tasas-divisas", type=float, nargs="+", default=[7.0, 5.0, 9.0],
                     help="assumed yearly rate of the dollar debt avoided, percent")  # fmt: skip
    sim.add_argument("--derechos", type=Path, default=Path("data/simulacion"))
    sim.add_argument("--calendario", type=Path, default=Path("data/calendario"))
    sim.add_argument("--conciliacion", type=Path, default=Path("data/conciliacion"))
    sim.add_argument("--instrumentos", type=Path, default=Path("inbox/lote-c/instruments.csv"))
    sim.add_argument("--descargas", type=Path, default=Path("manifests/downloads.csv"))
    sim.add_argument("--zip-desde", default="SRC-1375")
    sim.add_argument("--zip-hasta", default="SRC-1491")
    sim.add_argument("--pi", default="SRC-1566")
    sim.add_argument(
        "--cobro-desde", default="2026-01", help="first base month for collected/estimated"
    )
    sim.add_argument("--alicuotas", type=Path, default=Path("alicuotas/eventos.csv"))
    sim.add_argument("--reservas", type=float, default=49_323.0,
                     help="BCRA gross reserves at the start, millions of USD")  # fmt: skip
    sim.add_argument(
        "--depositos-tesoro", type=float, default=1_230.0, help="Treasury FX at the start, MUSD"
    )
    for name in ("financiamiento", "depositos", "compras", "pagados_en_pesos",
                 "colocados_por_pesos"):  # fmt: skip
        sim.add_argument(f"--{name.replace('_', '-')}", type=Path,
                         default=flu.get_default(name))  # fmt: skip
    sim.add_argument("--out", type=Path, default=Path("data/simulacion"))
    sim.set_defaults(func=cmd_simular)

    gra = sub.add_parser("graficos", help="report: bar charts, one currency per panel")
    gra.add_argument("--a3500", type=Path, default=Path("series/bcra_a3500.csv"))
    gra.add_argument("--corte", default="2026-06-30")
    gra.add_argument("--conciliacion", type=Path, default=Path("data/conciliacion"))
    gra.add_argument("--calendario", type=Path, default=Path("data/calendario"))
    gra.add_argument("--simulacion", type=Path, default=Path("data/simulacion"))
    gra.add_argument("--instrumentos", type=Path, default=Path("inbox/lote-c/instruments.csv"))
    gra.add_argument("--fmi", type=Path, default=Path("series/fmi_balanza_proyectada.csv"))
    gra.add_argument("--out", type=Path, default=Path("data/informe"))
    gra.set_defaults(func=cmd_graficos)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
