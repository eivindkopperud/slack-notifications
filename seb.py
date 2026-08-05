import requests

def get_latest_value_seb():
    response = requests.get("https://sebgroup.com/ssc/trading/fx-rates-bff/api/rates/swap?currency=NOK")
    data = response.json()
    for row in data['rows']:
        maturity = row['data'][0]['value']
        value = row['data'][1]['value']
        if maturity == "10 Yr":
            return value
    return None


def get_payload(old_value, new_value):
    sum_old = float(old_value)
    sum_new = float(new_value)
    if sum_new > sum_old:
        payload = {
            "text": f":chart_with_upwards_trend: *SWAP Rate har endret seg*\nGammel verdi: {old_value}\nNy verdi: {new_value}"
        }
    elif sum_new < sum_old:
        payload = {
            "text": f":chart_with_downwards_trend: *SWAP Rate har endret seg*\nGammel verdi: {old_value}\nNy verdi: {new_value}"
        }
    else:
        payload = {
            "text": f" *SWAP Rate*\n Midlertidig verdi: {new_value}"
        }
    return payload
