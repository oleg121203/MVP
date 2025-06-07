export function calculateAirflow(velocity, diameter) {
  const radius = diameter / 2;
  return velocity * Math.PI * radius * radius; // Q = V * π * r²
}

export function calculateHeatTransfer(flowRate, density, specificHeat, tempDiff) {
  // Q = m * cp * ΔT (W)
  // m = ρ * V (kg/s)
  const massFlow = flowRate * density;
  return massFlow * specificHeat * tempDiff;
}

export function calculatePressureDrop(flowRate, ductDiameter, ductLength, roughness) {
  // Darcy-Weisbach equation approximation
  const frictionFactor = 0.11 * Math.pow(roughness / ductDiameter + 68 / flowRate, 0.25);
  return (
    (frictionFactor * (ductLength / ductDiameter) * Math.pow(flowRate, 2)) /
    (2 * 9.81 * ductDiameter)
  );
}

export function calculateSystemEfficiency(heatTransfer, inputPower) {
  // COP = Q / W
  return heatTransfer / inputPower;
}

export function calculateDuctSize(airflow, velocity) {
  // A = Q / V
  const area = airflow / velocity;
  // Convert to diameter for circular ducts
  return 2 * Math.sqrt(area / Math.PI);
}
