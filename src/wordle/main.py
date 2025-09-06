from pathlib import Path

import pygame

from wordle.game import WordleGame, LetterResult


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BACKGROUND_COLOR = (0, 0, 0)
SQUARE_COLOR = (86, 87, 88)
FONT_COLOR = (255, 255, 255)
LETTER_RIGHT_POSITION_COLOR = (0, 255, 0)
LETTER_WRONG_POSITION_COLOR = (181, 159, 59)

SQUARE_SIZE = 52
SQUARE_THICKNESS = 2
SQUARE_MARGIN = 4
FONT_SIZE = 40

WORD_LENGTH = 5
MAX_ATTEMPTS = 6


def get_words():
    filepath = Path(__file__).parent.parent.parent / "assets" / "words.txt"

    with open(filepath) as file:
        words = [line.strip() for line in file]

    return words


def draw_background(screen: pygame.Surface, rect=None):
    screen.fill(BACKGROUND_COLOR, rect)


def create_matrix_of_squares():
    matrix = []
    for row in range(MAX_ATTEMPTS):
        matrix_row = []
        for column in range(WORD_LENGTH):
            position_x = column * SQUARE_SIZE + SQUARE_MARGIN * column
            position_y = row * SQUARE_SIZE + SQUARE_MARGIN * row

            square = pygame.Rect(position_x, position_y, SQUARE_SIZE, SQUARE_SIZE)
            matrix_row.append(square)
        matrix.append(matrix_row)

    return matrix


def draw_matrix(screen, matrix):
    for row in matrix:
        for square in row:
            draw_square(screen, square)


def draw_square(screen, square):
    pygame.draw.rect(screen, SQUARE_COLOR, square, SQUARE_THICKNESS)


def draw_guess(screen, matrix, current_attempt, guess):
    row = matrix[current_attempt]
    for letter, square in zip(guess, row):
        text_surface = font.render(letter, True, FONT_COLOR)
        text_rect = text_surface.get_rect(center=square.center)
        screen.blit(text_surface, text_rect)

    for index in range(len(guess), WORD_LENGTH):
        draw_background(screen, row[index])
        draw_square(screen, row[index])


def draw_result(screen, matrix, current_attempt, results):
    row = matrix[current_attempt]
    for square, result in zip(row, results):
        if result == LetterResult.RIGHT_LETTER_RIGHT_POSITION:
            pygame.draw.rect(screen, LETTER_RIGHT_POSITION_COLOR, square)
            draw_square(screen, square)

        elif result == LetterResult.RIGHT_LETTER_WRONG_POSITION:
            pygame.draw.rect(screen, LETTER_WRONG_POSITION_COLOR, square)
            draw_square(screen, square)


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, FONT_SIZE)

    running = True

    matrix = create_matrix_of_squares()
    current_attempt = 0
    current_guess = ""

    draw_background(screen)
    draw_matrix(screen, matrix)

    game = WordleGame(get_words())

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif not game.game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(current_guess) == WORD_LENGTH:
                    results = game.guess_word(current_guess)
                    draw_result(screen, matrix, current_attempt, results)
                    draw_guess(screen, matrix, current_attempt, current_guess)
                    current_attempt += 1
                    current_guess = ""

                elif (
                    len(current_guess) < WORD_LENGTH
                    and pygame.K_a <= event.key <= pygame.K_z
                ):
                    current_guess += event.unicode.upper()
                    draw_guess(screen, matrix, current_attempt, current_guess)

                elif event.key == pygame.K_BACKSPACE:
                    current_guess = current_guess[:-1]
                    draw_guess(screen, matrix, current_attempt, current_guess)

        pygame.display.flip()

    pygame.quit()
