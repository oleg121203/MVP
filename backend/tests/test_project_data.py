import pytest
from app.models import Project
from app.database import SessionLocal

def test_project_creation():
    db = SessionLocal()
    project = Project(
        title="Test Project",
        description="This is a test project",
        status="In Progress"
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    
    assert project.id is not None
    assert project.title == "Test Project"
    assert project.description == "This is a test project"
    assert project.status == "In Progress"
    
    db.delete(project)
    db.commit()
    db.close()

def test_project_update():
    db = SessionLocal()
    project = Project(
        title="Test Project",
        description="This is a test project",
        status="In Progress"
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    
    project.title = "Updated Project"
    project.description = "This is an updated test project"
    project.status = "Completed"
    db.commit()
    db.refresh(project)
    
    assert project.title == "Updated Project"
    assert project.description == "This is an updated test project"
    assert project.status == "Completed"
    
    db.delete(project)
    db.commit()
    db.close()
