import os

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds
from dotenv import load_dotenv
from py_clob_client.constants import AMOY

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:9788'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:9788'

load_dotenv()

def get_conditional_token_info(condition_id: str):
    """
    获取一个投资标的（一个条件token）的信息。

    Args:
        condition_id: 投资标的的 condition_id。

    Returns:
        投资标的的信息，如果找不到则返回 None。
    """
    host = "https://clob.polymarket.com"  # 或 "http://localhost:8080" 用于本地测试
    key = 'f14af2100840da79a81fd16a5e7577f25f425192a5cc0b009422853bc42658c4'
    creds = ApiCreds(
        api_key='09369d75-ba83-dc0e-aae0-a030fdfd9b72',
        api_secret='UkrywXphcs_1651ekaLsUbhmodtazfoQdAl2dMD6fFE=',
        api_passphrase='e984ff9344638352a6b96536450e48d350a0a23b977165b94f114a7d0f08da1a',
    )
    chain_id = AMOY
    client = ClobClient(host, key=key, chain_id=chain_id, creds=creds)

    # 获取特定 condition_id 的市场信息
    market_info = client.get_market(condition_id)

    if market_info:
        return market_info['tokens']
    else:
        print(f"Market with condition_id {condition_id} not found.")
        return None


if __name__ == "__main__":
    # 示例：使用 condition_id 获取投资标的信息
    condition_id_to_find = "0x20dbe01ca6d9787c9d203484ee77ffdf47c13a454ce785d9fd70c9cf8eb1fc62"  # 替换为你感兴趣的标的的 condition_id
    market_info = get_conditional_token_info(condition_id_to_find)
    print(market_info)




















    # 获取订单状态
import os
import time

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, OpenOrderParams, OrderArgs
from dotenv import load_dotenv
from py_clob_client.constants import AMOY
from py_clob_client.order_builder.constants import BUY

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:9788'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:9788'

load_dotenv()

def get_order_status(client: ClobClient, order_id: str):
    """
    Fetches and prints the status of an order.

    Args:
        client: The ClobClient instance.
        order_id: The ID of the order to query.
    """
    try:
        order = client.get_order(order_id)
        print("Order Status:")
        print(order)

        if order and 'state' in order:
            state = order['state']
            if state == "Open":
                print("Order is open and waiting to be filled.")
            elif state == "Filled":
                print("Order has been fully filled.")
            elif state == "Canceled":
                print("Order has been canceled.")
            elif state == "Expired":
                print("Order has expired.")
            else:
                print(f"Unknown order state: {state}")

            # Additional details you might want to check
            if 'fills' in order:
                print("Fills:")
                for fill in order['fills']:
                    print(fill)
        else:
            print(f"Order with ID {order_id} not found or unexpected response format.")

    except Exception as e:
        print(f"An error occurred while fetching order status: {e}")



host = "https://clob.polymarket.com"  # or "http://localhost:8080" for local testing
key = 'f14af2100840da79a81fd16a5e7577f25f425192a5cc0b009422853bc42658c4'
creds = ApiCreds(
    api_key='09369d75-ba83-dc0e-aae0-a030fdfd9b72',
    api_secret='UkrywXphcs_1651ekaLsUbhmodtazfoQdAl2dMD6fFE=',
    api_passphrase='e984ff9344638352a6b96536450e48d350a0a23b977165b94f114a7d0f08da1a',
)
chain_id = AMOY
client = ClobClient(host, key=key, chain_id=chain_id, creds=creds)


# --- Example: Placing an order and then querying its status ---
try:
    # Replace with your order details
    order_args = OrderArgs(
        price=0.5,
        size=1,
        side=BUY,
        token_id="57340959878398421678357543264767127245404802056106050362156330852499865274040"
    )
    
    # Place the order
    response = client.create_and_post_order(order_args)
    print("Order placed successfully. Response:")
    print(response)
    
    if response and 'orderID' in response:
        order_id = response['orderID']
        print(f"Order ID: {order_id}")
        
        # Wait for a few seconds to allow the order to be processed
        time.sleep(5)

        # Get the order status using the order_id
        get_order_status(client, order_id)
    else:
        print("Could not retrieve order ID from response.")

except Exception as e:
    print(f"An error occurred: {e}")










# 不断监控订单状态

import os
import time

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds
from dotenv import load_dotenv
from py_clob_client.constants import AMOY

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:9788'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:9788'

load_dotenv()

def get_order_status(client: ClobClient, order_id: str):
    """
    Fetches and prints the status of an order.

    Args:
        client: The ClobClient instance.
        order_id: The ID of the order to query.
    """
    try:
        order = client.get_order(order_id)
        print("-" * 30)  # Print a separator for clarity
        print(f"Status for order {order_id}:")
        if order and 'state' in order:
            print(f"  State: {order['state']}")
            if 'fills' in order:
                print(f"  Filled quantity: {float(order['filled_size'])/1e6}")
                print("  Fills:")
                for fill in order['fills']:
                    print(f"    - Price: {float(fill['price'])/1e6}, Quantity: {float(fill['size'])/1e6}, Timestamp: {fill['timestamp']}")
            if 'order' in order:
                print(f"  Created Time: {order['order']['time']}")
                print(f"  Price: {float(order['order']['price'])/1e6}")
                print(f"  Original Quantity: {float(order['order']['size'])/1e6}")
            else:
                print("  Order details not found in the response.")
        else:
            print(f"  Order with ID {order_id} not found or unexpected response format.")
        print("-" * 30)  # Print a separator for clarity

    except Exception as e:
        print(f"An error occurred while fetching order status: {e}")

def monitor_order_status(client: ClobClient, order_id: str, poll_interval: int = 5):
    """
    Monitors the status of an order at regular intervals.

    Args:
        client: The ClobClient instance.
        order_id: The ID of the order to monitor.
        poll_interval: The time interval (in seconds) between status checks.
    """
    print(f"Monitoring order {order_id} every {poll_interval} seconds...")
    try:
        while True:
            order = client.get_order(order_id)
            if order and 'state' in order:
                current_state = order['state']
                get_order_status(client, order_id)

                if current_state == "Filled" or current_state == "Canceled" or current_state == "Expired":
                    print(f"Order {order_id} has reached a terminal state: {current_state}")
                    break  # Exit the loop if the order is filled, canceled, or expired

            else:
                print(f"Order {order_id} not found or unexpected response format.")

            time.sleep(poll_interval)

    except Exception as e:
        print(f"An error occurred during order monitoring: {e}")

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

    order_id_to_monitor = '0xcd696e953a7f5b20abf2723d0426a08dd242ef7f79d6a98e20b8bac5637ab9bf'  # Replace with your order ID
    order = client.get_order(order_id_to_monitor)

    print(order)




    # Monitor the order status
    monitor_order_status(client, order_id_to_monitor)





