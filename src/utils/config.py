"""
Config and env loader.

Functions:
    load_config: Loads the config file.
    load_env: Loads any variable from the .env file.
"""

import os
from pathlib import Path
import sys
import tomllib
from dotenv import load_dotenv
from logging import Logger

import dotenv
from utils.log import setup_logger

CONFIG_PATH: Path = Path("config/config.toml")
ENV_PATH: Path = Path(".env")

logger = setup_logger("config_loader", "config_loader.log")


def load_config(
    config_path: Path = CONFIG_PATH, logger: Logger = logger
) -> dict | None:
    """
    Loads the configuration from a TOML file.

    Args:
        config_path (Path): Path to the configuration file.
        logger (Logger): Logger for logging messages.

    Returns:
        dict | None: The configuration as a dictionary, or None if loading fails.
    """
    try:
        with open(config_path, "rb") as file:
            Logger.info(f"Loaded config file at {config_path}.")
            return tomllib.load(file)
    except FileNotFoundError:
        logger.error(f"Config file not found at {config_path}. Exiting...")
        return None
    except tomllib.TOMLDecodeError:
        logger.error(f"Config file at {config_path} is not valid TOML. Exiting...")
        return None
    except Exception as e:
        logger.error(
            f"Unknown error occurred while loading config file: {e}. Exiting..."
        )
        return None


def load_env(
    env_var_name: str, env_path: Path = ENV_PATH, logger: Logger = logger
) -> str | None:
    """
    Loads a specified environment variable.

    Args:
        env_var_name (str): The name of the environment variable to load.
        env_path (Path): Path to the .env file.
        logger (Logger): Logger for logging messages.

    Returns:
        str | None: The value of the environment variable if found, or None otherwise.
    """
    # Check if .env file exists
    if not env_path.is_file():
        logger.error(f"Environment file not found at {env_path}. Exiting...")
        return None

    # Load environment variable from .env file and return it
    try:
        load_dotenv(env_path)
        env_var: str = os.getenv(env_var_name)
        if env_var is None:
            logger.error("API_KEY not found in environment variables.")
            return None
        logger.info(f"Loaded environment variable {env_var_name}.")
        return env_var
    except dotenv.exceptions.InvalidFileException:
        logger.error(
            f"Environment file at {env_path} is not valid. Exiting...",
        )
        return None
    except Exception as e:
        logger.error(
            f"Unknown error occurred while loading environment variables: {e}. Exiting..."
        )
        return None
