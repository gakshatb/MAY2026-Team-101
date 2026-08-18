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