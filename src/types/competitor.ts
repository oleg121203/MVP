export interface Competitor {
  id: string;
  name: string;
  marketShare: number;
  priceComparison: {
    average: number;
    range: [number, number];
  };
  lastUpdated: string;
}
