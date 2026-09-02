# slack-notifications

Henter renteverdier fra Finansportalen og SEB, lagrer dem lokalt og varsler i Slack
når de endrer seg.

## Oppsett

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Opprett en `.env`-fil i prosjektroten (den er gitignorert og skal aldri committes):

```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXXX/XXXX/XXXX

# Valgfritt: overstyr hvor historikken lagres. Standard er ./data
# DATA_DIR=/var/lib/slack-notifications/data
```

## Kjøring

```bash
python main.py
```

## Lagring

Tidligere ble siste verdi lagret i en GitHub Gist. Nå lagres den lokalt som JSON
under `data/`:

- `data/rates_seb.json`
- `data/rates_finansportalen.json`

Hver fil inneholder `last_value` og `last_updated`. Katalogen opprettes automatisk
og er gitignorert. Første kjøring for en kilde lagrer en baseline og sender et
`:new:`-varsel til Slack.

## Kjøring via cron

`main.py` er et engangsskript: det henter, sammenligner, varsler og avslutter.
Det er cron som står for gjentakelsen — skriptet skal ikke kjøre kontinuerlig.

Bruk `run.sh`, som bytter til prosjektkatalogen, bruker riktig venv-python og
roterer `cron.log` når den passerer 1 MB.

```bash
crontab -e
```

```cron
# slack-notifications: hverdager 08:00-20:55, hvert 5. minutt
*/5 8-20 * * 1-5 /sti/til/slack-notifications/run.sh >> /sti/til/slack-notifications/cron.log 2>&1
```

Dette tilsvarer de to cron-linjene i den gamle GitHub Actions-workflowen. Den
trengte to schedules fordi GitHub Actions kjører i UTC (`7-19` vinter, `6-18`
sommer). Lokal cron følger systemets tidssone og håndterer sommertid selv, så
én linje er nok. Sett tidssonen først:

```bash
sudo timedatectl set-timezone Europe/Oslo   # Raspberry Pi
```

På macOS må `/usr/sbin/cron` ha Full Disk Access
(Systeminnstillinger → Personvern og sikkerhet → Full disktilgang), ellers
kjører ikke jobben.

Sjekk at den kjører:

```bash
crontab -l
tail -f cron.log
```
