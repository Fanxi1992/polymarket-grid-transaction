import os

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, BalanceAllowanceParams, AssetType
from dotenv import load_dotenv
from py_clob_client.constants import AMOY
from grid_config import CLOB_HOST, CLOB_KEY, API_CREDENTIALS

load_dotenv()

def main():
    host = CLOB_HOST  # 或者你的 Polymarket API 地址
    key = CLOB_KEY  # 你的钱包私钥
    creds = ApiCreds(
        api_key=API_CREDENTIALS['api_key'],
        api_secret=API_CREDENTIALS['api_secret'],
        api_passphrase=API_CREDENTIALS['api_passphrase'],
    )
    chain_id = AMOY  # 或者 POLYGON
    client = ClobClient(host, key=key, chain_id=chain_id, creds=creds)

    # 查询 USDC 余额
    collateral_balance = client.get_balance_allowance(
        params=BalanceAllowanceParams(asset_type=AssetType.COLLATERAL)
    )
    print("USDC Balance:", collateral_balance)

    # 如果你想查询特定条件代币（例如 YES 或 NO 份额）的余额，你需要提供 token_id
    yes_balance = client.get_balance_allowance(
        params=BalanceAllowanceParams(
            asset_type=AssetType.CONDITIONAL,
            token_id="57340959878398421678357543264767127245404802056106050362156330852499865274040"
        )
    )
    print("YES Balance:", yes_balance)

    no_balance = client.get_balance_allowance(
        params=BalanceAllowanceParams(
            asset_type=AssetType.CONDITIONAL,
            token_id="57340959878398421678357543264767127245404802056106050362156330852499865274040"
        )
    )
    print("NO Balance:", no_balance)

if __name__ == "__main__":
    main()