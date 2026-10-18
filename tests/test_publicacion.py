from __future__ import annotations

from pathlib import Path

from argfx.publicacion import build_table, classify, copy_public
from argfx.storage import LocalObjectStore


def test_official_issuers_are_public_and_third_parties_are_not() -> None:
    assert classify("Presidencia de la Nación (Infoleg)")[0]
    assert classify("Ministerio de Economía, Contaduría General de la Nación")[0]
    assert classify("U.S. Department of the Treasury")[0]
    assert not classify("La Nación")[0]
    assert not classify("TN (Artear)")[0]
    assert not classify("Infobae")[0]
    assert not classify("Cámara Argentina de Fondos Comunes de Inversión (CAFCI)")[0]
    assert not classify("Venezuela, Convenio Cambiario N° 1, copia en Justia")[0]
    assert not classify("")[0]


def test_only_public_objects_are_copied_once(tmp_path: Path) -> None:
    inbox = tmp_path / "inbox" / "lote"
    inbox.mkdir(parents=True)
    (inbox / "sources.csv").write_text(
        "source_id,issuer,url\nSRC-1,BCRA,https://bcra\nSRC-2,Infobae,https://infobae\n"
    )
    objects = tmp_path / "objects.csv"
    objects.write_text(
        "sha256,size_bytes,object_key,media_type,original_filename,source_id,ingested_at\n"
        "aa,1,objects/aa,text/plain,a.txt,SRC-1,t\nbb,1,objects/bb,text/plain,b.txt,SRC-2,t\n"
    )
    src, dst = LocalObjectStore(tmp_path / "src"), LocalObjectStore(tmp_path / "dst")
    for key in ("objects/aa", "objects/bb"):
        f = tmp_path / "f"
        f.write_text(key)
        src.upload(f, key)
    rows = build_table(objects, tmp_path / "inbox")
    assert [r["publicar"] for r in rows] == ["si", "no"]
    assert copy_public(rows, src, dst) == 1
    assert dst.exists("objects/aa") and not dst.exists("objects/bb")
    assert copy_public(rows, src, dst) == 0
