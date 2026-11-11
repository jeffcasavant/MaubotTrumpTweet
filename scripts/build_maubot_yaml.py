#! /usr/bin/env python3

import tomllib

from ruamel.yaml import YAML

with open("pyproject.toml", mode="rb") as f:
    pyproject = tomllib.load(f)

maubot_yaml = {}

maubot_yaml["id"] = pyproject["project"]["name"]
maubot_yaml["version"] = pyproject["project"]["version"]
maubot_yaml["license"] = pyproject["project"]["license"]

with open("requirements.txt", mode="r", encoding="utf8") as f:
    maubot_yaml["dependencies"] = [line.strip() for line in f.readlines()]

for k, v in pyproject["tool"]["maubot"].items():
    maubot_yaml[k] = v

with open("maubot.yaml", mode="w", encoding="utf8") as f:
    YAML().dump(maubot_yaml, f)
