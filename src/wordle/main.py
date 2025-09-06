from pathlib import Path

from wordle.game import WordleGame


def get_words():
    filepath = Path(__file__).parent.parent.parent / "assets" / "words.txt"

    with open(filepath) as file:
        words = [line.strip() for line in file]

    return words


if __name__ == "__main__":
    game = WordleGame(get_words())
    results = game.guess_word(guess="audio")

    if game.won:
        print("You won!")
    else:
        print("You lost!")
        print(results)
