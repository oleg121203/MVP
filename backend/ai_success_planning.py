import asyncio
import sqlite3
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class SuccessPlan:
    plan_id: str
    customer_id: str
    created_date: str
    updated_date: str
    goals: Dict[str, Any]
    milestones: Dict[str, Any]
    status: str
    risk_factors: Dict[str, float]

@dataclass
class SuccessPrediction:
    prediction_id: str
    customer_id: str
    prediction_type: str
    predicted_date: str
    predicted_value: float
    confidence_score: float
    influencing_factors: Dict[str, float]

class AISuccessPlanning:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self._initialize_db()

    def _initialize_db(self) -> None:
        """Initialize database connection and create planning tables if not exists."""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        # Success Plans Table (already exists in customer_success_database.py, but ensuring)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS success_plans (
            plan_id TEXT PRIMARY KEY,
            customer_id TEXT,
            created_date TEXT,
            updated_date TEXT,
            goals TEXT,
            milestones TEXT,
            status TEXT,
            risk_factors TEXT,
            FOREIGN KEY (customer_id) REFERENCES customer_success(customer_id)
        )
        """)
        # Success Predictions Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS success_predictions (
            prediction_id TEXT PRIMARY KEY,
            customer_id TEXT,
            prediction_type TEXT,
            predicted_date TEXT,
            predicted_value REAL,
            confidence_score REAL,
            influencing_factors TEXT,
            FOREIGN KEY (customer_id) REFERENCES customer_success(customer_id)
        )
        """)
        self.conn.commit()

    async def _simulate_ai_planning(self, input_data: Dict[str, Any], planning_type: str) -> Dict[str, Any]:
        """Simulate AI processing for success planning and predictions."""
        await asyncio.sleep(1)  # Simulate async AI processing
        if planning_type == "success_plan":
            return {
                "plan_id": f"plan_{hash(str(input_data))}",
                "goals": {
                    "primary_goal": "Achieve 90% product adoption within 6 months",
                    "secondary_goal": "Increase user engagement by 20%",
                    "tertiary_goal": "Reduce time-to-value to under 30 days"
                },
                "milestones": {
                    "onboarding_complete": {"target_date": "2025-07-01", "status": "not_started"},
                    "first_value_realized": {"target_date": "2025-07-15", "status": "not_started"},
                    "full_adoption": {"target_date": "2025-12-01", "status": "not_started"}
                },
                "status": "draft",
                "risk_factors": {
                    "low_engagement": 0.3,
                    "technical_issues": 0.2,
                    "budget_constraints": 0.15,
                    "staff_turnover": 0.1,
                    "competitor_threat": 0.05
                }
            }
        elif planning_type == "churn_prediction":
            return {
                "prediction_id": f"pred_churn_{hash(str(input_data))}",
                "prediction_type": "churn_risk",
                "predicted_value": 0.22,  # Simulated churn risk
                "confidence_score": 0.78,
                "influencing_factors": {
                    "low_usage": 0.35,
                    "support_tickets": 0.25,
                    "payment_delays": 0.2,
                    "competitor_contact": 0.1,
                    "contract_renewal_approaching": 0.1
                }
            }
        elif planning_type == "expansion_prediction":
            return {
                "prediction_id": f"pred_expansion_{hash(str(input_data))}",
                "prediction_type": "expansion_potential",
                "predicted_value": 0.65,  # Simulated expansion potential
                "confidence_score": 0.85,
                "influencing_factors": {
                    "high_usage": 0.3,
                    "positive_feedback": 0.25,
                    "business_growth": 0.2,
                    "new_needs_identified": 0.15,
                    "budget_availability": 0.1
                }
            }
        elif planning_type == "recommendation":
            return {
                "recommendation_id": f"rec_{hash(str(input_data))}",
                "recommendations": [
                    "Schedule a check-in to address low engagement metrics.",
                    "Offer additional training sessions to improve product adoption.",
                    "Propose expansion options based on identified needs and usage patterns.",
                    "Prioritize support ticket resolution to reduce churn risk."
                ],
                "expected_improvement": 0.16
            }
        return {}

    async def generate_success_plan(self, customer_id: str, created_date: str, updated_date: str) -> SuccessPlan:
        """Generate a customer success plan using AI."""
        input_data = {"customer_id": customer_id}
        result = await self._simulate_ai_planning(input_data, "success_plan")
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO success_plans 
        (plan_id, customer_id, created_date, updated_date, goals, milestones, status, risk_factors)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (result["plan_id"], customer_id, created_date, updated_date, 
              str(result["goals"]), str(result["milestones"]), result["status"], 
              str(result["risk_factors"])))
        self.conn.commit()
        return SuccessPlan(
            plan_id=result["plan_id"],
            customer_id=customer_id,
            created_date=created_date,
            updated_date=updated_date,
            goals=result["goals"],
            milestones=result["milestones"],
            status=result["status"],
            risk_factors=result["risk_factors"]
        )

    async def predict_churn_risk(self, customer_id: str, predicted_date: str) -> SuccessPrediction:
        """Predict churn risk for a customer."""
        input_data = {"customer_id": customer_id}
        result = await self._simulate_ai_planning(input_data, "churn_prediction")
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO success_predictions 
        (prediction_id, customer_id, prediction_type, predicted_date, predicted_value, confidence_score, influencing_factors)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (result["prediction_id"], customer_id, result["prediction_type"], predicted_date, 
              result["predicted_value"], result["confidence_score"], str(result["influencing_factors"])))
        self.conn.commit()
        return SuccessPrediction(
            prediction_id=result["prediction_id"],
            customer_id=customer_id,
            prediction_type=result["prediction_type"],
            predicted_date=predicted_date,
            predicted_value=result["predicted_value"],
            confidence_score=result["confidence_score"],
            influencing_factors=result["influencing_factors"]
        )

    async def predict_expansion_potential(self, customer_id: str, predicted_date: str) -> SuccessPrediction:
        """Predict expansion potential for a customer."""
        input_data = {"customer_id": customer_id}
        result = await self._simulate_ai_planning(input_data, "expansion_prediction")
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO success_predictions 
        (prediction_id, customer_id, prediction_type, predicted_date, predicted_value, confidence_score, influencing_factors)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (result["prediction_id"], customer_id, result["prediction_type"], predicted_date, 
              result["predicted_value"], result["confidence_score"], str(result["influencing_factors"])))
        self.conn.commit()
        return SuccessPrediction(
            prediction_id=result["prediction_id"],
            customer_id=customer_id,
            prediction_type=result["prediction_type"],
            predicted_date=predicted_date,
            predicted_value=result["predicted_value"],
            confidence_score=result["confidence_score"],
            influencing_factors=result["influencing_factors"]
        )

    async def get_success_recommendations(self, customer_id: str, current_health: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI-driven recommendations for customer success."""
        input_data = {"customer_id": customer_id, "current_health": current_health}
        return await self._simulate_ai_planning(input_data, "recommendation")

    def update_success_plan(self, plan_id: str, updated_date: str, goals: Optional[Dict[str, Any]] = None, 
                            milestones: Optional[Dict[str, Any]] = None, status: Optional[str] = None, 
                            risk_factors: Optional[Dict[str, float]] = None) -> bool:
        """Update a success plan with new information."""
        cursor = self.conn.cursor()
        update_fields = []
        values = []
        if goals is not None:
            update_fields.append("goals = ?")
            values.append(str(goals))
        if milestones is not None:
            update_fields.append("milestones = ?")
            values.append(str(milestones))
        if status is not None:
            update_fields.append("status = ?")
            values.append(status)
        if risk_factors is not None:
            update_fields.append("risk_factors = ?")
            values.append(str(risk_factors))
        if update_fields:
            update_fields.append("updated_date = ?")
            values.append(updated_date)
            values.append(plan_id)
            query = f"UPDATE success_plans SET {', '.join(update_fields)} WHERE plan_id = ?"
            cursor.execute(query, values)
            self.conn.commit()
            return cursor.rowcount > 0
        return False

    def get_success_plan(self, plan_id: str) -> Optional[SuccessPlan]:
        """Retrieve a success plan by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM success_plans WHERE plan_id = ?", (plan_id,))
        row = cursor.fetchone()
        if row:
            return SuccessPlan(
                plan_id=row[0],
                customer_id=row[1],
                created_date=row[2],
                updated_date=row[3],
                goals=eval(row[4]),  # Convert string back to dict
                milestones=eval(row[5]),  # Convert string back to dict
                status=row[6],
                risk_factors=eval(row[7]) if row[7] else {}
            )
        return None

    def get_predictions_by_customer(self, customer_id: str) -> List[SuccessPrediction]:
        """Retrieve predictions for a customer."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM success_predictions WHERE customer_id = ?", (customer_id,))
        rows = cursor.fetchall()
        return [SuccessPrediction(
            prediction_id=row[0],
            customer_id=row[1],
            prediction_type=row[2],
            predicted_date=row[3],
            predicted_value=row[4],
            confidence_score=row[5],
            influencing_factors=eval(row[6])  # Convert string back to dict
        ) for row in rows]

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
