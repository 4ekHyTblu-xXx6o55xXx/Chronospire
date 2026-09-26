"""Логика боя."""
import random
import time
from config import CRIT_CHANCE, CRIT_MULTIPLIER
from items import get_item
from buffs import make_buff
from ui import (console, clear, print_slow, show_player_stats, show_enemy_stats,
                show_inventory, health_bar, clear, analyze_battle)
from rich.panel import Panel


def player_turn(player, enemy):
    """Возвращает: 'attack' (ход врага), 'item' (не тратит ход), 'inspect' (не тратит ход), 'skip' (ход врага)."""
    console.print("\n[bold cyan]Ваш ход:[/bold cyan]")
    console.print(" [1] Атаковать")
    console.print(" [2] Использовать предмет")
    console.print(" [3] Анализ боя (прогноз)")

    choice = input("Ваш выбор: ").strip()

    if choice == "1":
        crit = random.randint(1, 100) <= CRIT_CHANCE
        damage = int(player.effective_attack()) + random.randint(0, 5)
        if crit:
            damage = int(damage * CRIT_MULTIPLIER)
            console.print("[bold red]💥 Критический удар![/bold red]")
        final = max(1, damage - enemy.defense // 2)
        enemy.take_damage(final)
        console.print(f"Вы нанесли [red]{final}[/red] урона!")
        return "attack"
    elif choice == "2":
        if use_item_in_battle(player, enemy):
            return "item"
        return "inspect"
    elif choice == "3":
        analyze_battle(player, enemy)
        input("\nНажмите Enter чтобы продолжить...")
        return "inspect"
    else:
        console.print("[yellow]Неверный выбор, ход пропущен.[/yellow]")
        return "skip"


def use_item_in_battle(player, enemy) -> bool:
    show_inventory(player)
    if not player.inventory:
        return False
    try:
        choice = int(input("Выберите предмет (0 для отмены): "))
        if choice == 0:
            return False
        if not (1 <= choice <= len(player.inventory)):
            console.print("[red]Неверный номер.[/red]")
            return False
    except ValueError:
        return False

    item = player.inventory[choice - 1]
    if item["type"] != "зелье":
        console.print("[yellow]Этот предмет нельзя использовать в бою.[/yellow]")
        return False

    effect = item["effect"]
    if effect == "heal":
        healed = player.heal(item["value"])
        console.print(f"[green]Восстановлено {healed} HP.[/green]")
    elif effect == "attack":
        player.base_attack += item["value"]
        console.print(f"[green]Атака +{item['value']} до конца боя.[/green]")
    elif effect == "buff_rage":
        player.add_buff("rage")
        console.print("[bold red]🔥 Ярость активирована! +100% атаки на 3 хода.[/bold red]")
    elif effect == "buff_invuln":
        player.add_buff("invulnerable")
        console.print("[bold cyan]🛡️ Неуязвимость активирована! 2 хода.[/bold cyan]")
    elif effect == "dispel":
        enemy.clear_buffs()
        console.print("[bold magenta]✨ Свиток времени снял все баффы с врага![/bold magenta]")

    player.inventory.remove(item)
    return True


def enemy_turn(player, enemy):
    if not enemy.is_alive():
        return
    console.print(f"\n[bold red]{enemy.name} атакует...[/bold red]")
    time.sleep(0.7)

    # Проверка уклонения
    if random.randint(1, 100) <= player.total_dodge():
        console.print("[cyan]💨 Вы уклонились![/cyan]")
        return

    # Проверка неуязвимости
    if player.is_invulnerable():
        console.print("[bold cyan]🛡️ Неуязвимость поглотила удар![/bold cyan]")
        return

    damage = max(1, int(enemy.effective_attack()) - int(player.effective_defense()) // 2)
    player.take_damage(damage)
    console.print(f"Вы получили [red]{damage}[/red] урона!")


def battle(player, enemy) -> bool:
    """Проводит бой. Возвращает True, если игрок победил."""
    console.print(Panel.fit(
        f"[bold red]⚔ БОЙ С {enemy.name.upper()} ⚔[/bold red]\n[italic]{enemy.description}[/italic]",
        border_style="red"
    ))

    while player.is_alive() and enemy.is_alive():
        # Отображение состояния
        clear()
        console.print()
        show_player_stats(player)
        show_enemy_stats(enemy)

        # Проверка 2-й фазы Хаоса
        if (enemy.is_chaos and not enemy.second_phase_activated
                and enemy.health <= enemy.max_health * 0.5):
            print_slow("Что-то изменилось... Реальность искажается.",
                       color="bold magenta", typing_errors=False)
            print_slow("'Ты видел лишь тень моей силы...'",
                       color="italic", typing_errors=False)
            enemy.activate_chaos_second_phase()
            console.print("[bold red]💀 ХАОС ПРОБУДИЛСЯ![/bold red]")
            time.sleep(1.5)

        # Ход игрока
        action = player_turn(player, enemy)
        if not enemy.is_alive():
            break
        if action in ("item", "inspect"):
            continue

        # Тик баффов игрока
        player.tick_buffs()

        # Ход врага
        enemy_turn(player, enemy)
        enemy.tick_buffs()

    if not player.is_alive():
        return False

    console.print(Panel.fit(
        f"[bold green]🎉 Победа! {enemy.name} повержен![/bold green]",
        border_style="green"
    ))
    return True