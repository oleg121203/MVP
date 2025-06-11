import sqlite3
from typing import Dict, List, Any, Optional

class MarketExpansionDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self._initialize_db()

    def _initialize_db(self) -> None:
        """Initialize database connection and create tables if not exists."""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        # Markets Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS markets (
            market_id TEXT PRIMARY KEY,
            market_name TEXT,
            market_description TEXT,
            market_size REAL,
            growth_rate REAL,
            competitive_intensity REAL,
            entry_barriers TEXT,
            regulatory_environment TEXT,
            created_date TEXT,
            updated_date TEXT
        )
        """)
        # Expansion Strategies Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS expansion_strategies (
            strategy_id TEXT PRIMARY KEY,
            market_id TEXT,
            strategy_name TEXT,
            strategy_description TEXT,
            target_audience TEXT,
            value_proposition TEXT,
            go_to_market_plan TEXT,
            potential_impact Dict,
            status TEXT,
            created_date TEXT,
            updated_date TEXT,
            FOREIGN KEY (market_id) REFERENCES markets(market_id)
        )
        """)
        self.conn.commit()

    def add_market(self, market_id: str, market_name: str, market_description: str, market_size: float, growth_rate: float, competitive_intensity: float, entry_barriers: Dict[str, Any], regulatory_environment: Dict[str, Any], created_date: str, updated_date: str) -> bool:
        """Add a new market to the database."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO markets 
            (market_id, market_name, market_description, market_size, growth_rate, competitive_intensity, entry_barriers, regulatory_environment, created_date, updated_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (market_id, market_name, market_description, market_size, growth_rate, competitive_intensity, str(entry_barriers), str(regulatory_environment), created_date, updated_date))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_market(self, market_id: str, updated_date: str, market_name: Optional[str] = None, market_description: Optional[str] = None, market_size: Optional[float] = None, growth_rate: Optional[float] = None, competitive_intensity: Optional[float] = None, entry_barriers: Optional[Dict[str, Any]] = None, regulatory_environment: Optional[Dict[str, Any]] = None) -> bool:
        """Update market information."""
        cursor = self.conn.cursor()
        update_fields = []
        values = []
        if market_name is not None:
            update_fields.append("market_name = ?")
            values.append(market_name)
        if market_description is not None:
            update_fields.append("market_description = ?")
            values.append(market_description)
        if market_size is not None:
            update_fields.append("market_size = ?")
            values.append(market_size)
        if growth_rate is not None:
            update_fields.append("growth_rate = ?")
            values.append(growth_rate)
        if competitive_intensity is not None:
            update_fields.append("competitive_intensity = ?")
            values.append(competitive_intensity)
        if entry_barriers is not None:
            update_fields.append("entry_barriers = ?")
            values.append(str(entry_barriers))
        if regulatory_environment is not None:
            update_fields.append("regulatory_environment = ?")
            values.append(str(regulatory_environment))
        if update_fields:
            update_fields.append("updated_date = ?")
            values.append(updated_date)
            values.append(market_id)
            query = f"UPDATE markets SET {', '.join(update_fields)} WHERE market_id = ?"
            cursor.execute(query, values)
            self.conn.commit()
            return cursor.rowcount > 0
        return False

    def get_market(self, market_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a market by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM markets WHERE market_id = ?", (market_id,))
        row = cursor.fetchone()
        if row:
            return {
                "market_id": row[0],
                "market_name": row[1],
                "market_description": row[2],
                "market_size": row[3],
                "growth_rate": row[4],
                "competitive_intensity": row[5],
                "entry_barriers": eval(row[6]) if row[6] else {},
                "regulatory_environment": eval(row[7]) if row[7] else {},
                "created_date": row[8],
                "updated_date": row[9]
            }
        return None

    def get_all_markets(self) -> List[Dict[str, Any]]:
        """Retrieve all markets."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM markets")
        rows = cursor.fetchall()
        return [{
            "market_id": row[0],
            "market_name": row[1],
            "market_description": row[2],
            "market_size": row[3],
            "growth_rate": row[4],
            "competitive_intensity": row[5],
            "entry_barriers": eval(row[6]) if row[6] else {},
            "regulatory_environment": eval(row[7]) if row[7] else {},
            "created_date": row[8],
            "updated_date": row[9]
        } for row in rows]

    def add_strategy(self, strategy_id: str, market_id: str, strategy_name: str, strategy_description: str, target_audience: Dict[str, Any], value_proposition: Dict[str, Any], go_to_market_plan: Dict[str, Any], potential_impact: Dict[str, Any], status: str, created_date: str, updated_date: str) -> bool:
        """Add a new expansion strategy to the database."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO expansion_strategies 
            (strategy_id, market_id, strategy_name, strategy_description, target_audience, value_proposition, go_to_market_plan, potential_impact, status, created_date, updated_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (strategy_id, market_id, strategy_name, strategy_description, str(target_audience), str(value_proposition), str(go_to_market_plan), str(potential_impact), status, created_date, updated_date))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_strategy(self, strategy_id: str, updated_date: str, strategy_name: Optional[str] = None, strategy_description: Optional[str] = None, target_audience: Optional[Dict[str, Any]] = None, value_proposition: Optional[Dict[str, Any]] = None, go_to_market_plan: Optional[Dict[str, Any]] = None, potential_impact: Optional[Dict[str, Any]] = None, status: Optional[str] = None) -> bool:
        """Update expansion strategy information."""
        cursor = self.conn.cursor()
        update_fields = []
        values = []
        if strategy_name is not None:
            update_fields.append("strategy_name = ?")
            values.append(strategy_name)
        if strategy_description is not None:
            update_fields.append("strategy_description = ?")
            values.append(strategy_description)
        if target_audience is not None:
            update_fields.append("target_audience = ?")
            values.append(str(target_audience))
        if value_proposition is not None:
            update_fields.append("value_proposition = ?")
            values.append(str(value_proposition))
        if go_to_market_plan is not None:
            update_fields.append("go_to_market_plan = ?")
            values.append(str(go_to_market_plan))
        if potential_impact is not None:
            update_fields.append("potential_impact = ?")
            values.append(str(potential_impact))
        if status is not None:
            update_fields.append("status = ?")
            values.append(status)
        if update_fields:
            update_fields.append("updated_date = ?")
            values.append(updated_date)
            values.append(strategy_id)
            query = f"UPDATE expansion_strategies SET {', '.join(update_fields)} WHERE strategy_id = ?"
            cursor.execute(query, values)
            self.conn.commit()
            return cursor.rowcount > 0
        return False

    def get_strategy(self, strategy_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve an expansion strategy by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM expansion_strategies WHERE strategy_id = ?", (strategy_id,))
        row = cursor.fetchone()
        if row:
            return {
                "strategy_id": row[0],
                "market_id": row[1],
                "strategy_name": row[2],
                "strategy_description": row[3],
                "target_audience": eval(row[4]) if row[4] else {},
                "value_proposition": eval(row[5]) if row[5] else {},
                "go_to_market_plan": eval(row[6]) if row[6] else {},
                "potential_impact": eval(row[7]) if row[7] else {},
                "status": row[8],
                "created_date": row[9],
                "updated_date": row[10]
            }
        return None

    def get_strategies_by_market(self, market_id: str) -> List[Dict[str, Any]]:
        """Retrieve expansion strategies for a specific market."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM expansion_strategies WHERE market_id = ?", (market_id,))
        rows = cursor.fetchall()
        return [{
            "strategy_id": row[0],
            "market_id": row[1],
            "strategy_name": row[2],
            "strategy_description": row[3],
            "target_audience": eval(row[4]) if row[4] else {},
            "value_proposition": eval(row[5]) if row[5] else {},
            "go_to_market_plan": eval(row[6]) if row[6] else {},
            "potential_impact": eval(row[7]) if row[7] else {},
            "status": row[8],
            "created_date": row[9],
            "updated_date": row[10]
        } for row in rows]

    def get_strategies_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Retrieve expansion strategies by status."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM expansion_strategies WHERE status = ?", (status,))
        rows = cursor.fetchall()
        return [{
            "strategy_id": row[0],
            "market_id": row[1],
            "strategy_name": row[2],
            "strategy_description": row[3],
            "target_audience": eval(row[4]) if row[4] else {},
            "value_proposition": eval(row[5]) if row[5] else {},
            "go_to_market_plan": eval(row[6]) if row[6] else {},
            "potential_impact": eval(row[7]) if row[7] else {},
            "status": row[8],
            "created_date": row[9],
            "updated_date": row[10]
        } for row in rows]

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
