export interface GridParams {
  condition_id: string;
  initial_buy: number;
  each_buy: number;
  grid_max_price: number;
  grid_min_price: number;
  grid_interval: number;
  buy_order_standby_max: number;
  yes_or_no: 'Yes' | 'No';
}

export interface MarketInfo {
  outcome: string;
  price: number;
} 