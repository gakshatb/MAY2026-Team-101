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


def test_submit_complaint_short_description(client, citizen_auth_headers, sample_complaint_data):
    """Test complaint submission with description less than 30 characters."""
    data = sample_complaint_data.copy()
    data['description'] = 'Too short'
    
    response = client.post('/api/citizen/complaints',
                          data=data,
                          headers=citizen_auth_headers,
                          content_type='multipart/form-data')
    data = response.get_json()
    
    assert response.status_code == 400
    assert 'at least 30 characters' in data['message']

def test_submit_complaint_missing_area(client, citizen_auth_headers, sample_complaint_data):
    """Test complaint submission with missing address."""
    data = sample_complaint_data.copy()
    data['area'] = ''
    
    response = client.post('/api/citizen/complaints',
                          data=data,
                          headers=citizen_auth_headers,
                          content_type='multipart/form-data')
    data = response.get_json()
    
    assert response.status_code == 400
    assert 'Area/Locality is required' in data['message']

def test_list_complaints_success(client, citizen_auth_headers, sample_complaint_data):
    """Test listing all complaints for a citizen."""
    # Create a complaint first
    client.post('/api/citizen/complaints',
               data=sample_complaint_data,
               headers=citizen_auth_headers,
               content_type='multipart/form-data')
    
    response = client.get('/api/citizen/complaints',
                         headers=citizen_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert 'complaints' in data
    assert len(data['complaints']) >= 1
    assert data['complaints'][0]['title'] == sample_complaint_data['title']

def test_list_complaints_filter_by_status(client, citizen_auth_headers, sample_complaint_data):
    """Test listing complaints filtered by status."""
    # Create a complaint
    client.post('/api/citizen/complaints',
               data=sample_complaint_data,
               headers=citizen_auth_headers,
               content_type='multipart/form-data')
    
    # Filter by Pending status
    response = client.get('/api/citizen/complaints?status=Pending',
                         headers=citizen_auth_headers)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    for complaint in data['complaints']:
        assert complaint['status'] == 'Pending'