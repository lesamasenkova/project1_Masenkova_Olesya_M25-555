#!/usr/bin/env python3

from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    solve_puzzle,
)


def show_help(commands):
    """Отображает список доступных команд."""
    print("Доступные команды:")
    for cmd, desc in commands.items():
        print(f"  {cmd}: {desc}")


def process_command(game_state, command):
    """Обрабатывает ввод пользователя и вызывает действия."""
    parts = command.strip().lower().split(maxsplit=1)
    cmd = parts[0] if parts else ""
    arg = parts[1] if len(parts) > 1 else None

    directions = {"north", "south", "east", "west"}

    # Если направление введено без 'go'
    if cmd in directions:
        move_player(game_state, cmd)
        return

    match cmd:
        case "look" | "l":
            describe_current_room(game_state)
        case "go" | "move":
            if arg:
                move_player(game_state, arg)
            else:
                print("Укажите направление для команды 'go'.")
        case "take" | "get":
            if arg:
                take_item(game_state, arg)
            else:
                print("Укажите предмет для команды 'take'.")
        case "inventory" | "inv":
            show_inventory(game_state)
        case "solve":
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "quit" | "exit":
            game_state["game_over"] = True
            print("Игра завершена.")
        case "help":
            show_help(COMMANDS)
        case _:
            print(f"Неизвестная команда: {cmd}")


def main():
    """Точка входа в игру. Основной игровой цикл."""
    game_state = {
        "current_room": "entrance",
        "player_inventory": [],
        "steps": 0,
        "game_over": False,
    }
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)
    while not game_state["game_over"]:
        command = get_input("> ")
        process_command(game_state, command)


if __name__ == "__main__":
    main()

