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

def test_list_departments_success(client, admin_auth_headers , test_department):
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

def test_create_duplicate_department(client, admin_auth_headers, test_department):
    """Test creating a department with duplicate name."""
    dept_data = {
        "name": test_department.department_name,
        "code": "DUP",
        "description": "Duplicate department",
        "status": "Active"
    }
    
    response = client.post('/api/admin/departments',
                          json=dept_data,
                          headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 409
    assert 'already exists' in data['message']

def test_update_department_success(client, admin_auth_headers, test_department):
    """Test updating a department."""
    update_data = {
        "name": "Updated Department",
        "code": "UPD",
        "description": "Updated description",
        "status": "Inactive"
    }
    
    response = client.put(f'/api/admin/departments/{test_department.id}',
                         json=update_data,
                         headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'Department updated' in data['message']
    
    # Verify in database
    dept = Department.query.get(test_department.id)
    assert dept.department_name == update_data['name']
    assert dept.status == update_data['status']

def test_delete_department_success(client, admin_auth_headers, test_department):
    """Test deleting a department (no complaints/members)."""
    # Ensure department has no members or complaints
    response = client.delete(f'/api/admin/departments/{test_department.id}',
                            headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'Department deleted' in data['message']
    
    # Verify deleted
    dept = Department.query.get(test_department.id)
    assert dept is None

def test_assign_department_head(client, admin_auth_headers, test_department, registered_officer):
    """Test assigning a department head."""
    # First approve the officer
    client.patch(f'/api/admin/users/{registered_officer['user_record'].id}/approve',
                headers=admin_auth_headers)
    
    # Assign as head
    response = client.patch(f'/api/admin/departments/{test_department.id}/assign-head',
                           json={"officerId": registered_officer['user_record'].id},
                           headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'Department head assigned' in data['message']
    
    # Verify
    dept = Department.query.get(test_department.id)
    assert dept.user_id == registered_officer['user_record'].id



def test_list_officers_success(client, admin_auth_headers):
    """Test listing all officers."""
    response = client.get('/api/admin/officers', headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'officers' in data
    assert 'top_stats' in data
    assert 'quick_insights' in data
    assert 'pending_registrations' in data


def test_suspend_officer(client, admin_auth_headers, registered_officer):
    """Test suspending an officer."""
    
    client.patch(f'/api/admin/users/{registered_officer['user_record'].id}/approve',
                headers=admin_auth_headers)
    
    
    response = client.patch(f'/api/admin/officers/{registered_officer['user_record'].id}/suspend',
                           json={"reason": "Performance issues"},
                           headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'suspended' in data['message']
    
    
    officer = User.query.get(registered_officer['user_record'].id)
    assert officer.status == 'suspended'

def test_reactivate_officer(client, admin_auth_headers, pending_officer):
    """Test reactivating a suspended officer."""
    
    client.patch(f'/api/admin/users/{pending_officer.id}/approve',
                headers=admin_auth_headers)
    client.patch(f'/api/admin/officers/{pending_officer.id}/suspend',
                json={"reason": "Test"},
                headers=admin_auth_headers)
   
    response = client.patch(f'/api/admin/officers/{pending_officer.id}/reactivate',
                           headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'reactivated' in data['message']
    

    officer = User.query.get(pending_officer.id)
    assert officer.status == 'active'

def test_transfer_officer(client, admin_auth_headers, pending_officer, test_department):
    """Test transferring an officer to another department."""
    # Approve the officer
    client.patch(f'/api/admin/users/{pending_officer.id}/approve',
                headers=admin_auth_headers)
    
    # Transfer
    response = client.patch(f'/api/admin/officers/{pending_officer.id}/transfer',
                           json={"departmentId": test_department.id},
                           headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'transferred' in data['message']
    
    # Verify
    officer = User.query.get(pending_officer.id)
    assert officer.department_id == test_department.id

def test_officer_details(client, admin_auth_headers, pending_officer):
    """Test getting officer details."""
    
    client.patch(f'/api/admin/users/{pending_officer.id}/approve',
                headers=admin_auth_headers)
    
    response = client.get(f'/api/admin/officers/{pending_officer.id}',
                         headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert 'officer' in data
    assert 'top_stats' in data
    assert 'department' in data
    assert 'complaint_status_breakdown' in data
    assert 'monthly_trend' in data
    
    
    officer_data = data['officer']
    assert officer_data['id'] == pending_officer.id
    assert officer_data['name'] == pending_officer.name
    assert officer_data['email'] == pending_officer.email


def test_list_admin_complaints(client, admin_auth_headers, test_complaint):
    """Test listing all complaints from admin perspective."""
    response = client.get('/api/admin/complaints', headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'complaints' in data
    assert 'summary' in data
    assert 'departments' in data
    assert len(data['complaints']) >= 1

def test_get_admin_complaint_details(client, admin_auth_headers, test_complaint):
    """Test getting complaint details."""
    response = client.get(f'/api/admin/complaints/{test_complaint.id}',
                         headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'complaint' in data
    assert data['complaint']['raw_id'] == test_complaint.id
    assert 'description' in data['complaint']
    assert 'status_logs' in data['complaint']
    assert 'eligible_officers' in data['complaint']

def test_assign_complaint_to_officer(client, admin_auth_headers, test_complaint, pending_officer):
    """Test assigning a complaint to an officer."""
    # Approve the officer
    client.patch(f'/api/admin/users/{pending_officer.id}/approve',
                headers=admin_auth_headers)
    
    response = client.patch(f'/api/admin/complaints/{test_complaint.id}/assign',
                           json={"officer_id": pending_officer.id},
                           headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'Complaint assigned' in data['message']
    
    # Verify
    complaint = Complaint.query.get(test_complaint.id)
    assert complaint.assigned_officer == pending_officer.id

def test_close_complaint_by_admin(client, admin_auth_headers, test_complaint):
    """Test closing a complaint directly by admin."""
    response = client.patch(f'/api/admin/complaints/{test_complaint.id}/close',
                           json={"remark": "Duplicate complaint"},
                           headers=admin_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'Complaint closed' in data['message']
    
    # Verify
    complaint = Complaint.query.get(test_complaint.id)
    assert complaint.status == 'Closed'
    
    # Check status log
    status_log = StatusLog.query.filter_by(complaint_id=test_complaint.id).first()
    assert status_log is not None
    assert 'Duplicate complaint' in status_log.remark
