import os
import httpx

URL = "https://api.coingecko.com/api/v3/coins/markets"


class CoinGeckoError(Exception):
    pass


def fetch_markets(per_page: int = 10) -> list[dict]:
    headers = {}
    if os.getenv("COINGECKO_API_KEY"):
        headers["x-cg-demo-api-key"] = os.getenv("COINGECKO_API_KEY")
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": per_page, "page": 1}
    try:
        r = httpx.get(URL, params=params, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise CoinGeckoError(str(exc)) from exc
    return [
        {
            "symbol": c["symbol"].upper(),
            "name": c["name"],
            "price": c["current_price"],
            "change": round(c.get("price_change_percentage_24h") or 0, 2),
        }
        for c in data
    ]