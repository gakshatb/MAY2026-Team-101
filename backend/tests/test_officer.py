import pytest
from io import BytesIO
from datetime import datetime, timedelta
from models import (
    db, User, Complaint, Assignment, Department, StatusLog,
    Notification, Feedback, ActivityLog, now_ist
)


def test_officer_dashboard_success(client, officer_auth_headers, assigned_complaint_officer):
    """Test officer dashboard returns correct data."""
    response = client.get('/api/officer/dashboard', headers=officer_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'officer' in data
    assert 'kpi' in data
    assert 'statusBreakdown' in data
    assert 'weeklyTrend' in data
    assert 'emergencyComplaints' in data
    assert 'recentComplaints' in data
    assert 'workerAvailability' in data
    assert 'topWorkers' in data

    kpi = data['kpi']
    assert kpi['total'] >= 1
    assert kpi['assigned'] >= 1
    assert 'inProgress' in kpi
    assert 'resolved' in kpi
    assert 'emergency' in kpi


def test_list_officer_complaints_success(client, officer_auth_headers, assigned_complaint_officer):
    """Test listing complaints assigned to officer."""
    response = client.get('/api/officer/complaints', headers=officer_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'complaints' in data
    assert 'summary_stats' in data
    assert len(data['complaints']) >= 1
    assert data['complaints'][0]['title'] == 'Officer Assigned Complaint'

def test_list_complaints_filter_by_status(client, officer_auth_headers, assigned_complaint_officer):
    """Test filtering complaints by status."""
    response = client.get('/api/officer/complaints?status=Assigned', 
                         headers=officer_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    for complaint in data['complaints']:
        assert complaint['status'] == 'Assigned'

def test_get_complaint_details_success(client, officer_auth_headers, assigned_complaint_officer):
    """Test getting detailed complaint information."""
    response = client.get(f'/api/officer/complaints/{assigned_complaint_officer.id}', 
                         headers=officer_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'complaint' in data
    assert data['complaint']['rawId'] == assigned_complaint_officer.id
    assert data['complaint']['title'] == 'Officer Assigned Complaint'
    assert 'description' in data['complaint']
    assert 'images' in data['complaint']
    assert 'location' in data['complaint']
    assert 'history' in data['complaint']
    assert 'citizenDetails' in data['complaint']

def test_get_complaint_not_assigned(client, officer_auth_headers, registered_admin):
    """Test getting a complaint not assigned to the officer."""
    complaint = Complaint(
        title="Other Complaint",
        category="Garbage",
        description="This complaint is not assigned to this officer.",
        priority="Medium",
        department="Test Department",
        location="Other Location",
        ward="Ward 2",
        area="Other Area",
        street="Other Street",
        created_by=registered_admin['user_record'].id,
        status="Pending"
    )
    db.session.add(complaint)
    db.session.commit()
    
    response = client.get(f'/api/officer/complaints/{complaint.id}', 
                         headers=officer_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 403
    assert 'not assigned to you' in data['message']


def test_update_status_to_in_progress(client, officer_auth_headers, assigned_complaint_officer):
    """Test updating complaint status to 'In Progress'."""
    response = client.patch(f'/api/officer/complaints/{assigned_complaint_officer.id}/status',
                           json={
                               "status": "In Progress",
                               "remark": "Officer has reviewed and started work"
                           },
                           headers=officer_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'Status updated' in data['message']
    assert data['complaint']['status'] == 'In Progress'
    
    # Verify status log was created
    status_log = StatusLog.query.filter_by(complaint_id=assigned_complaint_officer.id).first()
    assert status_log is not None
    assert status_log.new_status == 'In Progress'

def test_invalid_status_transition(client, officer_auth_headers, assigned_complaint_officer):
    """Test invalid status transition (should fail)."""
    response = client.patch(f'/api/officer/complaints/{assigned_complaint_officer.id}/status',
                           json={
                               "status": "Resolved",  # Officers can't set Resolved directly
                               "remark": "Trying to resolve"
                           },
                           headers=officer_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 400
    assert 'Cannot change' in data['message']

def test_update_priority_success(client, officer_auth_headers, assigned_complaint_officer):
    """Test updating complaint priority."""
    response = client.patch(f'/api/officer/complaints/{assigned_complaint_officer.id}/priority',
                           json={"priority": "Emergency"},
                           headers=officer_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'Priority updated' in data['message']
    assert data['complaint']['priority'] == 'Emergency'
    
    # Verify in database
    complaint = Complaint.query.get(assigned_complaint_officer.id)
    assert complaint.priority == 'Emergency'

def test_return_complaint_to_admin(client, officer_auth_headers, assigned_complaint_officer):
    """Test returning a complaint to admin for re-review."""
    response = client.patch(f'/api/officer/complaints/{assigned_complaint_officer.id}/return-to-admin',
                           json={"remark": "This needs admin review for resource allocation"},
                           headers=officer_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'Complaint returned to admin' in data['message']
    
    # Verify
    complaint = Complaint.query.get(assigned_complaint_officer.id)
    assert complaint.status == 'Under Review'
    assert complaint.assigned_officer is None

def test_return_complaint_without_remark(client, officer_auth_headers, assigned_complaint_officer):
    """Test returning complaint without remark (should fail)."""
    response = client.patch(f'/api/officer/complaints/{assigned_complaint_officer.id}/return-to-admin',
                           json={},
                           headers=officer_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 400
    assert 'A remark explaining why this is being sent back is required.' in data['message']

def test_assign_worker_to_complaint(client, officer_auth_headers, assigned_complaint_officer, worker_user):
    """Test assigning a worker to a complaint."""
    response = client.patch(f'/api/officer/complaints/{assigned_complaint_officer.id}/assign-worker',
                           json={
                               "worker_id": worker_user.id,
                               "notes": "Please resolve this within 3 days",
                               "priority": "Emergency"
                           },
                           headers=officer_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'Assigned to' in data['message']
    assert data['complaint']['status'] == 'In Progress'
    
    # Verify assignment
    assignment = Assignment.query.filter_by(complaint_id=assigned_complaint_officer.id).first()
    assert assignment is not None
    assert assignment.worker_id == worker_user.id

def test_list_workers_success(client, officer_auth_headers, worker_user):
    """Test listing workers."""
    response = client.get('/api/officer/workers', headers=officer_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'workers' in data
    assert 'statistics' in data
    assert 'topPerformers' in data
    assert 'completionSummary' in data
    assert len(data['workers']) >= 1

def test_get_worker_details(client, officer_auth_headers, worker_user):
    """Test getting worker details."""
    response = client.get(f'/api/officer/workers/{worker_user.id}', 
                         headers=officer_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'worker' in data
    assert data['worker']['name'] == worker_user.name
    assert 'currentAssignments' in data['worker']
    assert 'timeline' in data['worker']
    assert 'totalCompleted' in data['worker']

def test_get_officer_profile(client, officer_auth_headers):
    """Test getting officer profile."""
    response = client.get('/api/officer/profile', headers=officer_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'profile' in data
    assert data['profile']['fullName'] == 'Officer'
    assert data['profile']['email'] == 'officer@gmail.com'
    assert data['profile']['empId'] in ['OFC-0001','OFC-0002']
    assert 'department' in data['profile']
    assert 'resolvedCount' in data['profile']
    assert 'avgRating' in data['profile']

def test_officer_endpoint_requires_auth(client):
    """Test that officer endpoints require authentication."""
    endpoints = [
        '/api/officer/dashboard',
        '/api/officer/complaints',
        '/api/officer/profile',
        '/api/officer/notifications',
        '/api/officer/workers'
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 401

def test_officer_endpoint_requires_officer_role(client, citizen_auth_headers):
    """Test that officer endpoints require officer role."""
    endpoints = [
        '/api/officer/dashboard',
        '/api/officer/complaints',
        '/api/officer/profile',
        '/api/officer/notifications',
        '/api/officer/workers'
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint, headers=citizen_auth_headers)
        assert response.status_code in [403, 401]