# labyrinth_game/constants.py

EVENT_PROBABILITY = 10
EVENT_TYPES_COUNT = 3
TRAP_DEATH_THRESHOLD = 3

ROOMS = {
    'entrance': {
        'description': (
            'Вы в темном входе лабиринта. Стены покрыты мхом. '
            'На полу лежит старый факел.'
        ),
        'exits': {'north': 'hall', 'east': 'trap_room'},
        'items': ['torch'],
        'puzzle': None
    },
    'hall': {
        'description': (
            'Большой зал с эхом. По центру пьедестала запечатанный сундук.'
        ),
        'exits': {
            'south': 'entrance',
            'west': 'library',
            'north': 'treasure_room',
            'east': 'trap_room'
        },
        'items': [],
        'puzzle': (
            'На пьедестале надпись: "Назовите число, которое идет '
            'после девяти". Введите ответ цифрой или словом.',
            '10'
        )
    },
    'trap_room': {
        'description': (
            'Комната с хитрой плиточной поломкой. '
            'На стене надпись: "Осторожно — ловушка".'
        ),
        'exits': {
            'west': 'entrance',
            'north': 'hall'
        },
        'items': ['rusty_key'],
        'puzzle': (
            'Система плит активна. Чтобы пройти, назовите слово "шаг" '
            'три раза подряд (введите "шаг шаг шаг")',
            'шаг шаг шаг'
        )
    },
    'library': {
        'description': (
            'Пыльная библиотека. На полках старые свитки. '
            'Где-то ключ от сокровищницы.'
        ),
        'exits': {
            'east': 'hall',
            'north': 'armory'
        },
        'items': ['ancient_book'],
        'puzzle': (
            'В одном свитке загадка: "Что растет, когда его съедают? '
            '(ответ одно слово)"',
            'резонанс'
        )
    },
    'armory': {
        'description': 'Старая оружейная. На стене меч и бронзовая шкатулка.',
        'exits': {
            'south': 'library',
            'north': 'secret_garden'
        },
        'items': ['sword', 'bronze_box'],
        'puzzle': None
    },
    'treasure_room': {
        'description': 'Комната с большим сундуком. Дверь заперта, нужен ключ.',
        'exits': {'south': 'hall'},
        'items': ['treasure_chest'],
        'puzzle': ('Дверь защищена кодом. (подсказка: 2*5= ? )', '10')
    },
    'secret_garden': {
        'description': 'Таинственный сад с цветами и амулетами.',
        'exits': {
            'south': 'armory',
            'east': 'fountain_room'
        },
        'items': ['magic_amulet', 'flower'],
        'puzzle': (
            'Табличка: "Какая буква в середине алфавита?" (русская)',
            'м'
        )
    },
    'fountain_room': {
        'description': 'Комната с фонтаном кристально чистой воды.',
        'exits': {'west': 'secret_garden'},
        'items': ['water_flask'],
        'puzzle': (
            'Фонтан дает загадку: "Что всегда движется, '
            'но никогда не покидает свое место?"',
            'время'
        )
    },
}

COMMANDS = {
    "go ": "перейти в направлении (north/south/east/west)",
    "look": "осмотреть текущую комнату",
    "take ": "поднять предмет",
    "use ": "использовать предмет из инвентаря",
    "inventory": "показать инвентарь",
    "solve": "попытаться решить загадку в комнате",
    "quit": "выйти из игры",
    "help": "показать это сообщение",
}

