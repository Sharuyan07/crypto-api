import pytest
from fastapi.testclient import TestClient
from app import coingecko, watchlist
from app.main import app

SAMPLE = [
    {"symbol": "BTC", "name": "Bitcoin", "price": 27000, "change": 2.3},
    {"symbol": "ETH", "name": "Ethereum", "price": 1800, "change": -1.2},
]

@pytest.fixture(autouse=True)
def schone_watchlist():
    watchlist.clear()
    yield
    watchlist.clear()

@pytest.fixture
def fake_markt(monkeypatch):
    def fake(per_page=10):
        return [dict(c) for c in SAMPLE][:per_page]
    monkeypatch.setattr(coingecko, "fetch_markets", fake)

@pytest.fixture
def client(fake_markt):
    return TestClient(app)

@pytest.fixture
def coingecko_down(monkeypatch, client):
    def kapot(per_page=10):
        raise coingecko.CoinGeckoError("down")
    monkeypatch.setattr(coingecko, "fetch_markets", kapot)