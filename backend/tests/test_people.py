import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app
import json
import uuid

client = TestClient(app)

def test_create_person_duplicate_email():
    # 1. Create a person with a unique email
    unique_email = f"test_{uuid.uuid4()}@example.com"
    payload = {
        "name": "Integration Test User",
        "email": unique_email,
        "custom_data": json.dumps({"role": "tester"})
    }
    
    response = client.post("/api/people/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == unique_email
    
    # 2. Try to create the same person again
    response_dup = client.post("/api/people/", json=payload)
    
    # 3. Verify we get 400 Bad Request (not 500)
    assert response_dup.status_code == 400
    assert response_dup.json()["detail"] == "A person with this email already exists."
