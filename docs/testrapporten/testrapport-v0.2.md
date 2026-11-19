# Testrapport v0.2

- Versie: v0.2
- Datum: 19-11-2026
- Getest door: Sharuyan Sinnathurai
- Omgeving: Python 3.12.10, pytest 9.2.0, Windows, FastAPI met uvicorn

## Samenvatting
- Geautomatiseerde tests: 14 (6 uit v0.1 en 8 nieuw)
- Geslaagd: 14
- Gefaald: 0
- Handmatige tests tegen de echte CoinGecko: 6 testcases, alle geslaagd (H1 tot en met H3 na een tweede poging, zie "Gevonden bugs")

## Geautomatiseerde testcases (CoinGecko gemockt)
| ID | Testcase | Verwacht | Werkelijk | Status |
|---|---|---|---|---|
| A1 | POST BTC | 201 | 201 | Geslaagd |
| A2 | POST met notitie en doelprijs | 201, velden terug | 201, velden terug | Geslaagd |
| A3 | POST dubbel | 409 | 409 | Geslaagd |
| A4 | POST zonder symbol | 422 | 422 | Geslaagd |
| A5 | POST negatieve doelprijs | 422 | 422 | Geslaagd |
| A6 | POST onbekende coin | 404 | 404 | Geslaagd |
| A7 | POST, CoinGecko down | 502 | 502 | Geslaagd |
| A8 | GET /watchlist na POST | lijst bevat BTC | lijst bevat BTC | Geslaagd |

## Handmatige testcases (curl.exe, echte CoinGecko)
| ID | Testcase | Verwacht | Werkelijk | Status |
|---|---|---|---|---|
| H1 | POST ETH met notitie en doelprijs | 201 | 201 Created | Geslaagd (2e poging) |
| H2 | GET /watchlist | 200, bevat BTC en ETH | 200, bevat BTC en ETH | Geslaagd (2e poging) |
| H3 | POST BTC dubbel | 409 | 409 Conflict | Geslaagd (2e poging) |
| H4 | POST onbekende coin XXX | 404 | 404 Not Found | Geslaagd |
| H5 | POST zonder symbol | 422 | 422 Unprocessable Entity | Geslaagd |
| H6 | POST negatieve doelprijs | 422 | 422 Unprocessable Entity | Geslaagd |

### Eerste poging van H1 tot en met H3
| Commando | Verwacht | Werkelijk | Oorzaak |
|---|---|---|---|
| POST BTC met notitie "kopen bij dip" | 201 | 422 JSON decode error | PowerShell knipte de tekst bij de spaties, waardoor curl kapotte JSON verstuurde |
| GET /watchlist | 200, bevat BTC | 200, lege lijst | BTC was door de mislukte POST niet toegevoegd |
| POST BTC (bedoeld als dubbele toevoeging) | 409 | 201 Created | BTC stond nog niet in de lijst, dus werd hij nu toegevoegd |

## Gevonden bugs en oplossingen
- Rode fase: 8 tests faalden met 405 (POST /crypto bestond niet) en 404 (/watchlist bestond niet). Opgelost door POST /crypto en GET /watchlist te implementeren in app/main.py.
- Eerste handmatige poging van H1 gaf 422 (JSON decode error). Oorzaak: PowerShell knipte de spaties in de notitie in stukken. Geen fout in de API. Opgelost door de notitie zonder spaties te versturen (kopen-bij-dip) en H1 tot en met H3 opnieuw uit te voeren.
- Warning: StarletteDeprecationWarning over httpx in de testclient. Heeft geen invloed op de werking.

## Bewijs
Rode fase (voor de implementatie): 8 failed, 6 passed.

![pytest rood](v0.2-pytest-rood.png)

Groene fase (na de implementatie): 14 passed.

![pytest groen](v0.2-pytest-groen.png)

Handmatige tests:

![H1](v0.2-t1-post.png)
![H2](v0.2-t2-watchlist.png)
![H3](v0.2-t3-dubbel.png)
![H4](v0.2-t4-onbekend.png)
![H5](v0.2-t5-zonder-symbol.png)
![H6](v0.2-t6-negatief.png)

## Conclusie
Release v0.2 is goedgekeurd: alle geautomatiseerde tests slagen en alle handmatige testcases slagen na het oplossen van het quoting-probleem in de testopdracht.