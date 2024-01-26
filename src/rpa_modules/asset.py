from utils.log import setup_logger
from utils.fetch import get_asset
from jsonpath_ng.ext import parser
from utils.patch import patch_workorder_desc

asset_log = setup_logger("asset", "asset.log")

def asset_RPA(w_id: int, json) -> str | None :
    """
    Process the asset data and update the work order description.

    Args:
        w_id (int): The ID of the work order.
        json (dict): The JSON data containing the asset information.

    Returns:
        None: If the assetID is None or "None".
        str: The patched work order description if the asset has a matching user-defined field.

    """
    assetID = json['data']['assetID']

    if assetID == None and assetID == "None":
        return
    else:
        asset = get_asset(assetID)
        assetJSON = json.loads(asset.content)

        m = None
        for match in parser.parse("data[*].userDefinedFields[?(@.name='Nyanskaffelser dækkes af:')]").find(assetJSON):
            m = match.value

        if m == None:
            return
        else:
            patch_string = m['name'] + " " + m['value']
            asset_log("\tAsset: " + str(assetID) + " nyanskaffelser bliver dækket og tilføjes på workorder " + str(w_id))
            patch_workorder_desc(w_id, patch_string)