import pygame

from wordle.screens.components.base_component import BaseComponent
from wordle.screens.components.game_board import WordleBoard


class GameScreenBase(BaseComponent):
    def __init__(
        self,
        screen_width,
        screen_height,
        background_color=(0, 0, 0),
        title="Wordle Game by Joeffison",
        word_length=5,
        max_attempts=6,
    ):
        super().__init__(screen_width, screen_height, background_color)
        self.title = title
        self.word_length = word_length
        self.max_attempts = max_attempts

    @property
    def surface(self):
        if not self._surface:
            self._surface = pygame.display.set_mode(self.size)

        return self._surface

    def draw(self):
        super().draw()
        pygame.display.set_caption(self.title)


class WordleScreenV0(GameScreenBase):
    def __init__(
        self,
        background_color=(0, 0, 0),
        title="Wordle Game by Joeffison",
        word_length=5,
        max_attempts=6,
    ):
        self.board = WordleBoard()

        super().__init__(
            screen_width=self.board.width,
            screen_height=self.board.height,
            background_color=background_color,
            title=title,
            word_length=word_length,
            max_attempts=max_attempts,
        )

    @property
    def board_position(self):
        return (self.width - self.board.width) // 2, 0

    def draw(self):
        super().draw()

        self.board.draw()
        self.surface.blit(self.board.surface, self.board_position)

    def draw_guess(self, current_attempt, guess):
        self.board.draw_guess(current_attempt, guess)
        self.surface.blit(self.board.surface, self.board_position)

    def draw_result(self, current_attempt, results):
        self.board.draw_result(current_attempt, results)
        self.surface.blit(self.board.surface, self.board_position)
