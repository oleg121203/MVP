from fastapi import FastAPI
import time
from .optimization_algorithms import optimize_supply_chain  # Import from sibling module

app = FastAPI()

@app.get("/monitor-supply-chain")
async def monitor_supply_chain(costs: list[float] = []):
    optimized_cost = optimize_supply_chain(costs)
    return {"status": "monitoring active", "timestamp": time.time(), "optimized_cost": optimized_cost}

# To run: uvicorn src.supply_chain.real_time_monitoring:app --reload
