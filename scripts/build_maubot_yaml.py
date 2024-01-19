#! /usr/bin/env python3

import toml
from ruamel import yaml

with open("pyproject.toml", mode="r", encoding="utf8") as f:
    pyproject = toml.loads(f.read())

maubot_yaml = {}

maubot_yaml["id"] = pyproject["tool"]["poetry"]["name"]
maubot_yaml["version"] = pyproject["tool"]["poetry"]["version"]
maubot_yaml["license"] = pyproject["tool"]["poetry"]["license"]

maubot_yaml['dependencies'] = []

for k, v in pyproject["tool"]["maubot"].items():
    maubot_yaml[k] = v

with open("maubot.yaml", mode="w", encoding="utf8") as f:
    f.write(yaml.dump(maubot_yaml))
