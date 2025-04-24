import requests
import json
import time


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

