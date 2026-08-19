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
