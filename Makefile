lint:
	pylint plugin.py

format:
	black plugin.py

build:
	mbc build
