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
        args.terminos, args.sigade, args.instrumentos, date.fromisoformat(args.corte), args.out
    )
    for k, v in counts.items():
        print(f"{k}: {v:,}")
    print(f"tablas en {args.out}/")
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
    cal.set_defaults(func=cmd_calendario)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
