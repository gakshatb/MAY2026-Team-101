from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

from models import Assignment, Complaint, Department, StatusLog, User, db


def _auth_header(user_id):
    return {'Authorization': f'Bearer {create_access_token(identity=str(user_id))}'}


def test_worker_can_view_and_resolve_only_own_task(client):
    department = Department(department_name='Roads', code='ROADS')
    citizen = User(name='Citizen', email='citizen@test.com', password='x', role='Citizen', status='active')
    officer = User(name='Officer', email='officer@test.com', password='x', role='Officer', status='active')
    worker = User(name='Worker', email='worker@test.com', password='x', role='Worker', status='active')
    other_worker = User(name='Other', email='other@test.com', password='x', role='Worker', status='active')
    db.session.add_all([department, citizen, officer, worker, other_worker])
    db.session.flush()
    officer.department_id = department.id
    worker.department_id = department.id
    other_worker.department_id = department.id
    complaint = Complaint(title='Large pothole', category='Potholes', description='A dangerous pothole needs urgent repair today.', priority='High', department='Roads', location='Main Road', created_by=citizen.id, assigned_officer=officer.id, status='In Progress')
    db.session.add(complaint)
    db.session.flush()
    db.session.add(Assignment(complaint_id=complaint.id, worker_id=worker.id, assigned_by=officer.id))
    db.session.commit()

    tasks_response = client.get('/api/worker/tasks', headers=_auth_header(worker.id))
    assert tasks_response.status_code == 200
    assert tasks_response.get_json()['tasks'][0]['raw_id'] == complaint.id

    denied_response = client.get(f'/api/worker/tasks/{complaint.id}', headers=_auth_header(other_worker.id))
    assert denied_response.status_code == 403

    response = client.patch(f'/api/worker/tasks/{complaint.id}/status', headers=_auth_header(worker.id), json={'status': 'Resolved', 'remark': 'Filled and compacted the pothole.'})
    assert response.status_code == 200
    assert Complaint.query.get(complaint.id).status == 'Resolved'
    assert StatusLog.query.filter_by(complaint_id=complaint.id, new_status='Resolved').count() == 1


def test_inactive_user_cannot_use_an_existing_token(client):
    user = User(name='Inactive', email='inactive@test.com', password=generate_password_hash('password'), role='Citizen', status='suspended')
    db.session.add(user)
    db.session.commit()
    response = client.get('/api/citizen/dashboard', headers=_auth_header(user.id))
    assert response.status_code == 403
