import finnhub
from api_keys import finnhub_key

finnhub_client = finnhub.Client(api_key=finnhub_key)


def get_price(ticker: str):
    return finnhub_client.quote(ticker)['c']

