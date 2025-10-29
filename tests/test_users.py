import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_users_empty(client: AsyncClient):
    """Test getting all users when there are none"""
    response = await client.get("/api/users")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, sample_user_data):
    """Test creating a new user"""
    response = await client.post("/api/users", json=sample_user_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["username"] == sample_user_data["username"]
    assert data["age"] == sample_user_data["age"]
    assert data["eye_color"] == sample_user_data["eye_color"]
    assert "id" in data
    assert isinstance(data["id"], int)


@pytest.mark.asyncio
async def test_get_users_with_data(client: AsyncClient, sample_user_data):
    """Test getting all users after creating one"""
    # Create a user
    create_response = await client.post("/api/users", json=sample_user_data)
    assert create_response.status_code == 200
    
    # Get all users
    response = await client.get("/api/users")
    assert response.status_code == 200
    
    users = response.json()
    assert len(users) == 1
    assert users[0]["username"] == sample_user_data["username"]
    assert users[0]["age"] == sample_user_data["age"]
    assert users[0]["eye_color"] == sample_user_data["eye_color"]


@pytest.mark.asyncio
async def test_get_user_by_id(client: AsyncClient, sample_user_data):
    """Test getting a user by ID"""
    # Create a user
    create_response = await client.post("/api/users", json=sample_user_data)
    assert create_response.status_code == 200
    created_user = create_response.json()
    user_id = created_user["id"]
    
    # Get user by ID
    response = await client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == sample_user_data["username"]
    assert data["age"] == sample_user_data["age"]
    assert data["eye_color"] == sample_user_data["eye_color"]


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(client: AsyncClient):
    """Test getting a user by ID that doesn't exist"""
    response = await client.get("/api/users/999")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, sample_user_data, sample_user_update_data):
    """Test updating a user"""
    # Create a user
    create_response = await client.post("/api/users", json=sample_user_data)
    assert create_response.status_code == 200
    created_user = create_response.json()
    user_id = created_user["id"]
    
    # Update user
    response = await client.put(f"/api/users/{user_id}", json=sample_user_update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == sample_user_update_data["username"]
    assert data["age"] == sample_user_update_data["age"]
    assert data["eye_color"] == sample_user_update_data["eye_color"]


@pytest.mark.asyncio
async def test_update_user_partial(client: AsyncClient, sample_user_data):
    """Test updating a user with partial data"""
    # Create a user
    create_response = await client.post("/api/users", json=sample_user_data)
    assert create_response.status_code == 200
    created_user = create_response.json()
    user_id = created_user["id"]
    
    # Update only username
    update_data = {"username": "partiallyupdated"}
    response = await client.put(f"/api/users/{user_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["username"] == "partiallyupdated"
    # Age and eye_color should remain unchanged
    assert data["age"] == sample_user_data["age"]
    assert data["eye_color"] == sample_user_data["eye_color"]


@pytest.mark.asyncio
async def test_update_user_not_found(client: AsyncClient, sample_user_update_data):
    """Test updating a user that doesn't exist"""
    response = await client.put("/api/users/999", json=sample_user_update_data)
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, sample_user_data):
    """Test deleting a user"""
    # Create a user
    create_response = await client.post("/api/users", json=sample_user_data)
    assert create_response.status_code == 200
    created_user = create_response.json()
    user_id = created_user["id"]
    
    # Delete user
    response = await client.delete(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"
    
    # Verify user is deleted
    get_response = await client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user_not_found(client: AsyncClient):
    """Test deleting a user that doesn't exist"""
    response = await client.delete("/api/users/999")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_user_validation(client: AsyncClient):
    """Test user creation validation"""
    # Test with missing required fields
    response = await client.post("/api/users", json={"username": "test"})
    assert response.status_code == 422  # Validation error
    
    # Test with invalid age (negative)
    response = await client.post("/api/users", json={
        "username": "test",
        "age": -1,
        "eye_color": "Blue"
    })
    assert response.status_code == 422  # Validation error
    
    # Test with age zero
    response = await client.post("/api/users", json={
        "username": "test",
        "age": 0,
        "eye_color": "Blue"
    })
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_update_user_validation(client: AsyncClient, sample_user_data):
    """Test user update validation"""
    # Create a user first
    create_response = await client.post("/api/users", json=sample_user_data)
    user_id = create_response.json()["id"]
    
    # Test with invalid age
    response = await client.put(f"/api/users/{user_id}", json={"age": -5})
    assert response.status_code == 422  # Validation error
    
    # Test with age zero
    response = await client.put(f"/api/users/{user_id}", json={"age": 0})
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_multiple_users(client: AsyncClient):
    """Test creating and retrieving multiple users"""
    # Create multiple users
    users_data = [
        {"username": "user1", "age": 20, "eye_color": "Blue"},
        {"username": "user2", "age": 25, "eye_color": "Brown"},
        {"username": "user3", "age": 30, "eye_color": "Green"},
    ]
    
    created_ids = []
    for user_data in users_data:
        response = await client.post("/api/users", json=user_data)
        assert response.status_code == 200
        created_ids.append(response.json()["id"])
    
    # Get all users
    response = await client.get("/api/users")
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 3
    
    # Verify all users are present
    usernames = {user["username"] for user in users}
    assert usernames == {"user1", "user2", "user3"}

