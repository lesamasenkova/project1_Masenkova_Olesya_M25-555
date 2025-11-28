import math

from labyrinth_game.constants import (
    EVENT_PROBABILITY,
    EVENT_TYPES_COUNT,
    ROOMS,
    TRAP_DEATH_THRESHOLD,
)


def describe_current_room(game_state):
    """Выводит описание текущей комнаты, предметов и выходов."""
    current_room_key = game_state['current_room']
    room = ROOMS[current_room_key]
    print(f"== {current_room_key.upper()} ==")
    print(room['description'])
    items = room.get('items', [])
    if items:
        print("Заметные предметы:")
        for item in items:
            print(f"- {item}")
    exits = room.get('exits', {})
    if exits:
        print("Выходы:")
        for direction in exits:
            print(f"- {direction}")
    if room.get('puzzle') is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    """Позволяет игроку попытаться разгадать загадку в комнате."""
    current_room = game_state['current_room']
    room = ROOMS[current_room]
    puzzle = room.get('puzzle')
    if puzzle is None:
        print("Загадок здесь нет.")
        return
    question, correct_answer = puzzle
    print(question)
    answer = input("Ваш ответ: ").strip().lower()
    # Альтернативные варианты ответов для загадок
    alternative_answers = {
        '10': ['десять'],
    }
    correct_answers = [correct_answer.lower()]
    if correct_answer.lower() in alternative_answers:
        correct_answers.extend(alternative_answers[correct_answer.lower()])
    if answer in correct_answers:
        print("Правильно! Вы решили загадку.")
        room['puzzle'] = None
        # Награда за решение загадки
        if current_room == 'hall':
            reward = 'treasure_key'
        elif current_room == 'trap_room':
            reward = 'torch'
        else:
            reward = 'mysterious_item'
        if reward not in game_state['player_inventory']:
            game_state['player_inventory'].append(reward)
            print(f"Вы получили предмет: {reward}")
    else:
        print("Неверно. Попробуйте снова.")
    if current_room == 'trap_room':
        trigger_trap(game_state)


def attempt_open_treasure(game_state):
    """Пробует открыть сундук с сокровищем в treasure_room."""
    current_room = game_state['current_room']
    if current_room != 'treasure_room':
        print("Здесь нет сундука для открытия.")
        return
    room = ROOMS[current_room]
    inventory = game_state.get('player_inventory', [])
    if 'treasure_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        if 'treasure_chest' in room['items']:
            room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return
    print("Сундук заперт. Для открытия нужно ввести код.")
    choice = input("Ввести код? (да/нет): ").strip().lower()
    if choice != 'да':
        print("Вы отступаете от сундука.")
        return
    code = input("Введите код: ").strip()
    puzzle = room.get('puzzle')
    if puzzle and code == puzzle[1]:
        print("Код верный! Сундук открыт!")
        if 'treasure_chest' in room['items']:
            room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
    else:
        print("Неверный код.")


def pseudo_random(seed, modulo):
    """Генерирует детерминированное псевдослучайное число для событий."""
    x = math.sin(seed * 12.9898)
    x = x * 43758.5453
    fractional_part = x - math.floor(x)
    result = int(fractional_part * modulo)
    return result


def trigger_trap(game_state):
    """Активирует ловушку в комнате."""
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state.get('player_inventory', [])
    if inventory:
        index = pseudo_random(game_state.get('steps', 0), len(inventory))
        lost_item = inventory.pop(index)
        print(f"Вы потеряли предмет: {lost_item}")
    else:
        damage_chance = pseudo_random(game_state.get('steps', 0), 10)
        if damage_chance < TRAP_DEATH_THRESHOLD:
            print("Вы получили смертельный урон от ловушки. Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вы уцелели после срабатывания ловушки.")


def random_event(game_state):
    """Проверяет вероятность случайного события после передвижения."""
    steps = game_state.get('steps', 0)
    # Пример: событие с вероятностью 1/10
    if pseudo_random(steps, EVENT_PROBABILITY) == 0:
        event_type = pseudo_random(steps, EVENT_TYPES_COUNT)
        current_room_key = game_state['current_room']
        inventory = game_state.get('player_inventory', [])
        room = ROOMS[current_room_key]
        if event_type == 0:
            print("Вы заметили на полу блестящую монетку.")
            if 'coin' not in room['items']:
                room['items'].append('coin')
        elif event_type == 1:
            print("Вы услышали шорох в темноте.")
            if 'sword' in inventory:
                print("Вы уверенно обнажили меч, и существо убежало.")
        elif event_type == 2:
            if current_room_key == 'trap_room' and 'torch' not in inventory:
                print("Внимание! В воздухе ощущается опасность...")
                trigger_trap(game_state)

