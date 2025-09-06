from pathlib import Path

import pygame

from wordle.game import WordleGame
from wordle.screens.wordle_v0 import WordleScreenV0

GAME_TITLE = "Wordle Game by Joeffison"
WORD_LENGTH = 5
MAX_ATTEMPTS = 6


def get_words():
    filepath = Path(__file__).parent.parent.parent / "assets" / "words.txt"

    with open(filepath) as file:
        words = [line.strip() for line in file]

    return words


if __name__ == "__main__":
    pygame.init()

    game = WordleGame(get_words())
    running = True

    game_screen = WordleScreenV0()
    game_screen.draw()

    current_attempt = 0
    current_guess = ""

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif not game.game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(current_guess) == WORD_LENGTH:
                    results = game.guess_word(current_guess)
                    game_screen.draw_result(current_attempt, results)
                    game_screen.draw_guess(current_attempt, current_guess)
                    current_attempt += 1
                    current_guess = ""

                elif (
                    len(current_guess) < WORD_LENGTH
                    and pygame.K_a <= event.key <= pygame.K_z
                ):
                    current_guess += event.unicode.upper()
                    game_screen.draw_guess(current_attempt, current_guess)

                elif event.key == pygame.K_BACKSPACE:
                    current_guess = current_guess[:-1]
                    game_screen.draw_guess(current_attempt, current_guess)

        pygame.display.flip()

    pygame.quit()
