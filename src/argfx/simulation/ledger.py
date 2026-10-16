"""Double-entry ledger for the accounting layer of the simulation.

Every transaction is a set of postings (sector, instrument, amount) that adds up to zero for
each instrument: what one sector gains as an asset another records as a liability (a negative
holding) or gives up. Instruments carry their currency in the name (`usd`, `ars`), and amounts
are in millions of that currency. With every transaction balanced, the sum of each instrument
over sectors stays at zero, which is the column check of a stock-flow consistent model.

Sectors: TES (Treasury), BCRA, EXP (exporters), PRIV (rest of the private sector, banks
included), ROW (rest of the world).
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

SECTORS = ("TES", "BCRA", "EXP", "PRIV", "ROW")

# instrument -> currency
INSTRUMENTS = {
    "divisas": "usd",  # foreign currency: the BCRA's are gross reserves; ROW is the issuer
    "base": "ars",  # BCRA monetary liabilities held by the private sector
    "dep_tes_ars": "ars",  # Treasury peso deposits at the BCRA
    "dep_tes_usd": "usd",  # Treasury FX deposits at the BCRA (D-001: not subtracted)
    "fondo_usd": "usd",  # stabilization fund of regime (d), a Treasury FX deposit at the BCRA
    "pasivos_remunerados": "ars",  # BCRA sterilization instruments
    "deuda_tes_ars": "ars",  # Treasury peso debt
    "deuda_tes_usd": "usd",  # Treasury FX debt
}


@dataclass(frozen=True)
class Posting:
    sector: str
    instrument: str
    amount: float


@dataclass
class Transaction:
    month: str
    kind: str
    postings: tuple[Posting, ...]

    def check(self, tol: float = 1e-6) -> None:
        by_instrument: dict[str, float] = defaultdict(float)
        for p in self.postings:
            if p.sector not in SECTORS or p.instrument not in INSTRUMENTS:
                raise ValueError(f"{self.kind}: unknown {p.sector}/{p.instrument}")
            by_instrument[p.instrument] += p.amount
        bad = {k: v for k, v in by_instrument.items() if abs(v) > tol}
        if bad:
            raise ValueError(f"{self.month} {self.kind}: unbalanced {bad}")


@dataclass
class Ledger:
    holdings: dict[tuple[str, str], float] = field(default_factory=lambda: defaultdict(float))
    journal: list[Transaction] = field(default_factory=list)

    def post(self, month: str, kind: str, *legs: tuple[str, str, float]) -> None:
        tx = Transaction(month, kind, tuple(Posting(*leg) for leg in legs if leg[2]))
        tx.check()
        for p in tx.postings:
            self.holdings[(p.sector, p.instrument)] += p.amount
        self.journal.append(tx)

    def transfer(self, month: str, kind: str, instrument: str, src: str, dst: str,
                 amount: float) -> None:  # fmt: skip
        """Move an asset from `src` to `dst` (for an issuer, `src` adds a liability)."""
        self.post(month, kind, (src, instrument, -amount), (dst, instrument, amount))

    def get(self, sector: str, instrument: str) -> float:
        return self.holdings.get((sector, instrument), 0.0)

    def column_sums(self) -> dict[str, float]:
        out: dict[str, float] = defaultdict(float)
        for (_, instrument), v in self.holdings.items():
            out[instrument] += v
        return dict(out)
