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