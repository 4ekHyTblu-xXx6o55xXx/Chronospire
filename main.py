"""Главный файл игры. Запуск: python main.py"""
import random
import time
import sys

from config import GAME_TITLE, DIFFICULTY_CHOICES, CLASS_BASE_STATS
from items import get_item
from player import Player
from enemy import Enemy
from locations import LOCATIONS
from battle import battle
from ui import (console, clear, print_slow, show_title, show_intro,
                show_player_stats, show_inventory, health_bar)
from rich.panel import Panel
from rich.table import Table
import music


# Меню

def choose_difficulty() -> str:
    clear()
    console.print(Panel.fit("[bold]ВЫБОР СЛОЖНОСТИ[/bold]", border_style="magenta"))
    options = [
        ("1", "Лёгкая",      "для начинающих"),
        ("2", "Средняя",     "сбалансированная"),
        ("3", "Сложная",     "испытание"),
        ("4", "Безумная",    "экстрим"),
        ("5", "Невозможная", "для мастеров (+ скрытый босс)"),
    ]
    for k, name, desc in options:
        console.print(f" [{k}] [bold]{name}[/bold] — {desc}")
    while True:
        choice = input("\nВаш выбор (1-5): ").strip()
        if choice in DIFFICULTY_CHOICES:
            return DIFFICULTY_CHOICES[choice]
        console.print("[red]Неверный выбор![/red]")


def create_character(difficulty: str) -> Player:
    clear()
    console.print(Panel.fit("[bold]СОЗДАНИЕ ПЕРСОНАЖА[/bold]", border_style="cyan"))
    while True:
        name = input("Имя героя: ").strip()
        if name:
            break
        console.print("[red]Имя не может быть пустым![/red]")

    console.print("\n[bold]Доступные классы:[/bold]")
    classes = list(CLASS_BASE_STATS.keys())
    for i, cls in enumerate(classes, 1):
        stats = CLASS_BASE_STATS[cls]
        console.print(f" [{i}] [bold]{cls}[/bold] — HP {stats['health']}, АТК {stats['attack']}, "
                      f"ЗАЩ {stats['defense']}, УКЛ {stats['dodge']}%")

    while True:
        choice = input("\nВыбор класса (1-3): ").strip()
        if choice in ("1", "2", "3"):
            class_name = classes[int(choice) - 1]
            break
        console.print("[red]Неверный выбор![/red]")

    player = Player(name, class_name, difficulty)
    console.print(f"\n[green]Создан персонаж: {player.name} — {player.class_name}[/green]")
    show_player_stats(player)
    input("\nНажмите Enter чтобы продолжить...")
    return player


# Магазин

SHOP_ITEMS = [
    "зелье_здоровья", "зелье_силы", "эликсир_богов",
    "зелье_ярости", "зелье_неуязвимости", "свиток_времени",
    "меч_воина", "посох_мага", "кольцо_могущества", "артефакт_хаоса",
    "щит_защиты", "плащ_теней", "панцирь_титана",
]


def shop(player: Player):
    while True:
        clear()
        console.print(Panel.fit(f"[bold yellow]🏪 МАГАЗИН[/bold yellow]\nЗолото: {player.gold} 💰",
                                border_style="yellow"))
        table = Table(border_style="yellow")
        table.add_column("#", justify="right")
        table.add_column("Название", style="bright_white")
        table.add_column("Цена", style="yellow")
        table.add_column("Описание", style="dim")
        for i, key in enumerate(SHOP_ITEMS, 1):
            item = get_item(key)
            table.add_row(str(i), item["name"], f"{item['price']}💰", item["description"])
        console.print(table)
        console.print(" [0] Выйти")

        try:
            choice = int(input("\nВыбор: ").strip())
        except ValueError:
            continue
        if choice == 0:
            return
        if 1 <= choice <= len(SHOP_ITEMS):
            item = get_item(SHOP_ITEMS[choice - 1])
            if player.gold >= item["price"]:
                player.gold -= item["price"]
                player.inventory.append(item)
                console.print(f"[green]Куплено: {item['name']}[/green]")
            else:
                console.print("[red]Недостаточно золота![/red]")
            input("Enter...")
        else:
            console.print("[red]Неверный выбор![/red]")


# Сундуки с лутом

def open_chest(player: Player, bonus: bool = False):
    owned_names = {i["name"] for i in player.inventory}
    if player.weapon:
        owned_names.add(player.weapon["name"])
    if player.armor:
        owned_names.add(player.armor["name"])

    available = [k for k in SHOP_ITEMS if get_item(k)["name"] not in owned_names]

    console.print(Panel.fit("[bold yellow]📦 СУНДУК[/bold yellow]", border_style="yellow"))

    if not available:
        gold = random.randint(100, 300) if not bonus else random.randint(50, 150)
        player.add_gold(gold)
        console.print(f"Найдено [yellow]{gold}[/yellow] золота!")
        return

    key = random.choice(available)
    item = get_item(key)
    player.inventory.append(item)
    console.print(f"Найден предмет: [bold]{item['name']}[/bold] — {item['description']}")

    gold = random.randint(50, 200) if not bonus else random.randint(25, 100)
    player.add_gold(gold)
    console.print(f"И [yellow]{gold}[/yellow] золота!")


# Распределение очков

def distribute_points(player: Player):
    while player.stat_points > 0:
        show_player_stats(player)
        console.print(f"\nОсталось очков: [yellow]{player.stat_points}[/yellow]")
        console.print(" [1] +10 HP")
        console.print(" [2] +5 Атака")
        console.print(" [3] +5 Защита")
        console.print(" [4] +2% Уклонение")
        console.print(" [5] Отложить")
        choice = input("Выбор: ").strip()
        if choice == "5":
            return
        if player.spend_stat_point(choice):
            console.print("[green]Улучшение применено![/green]")
        else:
            console.print("[red]Неверный выбор![/red]")


# Экипировка

def equip_menu(player: Player):
    equippable = [(i, item) for i, item in enumerate(player.inventory)
                  if item["type"] in ("оружие", "броня")]
    if not equippable:
        console.print("[yellow]Нет предметов для экипировки.[/yellow]")
        return
    show_inventory(player)
    console.print("[dim]Выберите номер предмета из инвентаря для экипировки[/dim]")
    try:
        choice = int(input("Номер (0 — отмена): ").strip())
    except ValueError:
        return
    if choice == 0 or not (1 <= choice <= len(player.inventory)):
        return
    item = player.inventory[choice - 1]
    if item["type"] in ("оружие", "броня"):
        player.equip(item)
        console.print(f"[green]Экипировано: {item['name']}[/green]")
    else:
        console.print("[yellow]Этот предмет нельзя экипировать.[/yellow]")


# Юз предметов вне боя

def use_item_menu(player: Player):
    show_inventory(player)
    if not player.inventory:
        return
    try:
        choice = int(input("Номер (0 — отмена): ").strip())
    except ValueError:
        return
    if choice == 0 or not (1 <= choice <= len(player.inventory)):
        return
    item = player.inventory[choice - 1]
    if item["type"] != "зелье":
        console.print("[yellow]Это не зелье.[/yellow]")
        return
    if item["effect"] == "heal":
        healed = player.heal(item["value"])
        console.print(f"[green]Восстановлено {healed} HP.[/green]")
        player.inventory.remove(item)
    else:
        console.print("[yellow]Это зелье можно использовать только в бою.[/yellow]")


# Локации

def explore_location(player: Player, index: int, visited: list, flags: dict) -> str:
    """Возвращает: 'continue', 'victory', 'hidden_victory', 'dead'."""
    loc = LOCATIONS[index]
    clear()
    console.print(Panel.fit(
        f"[bold cyan]{loc['name']}[/bold cyan]\n\n[italic]{loc['description']}[/italic]",
        border_style="cyan"
    ))

    if loc.get("required_difficulty") and player.difficulty != loc["required_difficulty"]:
        console.print("[red]Эта локация недоступна на вашей сложности.[/red]")
        input("Enter...")
        return "continue"

    # Повторный визит
    if visited[index] and loc["type"] not in ("отдых", "финальный бой", "скрытый бой"):
        if random.random() < 0.3:
            console.print("[yellow]Бонусный сундук![/yellow]")
            open_chest(player, bonus=True)
        else:
            console.print("[dim]Здесь больше нечего делать.[/dim]")
        input("Enter...")
        return "continue"

    visited[index] = True

    if loc["type"] == "бой":
        mapping = {0: 0, 2: 1, 4: 2}
        enemy_idx = mapping.get(index, 0)
        music.play("battle")
        enemy = Enemy(enemy_idx, player.difficulty)
        music.play("battle")
        won = battle(player, enemy)
        music.play("calm")
        if not won:
            return "dead"
        player.add_gold(enemy.gold)
        leveled = player.add_exp(enemy.exp)
        console.print(f"[green]+{enemy.exp} опыта[/green]")
        if leveled:
            console.print(f"[bold yellow]🎉 Новый уровень: {player.level}![/bold yellow]")
        input("Enter...")
        return "continue"

    elif loc["type"] == "сундук":
        open_chest(player)
        input("Enter...")
        return "continue"

    elif loc["type"] == "отдых":
        healed = player.heal(player.max_health // 2)
        console.print(f"[green]Вы отдохнули. +{healed} HP.[/green]")
        input("Enter...")
        return "continue"

    elif loc["type"] == "финальный бой":
        if flags.get("chronos_defeated"):
            console.print("[dim]Хронос уже повержен.[/dim]")
            input("Enter...")
            return "continue"
        print_slow("Вы достигли Престола Хроноса. Перед вами — бог времени!")
        music.play("battle")
        won = battle(player, Enemy(3, player.difficulty))
        if not won:
            return "dead"
        flags["chronos_defeated"] = True
        music.play("calm")
        player.add_exp(Enemy(3, player.difficulty).exp)
        player.add_gold(Enemy(3, player.difficulty).gold)
        if player.difficulty == "невозможная" and not flags.get("chaos_defeated"):
            console.print("[bold magenta]🌟 Открыто Измерение Забвения![/bold magenta]")
            input("Enter...")
            return "continue"
        return "victory"

    elif loc["type"] == "скрытый бой":
        if flags.get("chaos_defeated"):
            console.print("[dim]Хаос уже повержен.[/dim]")
            input("Enter...")
            return "continue"
        print_slow("Вы вошли в Измерение Забвения. Перед вами — Первозданный Хаос!")
        music.play("battle")
        won = battle(player, Enemy(4, player.difficulty))
        if not won:
            return "dead"
        flags["chaos_defeated"] = True
        music.play("calm")
        player.add_exp(Enemy(4, player.difficulty).exp)
        player.add_gold(Enemy(4, player.difficulty).gold)
        return "hidden_victory"

    return "continue"


# Перемещение

def travel_menu(player: Player, current_index: int, visited: list, flags: dict) -> int:
    while True:
        console.print("\n[bold]Куда идем?[/bold]")
        available = []
        if current_index < len(LOCATIONS) - 1:
            nxt = LOCATIONS[current_index + 1]
            if nxt["type"] == "скрытый бой":
                if player.difficulty == "невозможная" and flags.get("chronos_defeated"):
                    console.print(f" [1] → {nxt['name']} (скрытый босс)")
                    available.append(1)
            else:
                console.print(f" [1] → {nxt['name']}")
                available.append(1)
        if current_index > 0:
            console.print(f" [2] ← {LOCATIONS[current_index - 1]['name']}")
            available.append(2)
        console.print(" [3] Осмотреть локацию")
        console.print(" [4] Характеристики")
        console.print(" [5] Инвентарь → использовать")
        console.print(" [6] Инвентарь → экипировать")
        console.print(" [7] Распределить очки")
        console.print(" [8] Магазин")
        console.print(" [0] Выйти из игры")

        choice = input("Выбор: ").strip()

        if choice == "1" and 1 in available:
            return current_index + 1
        elif choice == "2" and 2 in available:
            return current_index - 1
        elif choice == "3":
            console.print(f"\n[italic]{LOCATIONS[current_index]['description']}[/italic]")
        elif choice == "4":
            show_player_stats(player)
        elif choice == "5":
            use_item_menu(player)
        elif choice == "6":
            equip_menu(player)
        elif choice == "7":
            distribute_points(player)
        elif choice == "8":
            shop(player)
        elif choice == "0":
            if input("Выйти? (y/n): ").lower() in ("y", "д"):
                return -1
        else:
            console.print("[red]Неверный выбор.[/red]")


# Концовки
def show_victory(player: Player):
    clear()
    console.print(Panel.fit("[bold green]★ ПОБЕДА! ★[/bold green]", border_style="green"))
    print_slow("Вы стоите над поверженным телом Хроноса.", color="green")
    print_slow("Боги времени пали. Время течет свободно.", color="green")
    print_slow(f"{player.name} вошел в легенду как спаситель вселенной!",
               color="bold green")


def show_hidden_victory(player: Player):
    clear()
    console.print(Panel.fit("[bold magenta]🌌 АБСОЛЮТНАЯ ПОБЕДА! 🌌[/bold magenta]", border_style="magenta"))
    print_slow("Вы победили не только богов, но и Первозданный Хаос.", color="magenta")
    print_slow(f"{player.name} — новый Повелитель Времени и Хаоса.",
               color="bold magenta")


def show_game_over():
    clear()
    console.print(Panel.fit("[bold red]ИГРА ОКОНЧЕНА[/bold red]", border_style="red"))
    print_slow("Вы пали в бою. Но память о вас не умрет.", color="red")

def main():
    music_ok = music.init_music()
    if music_ok:
        music.play("calm")

    clear()
    show_title()
    show_intro()

    input("\nНажмите Enter чтобы продолжить...")

    difficulty = choose_difficulty()
    player = create_character(difficulty)

    visited = [False] * len(LOCATIONS)
    flags = {}
    current = 0

    input("\nНажмите Enter чтобы начать путешествие...")

    while True:
        result = explore_location(player, current, visited, flags)
        if result == "dead":
            show_game_over()
            break
        if result == "victory":
            show_victory(player)
            break
        if result == "hidden_victory":
            show_hidden_victory(player)
            break

        current = travel_menu(player, current, visited, flags)
        if current == -1:
            console.print("[dim]Спасибо за игру![/dim]")
            break

    music.stop()
    input("\nНажмите Enter чтобы выйти...")


if __name__ == "__main__":
    main()