from typing import List, Dict, Any, Optional
import sqlite3
from datetime import datetime

class CustomerSupport:
    def __init__(self, db_path: str = ":memory:"):
        """Initialize Customer Support Database with SQLite"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._initialize_db()

    def _initialize_db(self) -> None:
        """Initialize database with necessary tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # Create tickets table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            subject TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            priority TEXT NOT NULL DEFAULT 'Medium',
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            assigned_to TEXT
        )
        """)

        # Create customers table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            company TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Create interactions table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            interaction_id TEXT PRIMARY KEY,
            ticket_id TEXT NOT NULL,
            customer_id TEXT NOT NULL,
            message TEXT NOT NULL,
            sender_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
        """)

        self.conn.commit()

    def add_customer(self, customer_id: str, name: str, email: str, phone: Optional[str] = None, company: Optional[str] = None) -> Dict[str, Any]:
        """Add a new customer to the database"""
        try:
            self.cursor.execute("""
            INSERT INTO customers (customer_id, name, email, phone, company)
            VALUES (?, ?, ?, ?, ?)
            """, (customer_id, name, email, phone, company))
            self.conn.commit()
            return {"status": "success", "message": f"Customer {customer_id} added", "customer_id": customer_id}
        except sqlite3.IntegrityError:
            return {"status": "error", "message": f"Customer {customer_id} or email {email} already exists"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_customer(self, customer_id: str, name: Optional[str] = None, email: Optional[str] = None, phone: Optional[str] = None, company: Optional[str] = None) -> Dict[str, Any]:
        """Update customer information"""
        updates = []
        values = []
        if name is not None:
            updates.append("name = ?")
            values.append(name)
        if email is not None:
            updates.append("email = ?")
            values.append(email)
        if phone is not None:
            updates.append("phone = ?")
            values.append(phone)
        if company is not None:
            updates.append("company = ?")
            values.append(company)

        if not updates:
            return {"status": "error", "message": "No updates provided"}

        values.append(customer_id)
        query = f"UPDATE customers SET {', '.join(updates)} WHERE customer_id = ?"
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            if self.cursor.rowcount == 0:
                return {"status": "error", "message": f"Customer {customer_id} not found"}
            return {"status": "success", "message": f"Customer {customer_id} updated", "customer_id": customer_id}
        except sqlite3.IntegrityError:
            return {"status": "error", "message": "Email already exists for another customer"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Retrieve a customer's details"""
        self.cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                "status": "success",
                "customer": {
                    "customer_id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "phone": row[3],
                    "company": row[4],
                    "created_at": row[5]
                }
            }
        return {"status": "error", "message": f"Customer {customer_id} not found"}

    def get_all_customers(self) -> Dict[str, Any]:
        """Retrieve all customers"""
        self.cursor.execute("SELECT * FROM customers")
        rows = self.cursor.fetchall()
        customers = []
        for row in rows:
            customers.append({
                "customer_id": row[0],
                "name": row[1],
                "email": row[2],
                "phone": row[3],
                "company": row[4],
                "created_at": row[5]
            })
        return {"status": "success", "customers": customers}

    def add_ticket(self, ticket_id: str, customer_id: str, subject: str, description: str, priority: str = "Medium", category: Optional[str] = None) -> Dict[str, Any]:
        """Add a new support ticket"""
        try:
            self.cursor.execute("""
            INSERT INTO tickets (ticket_id, customer_id, subject, description, priority, category)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (ticket_id, customer_id, subject, description, priority, category))
            self.conn.commit()
            return {"status": "success", "message": f"Ticket {ticket_id} added", "ticket_id": ticket_id}
        except sqlite3.IntegrityError:
            return {"status": "error", "message": f"Ticket {ticket_id} already exists"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_ticket(self, ticket_id: str, subject: Optional[str] = None, description: Optional[str] = None, status: Optional[str] = None, priority: Optional[str] = None, category: Optional[str] = None, assigned_to: Optional[str] = None) -> Dict[str, Any]:
        """Update ticket information"""
        updates = []
        values = []
        if subject is not None:
            updates.append("subject = ?")
            values.append(subject)
        if description is not None:
            updates.append("description = ?")
            values.append(description)
        if status is not None:
            updates.append("status = ?")
            values.append(status)
        if priority is not None:
            updates.append("priority = ?")
            values.append(priority)
        if category is not None:
            updates.append("category = ?")
            values.append(category)
        if assigned_to is not None:
            updates.append("assigned_to = ?")
            values.append(assigned_to)

        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            values.append(ticket_id)
            query = f"UPDATE tickets SET {', '.join(updates)} WHERE ticket_id = ?"
            try:
                self.cursor.execute(query, values)
                self.conn.commit()
                if self.cursor.rowcount == 0:
                    return {"status": "error", "message": f"Ticket {ticket_id} not found"}
                return {"status": "success", "message": f"Ticket {ticket_id} updated", "ticket_id": ticket_id}
            except Exception as e:
                return {"status": "error", "message": str(e)}
        return {"status": "error", "message": "No updates provided"}

    def get_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """Retrieve a ticket's details"""
        self.cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                "status": "success",
                "ticket": {
                    "ticket_id": row[0],
                    "customer_id": row[1],
                    "subject": row[2],
                    "description": row[3],
                    "status": row[4],
                    "priority": row[5],
                    "category": row[6],
                    "created_at": row[7],
                    "updated_at": row[8],
                    "assigned_to": row[9]
                }
            }
        return {"status": "error", "message": f"Ticket {ticket_id} not found"}

    def get_all_tickets(self, status: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve all tickets, optionally filtered by status"""
        query = "SELECT * FROM tickets"
        params = []
        if status:
            query += " WHERE status = ?"
            params.append(status)

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        tickets = []
        for row in rows:
            tickets.append({
                "ticket_id": row[0],
                "customer_id": row[1],
                "subject": row[2],
                "description": row[3],
                "status": row[4],
                "priority": row[5],
                "category": row[6],
                "created_at": row[7],
                "updated_at": row[8],
                "assigned_to": row[9]
            })
        return {"status": "success", "tickets": tickets}

    def get_customer_tickets(self, customer_id: str) -> Dict[str, Any]:
        """Retrieve all tickets for a specific customer"""
        self.cursor.execute("SELECT * FROM tickets WHERE customer_id = ?", (customer_id,))
        rows = self.cursor.fetchall()
        tickets = []
        for row in rows:
            tickets.append({
                "ticket_id": row[0],
                "customer_id": row[1],
                "subject": row[2],
                "description": row[3],
                "status": row[4],
                "priority": row[5],
                "category": row[6],
                "created_at": row[7],
                "updated_at": row[8],
                "assigned_to": row[9]
            })
        return {"status": "success", "tickets": tickets, "customer_id": customer_id}

    def add_interaction(self, interaction_id: str, ticket_id: str, customer_id: str, message: str, sender_type: str) -> Dict[str, Any]:
        """Add a new interaction to a ticket"""
        try:
            self.cursor.execute("""
            INSERT INTO interactions (interaction_id, ticket_id, customer_id, message, sender_type)
            VALUES (?, ?, ?, ?, ?)
            """, (interaction_id, ticket_id, customer_id, message, sender_type))
            self.conn.commit()
            # Update ticket's updated_at timestamp
            self.cursor.execute("UPDATE tickets SET updated_at = CURRENT_TIMESTAMP WHERE ticket_id = ?", (ticket_id,))
            self.conn.commit()
            return {"status": "success", "message": f"Interaction {interaction_id} added", "interaction_id": interaction_id}
        except sqlite3.IntegrityError:
            return {"status": "error", "message": f"Interaction {interaction_id} already exists"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_ticket_interactions(self, ticket_id: str) -> Dict[str, Any]:
        """Retrieve all interactions for a specific ticket"""
        self.cursor.execute("SELECT * FROM interactions WHERE ticket_id = ? ORDER BY created_at", (ticket_id,))
        rows = self.cursor.fetchall()
        interactions = []
        for row in rows:
            interactions.append({
                "interaction_id": row[0],
                "ticket_id": row[1],
                "customer_id": row[2],
                "message": row[3],
                "sender_type": row[4],
                "created_at": row[5]
            })
        return {"status": "success", "interactions": interactions, "ticket_id": ticket_id}

    def get_ticket_summary(self, ticket_id: str) -> Dict[str, Any]:
        """Get a summary of a ticket including interactions"""
        ticket_response = self.get_ticket(ticket_id)
        if ticket_response.get("status") != "success":
            return ticket_response

        interactions_response = self.get_ticket_interactions(ticket_id)
        if interactions_response.get("status") != "success":
            return interactions_response

        return {
            "status": "success",
            "ticket": ticket_response.get("ticket", {}),
            "interactions": interactions_response.get("interactions", [])
        }

    def close(self) -> None:
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
