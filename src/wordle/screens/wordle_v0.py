import abc

import pygame

from wordle.game import LetterResult


class WordScreenBase(abc.ABC):
    background_color = (0, 0, 0)

    def __init__(
        self,
        screen_width,
        screen_height,
        title="Wordle Game by Joeffison",
        word_length=5,
        max_attempts=6,
    ):
        self.title = title
        self.word_length = word_length
        self.max_attempts = max_attempts
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    def draw_background(self, rect=None):
        self.screen.fill(self.background_color, rect)


class WordleV0(WordScreenBase):
    background_color = (0, 0, 0)

    font_color = (255, 255, 255)
    font_size = 40

    letter_right_position_color = (83, 141, 78)
    letter_wrong_position_color = (181, 159, 59)

    square_color = (86, 87, 88)
    square_margin = 4
    square_size = 52
    square_thickness = 2

    def __init__(self, title="Wordle Game by Joeffison", word_length=5, max_attempts=6):
        super().__init__(
            screen_width=(self.square_margin + self.square_size) * word_length,
            screen_height=(self.square_margin + self.square_size) * max_attempts,
            title=title,
            word_length=word_length,
            max_attempts=max_attempts,
        )

        self.font = pygame.font.SysFont(None, self.font_size)
        self.matrix_of_squares = self._create_matrix_of_squares()

    def _create_matrix_of_squares(self):
        matrix = []
        for row in range(self.max_attempts):
            matrix_row = []
            for column in range(self.word_length):
                position_x = column * self.square_size + self.square_margin * column
                position_y = row * self.square_size + self.square_margin * row

                square = pygame.Rect(
                    position_x, position_y, self.square_size, self.square_size
                )
                matrix_row.append(square)
            matrix.append(matrix_row)

        return matrix

    def draw_screen(self):
        pygame.display.set_caption(self.title)

        self.draw_background()
        self._draw_matrix(self.screen, self.matrix_of_squares)

    def _draw_matrix(self, screen, matrix):
        for row in matrix:
            for square in row:
                self._draw_square(screen, square)

    def _draw_square(self, screen, square):
        pygame.draw.rect(screen, self.square_color, square, self.square_thickness)

    def draw_guess(self, current_attempt, guess):
        row = self.matrix_of_squares[current_attempt]
        for letter, square in zip(guess, row):
            text_surface = self.font.render(letter, True, self.font_color)
            text_rect = text_surface.get_rect(center=square.center)
            self.screen.blit(text_surface, text_rect)

        for index in range(len(guess), self.word_length):
            self.draw_background(row[index])
            self._draw_square(self.screen, row[index])

    def draw_result(self, current_attempt, results):
        row = self.matrix_of_squares[current_attempt]
        for square, result in zip(row, results):
            if result == LetterResult.RIGHT_LETTER_RIGHT_POSITION:
                pygame.draw.rect(self.screen, self.letter_right_position_color, square)
                self._draw_square(self.screen, square)

            elif result == LetterResult.RIGHT_LETTER_WRONG_POSITION:
                pygame.draw.rect(self.screen, self.letter_wrong_position_color, square)
                self._draw_square(self.screen, square)
