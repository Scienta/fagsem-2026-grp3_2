"""Norwegian tax calculation rules for income year 2024.

Scope: salary earners (lønnsmottakere) resident on Østlandet.
Reference: skatt.md in the project root.

All functions are pure and operate on Decimal or int kroner.
"""

from dataclasses import dataclass
from decimal import Decimal


# --- Constants: satser og grenser 2024 ---------------------------------------

MINSTEFRADRAG_SATS_LONN = Decimal("0.46")
MINSTEFRADRAG_MIN = Decimal("4000")
MINSTEFRADRAG_MAX_LONN = Decimal("104450")

PERSONFRADRAG_KLASSE_1 = Decimal("88250")

INNTEKTSSKATT_SATS_OSTLANDET = Decimal("0.22")

TRYGDEAVGIFT_SATS_LONN = Decimal("0.078")
TRYGDEAVGIFT_FRIGRENSE = Decimal("83000")
TRYGDEAVGIFT_NEDTRAPPING = Decimal("0.25")

# Trinnskatt lønnsmottakere 2024. Each entry: (lower, upper, rate).
# Lower is the income threshold above which the bracket applies; upper is the
# inclusive top of the bracket (None means unlimited).
TRINNSKATT_LONN_2024 = (
    (Decimal("208050"), Decimal("292850"), Decimal("0.017")),
    (Decimal("292850"), Decimal("670000"), Decimal("0.040")),
    (Decimal("670000"), Decimal("937900"), Decimal("0.136")),
    (Decimal("937900"), Decimal("1350000"), Decimal("0.166")),
    (Decimal("1350000"), None, Decimal("0.176")),
)


# --- Dataklasser -------------------------------------------------------------

@dataclass(frozen=True)
class Taxpayer:
    name: str
    age: int
    salary: Decimal


@dataclass(frozen=True)
class TaxResult:
    taxpayer: Taxpayer
    minstefradrag: Decimal
    alminnelig_inntekt: Decimal
    inntektsskatt: Decimal
    trinnskatt: Decimal
    trygdeavgift: Decimal
    total: Decimal


# --- Beregningsfunksjoner ----------------------------------------------------

def minstefradrag_lonn(salary: Decimal) -> Decimal:
    """Minstefradrag for lønnsinntekt 2024."""
    if salary <= 0:
        return Decimal("0")
    beregnet = salary * MINSTEFRADRAG_SATS_LONN
    return max(MINSTEFRADRAG_MIN, min(beregnet, MINSTEFRADRAG_MAX_LONN))


def alminnelig_inntekt(salary: Decimal, minstefradrag: Decimal,
                      personfradrag: Decimal = PERSONFRADRAG_KLASSE_1) -> Decimal:
    """Alminnelig inntekt etter minstefradrag og personfradrag. Aldri negativ."""
    result = salary - minstefradrag - personfradrag
    return result if result > 0 else Decimal("0")


def inntektsskatt(alm_inntekt: Decimal,
                  sats: Decimal = INNTEKTSSKATT_SATS_OSTLANDET) -> Decimal:
    return alm_inntekt * sats


def trinnskatt(personinntekt: Decimal,
               trinn=TRINNSKATT_LONN_2024) -> Decimal:
    """Progressiv trinnskatt – marginal per trinn."""
    if personinntekt <= 0:
        return Decimal("0")
    total = Decimal("0")
    for lower, upper, rate in trinn:
        if personinntekt <= lower:
            break
        top = personinntekt if upper is None else min(personinntekt, upper)
        total += (top - lower) * rate
    return total


def trygdeavgift_lonn(personinntekt: Decimal) -> Decimal:
    """Trygdeavgift lønn med nedtrappingsregel ved frikortgrensen."""
    if personinntekt <= 0:
        return Decimal("0")
    ra = personinntekt * TRYGDEAVGIFT_SATS_LONN
    over_frigrense = personinntekt - TRYGDEAVGIFT_FRIGRENSE
    maks = over_frigrense * TRYGDEAVGIFT_NEDTRAPPING if over_frigrense > 0 else Decimal("0")
    return min(ra, maks)


def beregn_skatt(taxpayer: Taxpayer) -> TaxResult:
    """Full beregning for en skatteyter på Østlandet med lønnsinntekt."""
    salary = Decimal(taxpayer.salary)
    mf = minstefradrag_lonn(salary)
    alm = alminnelig_inntekt(salary, mf)
    ink = inntektsskatt(alm)
    trn = trinnskatt(salary)
    try_avg = trygdeavgift_lonn(salary)
    total = ink + trn + try_avg
    return TaxResult(
        taxpayer=taxpayer,
        minstefradrag=mf,
        alminnelig_inntekt=alm,
        inntektsskatt=ink,
        trinnskatt=trn,
        trygdeavgift=try_avg,
        total=total,
    )
