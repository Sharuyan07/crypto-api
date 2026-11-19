from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

from app import coingecko, watchlist

app = FastAPI(title="Crypto API")


class WatchlistIn(BaseModel):
    symbol: str = Field(min_length=1, max_length=10)
    note: str | None = None
    target_price: float | None = Field(default=None, gt=0)


class WatchlistUpdate(BaseModel):
    note: str | None = None
    target_price: float | None = Field(default=None, gt=0)


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


@app.post("/crypto", status_code=201)
def add_to_watchlist(body: WatchlistIn):
    symbol = body.symbol.upper()
    coin = _find_coin(symbol)
    if coin is None:
        raise HTTPException(status_code=404, detail="Coin niet gevonden")
    if watchlist.get(symbol) is not None:
        raise HTTPException(status_code=409, detail="Coin staat al in de watchlist")
    item = {
        "symbol": symbol,
        "name": coin["name"],
        "note": body.note,
        "target_price": body.target_price,
    }
    watchlist.add(item)
    return item


@app.get("/watchlist")
def show_watchlist():
    return watchlist.get_all()


@app.put("/crypto/{symbol}")
def update_watchlist_item(symbol: str, body: WatchlistUpdate):
    symbol = symbol.upper()
    if watchlist.get(symbol) is None:
        raise HTTPException(status_code=404, detail="Coin staat niet in de watchlist")
    return watchlist.update(symbol, body.model_dump(exclude_unset=True))


@app.delete("/crypto/{symbol}", status_code=204)
def delete_from_watchlist(symbol: str):
    symbol = symbol.upper()
    if watchlist.get(symbol) is None:
        raise HTTPException(status_code=404, detail="Coin staat niet in de watchlist")
    watchlist.remove(symbol)
    return Response(status_code=204)