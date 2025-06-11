from typing import List, Dict, Any, Optional
import sqlite3
from datetime import datetime

class MarketingDatabase:
    def __init__(self, db_path: str = ":memory:"):
        """Initialize Marketing Database with SQLite"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._initialize_db()

    def _initialize_db(self) -> None:
        """Initialize database with necessary tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # Create campaigns table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            campaign_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            target_audience TEXT,
            channel TEXT NOT NULL,
            budget REAL,
            start_date TIMESTAMP,
            end_date TIMESTAMP,
            status TEXT NOT NULL DEFAULT 'Draft',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Create segments table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS segments (
            segment_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            criteria TEXT NOT NULL,
            size INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Create campaign_segments junction table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS campaign_segments (
            campaign_id TEXT,
            segment_id TEXT,
            PRIMARY KEY (campaign_id, segment_id),
            FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id),
            FOREIGN KEY (segment_id) REFERENCES segments(segment_id)
        )
        """)

        # Create content table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS content (
            content_id TEXT PRIMARY KEY,
            campaign_id TEXT,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            body TEXT,
            status TEXT NOT NULL DEFAULT 'Draft',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id)
        )
        """)

        # Create metrics table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            metric_id TEXT PRIMARY KEY,
            campaign_id TEXT,
            content_id TEXT,
            metric_type TEXT NOT NULL,
            value REAL NOT NULL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id),
            FOREIGN KEY (content_id) REFERENCES content(content_id)
        )
        """)

        self.conn.commit()

    def add_campaign(self, campaign_id: str, name: str, description: Optional[str] = None, target_audience: Optional[str] = None, channel: str = "Email", budget: Optional[float] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, status: str = "Draft") -> Dict[str, Any]:
        """Add a new marketing campaign to the database"""
        try:
            self.cursor.execute("""
            INSERT INTO campaigns (campaign_id, name, description, target_audience, channel, budget, start_date, end_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (campaign_id, name, description, target_audience, channel, budget, start_date, end_date, status))
            self.conn.commit()
            return {"status": "success", "message": f"Campaign {campaign_id} added", "campaign_id": campaign_id}
        except sqlite3.IntegrityError:
            return {"status": "error", "message": f"Campaign {campaign_id} already exists"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_campaign(self, campaign_id: str, name: Optional[str] = None, description: Optional[str] = None, target_audience: Optional[str] = None, channel: Optional[str] = None, budget: Optional[float] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
        """Update campaign information"""
        updates = []
        values = []
        if name is not None:
            updates.append("name = ?")
            values.append(name)
        if description is not None:
            updates.append("description = ?")
            values.append(description)
        if target_audience is not None:
            updates.append("target_audience = ?")
            values.append(target_audience)
        if channel is not None:
            updates.append("channel = ?")
            values.append(channel)
        if budget is not None:
            updates.append("budget = ?")
            values.append(budget)
        if start_date is not None:
            updates.append("start_date = ?")
            values.append(start_date)
        if end_date is not None:
            updates.append("end_date = ?")
            values.append(end_date)
        if status is not None:
            updates.append("status = ?")
            values.append(status)

        if not updates:
            return {"status": "error", "message": "No updates provided"}

        updates.append("updated_at = CURRENT_TIMESTAMP")
        values.append(campaign_id)
        query = f"UPDATE campaigns SET {', '.join(updates)} WHERE campaign_id = ?"
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            if self.cursor.rowcount == 0:
                return {"status": "error", "message": f"Campaign {campaign_id} not found"}
            return {"status": "success", "message": f"Campaign {campaign_id} updated", "campaign_id": campaign_id}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Retrieve a campaign's details"""
        self.cursor.execute("SELECT * FROM campaigns WHERE campaign_id = ?", (campaign_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                "status": "success",
                "campaign": {
                    "campaign_id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "target_audience": row[3],
                    "channel": row[4],
                    "budget": row[5],
                    "start_date": row[6],
                    "end_date": row[7],
                    "status": row[8],
                    "created_at": row[9],
                    "updated_at": row[10]
                }
            }
        return {"status": "error", "message": f"Campaign {campaign_id} not found"}

    def get_all_campaigns(self, status: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve all campaigns, optionally filtered by status"""
        query = "SELECT * FROM campaigns"
        params = []
        if status:
            query += " WHERE status = ?"
            params.append(status)

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        campaigns = []
        for row in rows:
            campaigns.append({
                "campaign_id": row[0],
                "name": row[1],
                "description": row[2],
                "target_audience": row[3],
                "channel": row[4],
                "budget": row[5],
                "start_date": row[6],
                "end_date": row[7],
                "status": row[8],
                "created_at": row[9],
                "updated_at": row[10]
            })
        return {"status": "success", "campaigns": campaigns}

    def add_segment(self, segment_id: str, name: str, criteria: str, size: Optional[int] = None) -> Dict[str, Any]:
        """Add a new customer segment to the database"""
        try:
            self.cursor.execute("""
            INSERT INTO segments (segment_id, name, criteria, size)
            VALUES (?, ?, ?, ?)
            """, (segment_id, name, criteria, size))
            self.conn.commit()
            return {"status": "success", "message": f"Segment {segment_id} added", "segment_id": segment_id}
        except sqlite3.IntegrityError:
            return {"status": "error", "message": f"Segment {segment_id} already exists"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_segment(self, segment_id: str, name: Optional[str] = None, criteria: Optional[str] = None, size: Optional[int] = None) -> Dict[str, Any]:
        """Update segment information"""
        updates = []
        values = []
        if name is not None:
            updates.append("name = ?")
            values.append(name)
        if criteria is not None:
            updates.append("criteria = ?")
            values.append(criteria)
        if size is not None:
            updates.append("size = ?")
            values.append(size)

        if not updates:
            return {"status": "error", "message": "No updates provided"}

        updates.append("updated_at = CURRENT_TIMESTAMP")
        values.append(segment_id)
        query = f"UPDATE segments SET {', '.join(updates)} WHERE segment_id = ?"
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            if self.cursor.rowcount == 0:
                return {"status": "error", "message": f"Segment {segment_id} not found"}
            return {"status": "success", "message": f"Segment {segment_id} updated", "segment_id": segment_id}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_segment(self, segment_id: str) -> Dict[str, Any]:
        """Retrieve a segment's details"""
        self.cursor.execute("SELECT * FROM segments WHERE segment_id = ?", (segment_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                "status": "success",
                "segment": {
                    "segment_id": row[0],
                    "name": row[1],
                    "criteria": row[2],
                    "size": row[3],
                    "created_at": row[4],
                    "updated_at": row[5]
                }
            }
        return {"status": "error", "message": f"Segment {segment_id} not found"}

    def get_all_segments(self) -> Dict[str, Any]:
        """Retrieve all segments"""
        self.cursor.execute("SELECT * FROM segments")
        rows = self.cursor.fetchall()
        segments = []
        for row in rows:
            segments.append({
                "segment_id": row[0],
                "name": row[1],
                "criteria": row[2],
                "size": row[3],
                "created_at": row[4],
                "updated_at": row[5]
            })
        return {"status": "success", "segments": segments}

    def associate_segment_with_campaign(self, campaign_id: str, segment_id: str) -> Dict[str, Any]:
        """Associate a segment with a campaign"""
        try:
            self.cursor.execute("""
            INSERT INTO campaign_segments (campaign_id, segment_id)
            VALUES (?, ?)
            """, (campaign_id, segment_id))
            self.conn.commit()
            return {"status": "success", "message": f"Segment {segment_id} associated with campaign {campaign_id}"}
        except sqlite3.IntegrityError:
            return {"status": "error", "message": f"Association already exists or invalid campaign/segment ID"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_campaign_segments(self, campaign_id: str) -> Dict[str, Any]:
        """Get all segments associated with a campaign"""
        self.cursor.execute("""
        SELECT s.* FROM segments s
        JOIN campaign_segments cs ON s.segment_id = cs.segment_id
        WHERE cs.campaign_id = ?
        """, (campaign_id,))
        rows = self.cursor.fetchall()
        segments = []
        for row in rows:
            segments.append({
                "segment_id": row[0],
                "name": row[1],
                "criteria": row[2],
                "size": row[3],
                "created_at": row[4],
                "updated_at": row[5]
            })
        return {"status": "success", "segments": segments}

    def add_content(self, content_id: str, campaign_id: str, title: str, content_type: str, body: Optional[str] = None, status: str = "Draft") -> Dict[str, Any]:
        """Add new content to a campaign"""
        try:
            self.cursor.execute("""
            INSERT INTO content (content_id, campaign_id, title, type, body, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (content_id, campaign_id, title, content_type, body, status))
            self.conn.commit()
            return {"status": "success", "message": f"Content {content_id} added", "content_id": content_id}
        except sqlite3.IntegrityError:
            return {"status": "error", "message": f"Content {content_id} already exists or campaign not found"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_content(self, content_id: str, title: Optional[str] = None, content_type: Optional[str] = None, body: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
        """Update content information"""
        updates = []
        values = []
        if title is not None:
            updates.append("title = ?")
            values.append(title)
        if content_type is not None:
            updates.append("type = ?")
            values.append(content_type)
        if body is not None:
            updates.append("body = ?")
            values.append(body)
        if status is not None:
            updates.append("status = ?")
            values.append(status)

        if not updates:
            return {"status": "error", "message": "No updates provided"}

        updates.append("updated_at = CURRENT_TIMESTAMP")
        values.append(content_id)
        query = f"UPDATE content SET {', '.join(updates)} WHERE content_id = ?"
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            if self.cursor.rowcount == 0:
                return {"status": "error", "message": f"Content {content_id} not found"}
            return {"status": "success", "message": f"Content {content_id} updated", "content_id": content_id}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_content(self, content_id: str) -> Dict[str, Any]:
        """Retrieve content details"""
        self.cursor.execute("SELECT * FROM content WHERE content_id = ?", (content_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                "status": "success",
                "content": {
                    "content_id": row[0],
                    "campaign_id": row[1],
                    "title": row[2],
                    "type": row[3],
                    "body": row[4],
                    "status": row[5],
                    "created_at": row[6],
                    "updated_at": row[7]
                }
            }
        return {"status": "error", "message": f"Content {content_id} not found"}

    def get_campaign_content(self, campaign_id: str, status: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve all content for a campaign, optionally filtered by status"""
        query = "SELECT * FROM content WHERE campaign_id = ?"
        params = [campaign_id]
        if status:
            query += " AND status = ?"
            params.append(status)

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        content_items = []
        for row in rows:
            content_items.append({
                "content_id": row[0],
                "campaign_id": row[1],
                "title": row[2],
                "type": row[3],
                "body": row[4],
                "status": row[5],
                "created_at": row[6],
                "updated_at": row[7]
            })
        return {"status": "success", "content": content_items}

    def add_metric(self, metric_id: str, campaign_id: Optional[str] = None, content_id: Optional[str] = None, metric_type: str = "Impression", value: float = 0.0) -> Dict[str, Any]:
        """Add a performance metric for a campaign or content"""
        try:
            self.cursor.execute("""
            INSERT INTO metrics (metric_id, campaign_id, content_id, metric_type, value)
            VALUES (?, ?, ?, ?, ?)
            """, (metric_id, campaign_id, content_id, metric_type, value))
            self.conn.commit()
            return {"status": "success", "message": f"Metric {metric_id} added", "metric_id": metric_id}
        except sqlite3.IntegrityError:
            return {"status": "error", "message": f"Metric {metric_id} already exists"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_campaign_metrics(self, campaign_id: str, metric_type: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve metrics for a campaign, optionally filtered by type"""
        query = "SELECT * FROM metrics WHERE campaign_id = ?"
        params = [campaign_id]
        if metric_type:
            query += " AND metric_type = ?"
            params.append(metric_type)

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        metrics = []
        for row in rows:
            metrics.append({
                "metric_id": row[0],
                "campaign_id": row[1],
                "content_id": row[2],
                "metric_type": row[3],
                "value": row[4],
                "recorded_at": row[5]
            })
        return {"status": "success", "metrics": metrics}

    def get_content_metrics(self, content_id: str, metric_type: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve metrics for a content item, optionally filtered by type"""
        query = "SELECT * FROM metrics WHERE content_id = ?"
        params = [content_id]
        if metric_type:
            query += " AND metric_type = ?"
            params.append(metric_type)

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        metrics = []
        for row in rows:
            metrics.append({
                "metric_id": row[0],
                "campaign_id": row[1],
                "content_id": row[2],
                "metric_type": row[3],
                "value": row[4],
                "recorded_at": row[5]
            })
        return {"status": "success", "metrics": metrics}

    def close(self) -> None:
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def __del__(self):
        """Ensure connection is closed on object deletion"""
        self.close()
