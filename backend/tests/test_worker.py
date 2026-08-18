import pytest
from io import BytesIO
from datetime import datetime
from models import (
    db, User, Complaint, Assignment, Department, StatusLog, 
    Notification, Feedback, ActivityLog, DepartmentApplication
)



def test_worker_dashboard_success(client, worker_auth_headers, assigned_complaint):
    """Test worker dashboard returns correct data."""
    response = client.get('/api/worker/dashboard', headers=worker_auth_headers)
    data = response.get_json()
    print(data)
    assert response.status_code == 200
    assert data['success'] is True
    assert 'dashboard' in data
    assert 'worker' in data['dashboard']
    assert 'counts' in data['dashboard']
    assert 'current_task' in data['dashboard']
    assert 'assigned_tasks' in data['dashboard']
    assert 'emergencies' in data['dashboard']

    assert data['dashboard']['worker']['name'] == 'Worker Test'
    assert data['dashboard']['worker']['department'] == 'Test Department'
    
  
    assert data['dashboard']['counts']['total'] >= 1
    assert data['dashboard']['counts']['active'] >= 1


def test_list_tasks_success(client, worker_auth_headers, assigned_complaint):
    """Test listing all tasks assigned to worker."""
    response = client.get('/api/worker/tasks', headers=worker_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'tasks' in data
    assert len(data['tasks']) >= 1
    assert data['tasks'][0]['title'] == 'Assigned Task'
    assert data['tasks'][0]['status'] == 'Assigned'


def test_list_tasks_filter_completed(client, worker_auth_headers, assigned_complaint):
    """Test filtering tasks by completed status."""
    response = client.get('/api/worker/tasks?status=completed', headers=worker_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert len(data['tasks']) == 0

def test_get_task_details_success(client, worker_auth_headers, assigned_complaint):
    """Test getting detailed task information."""
    response = client.get(f'/api/worker/tasks/{assigned_complaint.id}', 
                         headers=worker_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'task' in data
    assert data['task']['raw_id'] == assigned_complaint.id
    assert data['task']['title'] == 'Assigned Task'
    assert 'description' in data['task']
    assert 'images' in data['task']
    assert 'history' in data['task']

def test_get_task_not_assigned(client, worker_auth_headers, registered_admin):
    """Test getting a task not assigned to the worker."""
    complaint = Complaint(
        title="Other Complaint",
        category="Garbage",
        description="This complaint is not assigned to the worker.",
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
    
    response = client.get(f'/api/worker/tasks/{complaint.id}', 
                         headers=worker_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 403
    assert 'not assigned to you' in data['message']