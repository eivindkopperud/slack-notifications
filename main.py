import datetime
import os
import sys

import requests
from dotenv import load_dotenv

import finansportalen
import seb
import storage

load_dotenv()

slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

SOURCES = {
    "seb": {
        "label": "SWAP Rate",
        "fetch": seb.get_latest_value_seb,
        "payload": seb.get_payload,
    },
    "finansportalen": {
        "label": "Finansportalen",
        "fetch": finansportalen.get_latest_value_finansportalen,
        "payload": finansportalen.get_payload,
    },
}


def post_to_slack(payload):
    response = requests.post(slack_webhook_url, json=payload, timeout=30)
    if response.status_code != 200:
        print(f"Slack-varsel feilet ({response.status_code}): {response.text}")


def send_slack_notification(new_value, old_value, source):
    post_to_slack(SOURCES[source]["payload"](old_value, new_value))


def send_baseline_notification(source, value):
    post_to_slack(
        {
            "text": f":new: *{SOURCES[source]['label']}*\n"
            f"Første kjøring – ingen lagret historikk. Lagrer baseline: {value}"
        }
    )


def fetch_and_update_data(source):
    if source not in SOURCES:
        print(f"Fant ingen gyldige verdier for {source}")
        return

    latest_value = SOURCES[source]["fetch"]()
    if latest_value is None:
        print(f"Ingen verdi hentet for {source}")
        return

    last_value, last_updated = storage.read_data(source)

    if last_value is None:
        # Første kjøring på denne maskinen (eller data-katalogen mangler):
        # lagre baseline og varsle i Slack.
        print(f"Ingen lagret historikk for {source}. Lagrer baseline: {latest_value}")
        storage.write_data(source, latest_value)
        send_baseline_notification(source, latest_value)
        return

    updated_today = False
    if last_updated:
        try:
            updated_today = (
                datetime.datetime.fromisoformat(last_updated).date()
                == datetime.date.today()
            )
        except ValueError:
            print(f"Kunne ikke tolke last_updated: {last_updated}")

    if str(latest_value) != str(last_value):
        print(f"Ny verdi funnet: endret fra {last_value} til {latest_value}")
    elif not updated_today:
        print(
            f"Ingen endring, men data er ikke oppdatert i dag. Viser nyeste verdi: {latest_value}"
        )
    else:
        print(f"Ingen endringer funnet for {source}.")
        return

    storage.write_data(source, latest_value)
    send_slack_notification(latest_value, last_value, source)


def main():
    if not slack_webhook_url:
        print(
            "SLACK_WEBHOOK_URL mangler. Opprett en .env-fil (se .env.example) "
            "eller sett miljøvariabelen før du kjører skriptet."
        )
        sys.exit(1)

    for source in SOURCES:
        fetch_and_update_data(source)


if __name__ == "__main__":
    main()
