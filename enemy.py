"""Враги:"""
from config import (DIFFICULTY_MULTIPLIERS, CHAOS_PHASE2_HP_MULT,
                    CHAOS_PHASE2_ATTACK_MULT, CHAOS_PHASE2_DEFENSE_MULT)
from buffs import apply_buffs, make_buff


BASE_ENEMIES = [
    {"name": "Страж Бездны", "health": 50, "attack": 15, "defense": 10, "exp": 50, "gold": 25,
     "description": "Могучий страж, охраняющий врата Хроноспирали."},
    {"name": "Небесный Каратель", "health": 40, "attack": 20, "defense": 5, "exp": 60, "gold": 30,
     "description": "Крылатый воин, несущий гнев богов."},
    {"name": "Хранитель Времени", "health": 60, "attack": 12, "defense": 15, "exp": 70, "gold": 35,
     "description": "Древнее существо, контролирующее потоки времени."},
    {"name": "Бог Хронос", "health": 200, "attack": 30, "defense": 20, "exp": 500, "gold": 500,
     "description": "Верховный бог времени."},
    {"name": "Первозданный Хаос", "health": 400, "attack": 50, "defense": 30, "exp": 2000, "gold": 666,
     "description": "Существо, существовавшее до рождения времени."},
]


class Enemy:
    def __init__(self, index: int, difficulty: str):
        template = BASE_ENEMIES[index]
        mult = DIFFICULTY_MULTIPLIERS[difficulty]

        self.index = index
        self.name = template["name"]
        self.max_health = int(template["health"] * mult["enemy_health"])
        self.health = self.max_health
        self.base_attack = int(template["attack"] * mult["enemy_attack"])
        self.attack = self.base_attack
        self.defense = int(template["defense"] * mult["enemy_defense"])
        self.exp = int(template["exp"] * mult["exp_gain"])
        self.gold = template["gold"]
        self.description = template["description"]
        self.buffs = []

        self.is_chaos = (index == 4)
        self.second_phase_activated = False

    def take_damage(self, amount: int):
        self.health = max(0, self.health - amount)

    def is_alive(self) -> bool:
        return self.health > 0

    def effective_attack(self) -> float:
        return apply_buffs(self, "attack_mult", self.attack)

    def add_buff(self, key: str):
        for b in self.buffs:
            if b.key == key:
                b.duration = make_buff(key).duration
                return
        self.buffs.append(make_buff(key))

    def tick_buffs(self):
        self.buffs = [b for b in self.buffs if b.tick()]

    def clear_buffs(self):
        self.buffs = []

    def activate_chaos_second_phase(self):
        if self.second_phase_activated:
            return
        self.max_health = int(self.max_health * CHAOS_PHASE2_HP_MULT)
        self.health = self.max_health
        self.attack = int(self.base_attack * CHAOS_PHASE2_ATTACK_MULT)
        self.defense = int(self.defense * CHAOS_PHASE2_DEFENSE_MULT)
        self.name = "Пробужденный Первозданный Хаос"
        self.second_phase_activated = True