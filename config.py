"""Глобальные настройки и константы."""
GAME_TITLE = "ХРОНОСПИРАЛЬ"
GAME_SUBTITLE = "Эпическая сага о мести богам времени"

DIFFICULTY_MULTIPLIERS = {
    "лёгкая":     {"player_health": 1.5, "player_attack": 1.3, "player_defense": 1.3,
                   "enemy_health": 0.6, "enemy_attack": 0.6, "enemy_defense": 0.6, "exp_gain": 1.5},
    "средняя":    {"player_health": 1.2, "player_attack": 1.1, "player_defense": 1.1,
                   "enemy_health": 0.8, "enemy_attack": 0.8, "enemy_defense": 0.8, "exp_gain": 1.2},
    "сложная":    {"player_health": 1.0, "player_attack": 1.0, "player_defense": 1.0,
                   "enemy_health": 1.0, "enemy_attack": 1.0, "enemy_defense": 1.0, "exp_gain": 1.0},
    "безумная":   {"player_health": 0.9, "player_attack": 0.95, "player_defense": 0.9,
                   "enemy_health": 1.3, "enemy_attack": 1.2, "enemy_defense": 1.2, "exp_gain": 1.5},
    "невозможная": {"player_health": 0.8, "player_attack": 0.95, "player_defense": 0.9,
                   "enemy_health": 1.5, "enemy_attack": 1.4, "enemy_defense": 1.3, "exp_gain": 2.0},
}

DIFFICULTY_CHOICES = {"1": "лёгкая", "2": "средняя", "3": "сложная", "4": "безумная", "5": "невозможная"}

CLASS_BASE_STATS = {
    "Воин":    {"health": 150, "attack": 15, "defense": 15, "dodge": 5},
    "Маг":     {"health": 80,  "attack": 25, "defense": 5,  "dodge": 5},
    "Ассасин": {"health": 75,  "attack": 25, "defense": 5,  "dodge": 25},
}

CLASS_STARTING_ITEMS = {
    "Воин":    {"weapon": "меч_воина",  "armor": None,         "inventory": ["зелье_здоровья"]},
    "Маг":     {"weapon": "посох_мага", "armor": None,         "inventory": ["зелье_здоровья", "зелье_силы"]},
    "Ассасин": {"weapon": None,         "armor": "плащ_теней", "inventory": ["зелье_здоровья"]},
}

CHAOS_PHASE2_HP_MULT = 4.0
CHAOS_PHASE2_ATTACK_MULT = 1.4
CHAOS_PHASE2_DEFENSE_MULT = 1.2
CRIT_CHANCE = 10 # %
CRIT_MULTIPLIER = 1.5
EXP_BASE = 100
EXP_GROWTH = 1.5
STAT_POINTS_PER_LEVEL = 5
HEALTH_PER_LEVEL = 20
STARTING_GOLD = 100