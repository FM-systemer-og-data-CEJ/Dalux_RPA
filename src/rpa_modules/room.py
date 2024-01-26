"""
This module contains functions related to room operations in the RPA system.

It provides functionality to perform RPA operations for a room, including retrieving room information,
parsing room data, and patching workorder descriptions.

Functions:
    rum_RPA: Perform RPA operations for a room.
"""

from utils.log import setup_logger
from utils.fetch import get_room
from utils.parserS import parser
from utils.patch import patch_workorder_desc

rum_log = setup_logger("rum", "rum.log")


def rum_RPA(w_id: int, json: dict[str, dict[str, int]]) -> None:
    """
    Perform RPA operations for a room.

    Args:
        w_id (int): The workorder ID.
        json (dict[str, dict[str, int]]): The JSON data containing room information.

    Returns:
        None
    """
    roomID: int = json["data"]["roomID"]

    if roomID is None:
        return
    else:
        room = get_room(roomID)
        roomJSON = json.loads(room.content)

        p = None
        for match in parser.parse(
            "data[*].userDefinedFields[?(@.name=='Kritisk rum:')]"
        ).find(roomJSON):
            p = match.value["value"]

        if p is None:
            return
        else:
            patch_string = p["name"] + " " + p["value"]
            rum_log.info(
                "\tRum: "
                + str(roomID)
                + " er kritisk og tilføjes på workorder: "
                + str(w_id)
            )
            patch_workorder_desc(w_id, patch_string)
