import sqlite3
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class InnovationIdea:
    idea_id: str
    title: str
    description: str
    submitter_id: str
    submission_date: str
    status: str
    category: str
    potential_impact: Dict[str, Any]

@dataclass
class InnovationFeedback:
    feedback_id: str
    idea_id: str
    reviewer_id: str
    feedback_text: str
    feedback_date: str
    rating: float

class ProductInnovationDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self._initialize_db()

    def _initialize_db(self) -> None:
        """Initialize database connection and create tables if not exists."""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        # Innovation Ideas Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS innovation_ideas (
            idea_id TEXT PRIMARY KEY,
            title TEXT,
            description TEXT,
            submitter_id TEXT,
            submission_date TEXT,
            status TEXT,
            category TEXT,
            potential_impact TEXT
        )
        """)
        # Innovation Feedback Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS innovation_feedback (
            feedback_id TEXT PRIMARY KEY,
            idea_id TEXT,
            reviewer_id TEXT,
            feedback_text TEXT,
            feedback_date TEXT,
            rating REAL,
            FOREIGN KEY (idea_id) REFERENCES innovation_ideas(idea_id)
        )
        """)
        self.conn.commit()

    def add_innovation_idea(self, idea: InnovationIdea) -> bool:
        """Add a new innovation idea to the database."""
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO innovation_ideas 
        (idea_id, title, description, submitter_id, submission_date, status, category, potential_impact)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (idea.idea_id, idea.title, idea.description, idea.submitter_id, 
              idea.submission_date, idea.status, idea.category, str(idea.potential_impact)))
        self.conn.commit()
        return cursor.rowcount > 0

    def update_innovation_idea(self, idea_id: str, title: Optional[str] = None, 
                               description: Optional[str] = None, status: Optional[str] = None, 
                               category: Optional[str] = None, 
                               potential_impact: Optional[Dict[str, Any]] = None) -> bool:
        """Update an existing innovation idea."""
        cursor = self.conn.cursor()
        update_fields = []
        values = []
        if title is not None:
            update_fields.append("title = ?")
            values.append(title)
        if description is not None:
            update_fields.append("description = ?")
            values.append(description)
        if status is not None:
            update_fields.append("status = ?")
            values.append(status)
        if category is not None:
            update_fields.append("category = ?")
            values.append(category)
        if potential_impact is not None:
            update_fields.append("potential_impact = ?")
            values.append(str(potential_impact))
        if update_fields:
            values.append(idea_id)
            query = f"UPDATE innovation_ideas SET {', '.join(update_fields)} WHERE idea_id = ?"
            cursor.execute(query, values)
            self.conn.commit()
            return cursor.rowcount > 0
        return False

    def get_innovation_idea(self, idea_id: str) -> Optional[InnovationIdea]:
        """Retrieve an innovation idea by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM innovation_ideas WHERE idea_id = ?", (idea_id,))
        row = cursor.fetchone()
        if row:
            return InnovationIdea(
                idea_id=row[0],
                title=row[1],
                description=row[2],
                submitter_id=row[3],
                submission_date=row[4],
                status=row[5],
                category=row[6],
                potential_impact=eval(row[7]) if row[7] else {}
            )
        return None

    def get_ideas_by_status(self, status: str) -> List[InnovationIdea]:
        """Retrieve innovation ideas by status."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM innovation_ideas WHERE status = ?", (status,))
        rows = cursor.fetchall()
        return [InnovationIdea(
            idea_id=row[0],
            title=row[1],
            description=row[2],
            submitter_id=row[3],
            submission_date=row[4],
            status=row[5],
            category=row[6],
            potential_impact=eval(row[7]) if row[7] else {}
        ) for row in rows]

    def get_ideas_by_category(self, category: str) -> List[InnovationIdea]:
        """Retrieve innovation ideas by category."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM innovation_ideas WHERE category = ?", (category,))
        rows = cursor.fetchall()
        return [InnovationIdea(
            idea_id=row[0],
            title=row[1],
            description=row[2],
            submitter_id=row[3],
            submission_date=row[4],
            status=row[5],
            category=row[6],
            potential_impact=eval(row[7]) if row[7] else {}
        ) for row in rows]

    def add_feedback(self, feedback: InnovationFeedback) -> bool:
        """Add feedback for an innovation idea."""
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO innovation_feedback 
        (feedback_id, idea_id, reviewer_id, feedback_text, feedback_date, rating)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (feedback.feedback_id, feedback.idea_id, feedback.reviewer_id, 
              feedback.feedback_text, feedback.feedback_date, feedback.rating))
        self.conn.commit()
        return cursor.rowcount > 0

    def get_feedback_by_idea(self, idea_id: str) -> List[InnovationFeedback]:
        """Retrieve feedback for a specific innovation idea."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM innovation_feedback WHERE idea_id = ?", (idea_id,))
        rows = cursor.fetchall()
        return [InnovationFeedback(
            feedback_id=row[0],
            idea_id=row[1],
            reviewer_id=row[2],
            feedback_text=row[3],
            feedback_date=row[4],
            rating=row[5]
        ) for row in rows]

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
