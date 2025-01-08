# 先获取余额

import os

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, BalanceAllowanceParams, AssetType
from dotenv import load_dotenv
from py_clob_client.constants import AMOY

load_dotenv()


def main():
    host = "https://clob.polymarket.com"
    key = 'f14af2100840da79a81fd16a5e7577f25f425192a5cc0b009422853bc42658c4'
    creds = ApiCreds(
        api_key='09369d75-ba83-dc0e-aae0-a030fdfd9b72',
        api_secret='UkrywXphcs_1651ekaLsUbhmodtazfoQdAl2dMD6fFE=',
        api_passphrase='e984ff9344638352a6b96536450e48d350a0a23b977165b94f114a7d0f08da1a',
    )
    chain_id = AMOY
    client = ClobClient(host, key=key, chain_id=chain_id, creds=creds)

    collateral = client.get_balance_allowance(
        params=BalanceAllowanceParams(asset_type=AssetType.COLLATERAL)
    )
    print(collateral)

    yes = client.get_balance_allowance(
        params=BalanceAllowanceParams(
            asset_type=AssetType.CONDITIONAL,
            token_id="114114274400532757880593710274353078592581906741743124209803683408668086876506",
        )
    )
    print(yes)

    no = client.get_balance_allowance(
        params=BalanceAllowanceParams(
            asset_type=AssetType.CONDITIONAL,
            token_id="108397666409926231454966838232963026486591713328008484119238822937216538843695",
        )
    )
    print(no)


main()





# 下单之前检查授权
# 在下单之前，需要确保已经授权 USDC
from web3 import Web3

usdc_abi = """[{
    "constant": true,
    "inputs": [
        {"name": "_owner","type": "address"},
        {"name": "_spender","type": "address"}
    ],
    "name": "allowance",
    "outputs": [{"name": "","type": "uint256"}],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
}]"""

# USDC 合约地址（Polygon）
USDC_ADDRESS = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"

# 检查 USDC 授权
def check_usdc_allowance(wallet_address):
    web3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
    usdc_contract = web3.eth.contract(address=USDC_ADDRESS, abi=usdc_abi)
    allowance = usdc_contract.functions.allowance(
        wallet_address,
        "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E"  # Polymarket 合约地址
    ).call()
    return web3.from_wei(allowance, 'mwei')  # USDC 是 6 位小数






# 然后买入
import os
from py_clob_client.constants import POLYGON
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs
from py_clob_client.order_builder.constants import BUY

# 设置http和https代理
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:9788'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:9788'

host = "https://clob.polymarket.com"
key = 'f14af2100840da79a81fd16a5e7577f25f425192a5cc0b009422853bc42658c4'
chain_id = POLYGON

# Create CLOB client and get/set API credentials
client = ClobClient(host, key=key, chain_id=chain_id)
client.set_api_creds(client.create_or_derive_api_creds())

# Create and sign an order buying 100 YES tokens for 0.50c each
resp = client.create_and_post_order(OrderArgs(
    price=0.002,
    size=5,
    side=BUY,
    token_id="29410083705814933335366136380727963952233580532662793139230554474407589926841"
))

print(resp)





# FOK买入
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY


# 取消订单
def cancel_order(client: ClobClient, order_id: str):
    """
    Cancels an order.

    Args:
        client: The ClobClient instance.
        order_id: The ID of the order to cancel.
    """
    try:
        response = client.cancel(order_id)
        print(f"Cancellation request sent for order {order_id}. Response:")
        print(response)
    #     if response and 'state' in response:
    #         if response['state'] == "Canceled":
    #             print(f"Order {order_id} was successfully canceled.")
    #         else:
    #             print(f"Order {order_id} cancellation failed or has an unexpected state.")

    except Exception as e:
        print(f"An error occurred while canceling order {order_id}: {e}")

if __name__ == "__main__":
    host = "https://clob.polymarket.com"  # or "http://localhost:8080" for local testing
    key = 'f14af2100840da79a81fd16a5e7577f25f425192a5cc0b009422853bc42658c4'
    creds = ApiCreds(
        api_key='09369d75-ba83-dc0e-aae0-a030fdfd9b72',
        api_secret='UkrywXphcs_1651ekaLsUbhmodtazfoQdAl2dMD6fFE=',
        api_passphrase='e984ff9344638352a6b96536450e48d350a0a23b977165b94f114a7d0f08da1a',
    )
    chain_id = AMOY
    client = ClobClient(host, key=key, chain_id=chain_id, creds=creds)

    order_id_to_monitor = '0xcd696e953a7f5b20abf2723d0426a08dd242ef7f79d6a98e20b8bac5637ab9bf'  
    cancel_order(client, order_id_to_monitor)





# 查询订单，显示[]，已成交
import os

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, OpenOrderParams
from dotenv import load_dotenv
from py_clob_client.constants import AMOY

load_dotenv()


def main():
    host = "https://clob.polymarket.com"
    key = 'f14af2100840da79a81fd16a5e7577f25f425192a5cc0b009422853bc42658c4'
    creds = ApiCreds(
        api_key='09369d75-ba83-dc0e-aae0-a030fdfd9b72',
        api_secret='UkrywXphcs_1651ekaLsUbhmodtazfoQdAl2dMD6fFE=',
        api_passphrase='e984ff9344638352a6b96536450e48d350a0a23b977165b94f114a7d0f08da1a',
    )
    chain_id = AMOY
    client = ClobClient(host, key=key, chain_id=chain_id, creds=creds)

    resp = client.get_orders(
        OpenOrderParams(
            market="29410083705814933335366136380727963952233580532662793139230554474407589926841",
        )
    )
    print(resp)
    print("Done!")


main()












# 查询我的持仓
import os
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, BalanceAllowanceParams, AssetType
from dotenv import load_dotenv
from py_clob_client.constants import POLYGON  # 你的链 ID, 例：POLYGON

load_dotenv()


def check_balances():
    # 1. 初始化客户端
    host = "https://clob.polymarket.com"
    key = 'f14af2100840da79a81fd16a5e7577f25f425192a5cc0b009422853bc42658c4'
    creds = ApiCreds(
        api_key='09369d75-ba83-dc0e-aae0-a030fdfd9b72',
        api_secret='UkrywXphcs_1651ekaLsUbhmodtazfoQdAl2dMD6fFE=',
        api_passphrase='e984ff9344638352a6b96536450e48d350a0a23b977165b94f114a7d0f08da1a',
    )
    chain_id = POLYGON

    client = ClobClient(host, key=key, chain_id=chain_id, creds=creds)

    # 2. 查询 USDC
    usdc_balance = client.get_balance_allowance(
        params=BalanceAllowanceParams(asset_type=AssetType.COLLATERAL)
    )
    print("USDC余额与Allowance:", usdc_balance)

    # 3. 查询某个YES/NO代币（即某个token_id对应的条件化代币）
    # 下面示例用你的 token_id 替换
    token_id = "29410083705814933335366136380727963952233580532662793139230554474407589926841"
    cond_balance = client.get_balance_allowance(
        params=BalanceAllowanceParams(asset_type=AssetType.CONDITIONAL, token_id=token_id)
    )
    print(f"条件化代币({token_id})余额与Allowance:", cond_balance)


if __name__ == "__main__":
    check_balances()



















# 查询上一个交易的价格，辅助判断是否成交
import os

from py_clob_client.client import ClobClient
from dotenv import load_dotenv
from pprint import pprint

from py_clob_client.constants import AMOY


load_dotenv()


def main():
    host = "https://clob.polymarket.com"
    key = 'f14af2100840da79a81fd16a5e7577f25f425192a5cc0b009422853bc42658c4'
    chain_id = AMOY
    client = ClobClient(host, key=key, chain_id=chain_id)

    resp = client.get_last_trade_price(
        "29410083705814933335366136380727963952233580532662793139230554474407589926841"
    )
    pprint(resp)
    print("Done!")


main()






# 或者直接查询市场价格
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import BookParams


def main():
    host = "https://clob.polymarket.com"
    client = ClobClient(host)

    resp = client.get_price(
        "29410083705814933335366136380727963952233580532662793139230554474407589926841",
        "BUY",
    )
    print(resp)
    print("Done!")


main()









# 查询交易记录
import os

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, TradeParams
from dotenv import load_dotenv
from pprint import pprint

from py_clob_client.constants import AMOY

load_dotenv()


def main():
    host = "https://clob.polymarket.com"
    key = 'f14af2100840da79a81fd16a5e7577f25f425192a5cc0b009422853bc42658c4'
    creds = ApiCreds(
        api_key='09369d75-ba83-dc0e-aae0-a030fdfd9b72',
        api_secret='UkrywXphcs_1651ekaLsUbhmodtazfoQdAl2dMD6fFE=',
        api_passphrase='e984ff9344638352a6b96536450e48d350a0a23b977165b94f114a7d0f08da1a',
    )
    chain_id = AMOY
    client = ClobClient(host, key=key, chain_id=chain_id, creds=creds)
    
    wallet_address = client.get_address()
    market_id = "29410083705814933335366136380727963952233580532662793139230554474407589926841"

    print(f"\n钱包地址: {wallet_address}")
    
    # 1. 查询作为挂单方(maker)的交易
    maker_trades = client.get_trades(
        TradeParams(
            maker_address=wallet_address,
            market=market_id
        )
    )
    print(f"\n作为挂单方的交易: {maker_trades}")
    
    # 2. 查询市场所有交易（因为无法直接查询吃单方交易）
    market_trades = client.get_trades(
        TradeParams(
            market=market_id
        )
    )
    print(f"\n市场所有交易: {market_trades}")
    
    # 3. 如果需要找到作为吃单方的交易，需要手动过滤
    taker_trades = [
        trade for trade in market_trades 
        if hasattr(trade, 'taker') and trade.taker == wallet_address
    ]
    print(f"\n作为吃单方的交易（手动过滤）: {taker_trades}")

main()






















































from py_clob_client.client import ClobClient
from py_clob_client.constants import POLYGON

# 初始化客户端
host = "https://clob.polymarket.com"
key = "f14af2100840da79a81fd16a5e7577f25f425192a5cc0b009422853bc42658c4"  # 记得移除0x前缀
chain_id = POLYGON

# 创建客户端
client = ClobClient(host, key=key, chain_id=chain_id)

# 自动创建或派生 API 凭证
api_creds = client.create_or_derive_api_creds()
client.set_api_creds(api_creds)


# 打印所有属性
print("API 凭证对象的所有属性:")
print(dir(api_creds))



# 打印生成的凭证（可选，用于调试）
print("API Key:", api_creds.api_key)
print("API Secret:", api_creds.api_secret)
print("API Passphrase:", api_creds.api_passphrase)













import os

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds
from dotenv import load_dotenv
from py_clob_client.constants import AMOY

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:9788'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:9788'



def main():
    host = "https://clob.polymarket.com"
    key = 'f14af2100840da79a81fd16a5e7577f25f425192a5cc0b009422853bc42658c4'
    creds = ApiCreds(
        api_key='09369d75-ba83-dc0e-aae0-a030fdfd9b72',
        api_secret='UkrywXphcs_1651ekaLsUbhmodtazfoQdAl2dMD6fFE=',
        api_passphrase='e984ff9344638352a6b96536450e48d350a0a23b977165b94f114a7d0f08da1a',
    )
    chain_id = AMOY
    client = ClobClient(host, key=key, chain_id=chain_id, creds=creds)

    # 获取市场数据并保存到文件
    markets_data = client.get_markets()
    
    # 将数据写入txt文件
    with open('markets_data.txt', 'w', encoding='utf-8') as f:
        f.write(str(markets_data))  # 将数据转换为字符串并写入
    
    # 同时打印到控制台
    print(markets_data)




    
    # 获取简化市场数据
    simplified_markets = client.get_simplified_markets()
    
    # 将数据写入txt文件
    with open('simplified_markets.txt', 'w', encoding='utf-8') as f:
        f.write(str(simplified_markets))  # 将数据转换为字符串并写入
    
    # 同时打印到控制台
    print(simplified_markets)




    
    print(client.get_sampling_markets())
    print(client.get_sampling_simplified_markets())
    print(client.get_market("condition_id"))

    print("Done!")


main()