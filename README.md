# Skattkalkulatoren CLI Utility (Last updated: 2026-04-24)

## ⚙️ Oppsett
Før du starter, må et virtuelt miljø aktiveres og avhengigheter installeres:

1. **Aktiver venv:** `source .venv/bin/activate`
2. **Installer avhengigheter:** `pip install -r requirements.txt`
3. **Sett miljøvariabler (valgfritt):** `source set_env.sh` (Sett `PYTHONPATH` og andre nødvendige variabler)

## 🚀 Kjøring
Kjør hovedprogrammet ved å bruke:
`python tax_calculator.py <input_fil>`

Hvor `<input_fil>` er en tekstfil med skattedata i formatet vist her.

## 🧩 Inputformat
Skattedata skal formatere i følgende blokkstruktur per skatteyter:

```
Navn Person
Alder År
Inntekt NOK
```

**Eksempel:**
```
Roger Rud
50 År
125 000 NOK

Per Høneeier
42 År
7 000 000 NOK
```

## 📝 Prosjektstruktur
* `src/`: Inneholder kildekode for skattekalkulatoren.
* `test/`: Inneholder enhetstester for funksjonaliteten.
* `documentation/`: (Opprettes for mer detaljert dokumentasjon.)

## 📅 Oppdatert
Kjør alltid testene etter endringer:
`pytest --cov=src`

## ✍️ Kontroller og Dokumentasjon
Detaljerte skatteregler og kalkulasjonssteg finnes i [skatt.md](skatt.md). Mer informasjon om oppgaven finnes i [oppgave.md](oppgave.md).

```
