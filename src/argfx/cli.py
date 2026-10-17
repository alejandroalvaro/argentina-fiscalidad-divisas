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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
