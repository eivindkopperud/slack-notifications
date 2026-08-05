import requests

def process_data(data):
    processed_data = []
    for row in data:
        try:
            rate = row['effectiveInterestRate']
            processed_data.append(rate)
        except:
            print("Failed to process row: {}".format(row))
            pass
    return processed_data

def sort_data(data):
    return sorted(data, reverse=False)

def get_latest_value_finansportalen():
    response = requests.get("https://finans-api.forbrukerradet.no/bankprodukt/boliglan?age=45&fixedInterestRateYear[0]=fastrente_over_9&interestType=Fast&isSalaryRequired=true&loanAmount=1500000&loanType[0]=standardl%C3%A5n&marketRegion[0]=NationWide&membershipType[0]=None&membershipType[1]=HousingAssociation&paymentPeriod=30&purchasePrice=3000000&query=&requiredProductTypes[0]=None")
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
    elif sum_new < sum_old:
        payload = {
            "text": f":chart_with_downwards_trend: *Finansportalen har endret seg*\nGammel verdi: {old_value}\nNy verdi: {new_value}"
        }
    else:
        payload = {
            "text": f" *Finansportalen *\n: Midlertidig verdi: {new_value}"
        }
    return payload