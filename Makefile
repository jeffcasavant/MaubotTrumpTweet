FILES=plugin.py scripts/build_maubot_yaml.py

security:
	poetry run safety check
	poetry run bandit $(FILES)

lint:
	poetry run pylint $(FILES)
	poetry run black --check $(FILES)
	poetry run isort --check $(FILES)

format:
	poetry run black $(FILES)
	poetry run isort $(FILES)

build: maubot.yaml
	poetry run mbc build

requirements.txt: poetry.lock
	poetry export -f requirements.txt --without-hashes | sed 's/;.*//g' > requirements.txt

maubot.yaml: pyproject.toml requirements.txt
	poetry run scripts/build_maubot_yaml.py

test: lint security
