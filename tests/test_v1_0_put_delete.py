def test_put_wijzigt_notitie(client):
    client.post("/crypto", json={"symbol": "BTC"})
    r = client.put("/crypto/BTC", json={"note": "bewaren"})
    assert r.status_code == 200
    assert r.json()["note"] == "bewaren"


def test_put_wijzigt_alleen_meegestuurde_velden(client):
    client.post("/crypto", json={"symbol": "BTC", "target_price": 30000})
    r = client.put("/crypto/BTC", json={"note": "nieuw"})
    assert r.json()["target_price"] == 30000


def test_put_onbekend_item_404(client):
    assert client.put("/crypto/BTC", json={"note": "x"}).status_code == 404


def test_put_ongeldige_doelprijs_422(client):
    client.post("/crypto", json={"symbol": "BTC"})
    assert client.put("/crypto/BTC", json={"target_price": 0}).status_code == 422


def test_delete_204(client):
    client.post("/crypto", json={"symbol": "BTC"})
    assert client.delete("/crypto/BTC").status_code == 204


def test_delete_verwijdert_item(client):
    client.post("/crypto", json={"symbol": "BTC"})
    client.delete("/crypto/BTC")
    assert client.get("/watchlist").json() == []


def test_delete_onbekend_item_404(client):
    assert client.delete("/crypto/BTC").status_code == 404