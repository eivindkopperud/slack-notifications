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
og er gitignorert. Første kjøring for en kilde lagrer en baseline uten å sende
Slack-varsel.

## Kjøring på Raspberry Pi (cron)

Hverdager kl. 08–20, hvert 5. minutt. Sett riktig tidssone på Pi-en først
(`sudo timedatectl set-timezone Europe/Oslo`), så slipper du sommertid-justeringer.

```bash
crontab -e
```

```cron
*/5 8-19 * * 1-5 cd /home/pi/slack-notifications && .venv/bin/python main.py >> /home/pi/slack-notifications/cron.log 2>&1
```

Cron leser ikke `.env` selv — det gjør `python-dotenv` i `main.py`, og derfor må
`cd` til prosjektkatalogen stå i cron-linja.
