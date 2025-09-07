setup:
	asdf plugin add python
	asdf plugin add poetry
	asdf install
	poetry install --without dev,test

setup-dev: setup
	poetry install --only dev,test

play:
	poetry run python src/wordle/main.py

test:
	poetry run pytest .

format:
	poetry run black .
