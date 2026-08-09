import pytest
from models import User
from models import User, LoginSession
from werkzeug.security import generate_password_hash
from models import db

def test_register_success(client, sample_user_data):
    """Test successful user registration."""
    response = client.post('/api/register', json=sample_user_data)
    data = response.get_json()
    
    assert response.status_code == 201
    assert data['success'] is True
    assert 'Registration successful' in data['message']
    
    # Verify user was created in database
    user = User.query.filter_by(email=sample_user_data['email']).first()
    assert user is not None
    assert user.name == sample_user_data['fullName']
    assert user.email == sample_user_data['email']
    assert user.role == 'Citizen'
    assert user.status == 'active'



def test_register_officer_needs_approval(client):
    """Test registration for officer role needs admin approval."""
    data = {
        "fullName": "Officer Jane",
        "email": "officer@example.com",
        "mobile": "9876543211",
        "role": "Officer",
        "address": "Police Station",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400002",
        "gender": "Female",
        "password": "TestPassword123"
    }
    
    response = client.post('/api/register', json=data)
    response_data = response.get_json()
    
    assert response.status_code == 201
    assert response_data['success'] is True
    assert 'pending admin approval' in response_data['message']
    
    user = User.query.filter_by(email=data['email']).first()
    assert user.status == 'pending'

def test_register_duplicate_email(client, sample_user_data):
    """Test registration with duplicate email."""
    # First registration
    client.post('/api/register', json=sample_user_data)
    
    # Second registration with same email
    response = client.post('/api/register', json=sample_user_data)
    data = response.get_json()
    
    assert response.status_code == 409
    assert 'already registered' in data['message']






def test_register_worker_needs_approval(client):
    """Test registration for worker role needs admin approval."""
    data = {
        "fullName": "Worker John",
        "email": "worker@example.com",
        "mobile": "9876543212",
        "role": "Worker",
        "address": "Workshop Area",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400003",
        "gender": "Male",
        "password": "TestPassword123"
    }
    
    response = client.post('/api/register', json=data)
    response_data = response.get_json()
    
    assert response.status_code == 201
    assert response_data['success'] is True
    assert 'pending admin approval' in response_data['message']
    
    user = User.query.filter_by(email=data['email']).first()
    assert user.status == 'pending'













def test_login_success(client, registered_user):
    """Test successful login with an already registered user."""
    
    # Extract the pre-made credentials from our new fixture
    credentials = registered_user["raw_credentials"]
    
    # Perform the login action
    response = client.post('/api/login', json={
        'email': credentials['email'],
        'password': credentials['password']
    })
    
    data = response.get_json()
    
    # Assertions
    assert response.status_code == 200
    assert data['success'] is True
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data['user']['email'] == credentials['email'].lower()



def test_login_with_wrong_password(client, sample_user_data):
    """Test login with wrong password."""
    # Register a user
    client.post('/api/register', json=sample_user_data)
    
    # Login with wrong password
    response = client.post('/api/login', json={
        'email': sample_user_data['email'],
        'password': 'WrongPassword123'
    })
    data = response.get_json()
    
    assert response.status_code == 401
    assert 'Invalid email or password' in data['message']
    assert 'access_token' not in data

def test_login_with_nonexistent_email(client):
    """Test login with email that doesn't exist."""
    response = client.post('/api/login', json={
        'email': 'nonexistent@example.com',
        'password': 'TestPassword123'
    })
    data = response.get_json()
    
    assert response.status_code == 401
    assert 'Invalid email or password' in data['message']

def test_login_inactive_user(client, sample_user_data):
    """Test login with inactive/disabled user."""
    # Register a user
    client.post('/api/register', json=sample_user_data)
    
    # Manually set user status to inactive
    user = User.query.filter_by(email=sample_user_data['email']).first()
    user.status = 'inactive'
    db.session.commit()
    
    # Try to login
    response = client.post('/api/login', json={
        'email': sample_user_data['email'],
        'password': sample_user_data['password']
    })
    data = response.get_json()
    
    assert response.status_code == 403
    assert 'disabled' in data['message']

def test_login_pending_user(client , registered_officer):
    """Test login with pending user (not approved by admin)."""

    credentials = registered_officer['raw_credentials']
    
    response = client.post('/api/login', json={
        'email': credentials['email'],
        'password': credentials['password']
    })
    data = response.get_json()
    
    assert response.status_code == 403
    assert 'pending admin approval' in data['message']






def test_login_returns_user_info(client, sample_user_data):
    """Test that login returns correct user information."""
    # Register a user
    client.post('/api/register', json=sample_user_data)
    
    # Login
    response = client.post('/api/login', json={
        'email': sample_user_data['email'],
        'password': sample_user_data['password']
    })
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['user']['name'] == sample_user_data['fullName']
    assert data['user']['email'] == sample_user_data['email']
    assert data['user']['role'] == 'Citizen'
    assert 'profilePhoto' in data['user']
    assert 'id' in data['user']





