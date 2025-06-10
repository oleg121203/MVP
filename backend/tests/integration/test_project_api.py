import pytest
import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_project():
    response = client.post(
        "/api/v1/projects/",
        json={
            "title": "Test Project",
            "description": "This is a test project",
            "status": "In Progress"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Project"
    assert data["description"] == "This is a test project"
    assert data["status"] == "In Progress"
    assert "id" in data

    # Clean up after test
    project_id = data["id"]
    client.delete(f"/api/v1/projects/{project_id}")

def test_get_project():
    # First create a project
    response = client.post(
        "/api/v1/projects/",
        json={
            "title": "Test Project",
            "description": "This is a test project",
            "status": "In Progress"
        }
    )
    assert response.status_code == 200
    project_id = response.json()["id"]
    
    # Then get the project
    response = client.get(f"/api/v1/projects/{project_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Project"
    assert data["description"] == "This is a test project"
    assert data["status"] == "In Progress"
    assert data["id"] == project_id
    
    # Clean up after test
    client.delete(f"/api/v1/projects/{project_id}")

def test_update_project():
    # First create a project
    response = client.post(
        "/api/v1/projects/",
        json={
            "title": "Test Project",
            "description": "This is a test project",
            "status": "In Progress"
        }
    )
    assert response.status_code == 200
    project_id = response.json()["id"]
    
    # Then update the project
    response = client.put(
        f"/api/v1/projects/{project_id}",
        json={
            "title": "Updated Project",
            "description": "This is an updated test project",
            "status": "Completed"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Project"
    assert data["description"] == "This is an updated test project"
    assert data["status"] == "Completed"
    assert data["id"] == project_id
    
    # Clean up after test
    client.delete(f"/api/v1/projects/{project_id}")

def test_delete_project():
    # First create a project
    response = client.post(
        "/api/v1/projects/",
        json={
            "title": "Test Project",
            "description": "This is a test project",
            "status": "In Progress"
        }
    )
    assert response.status_code == 200
    project_id = response.json()["id"]
    
    # Then delete the project
    response = client.delete(f"/api/v1/projects/{project_id}")
    assert response.status_code == 200
    
    # Verify the project is deleted
    response = client.get(f"/api/v1/projects/{project_id}")
    assert response.status_code == 404
