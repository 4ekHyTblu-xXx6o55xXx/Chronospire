"""Весь визуал игры через rich."""
import time
import random
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
import os

os.system("")

console = Console(force_terminal=True, legacy_windows=False)


def clear():
    """Очищает экран через ANSI"""
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def print_slow(text: str, min_delay: float = 0.02, max_delay: float = 0.05,
               typing_errors: bool = True, color: str = None):
    """
    Медленный вывод текста с опечатками. Использует sys.stdout для корректной
    работы backspace (эффект стирания опечатки).
    """
    ansi_colors = {
        None: "",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "bold red": "\033[1;91m",
        "bold green": "\033[1;92m",
        "bold yellow": "\033[1;93m",
        "bold magenta": "\033[1;95m",
        "bold cyan": "\033[1;96m",
        "italic": "\033[3m",
        "dim": "\033[2m",
    }
    RESET = "\033[0m"

    color_code = ansi_colors.get(color, "")

    punctuation_delays = {
        '.': (0.3, 0.6), '!': (0.3, 0.6), '?': (0.3, 0.6),
        ',': (0.1, 0.3), ';': (0.2, 0.4), ':': (0.2, 0.4), '\n': (0.1, 0.3),
    }

    error_chars = {
        'а': 'фы', 'б': 'ьн', 'в': 'фцы', 'г': 'ьр', 'д': 'ыл',
        'е': 'ку', 'ё': 'ку', 'ж': 'эд', 'з': 'ьх', 'и': 'цу',
        'й': 'цы', 'к': 'ен', 'л': 'др', 'м': 'ьт', 'н': 'гк',
        'о': 'лп', 'п': 'ол', 'р': 'кг', 'с': 'вы', 'т': 'ьм',
        'у': 'ге', 'ф': 'яы', 'х': 'чз', 'ц': 'ув', 'ч': 'сх',
        'ш': 'щэ', 'щ': 'шэ', 'ъ': 'эю', 'ы': 'ва', 'ь': 'бю',
        'э': 'ъю', 'ю': 'ъэ', 'я': 'фч',
    }

    if color_code:
        sys.stdout.write(color_code)
        sys.stdout.flush()

    i = 0
    while i < len(text):
        char = text[i]

        # Симуляция опечатки
        if typing_errors and char.isalpha() and random.random() < 0.05 and i < len(text) - 1:
            if char.lower() in error_chars:
                error_char = random.choice(error_chars[char.lower()])
                # Печатаем неправильный символ
                sys.stdout.write(error_char)
                sys.stdout.flush()
                time.sleep(random.uniform(0.05, 0.1))
                # Стираем: backspace, пробел, backspace
                sys.stdout.write("\b \b")
                sys.stdout.flush()
                time.sleep(0.05)

        # Печатаем правильный символ
        sys.stdout.write(char)
        sys.stdout.flush()

        # Задержки
        if char in punctuation_delays:
            delay_min, delay_max = punctuation_delays[char]
            delay = random.uniform(delay_min, delay_max)
        elif char == ' ':
            delay = random.uniform(0.1, 0.3) if random.random() < 0.3 else random.uniform(min_delay, max_delay)
        else:
            delay = random.uniform(min_delay, max_delay)
            if char.isalpha() and random.random() < 0.1:
                delay *= random.uniform(1.5, 3.0)

        time.sleep(delay)
        i += 1

    if color_code:
        sys.stdout.write(RESET)
    sys.stdout.write("\n")
    sys.stdout.flush()


def show_title():
    """Заголовок игры."""
    clear()
    console.print()
    console.print(Align.center("[bold magenta]ХРОНОСПИРАЛЬ[/bold magenta]"))
    console.print(Align.center("[italic cyan]Эпическая сага о мести богам времени[/italic cyan]"))
    console.print()
    console.print(Align.center("[dim]" + "─" * 40 + "[/dim]"))
    console.print()


def show_intro():
    """Сюжетное вступление"""
    intro_lines = [
        "Давным-давно боги времени установили свое владычество.",
        "Они играли судьбами смертных, как пешками.",
        "Но однажды они уничтожили всё, что ты любил.",
        "Теперь ты поднимаешься по Хроноспирали, чтобы отомстить.",
        "Судьба вселенной висит на волоске...",
    ]
    for line in intro_lines:
        print_slow(line, min_delay=0.015, max_delay=0.04, typing_errors=True)
        time.sleep(0.3)
    console.print()


def health_bar(current: int, maximum: int, width: int = 30) -> Text:
    """Цветной прогресс-бар здоровья"""
    if maximum <= 0:
        maximum = 1
    ratio = max(0.0, min(1.0, current / maximum))
    filled = int(width * ratio)
    if ratio > 0.5:
        color = "green"
    elif ratio > 0.25:
        color = "yellow"
    else:
        color = "red"
    bar = Text()
    bar.append("█" * filled, style=color)
    bar.append("░" * (width - filled), style="dim")
    bar.append(f" {current}/{maximum}")
    return bar


def show_player_stats(player):
    """Карточка игрока"""
    table = Table(title=f"📜 {player.name} — {player.class_name}",
                  border_style="cyan", show_header=False)
    table.add_row("Уровень", str(player.level))
    table.add_row("Опыт", f"{player.exp}/{player.exp_to_next}")
    table.add_row("Здоровье", health_bar(player.health, player.max_health))
    table.add_row("Атака", str(player.total_attack()))
    table.add_row("Защита", str(player.total_defense()))
    table.add_row("Уклонение", f"{player.total_dodge()}%")
    table.add_row("Золото", f"{player.gold} 💰")
    table.add_row("Очки", str(player.stat_points))
    table.add_row("Оружие", player.weapon["name"] if player.weapon else "нет")
    table.add_row("Броня", player.armor["name"] if player.armor else "нет")
    if player.buffs:
        buffs_str = " | ".join(f"{b.name} ({b.duration})" for b in player.buffs)
        table.add_row("Баффы", buffs_str)
    console.print(table)


def show_enemy_stats(enemy):
    """Карточка врага"""
    table = Table(title=f"⚔ {enemy.name}", border_style="red", show_header=False)
    table.add_row("Здоровье", health_bar(enemy.health, enemy.max_health))
    table.add_row("Атака", str(int(enemy.effective_attack())))
    table.add_row("Защита", str(enemy.defense))
    if enemy.buffs:
        buffs_str = " | ".join(f"{b.name} ({b.duration})" for b in enemy.buffs)
        table.add_row("Баффы", buffs_str)
    console.print(table)


def show_inventory(player):
    """Отображает инвентарь игрока"""
    if not player.inventory:
        console.print("[yellow]Инвентарь пуст.[/yellow]")
        return
    table = Table(title="🎒 Инвентарь", border_style="yellow")
    table.add_column("#", justify="right")
    table.add_column("Название", style="bright_white")
    table.add_column("Описание", style="dim")
    for i, item in enumerate(player.inventory, 1):
        table.add_row(str(i), item["name"], item["description"])
    console.print(table)

def analyze_battle(player, enemy):
    """Анализ боя:"""
    from math import ceil

    # Урон игрока за ход
    player_dmg = max(1, int(player.effective_attack()) - enemy.defense // 2)

    # Урон врага с учётом уклонения и неуязвимости
    if player.is_invulnerable():
        enemy_dmg = 0.0
    else:
        raw = max(1, int(enemy.effective_attack()) - int(player.effective_defense()) // 2)
        enemy_dmg = raw * (1 - player.total_dodge() / 100)

    # Сколько ходов нужно каждому
    turns_to_kill = ceil(enemy.health / player_dmg) if player_dmg > 0 else 999
    turns_to_die = ceil(player.health / enemy_dmg) if enemy_dmg > 0 else 999

    # Прогноз
    diff = turns_to_die - turns_to_kill
    if diff >= 3:
        forecast = "[bold green]✅ УВЕРЕННАЯ ПОБЕДА[/bold green]"
    elif diff >= 1:
        forecast = "[bold yellow]⚠️ НА ГРАНИ — нужна тактика[/bold yellow]"
    elif diff == 0:
        forecast = "[bold red]🔥 РИСКОВАННЫЙ БОЙ — решит один ход[/bold red]"
    else:
        forecast = "[bold red]💀 ВЫСОКИЙ РИСК ПОРАЖЕНИЯ[/bold red]"

    # Собираем таблицу
    table = Table(title="📊 АНАЛИЗ БОЯ", border_style="blue")
    table.add_column("Параметр", style="cyan")
    table.add_column("Значение", style="white")
    table.add_row("Твой урон за ход", f"{player_dmg}")
    table.add_row("Урон врага за ход",
                  f"{enemy_dmg:.1f}" + (" [cyan](неуязвимость!)[/cyan]" if player.is_invulnerable() else ""))
    table.add_row("Ты убьёшь его за", f"{turns_to_kill} ход(ов)")
    table.add_row("Он убьёт тебя за", f"{turns_to_die} ход(ов)")
    table.add_row("Прогноз", forecast)
    console.print(table)