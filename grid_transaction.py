import os
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY, SELL
from py_clob_client.constants import AMOY
from dotenv import load_dotenv

@dataclass
class GridParams:
    """网格交易参数类"""
    condition_id: str
    initial_buy: int
    each_buy: int
    grid_max_price: float
    grid_min_price: float
    grid_interval: float
    buy_order_standby_max: int
    yes_or_no: str

class GridTrading:
    def __init__(self, params: GridParams):
        """初始化网格交易类"""
        self.params = params
        self.buy_order_monitor: Dict[float, Dict] = {}  # 买单监控列表
        self.sell_order_and_corresponding_buy_price: Dict[str, float] = {}  # 卖单与对应买入价格的映射
        self.token_id = None
        self.current_price = None
        self.effect_grid_list = []
        self.is_running = False
        self._init_client()

    def _init_client(self):
        """初始化交易客户端"""
        host = "https://clob.polymarket.com"
        key = 'f14af2100840da79a81fd16a5e7577f25f425192a5cc0b009422853bc42658c4'
        creds = ApiCreds(
            api_key='09369d75-ba83-dc0e-aae0-a030fdfd9b72',
            api_secret='UkrywXphcs_1651ekaLsUbhmodtazfoQdAl2dMD6fFE=',
            api_passphrase='e984ff9344638352a6b96536450e48d350a0a23b977165b94f114a7d0f08da1a',
        )
        self.client = ClobClient(host, key=key, chain_id=AMOY, creds=creds)

    def get_market_info(self) -> List[Dict]:
        """获取市场信息"""
        market_info = self.client.get_market(self.params.condition_id)
        if not market_info:
            raise Exception("无法获取市场信息")
        
        tokens = market_info['tokens']
        return [{'outcome': token['outcome'], 'price': token['price']} for token in tokens]

    def _initialize_trading(self):
        """初始化交易参数"""
        market_info = self.client.get_market(self.params.condition_id)['tokens']
        for token in market_info:
            if token['outcome'].lower() == self.params.yes_or_no.lower():
                self.token_id = token['token_id']
                self.current_price = token['price']
                break

    def _create_initial_order(self) -> Optional[str]:
        """创建初始买单"""
        if not self.token_id:
            return None
        
        buy_price = min(self.current_price + 0.05, 0.99)
        order_args = OrderArgs(
            price=buy_price,
            size=self.params.initial_buy,
            side=BUY,
            token_id=self.token_id
        )
        
        resp = self.client.create_and_post_order(order_args)
        if resp['success']:
            self.buy_order_monitor[buy_price] = {
                "order_id": resp['orderID'],
                "status": "买单未成交"
            }
            return resp['orderID']
        return None

    def _monitor_orders(self):
        """监控订单状态"""
        while self.is_running:
            # 监控买单
            for price, order_info in list(self.buy_order_monitor.items()):
                order = self.client.get_order(order_info['order_id'])
                if order['size_matched'] == order['original_size']:
                    if order_info['status'] == "买单未成交":
                        # 买单成交，创建对应的卖单
                        sell_price = min(price + self.params.grid_interval, 1)
                        sell_order = self._create_sell_order(
                            sell_price, 
                            int(order['original_size']), 
                            order['asset_id']
                        )
                        if sell_order:
                            self.buy_order_monitor[price]['status'] = "买单成交卖单未成交"
                            self.sell_order_and_corresponding_buy_price[sell_order] = price

            # 监控卖单
            for order_id, buy_price in list(self.sell_order_and_corresponding_buy_price.items()):
                order = self.client.get_order(order_id)
                if order['size_matched'] == order['original_size']:
                    # 卖单成交，清理相关记录
                    del self.sell_order_and_corresponding_buy_price[order_id]
                    del self.buy_order_monitor[buy_price]

            # 更新网格买单
            self._update_grid_orders()
            time.sleep(1)  # 避免过于频繁的API调用

    def _create_sell_order(self, price: float, size: int, token_id: str) -> Optional[str]:
        """创建卖单"""
        order_args = OrderArgs(
            price=price,
            size=size,
            side=SELL,
            token_id=token_id
        )
        resp = self.client.create_and_post_order(order_args)
        return resp['orderID'] if resp['success'] else None

    def _update_grid_orders(self):
        """更新网格订单"""
        # 获取最新市场价格
        market_info = self.get_market_info()
        for info in market_info:
            if info['outcome'].lower() == self.params.yes_or_no.lower():
                self.current_price = info['price']
                break

        # 计算需要的网格线
        available_grids = [
            price for price in self.effect_grid_list 
            if price < self.current_price
        ][:self.params.buy_order_standby_max]

        # 创建新的买单
        for grid_price in available_grids:
            if grid_price not in self.buy_order_monitor:
                self._create_grid_buy_order(grid_price)

        # 清理多余的未成交买单
        self._cleanup_excess_orders()

    def _create_grid_buy_order(self, price: float):
        """在网格线位置创建买单"""
        order_args = OrderArgs(
            price=price,
            size=self.params.each_buy,
            side=BUY,
            token_id=self.token_id
        )
        resp = self.client.create_and_post_order(order_args)
        if resp['success']:
            self.buy_order_monitor[price] = {
                "order_id": resp['orderID'],
                "status": "买单未成交"
            }

    def _cleanup_excess_orders(self):
        """清理多余的未成交买单"""
        unfilled_orders = [
            (price, info) for price, info in self.buy_order_monitor.items()
            if info['status'] == "买单未成交"
        ]
        unfilled_orders.sort(key=lambda x: x[0])
        
        while len(unfilled_orders) > self.params.buy_order_standby_max:
            price, info = unfilled_orders.pop(0)
            self.client.cancel(info['order_id'])
            del self.buy_order_monitor[price]

    def start(self):
        """启动网格交易"""
        if self.is_running:
            return False
        
        self.is_running = True
        self._initialize_trading()
        initial_order_id = self._create_initial_order()
        if initial_order_id:
            self._monitor_orders()
        return True

    def stop(self):
        """停止网格交易"""
        self.is_running = False

    def restart(self):
        """重启网格交易"""
        if not self.is_running:
            return self.start()
        return False
























