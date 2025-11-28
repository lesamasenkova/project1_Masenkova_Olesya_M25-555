from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import random_event


def show_inventory(game_state):
    """Показывает инвентарь игрока."""
    inventory = game_state.get("player_inventory", [])
    if inventory:
        print("Инвентарь игрока:")
        for item in inventory:
            print(f"- {item}")
    else:
        print("Ваш инвентарь пуст.")


def get_input(prompt="> "):
    """Считывает ввод пользователя, обрабатывает выход по Ctrl+C и Ctrl+D."""
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state, direction):
    """Перемещает игрока в новое помещение с возможными событиями."""
    current_room_key = game_state["current_room"]
    room = ROOMS[current_room_key]
    exits = room.get("exits", {})

    if direction in exits:
        next_room = exits[direction]
        if next_room == "treasure_room":
            if "rusty_key" in game_state.get("player_inventory", []):
                print(
                    "Вы используете найденный ключ, чтобы открыть путь "
                    "в комнату сокровищ."
                )
                game_state["current_room"] = next_room
                game_state["steps"] = game_state.get("steps", 0) + 1
                new_room = ROOMS[next_room]
                print(new_room["description"])
                random_event(game_state)
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
        else:
            game_state["current_room"] = next_room
            game_state["steps"] = game_state.get("steps", 0) + 1
            new_room = ROOMS[next_room]
            print(f"Вы переместились в комнату: {next_room.upper()}")
            print(new_room["description"])
            random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    """Позволяет игроку подобрать предмет из текущей комнаты."""
    current_room_key = game_state["current_room"]
    room = ROOMS[current_room_key]
    items = room.get("items", [])
    if item_name in items:
        game_state.setdefault("player_inventory", []).append(item_name)
        items.remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    """Обрабатывает использование предмета из инвентаря."""
    inventory = game_state.get("player_inventory", [])
    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    match item_name:
        case "torch":
            print("Вы зажгли факел, вокруг стало светлее.")
        case "sword":
            print("Вы крепко схватили меч и чувствуете уверенность в бою.")
        case "bronze_box":
            print("Вы открыли бронзовую шкатулку.")
            if "rusty_key" not in inventory:
                inventory.append("rusty_key")
            print("Внутри вы нашли ржавый ключ и положили его в инвентарь.")
        case _:
            print("Вы не знаете, как использовать этот предмет.")




