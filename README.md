# Crypto API

Een kleine REST API (FastAPI) die cryptoprijzen toont via [CoinGecko](https://www.coingecko.com/en/api) en waarmee je een eigen watchlist met favoriete coins bijhoudt. De API is gebouwd met testgedreven ontwikkeling (TDD) en pytest.

- **Auteur:** Sharuyan Sinnathurai
- **Repository:** https://github.com/Sharuyan07/crypto-api

## Installatie en starten (Windows)

```powershell
git clone https://github.com/Sharuyan07/crypto-api.git
cd crypto-api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

De API draait nu op http://localhost:8000. De interactieve documentatie (Swagger) staat op http://localhost:8000/docs.

Op Mac of Linux activeer je de virtual environment met `source .venv/bin/activate`.

### API-key (optioneel)

CoinGecko werkt ook zonder key, maar met rate limits. Heb je een (demo) key, zet die dan als omgevingsvariabele voordat je de server start:

```powershell
$env:COINGECKO_API_KEY="jouw_key"
```

Zet nooit je echte key in GitHub. Het bestand `.env` staat in `.gitignore`.

## Endpoints

| Methode | Endpoint | Beschrijving | Succes | Fouten |
|---|---|---|---|---|
| GET | `/crypto` | Top 10 populaire coins | 200 | 502 |
| GET | `/crypto/{symbol}` | Eén coin, bijvoorbeeld `BTC` | 200 | 404, 502 |
| POST | `/crypto` | Coin toevoegen aan de watchlist | 201 | 404, 409, 422, 502 |
| GET | `/watchlist` | Watchlist bekijken | 200 | - |
| PUT | `/crypto/{symbol}` | Notitie of doelprijs van een watchlist-item wijzigen | 200 | 404, 422 |
| DELETE | `/crypto/{symbol}` | Coin uit de watchlist verwijderen | 204 | 404 |

Prijzen zijn in USD. `change` is de verandering over 24 uur in procenten. Symbolen zijn hoofdletterongevoelig (`btc` en `BTC` werken allebei).

Foutmeldingen hebben de vorm `{"detail": "Coin niet gevonden"}`.

| Statuscode | Betekenis |
|---|---|
| 404 | Coin niet gevonden (of niet in de watchlist) |
| 409 | Coin staat al in de watchlist |
| 422 | Ongeldige invoer (bijvoorbeeld ontbrekend `symbol` of een doelprijs kleiner dan of gelijk aan 0) |
| 502 | CoinGecko is niet bereikbaar |

## Voorbeelden

De voorbeelden gebruiken `curl.exe` in PowerShell. Let op: gebruik in PowerShell geen spaties in de tekst van een notitie, want dan gaat de quoting mis (gebruik bijvoorbeeld `kopen-bij-dip`). In Postman of via `/docs` heb je dit probleem niet.

### GET /crypto

```powershell
curl.exe http://localhost:8000/crypto
```

```json
[
  {"symbol": "BTC", "name": "Bitcoin", "price": 63758, "change": -1.3},
  {"symbol": "ETH", "name": "Ethereum", "price": 1803.03, "change": -0.38}
]
```

### GET /crypto/{symbol}

```powershell
curl.exe http://localhost:8000/crypto/BTC
```

```json
{"symbol": "BTC", "name": "Bitcoin", "price": 63759, "change": -1.28}
```

### POST /crypto

```powershell
curl.exe -i -X POST http://localhost:8000/crypto -H "Content-Type: application/json" -d '{\"symbol\":\"ETH\",\"note\":\"kopen-bij-dip\",\"target_price\":1500}'
```

Response (201 Created):

```json
{"symbol": "ETH", "name": "Ethereum", "note": "kopen-bij-dip", "target_price": 1500.0}
```

`note` en `target_price` zijn optioneel. `target_price` moet groter zijn dan 0.

### GET /watchlist

```powershell
curl.exe http://localhost:8000/watchlist
```

```json
[{"symbol": "ETH", "name": "Ethereum", "note": "kopen-bij-dip", "target_price": 1500.0}]
```

### PUT /crypto/{symbol}

```powershell
curl.exe -i -X PUT http://localhost:8000/crypto/ETH -H "Content-Type: application/json" -d '{\"note\":\"bewaren\"}'
```

Response (200 OK). Alleen de meegestuurde velden worden gewijzigd:

```json
{"symbol": "ETH", "name": "Ethereum", "note": "bewaren", "target_price": 1500.0}
```

### DELETE /crypto/{symbol}

```powershell
curl.exe -i -X DELETE http://localhost:8000/crypto/ETH
```

Response: `204 No Content` (geen body).

## Tests draaien

```powershell
pytest -v
```

De tests gebruiken een mock van CoinGecko, dus ze zijn snel en hebben geen internet of API-key nodig. In totaal zijn er 21 tests, verdeeld over drie bestanden:

| Bestand | Release | Onderdeel |
|---|---|---|
| `tests/test_v0_1_get.py` | v0.1 | GET-endpoints |
| `tests/test_v0_2_post.py` | v0.2 | POST en GET /watchlist |
| `tests/test_v1_0_put_delete.py` | v1.0 | PUT en DELETE |

## Releases en testrapporten

Het project is gebouwd met TDD (Red, Green, Refactor). Per release staat er een testrapport met de testcases, de uitkomsten en het bewijs (pytest-uitvoer en screenshots).

| Release | Inhoud | Testrapport |
|---|---|---|
| v0.1 | GET `/crypto` en GET `/crypto/{symbol}` | [testrapport-v0.1.md](docs/testrapporten/testrapport-v0.1.md) |
| v0.2 | POST `/crypto` en GET `/watchlist` | [testrapport-v0.2.md](docs/testrapporten/testrapport-v0.2.md) |
| v1.0 | PUT en DELETE `/crypto/{symbol}` | [testrapport-v1.0.md](docs/testrapporten/testrapport-v1.0.md) |

## Projectstructuur

```
crypto-api/
├── app/
│   ├── main.py          # endpoints
│   ├── coingecko.py     # koppeling met CoinGecko
│   └── watchlist.py     # opslag van de watchlist
├── tests/               # pytest-tests
├── docs/testrapporten/  # testrapporten per release
├── pytest.ini
└── requirements.txt
```

## Beperkingen

- De watchlist staat in het geheugen en is leeg zodra je de server herstart.
- `GET /crypto/{symbol}` zoekt in de top 100 van CoinGecko.

## Gebruikte techniek

Python 3.12, FastAPI, uvicorn, httpx, pytest.