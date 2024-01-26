"""
Simple config and env loader.
"""

import tomllib

CONFIG_PATH = "src/config.toml"


def load_config():
    with open(CONFIG_PATH, "rb") as file:
        return tomllib.load(file)


api_key: str = "your-api-key"
