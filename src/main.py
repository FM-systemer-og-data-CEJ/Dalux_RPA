"""
This module is the main entry point for DALUX_RPA.
Including the functionality to process work orders based on command-line flags. 
It also and manages the application state based on responses and timers/counters.

Functions:
    main: Orchestrates the primary workflow of the application.
    process_flags: Handles the execution of specific RPA modules based on cli flags.
    determine_state: Determines the current state of the program.
"""
# TODO: Add error handling.

import json
import sys
import time
from enum import Enum

from rpa_modules.asset import asset_RPA
from rpa_modules.ean_psp import EAN_PSP_RPA
from rpa_modules.room import rum_RPA
from utils.config import load_config
from utils.fetch import get_workorder, peek, peek_long
from utils.log import setup_logger

logger = setup_logger("main", "main.log")

config = load_config()

# Retry config
retry_config = config["main"]["retry"]
SLEEP_TIME: int = retry_config["sleep_time"]
RETRY_LIMIT: int = retry_config["retry_limit"]
MAX_RETRIES: int = retry_config["max_retries"]
PEEKS_PER_LONG_PEEK: int = retry_config["peeks_per_long_peek"]

# Module config
modules_config = config["main"]["modules"]
EAN_PSP_MODULE: bool = modules_config["EAN_PSP"]
ROOM_MODULE: bool = modules_config["ROOM"]
ASSET_MODULE: bool = modules_config["ASSET"]

# Constants, success code.
SUCCESS_CODE: int = 200


def process_flags(workorder_id: int, response_json: dict) -> None:
    """
    Processes which modules are enabled from the config file.
    """
    if EAN_PSP_MODULE:
        logger.info(f"Processing EAN_PSP module for id {workorder_id}.")
        EAN_PSP_RPA(workorder_id, response_json)
    if ROOM_MODULE:
        logger.info(f"Processing ROOM module for id {workorder_id}.")
        rum_RPA(workorder_id, response_json)
    if ASSET_MODULE:
        logger.info(f"Processing ASSET module for id {workorder_id}.")
        asset_RPA(workorder_id, response_json)


class CurrentState(Enum):
    """
    enum for the current state of the RPA application.
    """
    SUCCESS = 1
    RETRY = 2
    PEEK = 3
    LONG_PEEK = 4


def determine_state(
        response_code: int, total_sleep: int, peek_counter: int
) -> CurrentState:
    """
    Determines the current state of the RPA application.
    """
    logger.info(f"Determining state of program.")
    if response_code == SUCCESS_CODE:
        logger.info(f"Response success: {SUCCESS_CODE}")
        return CurrentState.SUCCESS
    elif total_sleep % RETRY_LIMIT == 0:
        logger.info(f"Total sleep: {total_sleep} seconds. Going to peek.")
        if peek_counter >= PEEKS_PER_LONG_PEEK:
            logger.info(f"Peek counter: {peek_counter}. Going to long peek.")
            return CurrentState.LONG_PEEK
        else:
            logger.info(f"Peek counter: {peek_counter}. Going to peek.")
            return CurrentState.PEEK
    else:
        logger.info(f"Response code: {response_code}. Going to retry.")
        return CurrentState.RETRY


def main() -> None:
    """
    Main entry point for the RPA application.
    """
    # Command line inputs.
    workorder_id: int = int(sys.argv[1])
    logger.info(f"RPA at workorder id: {workorder_id}.")

    # Variables for the loop.
    total_sleep: int = 0
    peek_counter: int = 0
    retries: int = 0

    while retries < MAX_RETRIES:
        try:
            response = get_workorder(workorder_id)
            state = determine_state(response.status_code, total_sleep, peek_counter)

            match state:
                case CurrentState.SUCCESS:
                    logger.info(f"Successfully retrieved id {workorder_id}.")
                    response_json = json.loads(response.content)
                    total_sleep = 0
                    process_flags(workorder_id, response_json)
                    workorder_id += 1
                    logger.info(f"Successfully processed id {workorder_id}.")
                case CurrentState.RETRY:
                    logger.info(f"Sleeping for {SLEEP_TIME} seconds.")
                    time.sleep(SLEEP_TIME)
                    total_sleep += SLEEP_TIME
                    logger.info(f"Slept for {total_sleep} seconds.")
                case CurrentState.PEEK:
                    logger.info(f"Peeking at id {workorder_id}.")
                    old_w: int = workorder_id
                    workorder_id = peek(workorder_id)
                    if old_w == workorder_id:
                        peek_counter += 1
                        logger.info(f"old workorder id was equal to new workorder id. "
                                    f"Incrementing peek counter to {peek_counter}.")
                    logger.info(f"Peeked at id {workorder_id}.")
                case CurrentState.LONG_PEEK:
                    logger.info(f"Long peeking at id {workorder_id}.")
                    workorder_id = peek_long(workorder_id)
                    peek_counter = 0
                    logger.info(f"Long peeked at id {workorder_id}.")

            retries += 1
            logger.info(f"Loop completed. Retries: {retries}.")

        except Exception as e:
            logger.warning(f"Exception: {e} processing id {workorder_id}. Going to retry.")
            retries += 1


if __name__ == "__main__":
    main()
