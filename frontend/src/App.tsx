import React, { useState } from 'react';
import { GridForm } from './components/GridForm';
import { MarketInfo } from './components/MarketInfo.tsx';
import { GridParams, MarketInfo as MarketInfoType } from './types';
import { queryMarket, startGrid, stopGrid, restartGrid } from './services/api';
import './App.css';

const App: React.FC = () => {
  const [marketInfo, setMarketInfo] = useState<MarketInfoType[]>([]);
  const [gridStatus, setGridStatus] = useState<'stopped' | 'running'>('stopped');
  const [currentParams, setCurrentParams] = useState<GridParams | null>(null);

  const handleQueryMarket = async (params: GridParams) => {
    try {
      const data = await queryMarket(params);
      setMarketInfo(data);
    } catch (error) {
      alert(error instanceof Error ? error.message : '查询市场失败');
    }
  };

  const handleGridAction = async (params: GridParams) => {
    try {
      if (gridStatus === 'stopped') {
        await startGrid(params);
        setGridStatus('running');
        setCurrentParams(params);
      } else if (gridStatus === 'running') {
        await stopGrid(params.condition_id);
        setGridStatus('stopped');
      }
    } catch (error) {
      alert(error instanceof Error ? error.message : '操作失败');
    }
  };

  const handleRestartGrid = async () => {
    if (!currentParams) return;
    try {
      await restartGrid(currentParams.condition_id);
      setGridStatus('running');
    } catch (error) {
      alert(error instanceof Error ? error.message : '重启失败');
    }
  };

  return (
    <div className="app-container">
      <h1>Polymarket 网格交易策略</h1>
      <GridForm 
        onQueryMarket={handleQueryMarket}
        onGridAction={handleGridAction}
        gridStatus={gridStatus}
        onRestartGrid={handleRestartGrid}
      />
      {marketInfo.length > 0 && <MarketInfo data={marketInfo} />}
    </div>
  );
};

export default App;
