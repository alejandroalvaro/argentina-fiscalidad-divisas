"""Validate Grok batches without correcting anything.

Severity:
- error: breaks the delivery contract; the batch is not merged until fixed.
- warning: allowed, but a person should look at it (ambiguity, missing metadata).

Identical issues are grouped, with the count and the first offending row.
"""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from pydantic import ValidationError

from argfx.schemas import (
    FILE_SCHEMAS,
    SERIES_GLOB,
    SOURCE_ID,
    Claim,
    Instrument,
    ManifestRow,
    Row,
    SeriesObservation,
    Source,
)

Severity = Literal["error", "warning"]
SRC_TOKEN = re.compile(r"SRC-\d{4}")


@dataclass
class Issue:
    lote: str
    file: str
    column: str
    severity: Severity
    code: str
    message: str
    line: int | None = None  # line in the CSV file (header is line 1)
    count: int = 1


@dataclass
class Batch:
    lote: str
    rows: dict[str, list[tuple[int, Row]]] = field(default_factory=dict)  # file -> (line, model)


@dataclass
class Report:
    issues: list[Issue]
    files: list[str]
    rows_read: int

    @property
    def errors(self) -> int:
        return sum(i.count for i in self.issues if i.severity == "error")

    @property
    def warnings(self) -> int:
        return sum(i.count for i in self.issues if i.severity == "warning")


def _read(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return list(reader.fieldnames or []), list(reader)


def _check_file(
    lote: str, rel: str, path: Path, schema: type[Row], issues: list[Issue]
) -> list[tuple[int, Row]]:
    header, raw = _read(path)
    declared = [n for n, f in schema.model_fields.items()]
    required = [n for n, f in schema.model_fields.items() if f.is_required()]
    missing = [c for c in required if c not in header]
    for col in missing:
        issues.append(Issue(lote, rel, col, "error", "missing_column", "required column absent"))
    extra = [c for c in header if c not in declared]
    if extra:
        issues.append(
            Issue(
                lote,
                rel,
                ",".join(extra),
                "warning",
                "extra_columns",
                "columns outside the schema (kept as delivered)",
            )
        )
    parsed: list[tuple[int, Row]] = []
    for i, row in enumerate(raw):
        line = i + 2
        try:
            parsed.append((line, schema.model_validate(row)))
        except ValidationError as exc:
            for err in exc.errors():
                col = ".".join(str(p) for p in err["loc"]) or "?"
                issues.append(
                    Issue(
                        lote,
                        rel,
                        col,
                        "error",
                        "invalid_value",
                        f"{err['msg']} (value: {row.get(col)!r})",
                        line,
                    )
                )
    return parsed


def _batches(root: Path, issues: list[Issue]) -> tuple[list[Batch], list[str], int]:
    batches: list[Batch] = []
    files: list[str] = []
    rows_read = 0
    for lote_dir in sorted(p for p in root.iterdir() if p.is_dir() and p.name.startswith("lote-")):
        batch = Batch(lote_dir.name)
        targets = [(name, lote_dir / name, schema) for name, schema in FILE_SCHEMAS.items()]
        targets += [
            (p.relative_to(lote_dir).as_posix(), p, SeriesObservation)
            for p in sorted(lote_dir.glob(SERIES_GLOB))
        ]
        for rel, path, schema in targets:
            if not path.exists():
                if rel in ("sources.csv", "claims.csv", "documents_manifest.csv"):
                    issues.append(
                        Issue(
                            batch.lote,
                            rel,
                            "",
                            "error",
                            "missing_file",
                            "file required by GROK_TASKS.md",
                        )
                    )
                continue
            batch.rows[rel] = _check_file(batch.lote, rel, path, schema, issues)
            files.append(f"{batch.lote}/{rel}")
            rows_read += len(batch.rows[rel])
        for name in ("unresolved.md",):
            if not (lote_dir / name).exists():
                issues.append(
                    Issue(
                        batch.lote,
                        name,
                        "",
                        "error",
                        "missing_file",
                        "file required by GROK_TASKS.md",
                    )
                )
        # Other tables: only their source_id references are checked here.
        for path in sorted(lote_dir.glob("tablas/*.csv")):
            rel = path.relative_to(lote_dir).as_posix()
            if path.match(SERIES_GLOB):
                continue
            header, raw = _read(path)
            files.append(f"{batch.lote}/{rel}")
            rows_read += len(raw)
            if "source_id" in header:
                batch.rows[rel] = []
                for i, row in enumerate(raw):
                    _check_reference_list(batch.lote, rel, row.get("source_id", ""), i + 2, issues)
        batches.append(batch)
    return batches, files, rows_read


def _check_reference_list(lote: str, rel: str, value: str, line: int, issues: list[Issue]) -> None:
    value = (value or "").strip()
    if not value:
        issues.append(
            Issue(lote, rel, "source_id", "warning", "blank_source", "row without source_id", line)
        )
        return
    tokens = [t.strip() for t in value.split(";")]
    if not all(re.fullmatch(SOURCE_ID[1:-1], t) for t in tokens):
        issues.append(
            Issue(
                lote,
                rel,
                "source_id",
                "warning",
                "nonstandard_source_ref",
                "use SRC-xxxx, or several separated by ';', without free text",
                line,
            )
        )


def _cross_checks(batches: list[Batch], issues: list[Issue]) -> None:
    sources: dict[str, tuple[str, Source]] = {}
    seen: dict[str, Counter[str]] = defaultdict(Counter)
    for b in batches:
        for _line, s in b.rows.get("sources.csv", []):
            assert isinstance(s, Source)
            seen["source_id"][s.source_id] += 1
            sources[s.source_id] = (b.lote, s)
        for _line, c in b.rows.get("claims.csv", []):
            assert isinstance(c, Claim)
            seen["claim_id"][c.claim_id] += 1
        for _line, ins in b.rows.get("instruments.csv", []):
            assert isinstance(ins, Instrument)
            seen["instrument_id"][ins.instrument_id] += 1
    for col, counter in seen.items():
        for value, n in counter.items():
            if n > 1:
                issues.append(
                    Issue(
                        "*",
                        "*",
                        col,
                        "error",
                        "duplicate_id",
                        f"{value} appears {n} times across batches",
                    )
                )

    def known(lote: str, rel: str, sid: str, line: int) -> None:
        if sid not in sources:
            issues.append(
                Issue(
                    lote,
                    rel,
                    "source_id",
                    "error",
                    "unknown_source",
                    f"{sid} not found in any sources.csv",
                    line,
                )
            )

    for b in batches:
        for rel, rows in b.rows.items():
            for line, row in rows:
                if isinstance(row, Claim | Instrument | SeriesObservation):
                    known(b.lote, rel, row.source_id, line)
            if rel.startswith("tablas/") and not rows:
                continue
        _check_manifest(b, sources, issues)
        _check_content(b, issues)


def _check_manifest(b: Batch, sources: dict[str, tuple[str, Source]], issues: list[Issue]) -> None:
    rows = b.rows.get("documents_manifest.csv", [])
    originals: set[tuple[str, str]] = set()
    for line, m in rows:
        assert isinstance(m, ManifestRow)
        role = m.rol
        tokens = SRC_TOKEN.findall(m.source_id)
        clean = ";".join(tokens) == m.source_id.replace(" ", "")
        if not tokens or not clean:
            issues.append(
                Issue(
                    b.lote,
                    "documents_manifest.csv",
                    "source_id",
                    "error",
                    "nonstandard_source_ref",
                    "source_id must be SRC-xxxx (or a ';' list for derived files); "
                    "mark derived files with rol=derivado",
                    line,
                )
            )
            continue
        for sid in tokens:
            if sid not in sources:
                issues.append(
                    Issue(
                        b.lote,
                        "documents_manifest.csv",
                        "source_id",
                        "error",
                        "unknown_source",
                        f"{sid} not found in any sources.csv",
                        line,
                    )
                )
        if len(tokens) == 1 and tokens[0] in sources:
            src_sha = sources[tokens[0]][1].sha256
            if src_sha == m.sha256:
                originals.add((tokens[0], m.sha256))
            elif role != "derivado":
                issues.append(
                    Issue(
                        b.lote,
                        "documents_manifest.csv",
                        "sha256",
                        "error",
                        "sha_mismatch",
                        "sha256 differs from sources.csv and the row is not marked rol=derivado",
                        line,
                    )
                )
    for line, s in b.rows.get("sources.csv", []):
        assert isinstance(s, Source)
        if s.sha256 and (s.source_id, s.sha256) not in originals:
            issues.append(
                Issue(
                    b.lote,
                    "sources.csv",
                    "sha256",
                    "warning",
                    "no_manifest_row",
                    f"{s.source_id}: no documents_manifest row with the same sha256",
                    line,
                )
            )


def _check_content(b: Batch, issues: list[Issue]) -> None:
    for line, ins in b.rows.get("instruments.csv", []):
        assert isinstance(ins, Instrument)
        if ins.indexation == "ninguna informada":
            issues.append(
                Issue(
                    b.lote,
                    "instruments.csv",
                    "indexation",
                    "warning",
                    "indexation_unreported",
                    "the source does not report indexation; confirm against terms",
                    line,
                )
            )
        if ins.isin is None:
            issues.append(
                Issue(b.lote, "instruments.csv", "isin", "warning", "isin_missing", "no ISIN", line)
            )
        if getattr(ins, "holder_residency", None) in (None, ""):
            issues.append(
                Issue(
                    b.lote,
                    "instruments.csv",
                    "holder_residency",
                    "warning",
                    "residency_missing",
                    "holder residency unknown",
                    line,
                )
            )
    for rel, rows in b.rows.items():
        for line, obs in rows:
            if isinstance(obs, SeriesObservation) and obs.unidad is None:
                issues.append(
                    Issue(
                        b.lote,
                        rel,
                        "unidad",
                        "warning",
                        "unit_missing",
                        f"series {obs.series_id} without unit",
                        line,
                    )
                )


def _group(issues: list[Issue]) -> list[Issue]:
    grouped: dict[tuple[str, str, str, str, str, str], Issue] = {}
    for i in issues:
        # Group on the message without the specific value or series, so repeats collapse.
        msg = re.sub(r" \(value: .*\)$", "", i.message)
        msg = re.sub(r"series \S+", "series", msg)
        key = (i.lote, i.file, i.column, i.severity, i.code, msg)
        if key in grouped:
            grouped[key].count += 1
        else:
            grouped[key] = Issue(i.lote, i.file, i.column, i.severity, i.code, i.message, i.line)
    order = {"error": 0, "warning": 1}
    return sorted(grouped.values(), key=lambda i: (order[i.severity], i.lote, i.file, i.line or 0))


def validate_inbox(root: Path) -> Report:
    issues: list[Issue] = []
    batches, files, rows_read = _batches(root, issues)
    _cross_checks(batches, issues)
    return Report(_group(issues), files, rows_read)


def write_report(report: Report, out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path, md_path = out_dir / "issues.csv", out_dir / "resumen.md"
    cols = ["severity", "lote", "file", "line", "column", "code", "count", "message"]
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for i in report.issues:
            w.writerow({c: getattr(i, c) if getattr(i, c) is not None else "" for c in cols})
    lines = [
        "# Validación de lotes Grok",
        "",
        f"Archivos: {len(report.files)}. Filas leídas: {report.rows_read:,}. "
        f"Errores: {report.errors:,}. Advertencias: {report.warnings:,}.",
        "",
        "| Severidad | Lote | Archivo | Columna | Código | Casos | Primera línea | Detalle |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for i in report.issues:
        detail = i.message.replace("|", "\\|")
        lines.append(
            f"| {i.severity} | {i.lote} | {i.file} | {i.column} | {i.code} | {i.count} "
            f"| {i.line or ''} | {detail} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return csv_path, md_path
