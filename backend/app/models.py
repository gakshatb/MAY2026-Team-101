from datetime import datetime
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    complaints = db.relationship('Complaint', backref='citizen', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    
    worker_assignments = db.relationship(
        'Assignment', 
        foreign_keys='Assignment.worker_id', 
        backref='worker', 
        lazy=True
    )
    creator_assignments = db.relationship(
        'Assignment', 
        foreign_keys='Assignment.assigned_by', 
        backref='assigner', 
        lazy=True
    )


class Complaint(db.Model):
    __tablename__ = 'complaints'

    id = db.Column(db.Integer, primary_key=True)
    citizen_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='Pending', nullable=False)
    priority = db.Column(db.String(50), default='Medium', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    assignments = db.relationship('Assignment', backref='complaint', lazy=True)
    attachments = db.relationship('Attachment', backref='complaint', lazy=True)


class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), default='Assigned', nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Attachment(db.Model):
    __tablename__ = 'attachments'

    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)



