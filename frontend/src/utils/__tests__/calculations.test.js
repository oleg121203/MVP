import { calculateAirflow, calculateHeatTransfer } from '../calculations';

describe('HVAC Calculations', () => {
  test('calculates airflow correctly', () => {
    expect(calculateAirflow(2.5, 0.3)).toBeCloseTo(0.176, 3);
    expect(calculateAirflow(0, 0.3)).toBe(0);
  });

  test('calculates heat transfer correctly', () => {
    expect(calculateHeatTransfer(0.176, 1.2, 1.005, 10)).toBeCloseTo(2.123, 2);
  });
});
