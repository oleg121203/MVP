from typing import Dict, List, Optional
import pandas as pd
from sklearn.linear_model import LinearRegression
from joblib import load, dump
import os

from ..ai.vector_db_service import VectorDBService

class CostOptimizationService:
    def __init__(self, vector_db_service: VectorDBService):
        self.model = self._load_model()
        self.vector_db_service = vector_db_service
        self.labor_cost_per_hour = float(os.getenv('LABOR_COST_PER_HOUR', 50.0))  # Default $50/hour
        self.energy_cost_per_kwh = float(os.getenv('ENERGY_COST_PER_KWH', 0.12))  # Default $0.12/kWh

    def _load_model(self) -> LinearRegression:
        """
        Load the cost prediction model from file or initialize a new one.
        """
        try:
            return load("src/fastapi_app/ai/models/cost_optimization_model.joblib")
        except Exception as e:
            return LinearRegression()

    def analyze_costs(self, project_data: Dict) -> Dict:
        """
        Analyze project costs based on specifications and current materials.

        Args:
            project_data: Dictionary containing project specifications and materials.

        Returns:
            Dictionary with cost breakdown and potential savings.
        """
        # Extract project parameters
        area_sqm = project_data.get('specifications', {}).get('area_sqm', 100.0)
        materials = project_data.get('current_materials', [])
        energy_consumption_kwh = project_data.get('specifications', {}).get('energy_consumption_kwh', 1000.0)
        installation_hours = project_data.get('specifications', {}).get('installation_hours', 40.0)

        # Calculate material costs
        material_cost = sum(mat.get('cost_usd', 0.0) for mat in materials)

        # Calculate labor costs
        labor_cost = installation_hours * self.labor_cost_per_hour

        # Calculate energy costs (assuming annual cost for simplicity)
        energy_cost = energy_consumption_kwh * self.energy_cost_per_kwh

        # Total cost
        total_cost = material_cost + labor_cost + energy_cost

        # Estimate potential savings by querying for cheaper materials
        potential_savings = 0.0
        suggestions = []
        for mat in materials:
            query = f"{mat.get('name', '')} {mat.get('description', '')}"
            max_cost = mat.get('cost_usd', 0.0) * 0.8  # Look for materials up to 20% cheaper
            search_results = self.vector_db_service.search_similar(
                query=query,
                top_k=3,
                filter={'cost_usd': {'$lte': max_cost}}
            )
            for result in search_results:
                if result['score'] > 0.8:  # High similarity threshold
                    savings = mat.get('cost_usd', 0.0) - result['metadata'].get('cost_usd', 0.0)
                    if savings > 0:
                        potential_savings += savings
                        suggestions.append({
                            'original': mat.get('name', 'Unknown'),
                            'suggested': result['metadata'].get('name', 'Unknown'),
                            'savings_usd': savings,
                            'similarity': result['score']
                        })

        return {
            'total_cost_usd': total_cost,
            'breakdown': {
                'materials_usd': material_cost,
                'labor_usd': labor_cost,
                'energy_usd': energy_cost
            },
            'potential_savings_usd': potential_savings,
            'suggestions': suggestions
        }

    def compare_scenarios(self, scenarios: List[Dict]) -> List[Dict]:
        """
        Compare multiple cost scenarios for a project.

        Args:
            scenarios: List of dictionaries representing different scenarios with materials and settings.

        Returns:
            List of dictionaries with cost analysis for each scenario.
        """
        results = []
        for scenario in scenarios:
            name = scenario.get('name', 'Unnamed Scenario')
            materials = scenario.get('materials', [])
            settings = scenario.get('settings', {})

            # Calculate costs for this scenario
            material_cost = sum(mat.get('cost_usd', 0.0) for mat in materials)
            labor_hours = settings.get('labor_hours', 40.0)
            energy_kwh = settings.get('energy_consumption_kwh', 1000.0)
            labor_cost = labor_hours * self.labor_cost_per_hour
            energy_cost = energy_kwh * self.energy_cost_per_kwh
            total_cost = material_cost + labor_cost + energy_cost

            results.append({
                'name': name,
                'total_cost_usd': total_cost,
                'breakdown': {
                    'materials_usd': material_cost,
                    'labor_usd': labor_cost,
                    'energy_usd': energy_cost
                }
            })

        return results

    def get_material_suggestions(self, query: str, max_cost_usd: Optional[float] = None, top_k: int = 5) -> List[Dict]:
        """
        Suggest cost-effective materials based on a query.

        Args:
            query: Search query for materials.
            max_cost_usd: Maximum cost filter for suggestions.
            top_k: Number of top results to return.

        Returns:
            List of dictionaries with suggested materials.
        """
        filter_data = {'cost_usd': {'$lte': max_cost_usd}} if max_cost_usd else None
        return self.vector_db_service.search_similar(query, top_k, filter_data)

    def train_model(self, training_data: List[Dict]) -> None:
        """
        Train the cost prediction model with new data.

        Args:
            training_data: List of dictionaries containing project parameters and actual costs.
        """
        df = pd.DataFrame(training_data)
        if 'total_cost' in df.columns:
            X = df.drop(['total_cost'], axis=1)
            y = df['total_cost']
            self.model.fit(X, y)
            dump(self.model, "src/fastapi_app/ai/models/cost_optimization_model.joblib")
