import requests
from bs4 import BeautifulSoup
from copy import deepcopy

apikeypolygon = "bmN7i7CrzrpKqFvgbB1fEaztCwZKSUjJ"

def get_tickers():
    result = requests.get(url=f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&limit=100&apiKey={apikeypolygon}").json()
    return result

def get_stock_daily(stock_ticker, date_tmstp):
    url=f"https://api.polygon.io/v1/open-close/{stock_ticker}/{date_tmstp}?apiKey={apikeypolygon}"
    result = requests.get(url=url).json()
    return result

def scraping_marketwatch(stock_ticker):
    mi = 1000000
    bi = 1000000000
    tri = bi * 1000
    api_key_2captcha = "33f2bfc6db7c3a7af69aac6fd3eeb36e"
    proxy_2captcha = "	ud8c9f36f56c605c2-zone-custom:ud8c9f36f56c605c2@43.152.113.55:2333"
    url = f"https://www.marketwatch.com/investing/stock/{stock_ticker}"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    
    cookie_value=None
    #with open("cookies_datadome.json", 'r') as json_file:
    #    cookie_value = json.load(json_file)
    cookies = {'datadome': cookie_value}

    headers = {
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'text/plain',
        'origin': "https://www.marketwatch.com",
        'referer': url,
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': user_agent,
    }

    res = requests.get(url=url,
                       proxies={'http': 'http://'+proxy_2captcha},
                       cookies={'datadome': cookie_value},
                       headers=headers
                       )
    
    if res.status_code in ['401', '402', '403']:
        print(res.status_code)
        #código para solução do captcha (DataDome)
    
    if res.status_code not in ['200','201', '202', '203']:
        soup = BeautifulSoup(res.text, 'html.parser')
        performance = soup.find(class_='performance')
        competitors = soup.find(class_='Competitors')
        ###########################################################################
        try:
            tr_elements = performance.find('table').find_all('tr', class_="table__row")
            performance_dict = {
                "5 Day": 0.0,
                "1 Month": 0.0,
                "3 Month": 0.0,
                "YTD": 0.0,
                "1 Year": 0.0
            }
            for row in tr_elements:
                period = row.find('td', class_='table__cell')
                if period.get_text(strip=True) in performance_dict.keys():
                    period_value_tag = row.find(
                        "li", class_=["content__item", "value", "ignore-color"]
                    )
                    if period_value_tag:
                        period_value = period_value_tag.get_text(strip=True)
                        performance_dict[period.get_text(strip=True)] = period_value
            print(performance_dict)
        except AttributeError:
            performance_dict = {"error": "no performance data"}
        ###########################################################################
        try:
            competitors_list = []
            competitors_dict = {
                "name": "",
                "market_cap": {
                    "currency": "",
                    "value": 0.0
                }
            }
            tr_elements = competitors.find('table').find_all('tr', class_="table__row")
            for row in tr_elements[1:]:
                new_competitor = deepcopy(competitors_dict)
                new_competitor["name"] = row.find("td", class_=["table__cell", "w50"]).find("a").text
                currency_and_value = row.find("td", class_="number").text
                currency, value = currency_and_value[0], currency_and_value[1:]
                new_competitor['market_cap']["currency"] = currency
                if value[-1] == "T": #trilhão
                    new_competitor['market_cap']['value'] = float(value[:-1]) * tri
                if value[-1] == "B": #bilhão
                    new_competitor['market_cap']['value'] = float(value[:-1]) * bi
                if value[-1] == "M": #milhão (pouco provável, mas vai que...)
                    new_competitor['market_cap']['value'] = float(value[:-1]) * mi
                competitors_list.append(new_competitor)
        except AttributeError:
            competitors_dict = {"error": "no competitors data"}
        return performance_dict, competitors_list