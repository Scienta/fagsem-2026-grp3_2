#!/usr/bin/env python3
"""
Norsk skattekalkulator for Østlandet
"""

import sys
from pathlib import Path


class TaxCalculator:
    """Kalkulator for norsk skatt basert på regler fra skatt.md"""

    def __init__(self):
        # Trygdeavgiftssatser
        self.trygde_sats_loenn = 0.078
        self.trygde_sats_naering = 0.11
        self.trygde_sats_pensjon = 0.051

        # Trinnskatt for lønnsinntekter (2024)
        self.trinn_loenn = [
            {"nedre": 208051, "øvre": 292850, "sats": 0.017},
            {"nedre": 292851, "øvre": 670000, "sats": 0.04},
            {"nedre": 670001, "øvre": 937900, "sats": 0.136},
            {"nedre": 937901, "øvre": 1350000, "sats": 0.166},
            {"nedre": 1350001, "øvre": None, "sats": 0.176},
        ]

        # Trinnskatt for pensjonister (2024)
        self.trinn_pensjon = [
            {"nedre": 208051, "øvre": 292850, "sats": 0.009},
            {"nedre": 292851, "øvre": 670000, "sats": 0.02},
            {"nedre": 670001, "øvre": 937900, "sats": 0.118},
            {"nedre": 937901, "øvre": 1350000, "sats": 0.148},
            {"nedre": 1350001, "øvre": None, "sats": 0.176},
        ]

        # Personfradrag
        self.personfradrag = 88250

        # Minstefradrag (maksimaler)
        self.minstefradrag_loenn_maks = 104450
        self.minstefradrag_loenn_min = 4000
        self.minstefradrag_pensjon_maks = 86250
        self.minstefradrag_pensjon_min = 4000

    def _beregn_minstefradrag(self, inntekt, inntektstype):
        """Beregner minstefradrag"""
        if inntektstype == "pensjon":
            sats = 0.40
            maks = self.minstefradrag_pensjon_maks
        else:  # lønn eller næring
            sats = 0.46
            maks = self.minstefradrag_loenn_maks

        fradrag = max(self.minstefradrag_loenn_min, min(sats * inntekt, maks))
        return fradrag

    def _beregn_trinnskatt(self, personinntekt, inntektstype):
        """Beregner trinnskatt progressivt"""
        trinn = self.trinn_loenn if inntektstype == "lønn" else self.trinn_pensjon

        trinnskatt = 0
        for t in trinn:
            if personinntekt > t["nedre"]:
                grense = t["øvre"] if t["øvre"] is not None else personinntekt
                trinnskatt += (min(grense, personinntekt) - t["nedre"]) * t["sats"]

        return trinnskatt

    def _beregn_trygdeavgift(self, personinntekt, inntektstype):
        """Beregner trygdeavgift med nedtrappingsregel"""
        if inntektstype == "pensjon":
            sats = self.trygde_sats_pensjon
        elif inntektstype == "næring":
            sats = self.trygde_sats_naering
        else:  # lønn
            sats = self.trygde_sats_loenn

        raa_trygdeavgift = personinntekt * sats
        maks_trygdeavgift = max(0, personinntekt - 83000) * 0.25
        trygdeavgift = min(raa_trygdeavgift, maks_trygdeavgift)

        return trygdeavgift

    def beregn_skatt(self, navn, alder, inntekt, inntektstype="lønn"):
        """Beregner total skatt for en person"""
        # STEG 1: Beregn personinntekt
        personinntekt = inntekt

        # STEG 2: Beregn minstefradrag
        minstefradrag = self._beregn_minstefradrag(inntekt, inntektstype)

        # STEG 3: Beregn alminnelig inntekt
        alminnelig_inntekt = max(0,
                                 personinntekt
                                 - minstefradrag
                                 - self.personfradrag
                                )

        # STEG 4: Inntektsskatt (22 %)
        inntektsskatt = alminnelig_inntekt * 0.22

        # STEG 5: Trinnskatt
        trinnskatt = self._beregn_trinnskatt(personinntekt, inntektstype)

        # STEG 6: Trygdeavgift
        trygdeavgift = self._beregn_trygdeavgift(personinntekt, inntektstype)

        # STEG 7: Total skatt
        total_skatt = inntektsskatt + trinnskatt + trygdeavgift

        # STEG 8: Nettoinntekt
        netto = inntekt - total_skatt
        effektiv_sats = (total_skatt / inntekt * 100) if inntekt > 0 else 0

        return {
            "navn": navn,
            "alder": alder,
            "brutto_inntekt": inntekt,
            "minstefradrag": minstefradrag,
            "personfradrag": self.personfradrag,
            "alminnelig_inntekt": alminnelig_inntekt,
            "inntektsskatt": inntektsskatt,
            "trinnskatt": trinnskatt,
            "trygdeavgift": trygdeavgift,
            "total_skatt": total_skatt,
            "netto_inntekt": netto,
            "effektiv_sats": effektiv_sats,
        }


def les_inndata(filnavn):
    """Leser inn data fra input-fil"""
    data = []
    with open(filnavn, 'r', encoding='utf-8') as f:
        for linje in f:
            linje = linje.strip()
            if not linje:
                continue

            # Først sjekk om dette er inntekt (siste linje i en person)
            # Inntekt skal ha et tall som kan representeres med tusenadskomma eller NOK
            # Alder er alltid et enkelt tall (f.eks. "30 år")

            # Håndter personinntekt (tall eller tekst med NOK)
            # Inntekt linjer har alltid "NOK", alder linjer har aldri "NOK"
            if "NOK" in linje:
                # Dette er inntekt
                stripped = linje.replace(" ", "").replace("NOK", "").replace(",", "")
                if stripped.isdigit():
                    inntekt = int(stripped)
                    if "inntekt" not in data[-1]:
                        data[-1]["inntekt"] = inntekt
            else:
                # Dette er ikke inntekt, kan være navn eller alder
                # Sjekk om linjen inneholder tall (alder)
                if any(c.isdigit() for c in linje):
                    # Dette er alder
                    try:
                        alder = int("".join(c for c in linje if c.isdigit()))
                        data[-1]["alder"] = alder
                    except ValueError:
                        # Feil - ikke tall, men vi har navn allerede
                        data.append({"navn": linje})
                else:
                    # Dette er navn
                    data.append({"navn": linje})
    return data


def skriv_utdata(skatter, filnavn):
    """Skriver resultatet til fil"""
    with open(filnavn, 'w', encoding='utf-8') as f:
        for skatt in skatter:
            f.write(f"{skatt['navn']}\n")
            f.write(f"{int(skatt['total_skatt'])} NOK\n")


def main():
    """Hovedfunksjon"""
    if len(sys.argv) < 2:
        print("Bruk: python tax_calculator.py <input-fil> [output-fil]")
        sys.exit(1)

    input_fil = sys.argv[1]
    output_fil = sys.argv[2] if len(sys.argv) > 2 else "resultat.txt"

    # Les inn data
    data = les_inndata(input_fil)

    if not data:
        print("Ingen gyldig data å behandle")
        sys.exit(1)

    # Beregn skatt for hver person
    kalkulator = TaxCalculator()
    skatter = []

    for person in data:
        navn = person.get("navn", "Ukjent")
        alder = person.get("alder", 0)
        inntekt = person.get("inntekt", 0)

        # Bestem inntektstype basert på inntekt
        if inntekt > 50000:
            inntektstype = "lønn"
        elif inntekt > 0:
            inntektstype = "pensjon"
        else:
            inntektstype = "lønn"

        resultat = kalkulator.beregn_skatt(navn, alder, inntekt, inntektstype)
        skatter.append(resultat)

    # Skriv ut resultat
    skriv_utdata(skatter, output_fil)

    print(f"Skatt beregnet for {len(skatter)} personer")
    print(f"Resultat lagret i: {output_fil}")


if __name__ == "__main__":
    main()