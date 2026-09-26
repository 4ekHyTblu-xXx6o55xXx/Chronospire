"""Система временных эффектов"""
from dataclasses import dataclass, field

@dataclass
class Buff:
    key: str
    name: str
    duration: int
    effect: str
    value: float = 0.0
    description: str = ""

    def tick(self) -> bool:
        self.duration -= 1
        return self.duration > 0

BUFF_TEMPLATES = {
    "rage":         Buff("rage", "🔥 Ярость",         3, "attack_mult",   2.0,
                         "+100% к атаке"),
    "invulnerable": Buff("invulnerable", "🛡️ Неуязвимость", 2, "invulnerable", 1.0,
                         "Полный иммунитет к урону"),
    "stone_skin":   Buff("stone_skin", "🪨 Каменная кожа",  3, "defense_mult",  1.5,
                         "+50% к защите"),
    "weakened":     Buff("weakened",   "💫 Ослабление",      3, "attack_mult",   0.5,
                         "-50% к атаке"),
}


def make_buff(key: str) -> Buff:
    """Создает копию баффа из шаблона."""
    template = BUFF_TEMPLATES[key]
    return Buff(template.key, template.name, template.duration,
                template.effect, template.value, template.description)


def apply_buffs(entity, effect_type: str, base_value: float) -> float:
    """Применяет все активные баффы entity к базовому значению"""
    result = base_value
    for buff in getattr(entity, "buffs", []):
        if buff.effect == effect_type:
            if effect_type in ("attack_mult", "defense_mult"):
                result *= buff.value
    return result