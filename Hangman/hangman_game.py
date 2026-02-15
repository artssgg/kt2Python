import random
import json
# этапы виселицы
HANGMAN_STAGES = [
    """
       --------
       |      |
       |
       |
       |
       |
       -
    """,
    """
       --------
       |      |
       |      O
       |
       |
       |
       -
    """,
    """
       --------
       |      |
       |      O
       |      |
       |
       |
       -
    """,
    """
       --------
       |      |
       |      O
       |     /|
       |
       |
       -
    """,
    """
       --------
       |      |
       |      O
       |     /|\\
       |
       |
       -
    """,
    """
       --------
       |      |
       |      O
       |     /|\\
       |      |
       |
       -
    """,
    """
       --------
       |      |
       |      O
       |     /|\\
       |      |
       |     /
       -
    """,
    """
       --------
       |      |
       |      O
       |     /|\\
       |      |
       |     / \\
       -
    """
]

def load_words(filename="words.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            words = json.load(f)
        if words:
            return words
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    # Резервный список (на случай отсутствия файла)
    return [
        {"word": "ПИТОН", "hint": "язык программирования, а также змея"},
        {"word": "КРОКОДИЛ", "hint": "зелёное зубастое животное"}
    ]

def choose_word(words_list):
    entry = random.choice(words_list)
    return entry["word"], entry["hint"]

def display_hangman(tries):
    index = len(HANGMAN_STAGES) - 1 - tries
    return HANGMAN_STAGES[index]

def initialize_game(words_source):
    word, hint = choose_word(words_source)
    return {
        "word": word,
        "hint": hint,
        "display": ["_"] * len(word),
        "guessed_letters": set(),
        "wrong_letters": set(),
        "tries_left": 7,          # максимальное количество попыток
        "game_over": False
    }

def display_state(game):
    print("\n" + "=" * 40)
    print(f"Подсказка: {game['hint']}")
    print(display_hangman(game["tries_left"]))
    print("Слово: " + " ".join(game["display"]))
    print(f"Осталось попыток: {game['tries_left']}")
    if game["wrong_letters"]:
        print("Ошибочные буквы:", ", ".join(sorted(game["wrong_letters"])))
    print()

def get_guess():
    while True:
        guess = input("Введите букву или слово целиком: ").strip().upper()
        if not guess:
            print("Вы ничего не ввели. Попробуйте снова.")
            continue
        if not guess.isalpha():
            print("Можно использовать только буквы (без цифр и символов).")
            continue
        return guess

def process_guess(game, guess):
    # Если игра уже завершена, ничего не делаем
    if game["game_over"]:
        return
    # Случай: введена одна буква
    if len(guess) == 1:
        if guess in game["guessed_letters"] or guess in game["wrong_letters"]:
            print("Вы уже называли эту букву. Попробуйте другую.")
            return
        if guess in game["word"]:
            # Открываем все вхождения буквы
            game["guessed_letters"].add(guess)
            for i, ch in enumerate(game["word"]):
                if ch == guess:
                    game["display"][i] = guess
            print(f"Отлично! Буква {guess} есть в слове.")
        else:
            game["wrong_letters"].add(guess)
            game["tries_left"] -= 1
            print(f"Увы, буквы {guess} нет в слове.")
    # Случай: введено слово целиком
    elif len(guess) == len(game["word"]):
        if guess == game["word"]:
            # Полная победа
            game["display"] = list(game["word"])
            game["game_over"] = True
            print("Поздравляю! Слово угадано!")
        else:
            game["tries_left"] -= 1
            print("Неверное слово.")
    else:
        print("Длина слова не совпадает с загаданным. Попробуйте ещё раз.")
    # Проверка на окончание игры
    if "_" not in game["display"]:
        game["game_over"] = True
        print("Поздравляю! Слово отгадано!")
    elif game["tries_left"] == 0:
        game["game_over"] = True
        print("Вы исчерпали все попытки.")
def is_finished(game):
    """Возвращает True, если игра завершена (победа или поражение)."""
    return game["game_over"]
def display_result(game):
    """Выводит финальное сообщение в зависимости от исхода игры."""
    if "_" not in game["display"]:
        print(f"\nВы выиграли! Загаданное слово: {game['word']}")
    else:
        print(f"\nВы проиграли. Загаданное слово: {game['word']}")
def run_game():
    """Главная функция, запускающая полный игровой процесс."""
    words = load_words()
    game = initialize_game(words)
    print("Добро пожаловать в игру 'Виселица'!")
    while not is_finished(game):
        display_state(game)
        guess = get_guess()
        process_guess(game, guess)
    display_result(game)