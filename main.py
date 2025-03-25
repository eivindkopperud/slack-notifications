import os
import requests
import json
import datetime

import finansportalen
import seb

gist_url = "https://api.github.com/gists/4d17720b7a328e065b73e08780fa946f"
gist_token = os.getenv("GIST_TOKEN")
slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")


def get_gist_data(filename):
    headers = {"Authorization": f"token {gist_token}"}
    response = requests.get(gist_url, headers=headers)
    print("get_gist_data", response.json())
    if response.status_code == 200:
        content = json.loads(response.json()['files'][filename]['content'])

        return content["last_value"], content["last_updated"]
    return None, None


def update_gist(new_value, filename):
    headers = {"Authorization": f"token {gist_token}"}
    new_data = {
        "files": {
            filename: {
                "content": json.dumps({
                    "last_value": new_value,
                    "last_updated": datetime.datetime.now().isoformat()
                }, indent=4)
            }
        }
    }
    response = requests.patch(gist_url, headers=headers, json=new_data)
    print("update_gist", response.json())


def send_slack_notification(new_value, old_value, source):
    if source == "finansportalen":
        payload = finansportalen.get_payload(old_value, new_value)
        requests.post(slack_webhook_url, json=payload)
    elif source == "seb":
        payload = seb.get_payload(old_value, new_value)
        requests.post(slack_webhook_url, json=payload)
    else:
        print("Invalid source: {}", source)


def fetch_and_update_data(source):
    if source == "finansportalen":
        latest_value = finansportalen.get_latest_value_finansportalen()
    elif source == "seb":
        latest_value = seb.get_latest_value_seb()
    else:
        print(f"Fant ingen gyldige verdier for {source}")
        return

    last_value, _ = get_gist_data(f"rates_{source}.txt")

    if str(latest_value) != str(last_value):
        print(f"Ny verdi funnet: endret fra {latest_value} til {latest_value}")
        update_gist(latest_value, f"rates_{source}.txt", )
        send_slack_notification(latest_value, last_value, source)
    else:
        print("Ingen endringer funnet.")


def main():
    fetch_and_update_data("seb")
    fetch_and_update_data("finansportalen")


if __name__ == "__main__":
    main()
