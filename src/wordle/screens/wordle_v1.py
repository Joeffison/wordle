from wordle.screens.components.keyboard import Keyboard
from wordle.screens.wordle_v0 import WordleScreenV0


class WordleScreenV1(WordleScreenV0):
    def __init__(self, title="Wordle Game by Joeffison", word_length=5, max_attempts=6):
        super().__init__(
            title=title,
            word_length=word_length,
            max_attempts=max_attempts,
        )

        self.keyboard = Keyboard(background_color=self.background_color)

        # adjust size to fit the keyboard
        self.width = max(self.width, self.keyboard.width)
        self.height += self.keyboard.height

        self._keyboard_margin = 50

    @property
    def keyboard_position(self):
        return 0, self.height - self.keyboard.height + self._keyboard_margin

    def draw(self):
        super().draw()
        self.keyboard.draw()
        self.surface.blit(self.keyboard.surface, self.keyboard_position)

    def draw_guess(self, current_attempt, guess):
        super().draw_guess(current_attempt, guess)

        self.keyboard.draw_guess(current_attempt, guess)
        self.surface.blit(self.keyboard.surface, self.keyboard_position)

    def draw_result(self, current_attempt, guess, results):
        super().draw_result(current_attempt, guess, results)

        self.keyboard.draw_result(current_attempt, guess, results)
        self.surface.blit(self.keyboard.surface, self.keyboard_position)
