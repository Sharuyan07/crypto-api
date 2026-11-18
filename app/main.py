from fastapi import FastAPI, HTTPException
from app import coingecko

app = FastAPI(title="Crypto API")


def _markets(per_page):
    try:
        return coingecko.fetch_markets(per_page=per_page)
    except coingecko.CoinGeckoError:
        raise HTTPException(status_code=502, detail="CoinGecko is niet bereikbaar")


def _find_coin(symbol):
    for coin in _markets(100):
        if coin["symbol"] == symbol.upper():
            return coin
    return None


@app.get("/crypto")
def list_coins():
    return _markets(10)


@app.get("/crypto/{symbol}")
def get_coin(symbol: str):
    coin = _find_coin(symbol)
    if coin is None:
        raise HTTPException(status_code=404, detail="Coin niet gevonden")
    return coin