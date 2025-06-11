from typing import List, Dict, Any, Optional
import sqlite3
from datetime import datetime

class ProjectManagement:
    def __init__(self, db_path: str = 'ventai_projects.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.initialize_db()

    def initialize_db(self) -> None:
        """Initialize the SQLite database with necessary tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # Create projects table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                project_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                start_date TEXT,
                end_date TEXT,
                budget REAL,
                status TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')

        # Create tasks table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                project_id TEXT,
                name TEXT NOT NULL,
                description TEXT,
                start_date TEXT,
                end_date TEXT,
                status TEXT,
                priority TEXT,
                assigned_to TEXT,
                created_at TEXT,
                updated_at TEXT,
                FOREIGN KEY (project_id) REFERENCES projects(project_id)
            )
        ''')

        # Create resources table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS resources (
                resource_id TEXT PRIMARY KEY,
                project_id TEXT,
                name TEXT NOT NULL,
                type TEXT,
                quantity REAL,
                cost_per_unit REAL,
                status TEXT,
                created_at TEXT,
                updated_at TEXT,
                FOREIGN KEY (project_id) REFERENCES projects(project_id)
            )
        ''')

        self.conn.commit()

    def add_project(self, project_id: str, name: str, description: str, start_date: str, end_date: str, budget: float, status: str = 'Initiated') -> Dict[str, Any]:
        """Add a new project to the database"""
        try:
            current_time = datetime.now().isoformat()
            self.cursor.execute('''
                INSERT INTO projects (project_id, name, description, start_date, end_date, budget, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (project_id, name, description, start_date, end_date, budget, status, current_time, current_time))
            self.conn.commit()
            return {
                "status": "success",
                "message": f"Project {project_id} added successfully",
                "project_id": project_id
            }
        except sqlite3.Error as e:
            return {
                "status": "error",
                "message": str(e),
                "project_id": project_id
            }

    def update_project(self, project_id: str, name: Optional[str] = None, description: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, budget: Optional[float] = None, status: Optional[str] = None) -> Dict[str, Any]:
        """Update project details in the database"""
        try:
            updates = []
            values = []
            if name is not None:
                updates.append("name = ?")
                values.append(name)
            if description is not None:
                updates.append("description = ?")
                values.append(description)
            if start_date is not None:
                updates.append("start_date = ?")
                values.append(start_date)
            if end_date is not None:
                updates.append("end_date = ?")
                values.append(end_date)
            if budget is not None:
                updates.append("budget = ?")
                values.append(budget)
            if status is not None:
                updates.append("status = ?")
                values.append(status)

            if updates:
                updates.append("updated_at = ?")
                values.append(datetime.now().isoformat())
                values.append(project_id)
                query = f"UPDATE projects SET {', '.join(updates)} WHERE project_id = ?"
                self.cursor.execute(query, values)
                self.conn.commit()
                return {
                    "status": "success",
                    "message": f"Project {project_id} updated successfully",
                    "project_id": project_id
                }
            else:
                return {
                    "status": "error",
                    "message": "No updates provided",
                    "project_id": project_id
                }
        except sqlite3.Error as e:
            return {
                "status": "error",
                "message": str(e),
                "project_id": project_id
            }

    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Retrieve project details from the database"""
        try:
            self.cursor.execute("SELECT * FROM projects WHERE project_id = ?", (project_id,))
            project = self.cursor.fetchone()
            if project:
                return {
                    "status": "success",
                    "project": {
                        "project_id": project[0],
                        "name": project[1],
                        "description": project[2],
                        "start_date": project[3],
                        "end_date": project[4],
                        "budget": project[5],
                        "status": project[6],
                        "created_at": project[7],
                        "updated_at": project[8]
                    }
                }
            else:
                return {
                    "status": "error",
                    "message": f"Project {project_id} not found",
                    "project_id": project_id
                }
        except sqlite3.Error as e:
            return {
                "status": "error",
                "message": str(e),
                "project_id": project_id
            }

    def get_all_projects(self) -> Dict[str, Any]:
        """Retrieve all projects from the database"""
        try:
            self.cursor.execute("SELECT * FROM projects")
            projects = self.cursor.fetchall()
            return {
                "status": "success",
                "projects": [{
                    "project_id": p[0],
                    "name": p[1],
                    "description": p[2],
                    "start_date": p[3],
                    "end_date": p[4],
                    "budget": p[5],
                    "status": p[6],
                    "created_at": p[7],
                    "updated_at": p[8]
                } for p in projects]
            }
        except sqlite3.Error as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def add_task(self, task_id: str, project_id: str, name: str, description: str, start_date: str, end_date: str, status: str = 'Not Started', priority: str = 'Medium', assigned_to: Optional[str] = None) -> Dict[str, Any]:
        """Add a new task to a project"""
        try:
            current_time = datetime.now().isoformat()
            self.cursor.execute('''
                INSERT INTO tasks (task_id, project_id, name, description, start_date, end_date, status, priority, assigned_to, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (task_id, project_id, name, description, start_date, end_date, status, priority, assigned_to, current_time, current_time))
            self.conn.commit()
            return {
                "status": "success",
                "message": f"Task {task_id} added to project {project_id} successfully",
                "task_id": task_id,
                "project_id": project_id
            }
        except sqlite3.Error as e:
            return {
                "status": "error",
                "message": str(e),
                "task_id": task_id,
                "project_id": project_id
            }

    def update_task(self, task_id: str, name: Optional[str] = None, description: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, status: Optional[str] = None, priority: Optional[str] = None, assigned_to: Optional[str] = None) -> Dict[str, Any]:
        """Update task details in the database"""
        try:
            updates = []
            values = []
            if name is not None:
                updates.append("name = ?")
                values.append(name)
            if description is not None:
                updates.append("description = ?")
                values.append(description)
            if start_date is not None:
                updates.append("start_date = ?")
                values.append(start_date)
            if end_date is not None:
                updates.append("end_date = ?")
                values.append(end_date)
            if status is not None:
                updates.append("status = ?")
                values.append(status)
            if priority is not None:
                updates.append("priority = ?")
                values.append(priority)
            if assigned_to is not None:
                updates.append("assigned_to = ?")
                values.append(assigned_to)

            if updates:
                updates.append("updated_at = ?")
                values.append(datetime.now().isoformat())
                values.append(task_id)
                query = f"UPDATE tasks SET {', '.join(updates)} WHERE task_id = ?"
                self.cursor.execute(query, values)
                self.conn.commit()
                return {
                    "status": "success",
                    "message": f"Task {task_id} updated successfully",
                    "task_id": task_id
                }
            else:
                return {
                    "status": "error",
                    "message": "No updates provided",
                    "task_id": task_id
                }
        except sqlite3.Error as e:
            return {
                "status": "error",
                "message": str(e),
                "task_id": task_id
            }

    def get_tasks_by_project(self, project_id: str) -> Dict[str, Any]:
        """Retrieve all tasks for a specific project"""
        try:
            self.cursor.execute("SELECT * FROM tasks WHERE project_id = ?", (project_id,))
            tasks = self.cursor.fetchall()
            return {
                "status": "success",
                "tasks": [{
                    "task_id": t[0],
                    "project_id": t[1],
                    "name": t[2],
                    "description": t[3],
                    "start_date": t[4],
                    "end_date": t[5],
                    "status": t[6],
                    "priority": t[7],
                    "assigned_to": t[8],
                    "created_at": t[9],
                    "updated_at": t[10]
                } for t in tasks],
                "project_id": project_id
            }
        except sqlite3.Error as e:
            return {
                "status": "error",
                "message": str(e),
                "project_id": project_id
            }

    def add_resource(self, resource_id: str, project_id: str, name: str, resource_type: str, quantity: float, cost_per_unit: float, status: str = 'Available') -> Dict[str, Any]:
        """Add a new resource to a project"""
        try:
            current_time = datetime.now().isoformat()
            self.cursor.execute('''
                INSERT INTO resources (resource_id, project_id, name, type, quantity, cost_per_unit, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (resource_id, project_id, name, resource_type, quantity, cost_per_unit, status, current_time, current_time))
            self.conn.commit()
            return {
                "status": "success",
                "message": f"Resource {resource_id} added to project {project_id} successfully",
                "resource_id": resource_id,
                "project_id": project_id
            }
        except sqlite3.Error as e:
            return {
                "status": "error",
                "message": str(e),
                "resource_id": resource_id,
                "project_id": project_id
            }

    def update_resource(self, resource_id: str, name: Optional[str] = None, resource_type: Optional[str] = None, quantity: Optional[float] = None, cost_per_unit: Optional[float] = None, status: Optional[str] = None) -> Dict[str, Any]:
        """Update resource details in the database"""
        try:
            updates = []
            values = []
            if name is not None:
                updates.append("name = ?")
                values.append(name)
            if resource_type is not None:
                updates.append("type = ?")
                values.append(resource_type)
            if quantity is not None:
                updates.append("quantity = ?")
                values.append(quantity)
            if cost_per_unit is not None:
                updates.append("cost_per_unit = ?")
                values.append(cost_per_unit)
            if status is not None:
                updates.append("status = ?")
                values.append(status)

            if updates:
                updates.append("updated_at = ?")
                values.append(datetime.now().isoformat())
                values.append(resource_id)
                query = f"UPDATE resources SET {', '.join(updates)} WHERE resource_id = ?"
                self.cursor.execute(query, values)
                self.conn.commit()
                return {
                    "status": "success",
                    "message": f"Resource {resource_id} updated successfully",
                    "resource_id": resource_id
                }
            else:
                return {
                    "status": "error",
                    "message": "No updates provided",
                    "resource_id": resource_id
                }
        except sqlite3.Error as e:
            return {
                "status": "error",
                "message": str(e),
                "resource_id": resource_id
            }

    def get_resources_by_project(self, project_id: str) -> Dict[str, Any]:
        """Retrieve all resources for a specific project"""
        try:
            self.cursor.execute("SELECT * FROM resources WHERE project_id = ?", (project_id,))
            resources = self.cursor.fetchall()
            return {
                "status": "success",
                "resources": [{
                    "resource_id": r[0],
                    "project_id": r[1],
                    "name": r[2],
                    "type": r[3],
                    "quantity": r[4],
                    "cost_per_unit": r[5],
                    "status": r[6],
                    "created_at": r[7],
                    "updated_at": r[8]
                } for r in resources],
                "project_id": project_id
            }
        except sqlite3.Error as e:
            return {
                "status": "error",
                "message": str(e),
                "project_id": project_id
            }

    def get_project_summary(self, project_id: str) -> Dict[str, Any]:
        """Get a summary of a project including tasks and resources"""
        project_data = self.get_project(project_id)
        if project_data["status"] != "success":
            return project_data

        tasks_data = self.get_tasks_by_project(project_id)
        resources_data = self.get_resources_by_project(project_id)

        return {
            "status": "success",
            "project": project_data.get("project", {}),
            "tasks": tasks_data.get("tasks", []),
            "resources": resources_data.get("resources", []),
            "project_id": project_id
        }

    def close(self) -> None:
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
