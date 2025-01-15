import { GridParams, MarketInfo } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

export const queryMarket = async (params: GridParams): Promise<MarketInfo[]> => {
  const response = await fetch(`${API_BASE_URL}/query_market`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
  });
  const data = await response.json();
  if (!data.success) {
    throw new Error(data.detail || '查询市场失败');
  }
  return data.data;
};

export const startGrid = async (params: GridParams): Promise<void> => {
  const response = await fetch(`${API_BASE_URL}/start_grid`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
  });
  const data = await response.json();
  if (!data.success) {
    throw new Error(data.detail || '启动网格失败');
  }
};

export const stopGrid = async (conditionId: string): Promise<void> => {
  const response = await fetch(`${API_BASE_URL}/stop_grid/${conditionId}`, {
    method: 'POST',
  });
  const data = await response.json();
  if (!data.success) {
    throw new Error(data.detail || '停止网格失败');
  }
};

export const restartGrid = async (conditionId: string): Promise<void> => {
  const response = await fetch(`${API_BASE_URL}/restart_grid/${conditionId}`, {
    method: 'POST',
  });
  const data = await response.json();
  if (!data.success) {
    throw new Error(data.detail || '重启网格失败');
  }
}; 