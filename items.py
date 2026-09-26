"""Предметы и магазин:"""
ITEMS = {
    "зелье_здоровья":     {"name": "Зелье здоровья",     "type": "зелье",  "effect": "heal",         "value": 50,  "description": "Восстанавливает 50 HP",           "price": 50},
    "зелье_силы":         {"name": "Зелье силы",         "type": "зелье",  "effect": "attack",       "value": 10,  "description": "+10 к атаке до конца боя",        "price": 75},
    "эликсир_богов":      {"name": "Эликсир богов",      "type": "зелье",  "effect": "heal",         "value": 500, "description": "Восстанавливает 500 HP",          "price": 250},
    "зелье_ярости":       {"name": "Зелье ярости",       "type": "зелье",  "effect": "buff_rage",    "value": 0,   "description": "+100% к атаке на 3 хода",         "price": 300},
    "зелье_неуязвимости": {"name": "Зелье неуязвимости", "type": "зелье",  "effect": "buff_invuln",  "value": 0,   "description": "Иммунитет к урону на 2 хода",     "price": 500},
    "свиток_времени":     {"name": "Свиток времени",     "type": "зелье",  "effect": "dispel",       "value": 0,   "description": "Снимает все баффы с врага",       "price": 700},

    "меч_воина":          {"name": "Меч воина",          "type": "оружие", "effect": "attack",       "value": 15,  "description": "+15 к атаке",                     "price": 200},
    "посох_мага":         {"name": "Посох мага",         "type": "оружие", "effect": "attack",       "value": 20,  "description": "+20 к атаке",                     "price": 250},
    "кольцо_могущества":  {"name": "Кольцо могущества",  "type": "оружие", "effect": "attack",       "value": 35,  "description": "+35 к атаке",                     "price": 400},
    "артефакт_хаоса":     {"name": "Артефакт Хаоса",     "type": "оружие", "effect": "attack",       "value": 50,  "description": "+50 к атаке",                     "price": 600},
    "щит_защиты":         {"name": "Щит защиты",         "type": "броня",  "effect": "defense",      "value": 25,  "description": "+25 к защите",                    "price": 250},
    "плащ_теней":         {"name": "Плащ теней",         "type": "броня",  "effect": "dodge",        "value": 10,  "description": "+10% к уклонению",                "price": 250},
    "панцирь_титана":     {"name": "Панцирь титана",     "type": "броня",  "effect": "defense",      "value": 40,  "description": "+40 к защите",                    "price": 450},
}


def get_item(key: str) -> dict:
    if key not in ITEMS:
        raise KeyError(f"Предмет '{key}' не найден")
    return ITEMS[key].copy()