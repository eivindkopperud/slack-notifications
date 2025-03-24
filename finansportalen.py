import requests

def process_data(data):
    processed_data = []
    for row in data['data']:
        try:
            rate = row['effektivRente'].replace(",",".")
            processed_data.append(rate)
        except:
            print("Failed to process row: {}".format(row))
            pass
    return processed_data

def sort_data(data):
    return sorted(data, reverse=False)

def get_latest_value_finansportalen():
    response = requests.get("https://www.finansportalen.no/services/kalkulator/boliglan?alderstilbudAr=45&fastrente_6_10=ja&kalkulatortype=laan&kjopesum=3000000&laan_type=bolig&lanebelop=1500000&lopetidtermin_value=30&nasjonalt=ja&neiforutsettermedlemskap=ja&rente=fastrente_rente&rentetakIgnore=ja&standardlan=ja&visProduktpakker=ja&visUtenProduktpakker=ja")
    data = response.json()
    processed_data = process_data(data)
    sorted_data = sort_data(processed_data)

    return sorted_data[:5]

def get_payload(old_value, new_value):
    sum_old = sum(map(float, old_value))
    sum_new = sum(map(float, new_value))
    if sum_new > sum_old:
        payload = {
            "text": f":chart_with_upwards_trend: *Finansportalen har endret seg*\nGammel verdi: {old_value}\nNy verdi: {new_value}"
        }
    else:
        payload = {
            "text": f":chart_with_downwards_trend: *Finansportalen har endret seg*\nGammel verdi: {old_value}\nNy verdi: {new_value}"
        }
    return payload