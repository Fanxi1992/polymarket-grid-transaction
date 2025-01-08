import React from 'react';
import { MarketInfo as MarketInfoType } from '../types';
import './MarketInfo.css';

interface Props {
  data: MarketInfoType[];
}

export const MarketInfo: React.FC<Props> = ({ data }) => {
  return (
    <div className="market-info">
      <h2>市场信息</h2>
      {data.map((info, index) => (
        <div key={index} className="market-row">
          <span className="outcome">{info.outcome}:</span>
          <span className="price">{info.price.toFixed(4)}</span>
        </div>
      ))}
    </div>
  );
}; 