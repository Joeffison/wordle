import enum

import random

WORD_LENGTH = 5


class LetterResult(enum.Enum):
    RIGHT_LETTER_RIGHT_POSITION = 1
    RIGHT_LETTER_WRONG_POSITION = -1
    WRONG_LETTER = 0


class WordleGame:

    def __init__(self, words, max_attempts=6):
        self.valid_words = words
        self._word = random.choice(self.valid_words).lower()
        self._max_attempts = max_attempts
        self._guesses = []
        self.won = False

    @property
    def game_over(self):
        return self.won or len(self._guesses) >= self._max_attempts

    def guess_word(self, guess: str):
        if len(guess) != WORD_LENGTH:
            raise ValueError(f"Guess must have {WORD_LENGTH} letters")

        guess = guess.lower()
        if guess not in self.valid_words:
            raise ValueError(f"{guess} not a valid word")

        self._guesses.append(guess)
        if guess == self._word:
            self.won = True
            return [LetterResult.RIGHT_LETTER_RIGHT_POSITION] * WORD_LENGTH

        result = [LetterResult.WRONG_LETTER] * WORD_LENGTH
        for i in range(WORD_LENGTH):
            if guess[i] == self._word[i]:
                result[i] = LetterResult.RIGHT_LETTER_RIGHT_POSITION

            elif guess[i] in self._word:
                result[i] = LetterResult.RIGHT_LETTER_WRONG_POSITION

        return result
