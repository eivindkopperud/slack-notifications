import requests
import json
import time
from datetime import datetime


class NordnetAPIWrapper:
    LOGIN_URL = 'https://classic.nordnet.no/api/2/authentication/basic/login'
    ANONYMOUS_LOGIN_URL = 'https://classic.nordnet.no/api/2/login/anonymous'
    REFRESH_LOGIN_URL = 'https://www.nordnet.no/api/2/login'
    BATCH_URL = 'https://www.nordnet.no/api/2/batch'
    OSE_STOCKS_URL = 'https://www.nordnet.no/api/2/instrument_search/query/stocklist'
    HEADERS_BASE = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'Accept': 'application/json',
        'Connection': 'keep-alive',
        'content-type': 'application/json',
        'Referer': 'https://wwww.nordnet.no',
        'Client-Id': 'NEXT'
    }

    def get_upcoming_week(self):
        stocks = self.get_stock_data()
        upcoming_stocks = []
        ts = time.time()*1000
        for i in stocks:
            try:
                info = i["company_info"]

                report_date_ts = info["report_date"]
                diff = report_date_ts - ts
                days = diff//86400000

                #report_description = report_description = info["report_description"]
                #report_date = datetime.fromtimestamp(report_date_ts/1000).strftime("%d-%m-%Y")
                if days < 7:
                    upcoming_stocks.append(i)
                    #print(i["instrument_info"]["symbol"], datetime.fromtimestamp(report_date_ts/1000).strftime("%d-%m-%Y"), i['key_ratios_info'], i['historical_returns_info'])
            except KeyError:
                pass

        upcoming_stocks_additional = self.get_additional_data(upcoming_stocks)

        for i in upcoming_stocks_additional:
            print(i["instrument_info"]["symbol"], i["sector"]["group"], datetime.fromtimestamp(i["company_info"]["report_date"]/1000).strftime("%d-%m-%Y"), i['key_ratios_info'])

        return upcoming_stocks_additional




    def get_additional_data(self, stock_data):
        url = self.BATCH_URL

        print(len(stock_data))

        for i in range(0, len(stock_data), 5):
            chunk = stock_data[i:i + 5]
            batch_string = '['
            for j in range(0, len(chunk)):
                batch_string += '{{"relative_url":"instruments/{}","method":"GET"}}'.format(chunk[j]['instrument_info']['instrument_id'])
                if chunk[j] != chunk[-1]:
                    batch_string += ','
            batch_string += ']'
            params = {
                "batch": batch_string,
            }
            response = requests.post(url, params=params, headers=self.HEADERS_BASE)
            data_str = response.content.decode('utf-8')
            data_dict = json.loads(data_str)
            additional_data = data_dict
            for k in range(0, len(additional_data)):
                try:
                    sector = additional_data[k]["body"][0]["sector"]
                    sector_group = additional_data[k]["body"][0]["sector_group"]
                except KeyError:
                    sector = "UNKNOWN"
                    sector_group = "UNKNOWN"
                stock_data[i+k]["sector"] = {"sector": sector, "group": sector_group}
            time.sleep(5)

        return stock_data

    def get_stock_data(self):
        url = self.OSE_STOCKS_URL
        offset = 0
        total_hits = -1
        results = []

        while total_hits != offset:
            params = {
                "apply_filters": "exchange_country=NO",
                "limit": 100,
                "offset": offset
            }
            response = requests.get(url, params=params, headers=self.HEADERS_BASE)
            data_str = response.content.decode('utf-8')
            data_dict = json.loads(data_str)

            total_hits = data_dict['total_hits']
            rows = data_dict['rows']
            results.extend(data_dict['results'])

            offset = offset + rows
            time.sleep(5)

        return results

    def get_dummy_stock_data(self):
        url = self.OSE_STOCKS_URL
        offset = 0
        total_hits = -1
        results = []

        params = {
            "apply_filters": "exchange_country=NO",
            "limit": 30,
            "offset": offset
        }
        response = requests.get(url, params=params, headers=self.HEADERS_BASE)
        data_str = response.content.decode('utf-8')
        data_dict = json.loads(data_str)

        total_hits = data_dict['total_hits']
        rows = data_dict['rows']
        results.extend(data_dict['results'])

        return results

