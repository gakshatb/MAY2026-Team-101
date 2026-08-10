import pytest
import json
from io import BytesIO
from datetime import datetime, timedelta
from models import (
    db, User, Complaint, Department, ActivityLog, Feedback, 
    Announcement, ContactMessage, LoginSession, Notification,
    StatusLog
)


def test_admin_dashboard_success(client, admin_auth_headers):
    """Test admin dashboard returns all required data."""
    response = client.get('/api/admin/dashboard', headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'top_stats' in data
    assert 'department_performance' in data
    assert 'alerts' in data
    assert 'pending_approvals' in data
    assert 'platform_activity' in data
    assert 'growth_chart' in data
    assert 'category_breakdown' in data
    
    # Check top stats fields
    top_stats = data['top_stats']
    assert 'total_citizens' in top_stats
    assert 'total_officers' in top_stats
    assert 'total_workers' in top_stats
    assert 'total_complaints' in top_stats
    assert 'resolved_today' in top_stats

def test_admin_dashboard_requires_auth(client):
    """Test dashboard requires authentication."""
    response = client.get('/api/admin/dashboard')
    assert response.status_code == 401

def test_admin_dashboard_requires_admin_role(client, citizen_auth_headers):
    """Test dashboard requires admin role."""
    response = client.get('/api/admin/dashboard', headers=citizen_auth_headers)
    assert response.status_code in [403, 401]

def test_approve_pending_officer(client, admin_auth_headers, registered_officer):
    """Test approving a pending officer."""
    response = client.patch(f'/api/admin/users/{registered_officer['user_record'].id}/approve',
                           headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'approved' in data['message']
    
    # Verify user status changed
    user = User.query.get(registered_officer['user_record'].id)
    assert user.status == 'active'


def test_reject_pending_officer(client, admin_auth_headers, registered_officer):
    """Test rejecting a pending officer."""
    response = client.patch(f'/api/admin/users/{registered_officer['user_record'].id}/reject',
                           headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'rejected' in data['message']
    
    # Verify user status changed
    user = User.query.get(registered_officer['user_record'].id)
    assert user.status == 'rejected'

def test_approve_nonexistent_user(client, admin_auth_headers):
    """Test approving a non-existent user."""
    response = client.patch('/api/admin/users/99999/approve',
                           headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 404
    assert 'User not found' in data['message']

def test_list_departments_success(client, admin_auth_headers):
    """Test listing all departments."""
    response = client.get('/api/admin/departments', headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'departments' in data
    assert 'top_stats' in data
    assert 'quick_insights' in data
    assert len(data['departments']) >= 1


def test_create_department_success(client, admin_auth_headers):
    """Test creating a new department."""
    dept_data = {
        "name": "Sanitation Department 1",
        "code": "SAN1",
        "description": "Handles garbage and waste management",
        "status": "Active"
    }
    
    response = client.post('/api/admin/departments',
                          json=dept_data,
                          headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 201
    assert data['success'] is True
    assert 'Department created' in data['message']
    assert data['department']['name'] == dept_data['name']
    

    dept = Department.query.filter_by(department_name=dept_data['name']).first()
    assert dept is not None
    assert dept.code == dept_data['code']