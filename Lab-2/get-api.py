import requests
API_KEY = ''

with open('secrets.txt', 'r') as fp:
    API_KEY = fp.read()
print(API_KEY[-1])

def get_api(equity_name, api_token):
    url = 'https://www.alphavantage.co/query'
    params = dict(
        function='TIME_SERIES_INTRADAY',
        symbol=equity_name,
        interval = '60min',
        apikey=api_token
    )
    resp =requests.get(url,params=params)
    print(resp)
    data = resp.json()
    if 'Error Message' in data.keys():
        return 'Error response'
    meta_data = data['Meta Data']
    equity_price = data[f'Time Series ({params["interval"]})']
    print(meta_data, equity_price[list(equity_price.keys())[0]])
get_api('NVDA', API_KEY)