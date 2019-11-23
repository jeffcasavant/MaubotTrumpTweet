test:
	safety check -r requirements.txt
	bandit plugin.py

lint:
	pylint plugin.py

format:
	black plugin.py

build:
	mbc build
