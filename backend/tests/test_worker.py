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

def test_update_task_to_in_progress(client, worker_auth_headers, assigned_complaint):
    """Test updating task status to 'In Progress'."""
    response = client.patch(f'/api/worker/tasks/{assigned_complaint.id}/status',
                           json={
                               "status": "In Progress",
                               "remark": "Started working on the task"
                           },
                           headers=worker_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'Task updated' in data['message']
    assert data['task']['status'] == 'In Progress'

def test_update_task_to_resolved(client, worker_auth_headers, assigned_complaint):
    """Test updating task status to 'Resolved'."""
    
    client.patch(f'/api/worker/tasks/{assigned_complaint.id}/status',
                json={"status": "In Progress", "remark": "Started working"},
                headers=worker_auth_headers)
    
    
    response = client.patch(f'/api/worker/tasks/{assigned_complaint.id}/status',
                           json={
                               "status": "Resolved",
                               "remark": "Task completed successfully"
                           },
                           headers=worker_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'Task updated' in data['message']
    assert data['task']['status'] == 'Resolved'

def test_resolve_task_without_remark(client, worker_auth_headers, assigned_complaint):
    """Test resolving task without providing a remark ."""
    
    client.patch(f'/api/worker/tasks/{assigned_complaint.id}/status',
                json={"status": "In Progress", "remark": "Started working"},
                headers=worker_auth_headers)
    
    response = client.patch(f'/api/worker/tasks/{assigned_complaint.id}/status',
                           json={"status": "Resolved"},
                           headers=worker_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 400
    assert 'resolution note is required' in data['message']

def test_update_completed_task(client, worker_auth_headers, assigned_complaint):
    """Test updating a task that is already completed ."""
    
    client.patch(f'/api/worker/tasks/{assigned_complaint.id}/status',
                json={"status": "In Progress", "remark": "Started"},
                headers=worker_auth_headers)
    client.patch(f'/api/worker/tasks/{assigned_complaint.id}/status',
                json={"status": "Resolved", "remark": "Completed"},
                headers=worker_auth_headers)
    
    
    response = client.patch(f'/api/worker/tasks/{assigned_complaint.id}/status',
                           json={"status": "In Progress", "remark": "Try again"},
                           headers=worker_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 400
    assert 'completed task cannot be updated' in data['message']


def test_upload_task_photo_success(client, worker_auth_headers, assigned_complaint):
    """Test uploading a photo to a task."""
    image_data = BytesIO(b'fake image data')
    image_data.seek(0)
    
    response = client.post(f'/api/worker/tasks/{assigned_complaint.id}/photos',
                          data={'image': (image_data, 'task_photo.jpg')},
                          headers=worker_auth_headers,
                          content_type='multipart/form-data')
    data = response.get_json()
    
    assert response.status_code == 201
    assert data['success'] is True
    assert 'image_url' in data


def test_get_worker_profile(client, worker_auth_headers):
    """Test getting worker profile."""
    response = client.get('/api/worker/profile', headers=worker_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'profile' in data
    assert data['profile']['name'] == 'Worker Test'
    assert data['profile']['email'] == 'worker@example.com'
    assert data['profile']['empId'] in ['FW-0001', 'FW-0002']
    assert 'department' in data['profile']
    assert 'completedCount' in data['profile']
    assert 'avgRating' in data['profile']

def test_update_worker_profile(client, worker_auth_headers):
    """Test updating worker profile."""
    update_data = {
        "name": "Updated Worker",
        "phone": "9876543219",
        "address": "New Worker Address",
        "city": "New Mumbai",
        "state": "Maharashtra",
        "pincode": "400099",
        "gender": "Female",
        "nationality": "Indian"
    }
    
    response = client.put('/api/worker/profile',
                         json=update_data,
                         headers=worker_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert data['profile']['name'] == 'Updated Worker'

def test_list_worker_notifications(client, worker_auth_headers, assigned_complaint):
    """Test listing worker notifications."""
    response = client.get('/api/worker/notifications', headers=worker_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'notifications' in data

def test_mark_notification_read(client, worker_auth_headers, worker_user):
    """Test marking a notification as read."""
    # Create a notification
    notification = Notification(
        user_id=worker_user.id,
        title="Test Notification",
        message="Test message",
        type="info",
        is_read=False
    )
    db.session.add(notification)
    db.session.commit()
    
    response = client.patch(f'/api/worker/notifications/{notification.id}/read',
                           headers=worker_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    
    # Verify notification is read
    note = Notification.query.get(notification.id)
    assert note.is_read is True

def test_apply_to_department_success(client, worker_auth_headers, test_department):
    """Test applying to a department."""
    application_data = {
        "departmentId": test_department.id,
        "message": "I would like to join this department"
    }
    
    response = client.post('/api/worker/department-applications',
                          json=application_data,
                          headers=worker_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 201
    assert data['success'] is True
    assert 'application' in data
    assert data['application']['departmentId'] == test_department.id
    assert data['application']['status'] == 'Pending'

def test_apply_to_current_department(client, worker_auth_headers, test_department, worker_user):
    """Test applying to the department worker is already in."""
    # Set worker's department
    worker_user.department_id = test_department.id
    db.session.commit()
    
    application_data = {
        "departmentId": test_department.id,
        "message": "I want to stay in this department"
    }
    
    response = client.post('/api/worker/department-applications',
                          json=application_data,
                          headers=worker_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 400
    assert 'already in this department' in data['message']

def test_worker_endpoint_requires_auth(client):
    """Test that worker endpoints require authentication."""
    endpoints = [
        '/api/worker/dashboard',
        '/api/worker/tasks',
        '/api/worker/profile',
        '/api/worker/notifications',
        '/api/worker/departments'
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 401

def test_worker_endpoint_requires_worker_role(client, admin_auth_headers):
    """Test that worker endpoints require worker role."""
    endpoints = [
        '/api/worker/dashboard',
        '/api/worker/tasks',
        '/api/worker/profile',
        '/api/worker/notifications',
        '/api/worker/departments'
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint, headers=admin_auth_headers)
        assert response.status_code in [403, 401]