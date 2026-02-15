import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app, get_db
import json
import pytest

# ... (imports)

# Setup the database for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency for tests
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_form_with_inline_sections():
    # 1. Create a custom field first to use in the form
    field_payload = {
        "entity_type": "person", 
        "key_name": "fav_color",
        "label": "Favorite Color",
        "field_type": "text",
        "options": json.dumps([]),
        "validation_rules": json.dumps({}),
        "is_active": True
    }
    response = client.post("/api/fields/", json=field_payload)
    assert response.status_code == 200, f"Failed to create field. Status: {response.status_code}, Response: {response.text}"
    field_id = response.json()["id"]

    # 2. Create Form with Inline Sections and Field Linkage
    form_payload = {
        "name": "TDD Section Form",
        "description": "Form created via TDD",
        "sections": [
            {
                "name": "Personal Details",
                "description": "Basic info",
                "order_index": 0,
                "temp_id": "temp-section-1"
            },
            {
                "name": "Employment",
                "description": "Job info",
                "order_index": 1,
                "temp_id": "temp-section-2"
            }
        ],
        "fields": [
            {
                "field_id": field_id,
                "is_required": True,
                "section_temp_id": "temp-section-1" # Link to "Personal Details"
            }
        ]
    }

    response = client.post("/api/forms/", json=form_payload)
    
    # Assertions
    assert response.status_code == 200, f"Response: {response.text}"
    data = response.json()
    assert data["name"] == "TDD Section Form"
    assert len(data["sections"]) == 2
    
    # Verify sections are created and returned
    section_names = [s["name"] for s in data["sections"]]
    assert "Personal Details" in section_names
    assert "Employment" in section_names
    
    # Verify field association with the correct section
    assert len(data["fields"]) == 1
    field_assoc = data["fields"][0]
    assert field_assoc["field_id"] == field_id
    assert field_assoc["section_id"] is not None
    
    # Verify the section_id corresponds to "Personal Details"
    # We need to find the ID of "Personal Details" section from the response
    personal_section = next(s for s in data["sections"] if s["name"] == "Personal Details")
    assert field_assoc["section_id"] == personal_section["id"]
