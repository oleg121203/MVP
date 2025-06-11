from typing import List, Dict, Any, Optional
import sqlite3
from datetime import datetime

class FinancialManagement:
    def __init__(self, db_path: str = 'ventai_enterprise.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._initialize_db()

    def _initialize_db(self) -> None:
        """Initialize the financial database with required tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Create budgets table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                total_amount REAL NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        # Create expenses table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id TEXT PRIMARY KEY,
                budget_id TEXT NOT NULL,
                project_id TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                expense_date TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (budget_id) REFERENCES budgets(id)
            )
        ''')
        
        # Create financial_transactions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS financial_transactions (
                id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                transaction_date TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        self.conn.commit()

    def add_budget(self, budget_id: str, project_id: str, total_amount: float, start_date: str, end_date: str) -> bool:
        """Add a new budget for a project"""
        try:
            current_time = datetime.now().isoformat()
            self.cursor.execute('''
                INSERT INTO budgets (id, project_id, total_amount, start_date, end_date, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (budget_id, project_id, total_amount, start_date, end_date, current_time, current_time))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding budget: {e}")
            return False

    def update_budget(self, budget_id: str, total_amount: Optional[float] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> bool:
        """Update budget information"""
        try:
            current_time = datetime.now().isoformat()
            updates = []
            values = []
            if total_amount is not None:
                updates.append("total_amount = ?")
                values.append(total_amount)
            if start_date is not None:
                updates.append("start_date = ?")
                values.append(start_date)
            if end_date is not None:
                updates.append("end_date = ?")
                values.append(end_date)
            
            if not updates:
                return False
                
            updates.append("updated_at = ?")
            values.append(current_time)
            values.append(budget_id)
            
            query = f"UPDATE budgets SET {', '.join(updates)} WHERE id = ?"
            self.cursor.execute(query, values)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating budget: {e}")
            return False

    def get_budget(self, budget_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve budget details by ID"""
        try:
            self.cursor.execute("SELECT * FROM budgets WHERE id = ?", (budget_id,))
            result = self.cursor.fetchone()
            if result:
                columns = ["id", "project_id", "total_amount", "start_date", "end_date", "created_at", "updated_at"]
                return dict(zip(columns, result))
            return None
        except sqlite3.Error as e:
            print(f"Error retrieving budget: {e}")
            return None

    def add_expense(self, expense_id: str, budget_id: str, project_id: str, category: str, amount: float, description: str, expense_date: str) -> bool:
        """Add a new expense under a budget"""
        try:
            current_time = datetime.now().isoformat()
            self.cursor.execute('''
                INSERT INTO expenses (id, budget_id, project_id, category, amount, description, expense_date, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (expense_id, budget_id, project_id, category, amount, description, expense_date, current_time, current_time))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding expense: {e}")
            return False

    def get_expenses_by_budget(self, budget_id: str) -> List[Dict[str, Any]]:
        """Retrieve all expenses for a specific budget"""
        try:
            self.cursor.execute("SELECT * FROM expenses WHERE budget_id = ?", (budget_id,))
            results = self.cursor.fetchall()
            columns = ["id", "budget_id", "project_id", "category", "amount", "description", "expense_date", "created_at", "updated_at"]
            return [dict(zip(columns, row)) for row in results]
        except sqlite3.Error as e:
            print(f"Error retrieving expenses: {e}")
            return []

    def add_transaction(self, transaction_id: str, project_id: str, transaction_type: str, amount: float, description: str, transaction_date: str) -> bool:
        """Add a new financial transaction for a project"""
        try:
            current_time = datetime.now().isoformat()
            self.cursor.execute('''
                INSERT INTO financial_transactions (id, project_id, type, amount, description, transaction_date, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (transaction_id, project_id, transaction_type, amount, description, transaction_date, current_time, current_time))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding transaction: {e}")
            return False

    def get_transactions_by_project(self, project_id: str) -> List[Dict[str, Any]]:
        """Retrieve all transactions for a specific project"""
        try:
            self.cursor.execute("SELECT * FROM financial_transactions WHERE project_id = ?", (project_id,))
            results = self.cursor.fetchall()
            columns = ["id", "project_id", "type", "amount", "description", "transaction_date", "created_at", "updated_at"]
            return [dict(zip(columns, row)) for row in results]
        except sqlite3.Error as e:
            print(f"Error retrieving transactions: {e}")
            return []

    def get_financial_summary(self, project_id: str) -> Dict[str, Any]:
        """Generate a financial summary for a project"""
        try:
            # Get budget information
            self.cursor.execute("SELECT * FROM budgets WHERE project_id = ?", (project_id,))
            budget_data = self.cursor.fetchone()
            budget_columns = ["id", "project_id", "total_amount", "start_date", "end_date", "created_at", "updated_at"]
            budget = dict(zip(budget_columns, budget_data)) if budget_data else None

            # Get total expenses
            self.cursor.execute("SELECT SUM(amount) FROM expenses WHERE project_id = ?", (project_id,))
            total_expenses = self.cursor.fetchone()[0] or 0.0

            # Get transaction summary
            self.cursor.execute("SELECT type, SUM(amount) FROM financial_transactions WHERE project_id = ? GROUP BY type", (project_id,))
            transaction_summary = dict(self.cursor.fetchall())

            return {
                "status": "success",
                "project_id": project_id,
                "budget": budget,
                "total_expenses": total_expenses,
                "remaining_budget": budget["total_amount"] - total_expenses if budget else 0.0,
                "transactions": transaction_summary
            }
        except sqlite3.Error as e:
            print(f"Error generating financial summary: {e}")
            return {"status": "error", "message": str(e)}

    def close_connection(self) -> None:
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
