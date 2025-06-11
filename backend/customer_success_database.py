import sqlite3
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class CustomerSuccess:
    customer_id: str
    account_manager_id: str
    success_plan_id: Optional[str]
    health_score: float
    last_checkin_date: str
    next_checkin_date: str
    churn_risk: float
    expansion_potential: float

@dataclass
class SuccessInteraction:
    interaction_id: str
    customer_id: str
    interaction_type: str
    interaction_date: str
    notes: str
    outcome: str

@dataclass
class SuccessPlan:
    plan_id: str
    customer_id: str
    created_date: str
    updated_date: str
    goals: Dict[str, Any]
    milestones: Dict[str, Any]
    status: str

class CustomerSuccessDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self._initialize_db()

    def _initialize_db(self) -> None:
        """Initialize database connection and create tables if not exists."""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        # Customers Success Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_success (
            customer_id TEXT PRIMARY KEY,
            account_manager_id TEXT,
            success_plan_id TEXT,
            health_score REAL,
            last_checkin_date TEXT,
            next_checkin_date TEXT,
            churn_risk REAL,
            expansion_potential REAL,
            FOREIGN KEY (success_plan_id) REFERENCES success_plans(plan_id)
        )
        """)
        # Success Interactions Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS success_interactions (
            interaction_id TEXT PRIMARY KEY,
            customer_id TEXT,
            interaction_type TEXT,
            interaction_date TEXT,
            notes TEXT,
            outcome TEXT,
            FOREIGN KEY (customer_id) REFERENCES customer_success(customer_id)
        )
        """)
        # Success Plans Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS success_plans (
            plan_id TEXT PRIMARY KEY,
            customer_id TEXT,
            created_date TEXT,
            updated_date TEXT,
            goals TEXT,
            milestones TEXT,
            status TEXT,
            FOREIGN KEY (customer_id) REFERENCES customer_success(customer_id)
        )
        """)
        self.conn.commit()

    def add_customer_success(self, customer: CustomerSuccess) -> bool:
        """Add or update a customer's success profile."""
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO customer_success 
        (customer_id, account_manager_id, success_plan_id, health_score, last_checkin_date, next_checkin_date, churn_risk, expansion_potential)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (customer.customer_id, customer.account_manager_id, customer.success_plan_id, 
              customer.health_score, customer.last_checkin_date, customer.next_checkin_date, 
              customer.churn_risk, customer.expansion_potential))
        self.conn.commit()
        return cursor.rowcount > 0

    def update_customer_health(self, customer_id: str, health_score: float, churn_risk: float, expansion_potential: float, last_checkin_date: str, next_checkin_date: str) -> bool:
        """Update a customer's health metrics."""
        cursor = self.conn.cursor()
        cursor.execute("""
        UPDATE customer_success 
        SET health_score = ?, churn_risk = ?, expansion_potential = ?, last_checkin_date = ?, next_checkin_date = ?
        WHERE customer_id = ?
        """, (health_score, churn_risk, expansion_potential, last_checkin_date, next_checkin_date, customer_id))
        self.conn.commit()
        return cursor.rowcount > 0

    def add_success_interaction(self, interaction: SuccessInteraction) -> bool:
        """Add a customer success interaction."""
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO success_interactions 
        (interaction_id, customer_id, interaction_type, interaction_date, notes, outcome)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (interaction.interaction_id, interaction.customer_id, interaction.interaction_type, 
              interaction.interaction_date, interaction.notes, interaction.outcome))
        self.conn.commit()
        return cursor.rowcount > 0

    def add_success_plan(self, plan: SuccessPlan) -> bool:
        """Add or update a customer success plan."""
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO success_plans 
        (plan_id, customer_id, created_date, updated_date, goals, milestones, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (plan.plan_id, plan.customer_id, plan.created_date, plan.updated_date, 
              str(plan.goals), str(plan.milestones), plan.status))
        self.conn.commit()
        return cursor.rowcount > 0

    def get_customer_success(self, customer_id: str) -> Optional[CustomerSuccess]:
        """Retrieve a customer's success profile."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customer_success WHERE customer_id = ?", (customer_id,))
        row = cursor.fetchone()
        if row:
            return CustomerSuccess(
                customer_id=row[0],
                account_manager_id=row[1],
                success_plan_id=row[2],
                health_score=row[3],
                last_checkin_date=row[4],
                next_checkin_date=row[5],
                churn_risk=row[6],
                expansion_potential=row[7]
            )
        return None

    def get_success_interactions(self, customer_id: str) -> List[SuccessInteraction]:
        """Retrieve interactions for a customer."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM success_interactions WHERE customer_id = ?", (customer_id,))
        rows = cursor.fetchall()
        return [SuccessInteraction(
            interaction_id=row[0],
            customer_id=row[1],
            interaction_type=row[2],
            interaction_date=row[3],
            notes=row[4],
            outcome=row[5]
        ) for row in rows]

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
                status=row[6]
            )
        return None

    def get_customers_by_health(self, min_health: float, max_health: float) -> List[CustomerSuccess]:
        """Retrieve customers within a health score range."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customer_success WHERE health_score BETWEEN ? AND ?", (min_health, max_health))
        rows = cursor.fetchall()
        return [CustomerSuccess(
            customer_id=row[0],
            account_manager_id=row[1],
            success_plan_id=row[2],
            health_score=row[3],
            last_checkin_date=row[4],
            next_checkin_date=row[5],
            churn_risk=row[6],
            expansion_potential=row[7]
        ) for row in rows]

    def get_customers_by_churn_risk(self, min_risk: float) -> List[CustomerSuccess]:
        """Retrieve customers with churn risk above a threshold."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customer_success WHERE churn_risk >= ?", (min_risk,))
        rows = cursor.fetchall()
        return [CustomerSuccess(
            customer_id=row[0],
            account_manager_id=row[1],
            success_plan_id=row[2],
            health_score=row[3],
            last_checkin_date=row[4],
            next_checkin_date=row[5],
            churn_risk=row[6],
            expansion_potential=row[7]
        ) for row in rows]

    def get_customers_by_expansion_potential(self, min_potential: float) -> List[CustomerSuccess]:
        """Retrieve customers with expansion potential above a threshold."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customer_success WHERE expansion_potential >= ?", (min_potential,))
        rows = cursor.fetchall()
        return [CustomerSuccess(
            customer_id=row[0],
            account_manager_id=row[1],
            success_plan_id=row[2],
            health_score=row[3],
            last_checkin_date=row[4],
            next_checkin_date=row[5],
            churn_risk=row[6],
            expansion_potential=row[7]
        ) for row in rows]

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
