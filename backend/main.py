from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from grid_transaction import GridTrading, GridParams

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 存储正在运行的网格交易实例
active_grid_traders: Dict[str, GridTrading] = {}

class GridParamsModel(BaseModel):
    """网格参数请求模型"""
    condition_id: str
    initial_buy: int
    each_buy: int
    grid_max_price: float
    grid_min_price: float
    grid_interval: float
    buy_order_standby_max: int
    yes_or_no: str

@app.post("/api/query_market")
async def query_market(params: GridParamsModel):
    """查询市场信息"""
    try:
        # 创建临时GridTrading实例来查询市场
        grid_params = GridParams(**params.dict())
        trader = GridTrading(grid_params)
        market_info = trader.get_market_info()
        return {"success": True, "data": market_info}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/start_grid")
async def start_grid(params: GridParamsModel):
    """启动网格交易"""
    try:
        grid_params = GridParams(**params.dict())
        trader = GridTrading(grid_params)
        
        # 存储交易实例
        active_grid_traders[params.condition_id] = trader
        
        # 启动交易
        success = trader.start()
        return {"success": success, "message": "网格交易已启动" if success else "启动失败"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/stop_grid/{condition_id}")
async def stop_grid(condition_id: str):
    """停止网格交易"""
    if condition_id not in active_grid_traders:
        raise HTTPException(status_code=404, detail="未找到运行中的网格交易")
    
    trader = active_grid_traders[condition_id]
    trader.stop()
    del active_grid_traders[condition_id]
    return {"success": True, "message": "网格交易已停止"}

@app.post("/api/restart_grid/{condition_id}")
async def restart_grid(condition_id: str):
    """重启网格交易"""
    if condition_id not in active_grid_traders:
        raise HTTPException(status_code=404, detail="未找到可重启的网格交易")
    
    trader = active_grid_traders[condition_id]
    success = trader.restart()
    return {"success": success, "message": "网格交易已重启" if success else "重启失败"} 