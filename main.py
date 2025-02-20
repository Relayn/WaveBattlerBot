# src/bot_sea_battle.py
"""Телеграм-бот для игры в Морской Бой.

Этот скрипт реализует простую игру в Морской Бой, где пользователь играет против бота.
Игра ведётся на поле 10x10, корабли разных размеров размещаются случайным образом.
Пользователь и бот по очереди стреляют по полям друг друга, пока один из них не потопит все корабли противника.
"""

import telebot
import random
from typing import List, Tuple
import json

def load_config():
    try:
        with open('.venv/config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        config = {"BOT_TOKEN": "ваш_токен_бота"}
        with open('.venv/config.json', 'w') as f:
            json.dump(config, f, indent=4)
        return config

# Константы игры
config = load_config()
BOT_TOKEN = config['BOT_TOKEN']
BOARD_SIZE = 10  # Размер игрового поля
EMPTY, SHIP, HIT, MISS = '~', 'S', 'X', 'O'  # Символы для обозначения состояний клеток

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Игровые поля и списки кораблей
user_board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]  # Игровое поле пользователя
bot_board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]  # Игровое поле бота
user_ships = []  # Список размеров кораблей пользователя
bot_ships = []  # Список размеров кораблей бота

def create_board() -> List[List[str]]:
    """Создаёт новое пустое игровое поле.

    Returns:
        Двумерный список, представляющий игровое поле, заполненное символами EMPTY.
    """
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def display_board(board: List[List[str]]) -> str:
    """Генерирует строковое представление игрового поля.

    Args:
        board: Двумерный список, представляющий игровое поле.

    Returns:
        Строка для отображения поля.
    """
    header = "  " + " ".join(str(i + 1) for i in range(BOARD_SIZE)) + "\n"
    rows = "\n".join(
        chr(65 + i) + " " + " ".join(board[i]) for i in range(BOARD_SIZE)
    )
    return header + rows

def display_player_shots(board: List[List[str]]) -> str:
    """Генерирует строковое представление выстрелов игрока по полю бота.

    Скрывает корабли, показывая только попадания и промахи.

    Args:
        board: Двумерный список, представляющий поле бота.

    Returns:
        Строка для отображения выстрелов игрока.
    """
    header = "  " + " ".join(str(i + 1) for i in range(BOARD_SIZE)) + "\n"
    rows = "\n".join(
        chr(65 + i) + " " + " ".join(
            cell if cell in {HIT, MISS} else EMPTY for cell in row
        ) for i, row in enumerate(board)
    )
    return header + rows

def display_bot_shots(board: List[List[str]]) -> str:
    """Генерирует строковое представление выстрелов бота по полю игрока.

    Скрывает корабли, показывая только попадания и промахи.

    Args:
        board: Двумерный список, представляющий поле игрока.

    Returns:
        Строка для отображения выстрелов бота.
    """
    header = "  " + " ".join(str(i + 1) for i in range(BOARD_SIZE)) + "\n"
    rows = "\n".join(
        chr(65 + i) + " " + " ".join(
            cell if cell in {HIT, MISS} else EMPTY for cell in row
        ) for i, row in enumerate(board)
    )
    return header + rows

def place_ships(board: List[List[str]], ships: List[int]) -> None:
    """Размещает корабли на поле случайным образом.

    Args:
        board: Двумерный список, представляющий игровое поле.
        ships: Список целых чисел, представляющих размеры кораблей.
    """
    for ship in ships:
        placed = False
        while not placed:
            # Случайно выбираем начальную позицию и направление
            x = random.randint(0, BOARD_SIZE - 1)
            y = random.randint(0, BOARD_SIZE - 1)
            direction = random.choice(['horizontal', 'vertical'])
            if direction == 'horizontal' and y + ship <= BOARD_SIZE:
                # Проверяем возможность горизонтального размещения
                if all(board[x][y + i] == EMPTY for i in range(ship)):
                    for i in range(ship):
                        board[x][y + i] = SHIP
                    placed = True
            elif direction == 'vertical' and x + ship <= BOARD_SIZE:
                # Проверяем возможность вертикального размещения
                if all(board[x + i][y] == EMPTY for i in range(ship)):
                    for i in range(ship):
                        board[x + i][y] = SHIP
                    placed = True

def parse_coordinates(coord: str) -> Tuple[int, int]:
    """Преобразует строковые координаты в индексы поля.

    Args:
        coord: Строка, например "A3", обозначающая координаты.

    Returns:
        Кортеж (x, y), где x — индекс строки, y — индекс столбца.
    """
    return ord(coord[0].upper()) - ord('A'), int(coord[1:]) - 1

def is_valid_shot(coord: str) -> bool:
    """Проверяет, являются ли координаты допустимыми для выстрела.

    Args:
        coord: Строка, например "A3", обозначающая координаты.

    Returns:
        True, если координаты корректны, иначе False.
    """
    if len(coord) < 2 or not coord[0].isalpha() or not coord[1:].isdigit():
        return False
    x, y = parse_coordinates(coord)
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

@bot.message_handler(commands=['start'])
def start(message):
    """Обрабатывает команду /start для начала игры."""
    global user_board, bot_board, user_ships, bot_ships
    user_board = create_board()
    bot_board = create_board()
    user_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    bot_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    place_ships(bot_board, bot_ships)
    bot.send_message(message.chat.id, "Добро пожаловать в Морской Бой! Используйте /place_ships, чтобы разместить корабли.")

@bot.message_handler(commands=['place_ships'])
def place_ships_command(message):
    """Обрабатывает команду /place_ships для размещения кораблей пользователя."""
    place_ships(user_board, user_ships)
    bot.send_message(message.chat.id, "Ваши корабли были размещены.")
    bot.send_message(message.chat.id, "Ваше поле:\n" + display_board(user_board))
    bot.send_message(message.chat.id, "Используйте /shoot, чтобы начать бой!")

@bot.message_handler(commands=['shoot'])
def shoot(message):
    """Обрабатывает команду /shoot для начала фазы стрельбы."""
    bot.send_message(
        message.chat.id,
        "Ваши выстрелы:\n" + display_player_shots(bot_board)
    )
    bot.send_message(message.chat.id, "Введите координаты для выстрела (например, А3):")
    bot.register_next_step_handler(message, process_shot)

def process_shot(message):
    """Обрабатывает выстрел пользователя и управляет логикой игры."""
    shot = message.text.strip()
    if not is_valid_shot(shot):
        bot.send_message(message.chat.id, "Некорректные координаты. Введите корректные координаты (например, А3).")
        return
    x, y = parse_coordinates(shot)

    if bot_board[x][y] == SHIP:
        bot_board[x][y] = HIT
        bot.send_message(message.chat.id, f"Попадание по координатам {shot}!")
    elif bot_board[x][y] in {HIT, MISS}:
        bot.send_message(message.chat.id, f"По координатам {shot} уже стреляли. Попробуйте снова.")
        return
    else:
        bot_board[x][y] = MISS
        bot.send_message(message.chat.id, f"Мимо по координатам {shot}.")

    bot.send_message(
        message.chat.id,
        "Ваши обновлённые выстрелы:\n" + display_player_shots(bot_board)
    )
    bot_turn(message)

def bot_turn(message):
    """Выполняет ход бота, стреляя по полю пользователя."""
    while True:
        # Случайно выбираем позицию для выстрела
        x, y = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
        if user_board[x][y] not in {HIT, MISS}:
            break
    if user_board[x][y] == SHIP:
        user_board[x][y] = HIT
        bot.send_message(message.chat.id, f"Бот попал по координатам {chr(x + ord('A'))}{y + 1}!")
    else:
        user_board[x][y] = MISS
        bot.send_message(message.chat.id, f"Бот промахнулся по координатам {chr(x + ord('A'))}{y + 1}.")

    # Отображаем поле пользователя после выстрела бота
    bot.send_message(
        message.chat.id,
        "Ваше поле после выстрела бота:\n" + display_bot_shots(user_board)
    )

    # Проверяем условия победы
    if all(all(cell != SHIP for cell in row) for row in bot_board):
        bot.send_message(message.chat.id, "Вы выиграли!")
    elif all(all(cell != SHIP for cell in row) for row in user_board):
        bot.send_message(message.chat.id, "Бот выиграл!")
    else:
        bot.send_message(message.chat.id, "Используйте /shoot, чтобы сделать ещё один выстрел.")

@bot.message_handler(commands=['help'])
def help_command(message):
    """Обрабатывает команду /help для отображения списка доступных команд."""
    bot.send_message(message.chat.id, """
Доступные команды:
/start - Начать новую игру.
/place_ships - Разместить корабли на поле.
/shoot - Стрелять по полю противника.
/help - Показать список команд.
    """)

# Запуск бота
bot.polling()