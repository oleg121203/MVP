from typing import Dict, List, Optional
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from joblib import load, dump
import json
import os
from pathlib import Path

class ProjectAnalysisService:
    def __init__(self):
        self.model = self._load_model()
        self.compliance_rules = self._load_compliance_rules()

    def _load_model(self) -> GradientBoostingRegressor:
        try:
            return load("src/fastapi_app/ai/models/project_analysis_model.joblib")
        except Exception as e:
            # Initialize new model if none exists
            return GradientBoostingRegressor(n_estimators=100)

    def _load_compliance_rules(self) -> Dict:
        """
        Load compliance rules from a configuration file or environment variables.
        
        Returns:
            Dict: Compliance rules dictionary
        """
        config_file = Path('src/fastapi_app/config/compliance_rules.json')
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading compliance rules from file: {e}")
        
        # Fallback to environment variables or default values
        return {
            "max_energy_consumption": float(os.getenv('MAX_ENERGY_CONSUMPTION', 1000)),  # kWh per sqm
            "min_ventilation_rate": float(os.getenv('MIN_VENTILATION_RATE', 0.35)),    # ACH (Air Changes per Hour)
            "max_noise_level": float(os.getenv('MAX_NOISE_LEVEL', 45)),                # dB
        }

    def analyze_project(self, project_data: Dict) -> Dict:
        """
        Analyze project data to provide insights and recommendations.

        Args:
            project_data: Dict containing project parameters such as:
                - area (sqm)
                - occupancy
                - climate_zone
                - system_type
                - energy_consumption (kWh)
                - ventilation_rate (ACH)
                - noise_level (dB)

        Returns:
            Dict with analysis results including compliance status and recommendations.
        """
        # Convert project data to DataFrame for model prediction
        X = pd.DataFrame([project_data])

        # Predict optimal parameters
        predictions = self.model.predict(X.drop(["energy_consumption", "ventilation_rate", "noise_level"], axis=1, errors="ignore"))

        # Check compliance with rules
        compliance_issues = self._check_compliance(project_data)

        return {
            "compliance_status": "Compliant" if not compliance_issues else "Non-Compliant",
            "compliance_issues": compliance_issues,
            "recommendations": {
                "optimal_system_type": predictions[0][0] if len(predictions) > 0 else "N/A",
                "energy_savings_potential": predictions[0][1] if len(predictions) > 1 else 0,
                "priority_actions": self._generate_recommendations(compliance_issues, predictions[0])
            }
        }

    def _check_compliance(self, project_data: Dict) -> List[str]:
        issues = []
        if project_data.get("energy_consumption", 0) > self.compliance_rules["max_energy_consumption"]:
            issues.append(f"Energy consumption exceeds limit by {project_data.get('energy_consumption', 0) - self.compliance_rules['max_energy_consumption']} kWh/sqm")
        if project_data.get("ventilation_rate", 0) < self.compliance_rules["min_ventilation_rate"]:
            issues.append(f"Ventilation rate below minimum by {self.compliance_rules['min_ventilation_rate'] - project_data.get('ventilation_rate', 0)} ACH")
        if project_data.get("noise_level", 0) > self.compliance_rules["max_noise_level"]:
            issues.append(f"Noise level exceeds limit by {project_data.get('noise_level', 0) - self.compliance_rules['max_noise_level']} dB")
        return issues

    def _generate_recommendations(self, compliance_issues: List[str], predictions: List[float]) -> List[str]:
        recommendations = []
        if any("Energy consumption" in issue for issue in compliance_issues):
            recommendations.append("Consider upgrading to a more energy-efficient HVAC system.")
        if any("Ventilation rate" in issue for issue in compliance_issues):
            recommendations.append("Increase ventilation by adjusting system settings or upgrading equipment.")
        if any("Noise level" in issue for issue in compliance_issues):
            recommendations.append("Install noise reduction measures or replace noisy components.")
        if predictions[1] > 0:
            recommendations.append(f"Potential energy savings of {predictions[1]:.2f} kWh with optimized settings.")
        return recommendations

    def train_model(self, training_data: List[Dict]) -> None:
        """
        Train the analysis model with new project data.

        Args:
            training_data: List of dictionaries containing project parameters and outcomes.
        """
        df = pd.DataFrame(training_data)
        if "optimal_system_type" in df.columns and "energy_savings" in df.columns:
            X = df.drop(["optimal_system_type", "energy_savings"], axis=1)
            y = df[["optimal_system_type", "energy_savings"]]
            self.model.fit(X, y)
            dump(self.model, "ai/models/project_analysis_model.joblib")
