import requests

def process_data(data):
    processed_data = []
    for row in data['data']:
        try:
            provider = row['boliglan']['leverandorVisningsnavn']
            rate = row['effektivRente'].replace(",",".")
            processed_data.append({'provider': provider, 'rate': rate})
        except:
            print("Failed to process row: {}".format(row))
            pass
    return processed_data

def sort_data(data):
    sorted_data = sorted(data, key=lambda k: k['rate'], reverse=True)
    return sorted_data[:5]

def get_latest_value_finansportalen():
    response = requests.get("https://www.finansportalen.no/services/kalkulator/boliglan?alderstilbudAr=45&fastrente_6_10=ja&kalkulatortype=laan&kjopesum=3000000&laan_type=bolig&lanebelop=1500000&lopetidtermin_value=30&nasjonalt=ja&neiforutsettermedlemskap=ja&rente=fastrente_rente&rentetakIgnore=ja&standardlan=ja&visProduktpakker=ja&visUtenProduktpakker=ja")
    data = response.json()
    processed_data = process_data(data)
    sorted_data = sorted(processed_data, key=lambda k: k['rate'], reverse=False)

    return sorted_data[0:5]