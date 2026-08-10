import pytest
import json

def test_submit_complaint_success(client, citizen_auth_headers, sample_complaint_data):
    """Test successful complaint submission."""
    response = client.post('/api/citizen/complaints', 
                          data=sample_complaint_data,
                          headers=citizen_auth_headers,
                          content_type='multipart/form-data')
    data = response.get_json()
    
    assert response.status_code == 201
    assert data['success'] is True
    assert 'Complaint submitted successfully' in data['message']
    assert 'complaint' in data
    assert data['complaint']['title'] == sample_complaint_data['title']
    assert data['complaint']['category'] == sample_complaint_data['category']
    assert data['complaint']['status'] == 'Pending'
    assert data['complaint']['department'] == 'Roads & Infrastructure'


