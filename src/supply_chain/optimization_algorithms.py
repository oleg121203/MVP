def optimize_supply_chain(costs):
    '''Simple optimization algorithm for supply chain costs. Returns an optimized cost estimate.''' 
    if not costs:
        return 0.0
    average_cost = sum(costs) / len(costs)
    optimized_cost = average_cost * 0.85  # Apply a 15% optimization factor as a placeholder
    return optimized_cost
