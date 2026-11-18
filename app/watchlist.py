_items: dict[str, dict] = {}


def get_all():
    return list(_items.values())


def get(symbol):
    return _items.get(symbol)


def add(item):
    _items[item["symbol"]] = item


def update(symbol, changes):
    _items[symbol].update(changes)
    return _items[symbol]


def remove(symbol):
    del _items[symbol]


def clear():
    _items.clear()