"""Класс Player"""
from config import (DIFFICULTY_MULTIPLIERS, CLASS_BASE_STATS, CLASS_STARTING_ITEMS,
                    EXP_BASE, EXP_GROWTH, STAT_POINTS_PER_LEVEL, HEALTH_PER_LEVEL,
                    STARTING_GOLD)
from items import get_item
from buffs import make_buff, apply_buffs


class Player:
    def __init__(self, name: str, class_name: str, difficulty: str):
        self.name = name
        self.class_name = class_name
        self.difficulty = difficulty
        mult = DIFFICULTY_MULTIPLIERS[difficulty]

        base = CLASS_BASE_STATS[class_name]
        self.max_health = int(base["health"] * mult["player_health"])
        self.health = self.max_health
        self.base_attack = int(base["attack"] * mult["player_attack"])
        self.base_defense = int(base["defense"] * mult["player_defense"])
        self.base_dodge = base["dodge"]

        self.level = 1
        self.exp = 0
        self.exp_to_next = EXP_BASE
        self.stat_points = 0
        self.gold = STARTING_GOLD

        self.weapon = None
        self.armor = None
        self.inventory = []
        self.buffs = []

        starting = CLASS_STARTING_ITEMS[class_name]
        if starting["weapon"]:
            self.weapon = get_item(starting["weapon"])
        if starting["armor"]:
            self.armor = get_item(starting["armor"])
        for key in starting["inventory"]:
            self.inventory.append(get_item(key))

    # Характеристики
    def total_attack(self) -> int:
        bonus = self.weapon["value"] if self.weapon else 0
        return self.base_attack + bonus

    def total_defense(self) -> int:
        bonus = self.armor["value"] if self.armor and self.armor["effect"] == "defense" else 0
        return self.base_defense + bonus

    def total_dodge(self) -> int:
        bonus = self.armor["value"] if self.armor and self.armor["effect"] == "dodge" else 0
        return self.base_dodge + bonus

    def effective_attack(self) -> float:
        return apply_buffs(self, "attack_mult", self.total_attack())

    def effective_defense(self) -> float:
        return apply_buffs(self, "defense_mult", self.total_defense())

    # Баффы
    def add_buff(self, key: str):
        # Обновление длительности повторяющихся баффов
        for b in self.buffs:
            if b.key == key:
                b.duration = make_buff(key).duration
                return
        self.buffs.append(make_buff(key))

    def tick_buffs(self):
        self.buffs = [b for b in self.buffs if b.tick()]

    def is_invulnerable(self) -> bool:
        return any(b.effect == "invulnerable" for b in self.buffs)

    # Здоровье
    def take_damage(self, amount: int):
        self.health = max(0, self.health - amount)

    def heal(self, amount: int) -> int:
        before = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - before

    def is_alive(self) -> bool:
        return self.health > 0

    # Прогрессия
    def add_exp(self, amount: int) -> bool:
        self.exp += amount
        leveled = False
        while self.exp >= self.exp_to_next:
            self.exp -= self.exp_to_next
            self.exp_to_next = int(self.exp_to_next * EXP_GROWTH)
            self.level += 1
            self.max_health += HEALTH_PER_LEVEL
            self.health = self.max_health
            self.stat_points += STAT_POINTS_PER_LEVEL
            leveled = True
        return leveled

    def add_gold(self, amount: int):
        self.gold += amount

    # Инвентарь
    def equip(self, item: dict):
        if item["type"] == "оружие":
            if self.weapon:
                self.inventory.append(self.weapon)
            self.weapon = item
            self.inventory.remove(item)
        elif item["type"] == "броня":
            if self.armor:
                self.inventory.append(self.armor)
            self.armor = item
            self.inventory.remove(item)

    def spend_stat_point(self, choice: str) -> bool:
        if self.stat_points <= 0:
            return False
        if choice == "1":
            self.max_health += 10
            self.health += 10
        elif choice == "2":
            self.base_attack += 5
        elif choice == "3":
            self.base_defense += 5
        elif choice == "4":
            self.base_dodge += 2
        else:
            return False
        self.stat_points -= 1
        return True