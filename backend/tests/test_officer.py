import pytest
from io import BytesIO
from datetime import datetime, timedelta
from models import (
    db, User, Complaint, Assignment, Department, StatusLog,
    Notification, Feedback, ActivityLog, now_ist
)


def test_officer_dashboard_success(client, officer_auth_headers, assigned_complaint):
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
    