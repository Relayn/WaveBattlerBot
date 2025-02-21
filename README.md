# WaveBattlerBot

WaveBattlerBot — это бот для игры "Морской бой", написанный на Python. В этой реализации игрок сражается с ботом, совершая выстрелы по расположенным на игровой доске кораблям.

## Описание

В проекте реализованы следующие возможности:
- **Создание игровой доски.** Используется функция `create_board` для инициализации доски с пустыми ячейками, кораблями, попаданиями и промахами.
- **Отображение досок и результатов выстрелов.** Функции `display_board`, `display_player_shots` и `display_bot_shots` отвечают за визуализацию текущего состояния игрового поля.
- **Расстановка кораблей.** Пользователь может расставить свои корабли посредством команды, а бот генерирует расположение кораблей автоматически с помощью функции `place_ships` (а также `place_ships_command` для интерактивной расстановки).
- **Обработка выстрелов.** Функции `shoot`, `process_shot` и `is_valid_shot` обеспечивают проверку корректности выстрелов, их обработку и обновление игровых досок.
- **Логика хода бота.** Функция `bot_turn` реализует алгоритм хода бота.
- **Помощь по игровым командам.** Команда `help_command` выводит подсказки, объясняющие правила и доступные команды игры.
- **Запуск игры.** Основная функция `start` объединяет все компоненты и запускает игровой процесс.

## Установка и запуск

1. **Требования:**
    - Python 3.13.1.
    - Установленные пакеты: `pygame`, `requests`, `selenium`.

2. **Настройка:**
    - Откройте файл `main.py` и проверьте, что переменная `BOT_TOKEN` содержит ваш токен (используйте необходимые данные для авторизации, если это предусмотрено).

3. **Запуск:**
    - Выполните команду для запуска игры в терминале:
      ```python
      python main.py
      ```

## Управление игрой

- **Расстановка кораблей:**
    - Выполните команду для расстановки кораблей (через функцию `place_ships_command`).
    - Введите координаты в указанном формате.

- **Выстрелы:**
    - Используйте команду `shoot` для выстрела по вражеской доске.
    - После каждого выстрела происходит проверка корректности координат с помощью `is_valid_shot` и обработка попадания или промаха через `process_shot`.

- **Ход бота:**
    - После хода игрока бот автоматически совершает свой ход через функцию `bot_turn`.

- **Получение справки:**
    - Для вывода информации о доступных командах используйте команду `help`.

## Лицензия

Данный проект является открытым программным обеспечением. Смотрите файл `LICENSE` для подробной информации.
 
## Контактная информация
- Автор: Алексей Новопашин
- Email: aleksnovop@gmail.com
- GitHub: https://github.com/Relayn