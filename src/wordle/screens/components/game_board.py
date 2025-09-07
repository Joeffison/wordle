import pygame

from wordle.game import LetterResult
from wordle.screens.components.base_component import BaseComponent


class WordleBoard(BaseComponent):
    font_color = (255, 255, 255)
    font_size = 40

    letter_right_position_color = (83, 141, 78)
    letter_wrong_position_color = (181, 159, 59)

    square_color = (86, 87, 88)
    square_margin = 4
    square_size = 52
    square_thickness = 2

    def __init__(self, word_length=5, max_attempts=6):
        super().__init__(
            width=(self.square_margin + self.square_size) * word_length,
            height=(self.square_margin + self.square_size) * max_attempts,
            background_color=(0, 0, 0),
        )
        self.word_length = word_length
        self.max_attempts = max_attempts

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

    def draw(self):
        super().draw()
        self._draw_matrix(self.surface, self.matrix_of_squares)

    def _draw_matrix(self, surface, matrix):
        for row in matrix:
            for square in row:
                self._draw_square(surface, square)

    def _draw_square(self, surface, square):
        pygame.draw.rect(surface, self.square_color, square, self.square_thickness)

    def draw_guess(self, current_attempt, guess):
        row = self.matrix_of_squares[current_attempt]
        for letter, square in zip(guess, row):
            text_surface = self.font.render(letter, True, self.font_color)
            text_rect = text_surface.get_rect(center=square.center)
            self.surface.blit(text_surface, text_rect)

        for index in range(len(guess), self.word_length):
            self.draw_background(row[index])
            self._draw_square(self.surface, row[index])

    def draw_result(self, current_attempt, guess, results):
        row = self.matrix_of_squares[current_attempt]
        for square, result in zip(row, results):
            if result == LetterResult.RIGHT_LETTER_RIGHT_POSITION:
                pygame.draw.rect(self.surface, self.letter_right_position_color, square)
                self._draw_square(self.surface, square)

            elif result == LetterResult.RIGHT_LETTER_WRONG_POSITION:
                pygame.draw.rect(self.surface, self.letter_wrong_position_color, square)
                self._draw_square(self.surface, square)
