import React, { useState, useEffect } from 'react';
import { GridParams } from '../types';
import './GridForm.css';

interface Props {
  onQueryMarket: (params: GridParams) => void;
  onGridAction: (params: GridParams) => void;
  onRestartGrid: () => void;
  gridStatus: 'stopped' | 'running';
}

export const GridForm: React.FC<Props> = ({
  onQueryMarket,
  onGridAction,
  onRestartGrid,
  gridStatus,
}) => {
  const [params, setParams] = useState<GridParams>({
    condition_id: '',
    initial_buy: 6,
    each_buy: 5,
    grid_max_price: 1,
    grid_min_price: 0,
    grid_interval: 0.01,
    buy_order_standby_max: 1,
    yes_or_no: 'Yes',
  });

  const [isValid, setIsValid] = useState(false);

  useEffect(() => {
    const validate = () => {
      return (
        params.condition_id.trim() !== '' &&
        params.initial_buy >= 6 &&
        params.initial_buy % 2 === 0 &&
        params.each_buy >= 5 &&
        params.grid_max_price >= 0 &&
        params.grid_max_price <= 1 &&
        params.grid_min_price >= 0 &&
        params.grid_min_price <= 1 &&
        params.grid_interval > 0 &&
        params.grid_interval < 0.1 &&
        params.buy_order_standby_max > 0
      );
    };
    setIsValid(validate());
  }, [params]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setParams(prev => ({
      ...prev,
      [name]: type === 'number' ? Number(value) : value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!isValid) return;
    onQueryMarket(params);
  };

  const handleGridAction = () => {
    if (!isValid) return;
    if (gridStatus === 'stopped') {
      onGridAction(params);
    } else {
      onGridAction(params);
    }
  };

  return (
    <form className="grid-form" onSubmit={handleSubmit}>
      {/* Condition ID */}
      <div className="form-group">
        <label>Condition ID:</label>
        <input
          type="text"
          name="condition_id"
          value={params.condition_id}
          onChange={handleChange}
          required
        />
      </div>

      {/* Initial Buy */}
      <div className="form-group">
        <label>Initial Buy (≥6, 偶数):</label>
        <input
          type="number"
          name="initial_buy"
          value={params.initial_buy}
          onChange={handleChange}
          min="6"
          step="2"
          required
        />
      </div>

      {/* Each Buy */}
      <div className="form-group">
        <label>Each Buy (≥5):</label>
        <input
          type="number"
          name="each_buy"
          value={params.each_buy}
          onChange={handleChange}
          min="5"
          required
        />
      </div>

      {/* Grid Max Price */}
      <div className="form-group">
        <label>Grid Max Price (0-1):</label>
        <input
          type="number"
          name="grid_max_price"
          value={params.grid_max_price}
          onChange={handleChange}
          min="0"
          max="1"
          step="0.01"
          required
        />
      </div>

      {/* Grid Min Price */}
      <div className="form-group">
        <label>Grid Min Price (0-1):</label>
        <input
          type="number"
          name="grid_min_price"
          value={params.grid_min_price}
          onChange={handleChange}
          min="0"
          max="1"
          step="0.01"
          required
        />
      </div>

      {/* Grid Interval */}
      <div className="form-group">
        <label>Grid Interval (0-0.1):</label>
        <input
          type="number"
          name="grid_interval"
          value={params.grid_interval}
          onChange={handleChange}
          min="0"
          max="0.1"
          step="0.001"
          required
        />
      </div>

      {/* Buy Order Standby Max */}
      <div className="form-group">
        <label>Buy Order Standby Max:</label>
        <input
          type="number"
          name="buy_order_standby_max"
          value={params.buy_order_standby_max}
          onChange={handleChange}
          min="1"
          required
        />
      </div>

      {/* Yes or No Selection */}
      <div className="form-group">
        <label>Direction:</label>
        <select
          name="yes_or_no"
          value={params.yes_or_no}
          onChange={handleChange}
          required
        >
          <option value="Yes">Yes</option>
          <option value="No">No</option>
        </select>
      </div>

      {/* 按钮组 */}
      <div className="form-actions">
        <button 
          type="submit" 
          disabled={!isValid}
          className="query-button"
        >
          查询市场
        </button>
        <button
          type="button"
          disabled={!isValid}
          className="grid-button"
          onClick={handleGridAction}
        >
          {gridStatus === 'stopped' ? '开启网格' : '终止网格'}
        </button>
        {gridStatus === 'stopped' && (
          <button
            type="button"
            className="restart-button"
            onClick={onRestartGrid}
          >
            重启网格
          </button>
        )}
      </div>
    </form>
  );
}; 