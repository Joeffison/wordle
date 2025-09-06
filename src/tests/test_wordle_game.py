import pytest

from wordle.game import WordleGame


@pytest.fixture
def words():
    return [
        "audio",
        "blink",
        "click",
    ]


@pytest.fixture
def game(words):
    return WordleGame(words)


@pytest.mark.parametrize("guess", ["audio", "click"])
def test_guess_correctly(game, guess):
    game._word = guess
    game.guess_word(guess)

    assert game.won is True
    assert game.game_over is True


@pytest.mark.parametrize("guess", ["audio", "click"])
def test_guess_is_case_insensitive(game, guess):
    game._word = guess.lower()
    game.guess_word(guess.upper())

    assert game.won is True
    assert game.game_over is True


def test_guess_with_invalid_length(game):
    with pytest.raises(Exception) as err:
        game.guess_word("abc")

    assert f"Guess must have 5 letters" in str(err)
