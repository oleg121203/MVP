import pytest
from ventai.backend.main import app
from ventai.backend.database import Base, get_db

@pytest.fixture
def client():
    return TestClient(app)

# Test cases remain the same as before
