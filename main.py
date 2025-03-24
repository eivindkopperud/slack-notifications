import os
import requests
import json
import datetime

import finansportalen

gist_url = "https://api.github.com/gists/4d17720b7a328e065b73e08780fa946f"
gist_token = os.getenv("GIST_TOKEN")
slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

def get_latest_value():
    response = requests.get("https://sebgroup.com/ssc/trading/fx-rates-bff/api/rates/swap?currency=NOK")
    data = response.json()
    for row in data['rows']:
        maturity = row['data'][0]['value']
        value = row['data'][1]['value']
        decimals = row['data'][1]['decimals']
        diff = row['data'][2]['value']
        if maturity == "10 Yr" and decimals == 2 and diff == 0.0:
            return value
    return None

def get_gist_data(filename):
    headers = {"Authorization": f"token {gist_token}"}
    response = requests.get(gist_url, headers=headers)
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
    requests.patch(gist_url, headers=headers, json=new_data)

def send_slack_notification(new_value, old_value):
    payload = {
        "text": f":rotating_light: *SWAP Rate har endret seg*\nGammel verdi: {old_value}\nNy verdi: {new_value}"
    }
    requests.post(slack_webhook_url, json=payload)

def main():
    latest_value = get_latest_value()
    latest_value_finansportalen = finansportalen.get_latest_value_finansportalen()

    if not latest_value:
        print("Fant ingen gyldig verdi for 10 Yr")
        return

    last_value, _ = get_gist_data("rates.txt")
    last_value_finansportalen, _ = get_gist_data("rates_finansportalen.txt")

    if str(latest_value) != str(last_value):
        print(f"Ny verdi funnet: endret fra {last_value} til {latest_value}")
        update_gist(latest_value, "rates.txt")
        send_slack_notification(latest_value, last_value)
    else:
        print("Ingen endringer funnet.")

    if latest_value_finansportalen != last_value_finansportalen:
        print(f"Endring på Finansportalen: endret fra {last_value} til {latest_value}")
        update_gist(latest_value, "rates_finansportalen.txt")
        send_slack_notification(latest_value_finansportalen, last_value_finansportalen)
    else:
        print("Ingen endringer funnet.")


if __name__ == "__main__":
    main()
