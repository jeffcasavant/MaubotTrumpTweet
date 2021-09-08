#! /usr/bin/env python3

import toml
from ruamel import yaml

with open("pyproject.toml", mode="r", encoding="utf8") as f:
    pyproject = toml.loads(f.read())

maubot_yaml = {}

maubot_yaml["id"] = pyproject["tool"]["poetry"]["name"]
maubot_yaml["version"] = pyproject["tool"]["poetry"]["version"]
maubot_yaml["license"] = pyproject["tool"]["poetry"]["license"]

with open("requirements.txt", mode="r", encoding="utf8") as f:
    maubot_yaml["dependencies"] = [line.strip() for line in f.readlines()]

for k, v in pyproject["tool"]["maubot"].items():
    maubot_yaml[k] = v

with open("maubot.yaml", mode="w", encoding="utf8") as f:
    f.write(yaml.dump(maubot_yaml))
