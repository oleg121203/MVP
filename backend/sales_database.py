import sqlite3
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class Customer:
    customer_id: str
    name: str
    email: str
    phone: str
    company: str
    industry: str
    location: str
    customer_since: str
    status: str

@dataclass
class Transaction:
    transaction_id: str
    customer_id: str
    product_id: str
    amount: float
    transaction_date: str
    status: str

@dataclass
class SalesOpportunity:
    opportunity_id: str
    customer_id: str
    description: str
    value: float
    probability: float
    stage: str
    created_date: str
    last_updated: str

class SalesDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self._initialize_db()

    def _initialize_db(self) -> None:
        """Initialize database connection and create sales tables if not exists."""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        # Customers Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            company TEXT,
            industry TEXT,
            location TEXT,
            customer_since TEXT,
            status TEXT
        )
        """)
        # Transactions Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            customer_id TEXT,
            product_id TEXT,
            amount REAL,
            transaction_date TEXT,
            status TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
        """)
        # Sales Opportunities Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales_opportunities (
            opportunity_id TEXT PRIMARY KEY,
            customer_id TEXT,
            description TEXT,
            value REAL,
            probability REAL,
            stage TEXT,
            created_date TEXT,
            last_updated TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
        """)
        self.conn.commit()

    def add_customer(self, customer: Customer) -> None:
        """Add a new customer to the database."""
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO customers 
        (customer_id, name, email, phone, company, industry, location, customer_since, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (customer.customer_id, customer.name, customer.email, customer.phone, 
              customer.company, customer.industry, customer.location, 
              customer.customer_since, customer.status))
        self.conn.commit()

    def update_customer(self, customer_id: str, updates: Dict[str, Any]) -> bool:
        """Update customer information."""
        cursor = self.conn.cursor()
        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values())
        values.append(customer_id)
        query = f"UPDATE customers SET {set_clause} WHERE customer_id = ?"
        cursor.execute(query, values)
        self.conn.commit()
        return cursor.rowcount > 0

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Retrieve a customer by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
        row = cursor.fetchone()
        if row:
            return Customer(
                customer_id=row[0],
                name=row[1],
                email=row[2],
                phone=row[3],
                company=row[4],
                industry=row[5],
                location=row[6],
                customer_since=row[7],
                status=row[8]
            )
        return None

    def get_all_customers(self, status: Optional[str] = None) -> List[Customer]:
        """Retrieve all customers, optionally filtered by status."""
        cursor = self.conn.cursor()
        if status:
            cursor.execute("SELECT * FROM customers WHERE status = ?", (status,))
        else:
            cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()
        return [Customer(
            customer_id=row[0],
            name=row[1],
            email=row[2],
            phone=row[3],
            company=row[4],
            industry=row[5],
            location=row[6],
            customer_since=row[7],
            status=row[8]
        ) for row in rows]

    def add_transaction(self, transaction: Transaction) -> None:
        """Add a new transaction to the database."""
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO transactions 
        (transaction_id, customer_id, product_id, amount, transaction_date, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (transaction.transaction_id, transaction.customer_id, transaction.product_id, 
              transaction.amount, transaction.transaction_date, transaction.status))
        self.conn.commit()

    def get_transactions_by_customer(self, customer_id: str) -> List[Transaction]:
        """Retrieve all transactions for a specific customer."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE customer_id = ?", (customer_id,))
        rows = cursor.fetchall()
        return [Transaction(
            transaction_id=row[0],
            customer_id=row[1],
            product_id=row[2],
            amount=row[3],
            transaction_date=row[4],
            status=row[5]
        ) for row in rows]

    def get_transaction_summary(self, customer_id: Optional[str] = None) -> Dict[str, Any]:
        """Get transaction summary (total amount, count) optionally by customer."""
        cursor = self.conn.cursor()
        if customer_id:
            cursor.execute("""
            SELECT COUNT(*), SUM(amount) 
            FROM transactions 
            WHERE customer_id = ? AND status = 'completed'
            """, (customer_id,))
        else:
            cursor.execute("""
            SELECT COUNT(*), SUM(amount) 
            FROM transactions 
            WHERE status = 'completed'
            """)
        count, total = cursor.fetchone()
        return {"transaction_count": count or 0, "total_amount": total or 0.0}

    def add_opportunity(self, opportunity: SalesOpportunity) -> None:
        """Add a new sales opportunity to the database."""
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO sales_opportunities 
        (opportunity_id, customer_id, description, value, probability, stage, created_date, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (opportunity.opportunity_id, opportunity.customer_id, opportunity.description, 
              opportunity.value, opportunity.probability, opportunity.stage, 
              opportunity.created_date, opportunity.last_updated))
        self.conn.commit()

    def update_opportunity(self, opportunity_id: str, updates: Dict[str, Any]) -> bool:
        """Update sales opportunity details."""
        cursor = self.conn.cursor()
        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values())
        values.append(opportunity_id)
        query = f"UPDATE sales_opportunities SET {set_clause} WHERE opportunity_id = ?"
        cursor.execute(query, values)
        self.conn.commit()
        return cursor.rowcount > 0

    def get_opportunities_by_customer(self, customer_id: str) -> List[SalesOpportunity]:
        """Retrieve all opportunities for a specific customer."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sales_opportunities WHERE customer_id = ?", (customer_id,))
        rows = cursor.fetchall()
        return [SalesOpportunity(
            opportunity_id=row[0],
            customer_id=row[1],
            description=row[2],
            value=row[3],
            probability=row[4],
            stage=row[5],
            created_date=row[6],
            last_updated=row[7]
        ) for row in rows]

    def get_opportunity_summary(self, customer_id: Optional[str] = None) -> Dict[str, Any]:
        """Get opportunity summary (count, total value, weighted value) optionally by customer."""
        cursor = self.conn.cursor()
        if customer_id:
            cursor.execute("""
            SELECT COUNT(*), SUM(value), SUM(value * probability) 
            FROM sales_opportunities 
            WHERE customer_id = ? AND stage NOT IN ('closed_won', 'closed_lost')
            """, (customer_id,))
        else:
            cursor.execute("""
            SELECT COUNT(*), SUM(value), SUM(value * probability) 
            FROM sales_opportunities 
            WHERE stage NOT IN ('closed_won', 'closed_lost')
            """)
        count, total_value, weighted_value = cursor.fetchone()
        return {
            "opportunity_count": count or 0,
            "total_value": total_value or 0.0,
            "weighted_value": weighted_value or 0.0
        }

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
