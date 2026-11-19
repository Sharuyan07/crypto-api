def test_get_crypto_geeft_200_en_lijst(client):
    r = client.get("/crypto")
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_get_crypto_velden(client):
    assert set(client.get("/crypto").json()[0]) == {"symbol", "name", "price", "change"}


def test_get_symbol_btc(client):
    r = client.get("/crypto/BTC")
    assert r.status_code == 200
    assert r.json()["name"] == "Bitcoin"


def test_get_symbol_hoofdletterongevoelig(client):
    assert client.get("/crypto/btc").status_code == 200


def test_get_onbekend_symbol_404(client):
    assert client.get("/crypto/XXX").status_code == 404


def test_get_crypto_coingecko_down_502(coingecko_down, client):
    assert client.get("/crypto").status_code == 502