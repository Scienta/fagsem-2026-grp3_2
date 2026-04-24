
# Norske skatteregler (forenklet) – for skattekalkulatør

> **Gyldighet:** Inntektsåret 2024 (skatteoppgjør 2025)
> **Målgruppe:** Coding agent som skal implementere en norsk skattekalkulatør
> **Kilde:** Skatteetaten.no (forenklet fremstilling – ikke juridisk rådgivning)

---

## 1. Grunnbegreper

| Begrep | Forklaring |
|---|---|
| **Bruttoinntekt** | Lønn, næringsinntekt, pensjon o.l. før fradrag |
| **Alminnelig inntekt** | Bruttoinntekt minus alle fradrag (minstefradrag, personfradrag, renter, osv.) |
| **Personinntekt** | Bruttoinntekt (lønn/pensjon) – grunnlag for trinnskatt og trygdeavgift |
| **Skattekommune** | Kommunen man er bosatt i per 1. januar i inntektsåret |

---

## 2. Skatter og avgifter – oversikt

En norsk lønnsmottaker betaler typisk fire komponenter:

```
Total skatt = Inntektsskatt (flat) + Trinnskatt + Trygdeavgift + (Formuesskatt hvis aktuelt)
```

---

## 3. Inntektsskatt (flat skatt på alminnelig inntekt)

Flat sats på **alminnelig inntekt** (etter fradrag):

| Skatteyter | Sats |
|---|---|
| Person bosatt i Norge (utenom Finnmark/Nord-Troms) | **22 %** |
| Person bosatt i Finnmark eller Nord-Troms | **18,5 %** |

> Satsen gjelder sum av kommuneskatt + fylkesskatt + fellesskatt.

---

## 4. Trinnskatt (på personinntekt)

Trinnskatt beregnes **direkte på brutto personinntekt** (lønn, pensjon) – **ingen fradrag trekkes fra**.

### Lønnsmottakere og næringsdrivende – trinn 2024

| Trinn | Inntekt fra (kr) | Inntekt til (kr) | Sats |
|---|---|---|---|
| 1 | 208 051 | 292 850 | 1,7 % |
| 2 | 292 851 | 670 000 | 4,0 % |
| 3 | 670 001 | 937 900 | 13,6 % |
| 4 | 937 901 | 1 350 000 | 16,6 % |
| 5 | 1 350 001 | ∞ | 17,6 % |

> Under 208 051 kr: **ingen trinnskatt**

### Pensjonister – trinn 2024

| Trinn | Inntekt fra (kr) | Inntekt til (kr) | Sats |
|---|---|---|---|
| 1 | 208 051 | 292 850 | 0,9 % |
| 2 | 292 851 | 670 000 | 2,0 % |
| 3 | 670 001 | 937 900 | 11,8 % |
| 4 | 937 901 | 1 350 000 | 14,8 % |
| 5 | 1 350 001 | ∞ | 17,6 % |

**Beregning (trinnskatt er progressiv – marginal per trinn):**
```
trinnskatt = sum over alle trinn av:
    min(personinntekt, øvre_grense) - nedre_grense) * sats
    (kun hvis personinntekt > nedre_grense)
```

---

## 5. Trygdeavgift (på personinntekt)

| Inntektstype | Sats 2024 |
|---|---|
| Lønnsinntekt | **7,8 %** |
| Næringsinntekt (selvstendig) | **11,0 %** |
| Pensjon og trygd | **5,1 %** |
| Under friinntektsgrensen (83 000 kr) | **0 %** |

**Nedtrappingsregel (frikortgrense):**
Trygdeavgiften kan **ikke overstige 25 % av inntekten over 83 000 kr**.
Dette forhindrer at avgiften spiser mer enn overskuddet ved lav inntekt.

```
maks_trygdeavgift = 0.25 * max(0, personinntekt - 83_000)
trygdeavgift = min(sats * personinntekt, maks_trygdeavgift)
```

---

## 6. Fradrag

### 6.1 Minstefradrag (automatisk)

Beregnes automatisk for lønn og pensjon. Trekkes fra bruttoinntekt før skatt på alminnelig inntekt.

| Type | Sats | Minimum (kr) | Maksimum (kr) |
|---|---|---|---|
| Lønn | 46 % av lønn | 4 000 | 104 450 |
| Pensjon | 40 % av pensjon | 4 000 | 86 250 |

```
minstefradrag_lønn = max(4_000, min(0.46 * lønn, 104_450))
minstefradrag_pensjon = max(4_000, min(0.40 * pensjon, 86_250))
```

### 6.2 Personfradrag

Fast beløp som trekkes fra alminnelig inntekt etter minstefradrag.

| Skatteklasse | Beløp 2024 (kr) |
|---|---|
| Klasse 1 (alle voksne) | 88 250 |
| Klasse 2 (utgår) | Ikke lenger i bruk |

> Nesten alle skattytere bruker klasse 1.

### 6.3 Andre vanlige fradrag (valgfrie å implementere)

| Fradrag | Maks (kr) | Beskrivelse |
|---|---|---|
| Renteutgifter | Ubegrenset | Gjeldsrenter på boliglån o.l. |
| BSU (boligsparing ungdom) | 27 500/år spart → 10 % skattefradrag (maks 2 750 kr) | Under 34 år |
| Fagforeningskontingent | 7 700 | Direkte fradrag i alminnelig inntekt |
| Pendlerfradrag | Varierer | Reisekostnader over 14 400 kr/år |
| Foreldrefradrag | 25 000 (1 barn), +15 000 per ekstra barn | Barnepass |

---

## 7. Beregning – steg for steg

```
INNDATA:
  - brutto_lønn         (kr)
  - andre_inntekter     (kr, f.eks. pensjon, kapitalinntekt)
  - renteutgifter       (kr)
  - andre_fradrag       (kr, sum av valgfrie fradrag)
  - inntektstype        ("lønn" | "pensjon" | "næring")

STEG 1 – Beregn personinntekt
  personinntekt = brutto_lønn + andre_inntekter (kun lønn/pensjon/næring)

STEG 2 – Beregn minstefradrag
  minstefradrag = max(4_000, min(0.46 * brutto_lønn, 104_450))
  (bruk pensjonssats hvis pensjon)

STEG 3 – Beregn alminnelig inntekt
  alminnelig_inntekt = personinntekt
                       - minstefradrag
                       - personfradrag (88_250)
                       - renteutgifter
                       - andre_fradrag
  alminnelig_inntekt = max(0, alminnelig_inntekt)  # aldri negativ

STEG 4 – Inntektsskatt (22 %)
  inntektsskatt = alminnelig_inntekt * 0.22

STEG 5 – Trinnskatt
  trinnskatt = sum av marginalskatt per trinn (se tabell over)

STEG 6 – Trygdeavgift
  rå_trygdeavgift = personinntekt * sats  (7.8% / 11% / 5.1%)
  maks_trygdeavgift = max(0, personinntekt - 83_000) * 0.25
  trygdeavgift = min(rå_trygdeavgift, maks_trygdeavgift)

STEG 7 – Total skatt
  total_skatt = inntektsskatt + trinnskatt + trygdeavgift

STEG 8 – Nettoinntekt
  netto = brutto_lønn - total_skatt
  effektiv_skattesats = total_skatt / brutto_lønn * 100
```

---

## 8. Eksempelberegning (lønn 700 000 kr, 2024)

| Post | Beløp (kr) |
|---|---|
| Brutto lønn | 700 000 |
| Minstefradrag | −104 450 (maks) |
| Personfradrag | −88 250 |
| **Alminnelig inntekt** | **507 300** |
| Inntektsskatt (22 %) | 111 606 |
| Trinnskatt (trinn 1+2+3 delvis) | 1 445 + 15 124 + 4 082 = **20 651** |
| Trygdeavgift (7,8 %) | 54 600 |
| **Total skatt** | **186 857** |
| **Nettoinntekt** | **513 143** |
| **Effektiv skattesats** | **26,7 %** |

---

## 9. Formuesskatt (valgfritt å implementere)

| Grense | Sats |
|---|---|
| Under 1 700 000 kr (enslig) / 3 400 000 kr (ektepar) | 0 % |
| Over grensen | 1,0 % (kommunal 0,7 % + statlig 0,3 %) |

Formue inkluderer: bankinnskudd (100 %), aksjer (80 % av verdi), primærbolig (25 % av markedsverdi), sekundærbolig (100 %), fritidseiendom (30 % av verdi), minus gjeld.

---

## 10. Viktige forenklinger og avgrensninger

- Kalkulatøren dekker **lønnsmottakere** primært
- **Kapitalskatt** (aksjegevinster, utbytte) skattlegges med 37,84 % og er ikke inkludert i dette rammeverket
- **Næringsdrivende** (ENK) har egne regler for personinntektsberegning
- **Skatteklasse 2** er fjernet fra 2021
- **Kildeskatt** for utenlandske arbeidstakere er ikke dekket
- Alle tall er for **inntektsåret 2024**

---

## 11. Referanser

- [Skatteetaten – satser 2024](https://www.skatteetaten.no/satser/)
- [Skatteetaten – trinnskatt](https://www.skatteetaten.no/person/skatt/hjelp-til-riktig-skatt/arbeid-trygd-og-pensjon/trinnskatt/)
- [Skatteetaten – minstefradrag](https://www.skatteetaten.no/person/skatt/hjelp-til-riktig-skatt/arbeid-trygd-og-pensjon/minstefradrag/)
