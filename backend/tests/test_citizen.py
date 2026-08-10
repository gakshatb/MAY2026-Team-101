import pytest
import json
from io import BytesIO
from models import User, Complaint, StatusLog, ComplaintImages, Feedback, Notification, ActivityLog






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


def test_submit_complaint_with_image(client, citizen_auth_headers, sample_complaint_data):
    """Test complaint submission with an image attachment."""
    # Create a test image
    image_data = BytesIO(b'fake image data')
    image_data.seek(0)
    
    data = sample_complaint_data.copy()
    response = client.post('/api/citizen/complaints',
                          data={
                              **data,
                              'image': (image_data, 'test_image.jpg')
                          },
                          headers=citizen_auth_headers,
                          content_type='multipart/form-data')
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] is True
    
    # Verify image was saved
    complaint_id = data['complaint']['raw_id']
    complaint = Complaint.query.get(complaint_id)
    assert complaint.images is not None
    assert len(complaint.images) > 0


def test_submit_complaint_invalid_category(client, citizen_auth_headers, sample_complaint_data):
    """Test complaint submission with invalid category."""
    data = sample_complaint_data.copy()
    data['category'] = 'Invalid Category'
    
    response = client.post('/api/citizen/complaints',
                          data=data,
                          headers=citizen_auth_headers,
                          content_type='multipart/form-data')
    data = response.get_json()
    
    assert response.status_code == 400
    assert 'Invalid category' in data['message']