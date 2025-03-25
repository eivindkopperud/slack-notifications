import requests

def get_latest_value_seb():
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


def get_payload(old_value, new_value):
    if float(new_value) > float(old_value):
        payload = {
            "text": f":chart_with_upwards_trend: *SWAP Rate har endret seg*\nGammel verdi: {old_value}\nNy verdi: {new_value}"
        }
    else:
        payload = {
            "text": f":chart_with_downwards_trend: *SWAP Rate har endret seg*\nGammel verdi: {old_value}\nNy verdi: {new_value}"
        }
    return payload