def test_post_geldig_201(client):
    r = client.post("/crypto", json={"symbol": "BTC"})
    assert r.status_code == 201
    assert r.json()["symbol"] == "BTC"
    assert r.json()["name"] == "Bitcoin"


def test_post_met_notitie_en_doelprijs(client):
    r = client.post("/crypto", json={"symbol": "eth", "note": "kopen bij dip", "target_price": 1500})
    assert r.status_code == 201
    assert r.json()["symbol"] == "ETH"
    assert r.json()["note"] == "kopen bij dip"
    assert r.json()["target_price"] == 1500


def test_post_dubbel_409(client):
    client.post("/crypto", json={"symbol": "BTC"})
    assert client.post("/crypto", json={"symbol": "BTC"}).status_code == 409


def test_post_zonder_symbol_422(client):
    assert client.post("/crypto", json={}).status_code == 422


def test_post_negatieve_doelprijs_422(client):
    r = client.post("/crypto", json={"symbol": "BTC", "target_price": -5})
    assert r.status_code == 422


def test_post_onbekende_coin_404(client):
    assert client.post("/crypto", json={"symbol": "XXX"}).status_code == 404


def test_post_coingecko_down_502(coingecko_down, client):
    assert client.post("/crypto", json={"symbol": "BTC"}).status_code == 502


def test_watchlist_toont_coin(client):
    client.post("/crypto", json={"symbol": "BTC"})
    r = client.get("/watchlist")
    assert r.status_code == 200
    assert [i["symbol"] for i in r.json()] == ["BTC"]