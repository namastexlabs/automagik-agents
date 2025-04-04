import pytest
import uuid

# Test data
test_user = {
    "email": f"test_{uuid.uuid4()}@example.com",
    "phone_number": f"+1{uuid.uuid4().hex[:10]}",
    "user_data": {"test_key": "test_value"}
}

# Global variable to store created user ID
created_user_id = None

def test_list_users(client):
    """Test listing users endpoint"""
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "users" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "total_pages" in data
    
    # Check data types
    assert isinstance(data["users"], list)
    assert isinstance(data["total"], int)
    assert isinstance(data["page"], int)
    assert isinstance(data["page_size"], int)
    assert isinstance(data["total_pages"], int)

def test_create_user(client):
    """Test creating a new user"""
    global created_user_id
    
    response = client.post("/api/v1/users", json=test_user)
    assert response.status_code == 200
    
    # Check response data
    user_data = response.json()
    assert user_data["email"] == test_user["email"]
    assert user_data["phone_number"] == test_user["phone_number"]
    assert user_data["user_data"] == test_user["user_data"]
    assert "id" in user_data
    assert "created_at" in user_data
    assert "updated_at" in user_data
    
    # Store user ID for later tests
    created_user_id = user_data["id"]

def test_get_user_by_id(client):
    """Test getting a user by ID"""
    global created_user_id
    assert created_user_id is not None, "User creation test must pass before this test"
    
    response = client.get(f"/api/v1/users/{created_user_id}")
    assert response.status_code == 200
    
    # Check response data
    user_data = response.json()
    assert user_data["id"] == created_user_id
    assert user_data["email"] == test_user["email"]
    assert user_data["phone_number"] == test_user["phone_number"]
    assert user_data["user_data"] == test_user["user_data"]

def test_get_user_by_email(client):
    """Test getting a user by email"""
    response = client.get(f"/api/v1/users/{test_user['email']}")
    assert response.status_code == 200
    
    # Check response data
    user_data = response.json()
    assert user_data["email"] == test_user["email"]
    assert user_data["phone_number"] == test_user["phone_number"]
    assert user_data["user_data"] == test_user["user_data"]

def test_get_user_by_phone(client):
    """Test getting a user by phone number"""
    response = client.get(f"/api/v1/users/{test_user['phone_number']}")
    assert response.status_code == 200
    
    # Check response data
    user_data = response.json()
    assert user_data["email"] == test_user["email"]
    assert user_data["phone_number"] == test_user["phone_number"]
    assert user_data["user_data"] == test_user["user_data"]

def test_update_user(client):
    """Test updating a user"""
    global created_user_id
    assert created_user_id is not None, "User creation test must pass before this test"
    
    # Updated data
    updated_data = {
        "email": f"updated_{uuid.uuid4()}@example.com",
        "user_data": {"updated_key": "updated_value"}
    }
    
    response = client.put(f"/api/v1/users/{created_user_id}", json=updated_data)
    assert response.status_code == 200
    
    # Check response data
    user_data = response.json()
    assert user_data["id"] == created_user_id
    assert user_data["email"] == updated_data["email"]
    assert user_data["user_data"] == updated_data["user_data"]
    # Phone number should remain unchanged
    assert user_data["phone_number"] == test_user["phone_number"]

def test_get_nonexistent_user(client):
    """Test getting a user that doesn't exist"""
    response = client.get(f"/api/v1/users/{uuid.uuid4()}")
    assert response.status_code == 404

def test_delete_user(client):
    """Test deleting a user"""
    global created_user_id
    assert created_user_id is not None, "User creation test must pass before this test"
    
    response = client.delete(f"/api/v1/users/{created_user_id}")
    assert response.status_code == 200
    assert response.json() == {"success": True}
    
    # Verify user is actually deleted
    response = client.get(f"/api/v1/users/{created_user_id}")
    assert response.status_code == 404

if __name__ == "__main__":
    pytest.main(["-xvs", __file__]) 