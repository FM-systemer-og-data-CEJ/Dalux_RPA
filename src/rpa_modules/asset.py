from utils.log import setup_logger
from utils.fetch import get_asset
from jsonpath_ng.ext import parser
from utils.patch import patch_workorder_desc

asset_log = setup_logger("asset", "asset.log")

def asset_RPA(w_id, json):
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