import os
import sys
import pytest
from flask import Flask
from api_auth_utils import limiter
from werkzeug.security import generate_password_hash
from models import db ,User , Department , Complaint , Assignment
# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app
from models import db

@pytest.fixture
def client():
    """Test client for the app."""
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_SECRET_KEY': 'test-secret-key',
        'RATELIMIT_STORAGE_URI': 'memory://',
        'RATELIMIT_ENABLED': False,  # Disable rate limiting for tests
    })

    with flask_app.app_context():
        limiter.enabled = False
    
    with flask_app.app_context():
        db.create_all()
        yield flask_app.test_client()
        db.session.remove()
        db.drop_all()


#==============================================
#----------ADMIN TEST FIXTURES----------------
#==============================================

@pytest.fixture
def sample_admin_data():
    """Sample valid user data."""
    return {
        "fullName": "Admin",
        "email": "admin1@gmail.com",
        "mobile": "9991999999",
        "role": "Admin",
        "address": "123 Main Street",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400001",
        "gender": "Male",
        "password": "Admin@123"
    }

@pytest.fixture
def registered_admin(sample_admin_data):
    """Fixture that pre-registers an active user directly into the database."""
    # Create the user object exactly how your backend expects it
    user = User(
        name=sample_admin_data["fullName"],
        email=sample_admin_data["email"].lower(),
        phone=sample_admin_data["mobile"],
        password=generate_password_hash(sample_admin_data["password"]),
        address=sample_admin_data["address"],
        city=sample_admin_data["city"],
        state=sample_admin_data.get("state"),
        pincode=sample_admin_data["pincode"],
        gender=sample_admin_data.get("gender"),
        role=sample_admin_data["role"],
        status='active'  # Explicitly make them active so login doesn't return 403
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Return both the database user object and the raw password for testing login
    return {
        "user_record": user,
        "raw_credentials": {
            "email": sample_admin_data["email"],
            "password": sample_admin_data["password"]
        }
    }


@pytest.fixture
def admin_auth_headers(client, registered_admin):
    """Get authentication headers for admin user."""

    credentaisl = registered_admin['raw_credentials']
    response = client.post('/api/login', json={
        'email': credentaisl['email'],
        'password': credentaisl['password']
    })
    data = response.get_json()
    return {
        'Authorization': f"Bearer {data['access_token']}",
        'refresh_token': data['refresh_token'],
        'user_id': registered_admin['user_record'].id
    }


#==============================================
#----------CITIZEN TEST FIXTURES----------------
#==============================================


@pytest.fixture
def sample_officer_data():
    """Sample valid user data."""
    return {
        "fullName": "Officer",
        "email": "officer@gmail.com",
        "mobile": "9999999999",
        "role": "Officer",
        "address": "123 Main Street",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400001",
        "gender": "Male",
        "password": "Officer@123"
    }



@pytest.fixture
def sample_user_data():
    """Sample valid user data for registration and login tests."""
    return {
        "fullName": "John Doe",
        "email": "john.doe@example.com",
        "mobile": "9876543210",
        "role": "Citizen",
        "address": "123 Main Street",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400001",
        "gender": "Male",
        "password": "TestPassword123"
    }


@pytest.fixture
def registered_user(sample_user_data):
    """Fixture that pre-registers an active user directly into the database."""
    # Create the user object exactly how your backend expects it
    user = User(
        name=sample_user_data["fullName"],
        email=sample_user_data["email"].lower(),
        phone=sample_user_data["mobile"],
        password=generate_password_hash(sample_user_data["password"]),
        address=sample_user_data["address"],
        city=sample_user_data["city"],
        state=sample_user_data.get("state"),
        pincode=sample_user_data["pincode"],
        gender=sample_user_data.get("gender"),
        role=sample_user_data["role"],
        status='active'  # Explicitly make them active so login doesn't return 403
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Return both the database user object and the raw password for testing login
    return {
        "user_record": user,
        "raw_credentials": {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
    }


@pytest.fixture
def registered_officer(sample_officer_data):
    """Fixture that pre-registers an active user directly into the database."""
    # Create the user object exactly how your backend expects it
    user = User(
        name=sample_officer_data["fullName"],
        email=sample_officer_data["email"].lower(),
        phone=sample_officer_data["mobile"],
        password=generate_password_hash(sample_officer_data["password"]),
        address=sample_officer_data["address"],
        city=sample_officer_data["city"],
        state=sample_officer_data.get("state"),
        pincode=sample_officer_data["pincode"],
        gender=sample_officer_data.get("gender"),
        role=sample_officer_data["role"],
        status= 'pending'
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Return both the database user object and the raw password for testing login
    return {
        "user_record": user,
        "raw_credentials": {
            "email": sample_officer_data["email"],
            "password": sample_officer_data["password"]
        }
    }

@pytest.fixture
def pending_officer(registered_officer):
    return registered_officer['user_record']


###########################################################

@pytest.fixture
def citizen_auth_headers(client, registered_user):
    """Get authentication headers for citizen user."""

    credentials = registered_user['raw_credentials']

    response = client.post('/api/login', json={
        'email': credentials['email'],
        'password': credentials['password']
    })
    data = response.get_json()
    return {
        'Authorization': f"Bearer {data['access_token']}",
        'refresh_token': data['refresh_token'],
        'user_id': registered_user['user_record'].id
    }


@pytest.fixture
def sample_complaint_data():
    """Sample complaint data for testing."""
    return {
        "title": "Pothole on Main Road",
        "category": "Potholes",
        "priority": "High",
        "description": "There is a large pothole on Main Road near the market. It has been there for weeks and is causing traffic issues.",
        "city": "Mumbai",
        "ward": "Ward 5",
        "area": "Andheri East",
        "street": "Main Road",
        "landmark": "Near City Market",
        "incidentDate": "2026-08-01",
        "visitTime": "10:00 AM",
        "urgencyNote": "This needs immediate attention as it's causing accidents."
    }

@pytest.fixture
def created_complaint(client, citizen_auth_headers, sample_complaint_data):

    """Create a complaint and return the complaint ID."""
    response = client.post('/api/citizen/complaints', 
                          data=sample_complaint_data,
                          headers=citizen_auth_headers,
                          content_type='multipart/form-data')
    data = response.get_json()
    return data['complaint']['raw_id']


#====================================================
#====================================================

@pytest.fixture
def test_department(registered_admin):

    """Create a test department."""
    dept = Department(
        department_name="Test Department",
        code="TEST",
        description="Test department for admin tests",
        status="Active",
        user_id=registered_admin['user_record'].id
    )
    db.session.add(dept)
    db.session.commit()
    db.session.refresh(dept)
    return dept

#=================================================
#=================================================

@pytest.fixture
def test_complaint(client, registered_admin):
    """Create a test complaint."""
    complaint = Complaint(
        title="Test Complaint",
        category="Potholes",
        description="This is a test complaint for admin testing.",
        priority="High",
        department="Test Department",
        location="Test Location",
        ward="Ward 1",
        area="Test Area",
        street="Test Street",
        created_by=registered_admin['user_record'].id,
        status="Pending"
    )
    db.session.add(complaint)
    db.session.commit()
    db.session.refresh(complaint)
    return complaint

@pytest.fixture
def worker_user(client):
    """Create a worker user."""
    from werkzeug.security import generate_password_hash
    
    user = User(
        name="Worker Test",
        email="worker@example.com",
        phone="9876543212",
        password=generate_password_hash("TestPassword123"),
        address="Worker Address",
        city="Mumbai",
        state="Maharashtra",
        pincode="400003",
        gender="Male",
        role="Worker",
        status="active"
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    return user

@pytest.fixture
def worker_auth_headers(client, worker_user):
    """Get authentication headers for worker user."""
    response = client.post('/api/login', json={
        'email': worker_user.email,
        'password': 'TestPassword123'
    })
    data = response.get_json()
    return {
        'Authorization': f"Bearer {data['access_token']}",
        'refresh_token': data['refresh_token'],
        'user_id': worker_user.id
    }




@pytest.fixture
def assigned_complaint(client, worker_user, registered_admin, test_department):
    """Create a complaint assigned to the worker."""
    worker_user.department_id = test_department.id 
    db.session.commit()

    complaint = Complaint(
        title="Assigned Task",
        category="Potholes",
        description="This is a task assigned to the worker for testing.",
        priority="High",
        department=test_department.department_name,
        location="Test Location",
        ward="Ward 1",
        area="Test Area",
        street="Test Street",
        created_by=registered_admin['user_record'].id,
        assigned_officer=registered_admin['user_record'].id,
        status="Assigned"
    )
    db.session.add(complaint)
    db.session.commit()
    db.session.refresh(complaint)
    
    # Create assignment
    assignment = Assignment(
        complaint_id=complaint.id,
        worker_id=worker_user.id,
        assigned_by=registered_admin['user_record'].id
    )
    db.session.add(assignment)
    db.session.commit()
    
    return complaint


