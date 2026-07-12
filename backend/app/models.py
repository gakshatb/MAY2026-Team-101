# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy



# db = SQLAlchemy()

# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)
#     mobile = db.Column(db.Integer , nullable  = False)
#     role = db.Column(db.String(50), nullable=False)

#     complaints = db.relationship('Complaint', backref='citizen', lazy=True)
#     notifications = db.relationship('Notification', backref='user', lazy=True)
    
#     worker_assignments = db.relationship(
#         'Assignment', 
#         foreign_keys='Assignment.worker_id', 
#         backref='worker', 
#         lazy=True
#     )
#     creator_assignments = db.relationship(
#         'Assignment', 
#         foreign_keys='Assignment.assigned_by', 
#         backref='assigner', 
#         lazy=True
#     )

# class Citizens(db.Model):
#     __tablename__ = 'citizens'
#     id = db.Column(db.Integer , primary_key = True)
#     user_id = db.Column(db.Integer , db.ForeignKey('users.id') , nullable= False)
#     name = db.Column(db.String(30) , nullable = False)
#     contact = db.Column(db.Integer , nullable = False)
#     pincode = db.Column(db.Integer , nullable = False)
#     add = db.Column(db.String(100) , nullable = False)
#     city = db.Column(db.String(30) , nullable = False)

# class Worker(db.Model):
#     __tablename__ = 'workers'
#     id = db.Column(db.Integer , primary_key = True)
#     user_id = db.Column(db.Integer , db.ForeignKey('users.id') , nullable= False)
#     name = db.Column(db.String(30) , nullable = False)
#     contact = db.Column(db.Integer , nullable = False)
#     Expertise = db.Column(db.String(30) , nullable = False)


# class Complaint(db.Model):
#     __tablename__ = 'complaints'

#     id = db.Column(db.Integer, primary_key=True)
#     citizen_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     title = db.Column(db.String(255), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     location = db.Column(db.String(255), nullable=False)
#     status = db.Column(db.String(50), default='Pending', nullable=False)
#     priority = db.Column(db.String(50), default='Medium', nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

#     assignments = db.relationship('Assignment', backref='complaint', lazy=True)
#     attachments = db.relationship('Attachment', backref='complaint', lazy=True)


# class Assignment(db.Model):
#     __tablename__ = 'assignments'

#     id = db.Column(db.Integer, primary_key=True)
#     complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), nullable=False)
#     worker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     status = db.Column(db.String(50), default='Assigned', nullable=False)
#     assigned_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


# class Attachment(db.Model):
#     __tablename__ = 'attachments'

#     id = db.Column(db.Integer, primary_key=True)
#     complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), nullable=False)
#     image_path = db.Column(db.String(255), nullable=False)


# class Notification(db.Model):
#     __tablename__ = 'notifications'

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     message = db.Column(db.Text, nullable=False)
#     is_read = db.Column(db.Boolean, default=False, nullable=False)





from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ===========================
# USER
# ===========================

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    mobile = db.Column(db.String(15), nullable=False)

    role = db.Column(
        db.String(20),
        nullable=False
    )  # citizen, administrator, officer, worker

    address = db.Column(db.Text)

    city = db.Column(db.String(100))

    pincode = db.Column(db.String(10))

    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ===========================
# DEPARTMENT
# ===========================

class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    description = db.Column(db.Text)

    officer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ===========================
# COMPLAINT
# ===========================

class Complaint(db.Model):
    __tablename__ = "complaints"

    id = db.Column(db.Integer, primary_key=True)

    citizen_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    title = db.Column(db.String(255), nullable=False)

    description = db.Column(db.Text, nullable=False)

    location = db.Column(db.String(255), nullable=False)

    latitude = db.Column(db.Float)

    longitude = db.Column(db.Float)

    priority = db.Column(
        db.String(20),
        default="Medium"
    )

    status = db.Column(
        db.String(30),
        default="Submitted"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


# ===========================
# COMPLAINT ATTACHMENTS
# ===========================

class ComplaintAttachment(db.Model):

    __tablename__ = "complaint_attachments"

    id = db.Column(db.Integer, primary_key=True)

    complaint_id = db.Column(
        db.Integer,
        db.ForeignKey("complaints.id"),
        nullable=False
    )

    image_path = db.Column(db.String(255))

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ===========================
# ASSIGNMENT
# ===========================

class Assignment(db.Model):

    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)

    complaint_id = db.Column(
        db.Integer,
        db.ForeignKey("complaints.id"),
        nullable=False
    )

    worker_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    assigned_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Assigned"
    )

    remarks = db.Column(db.Text)

    assigned_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    completed_at = db.Column(db.DateTime)


# ===========================
# FEEDBACK
# ===========================

class Feedback(db.Model):

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)

    complaint_id = db.Column(
        db.Integer,
        db.ForeignKey("complaints.id"),
        nullable=False
    )

    citizen_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    rating = db.Column(db.Integer)

    comment = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ===========================
# NOTIFICATIONS
# ===========================

class Notification(db.Model):

    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(db.String(255))

    message = db.Column(db.Text)

    is_read = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ===========================
# WORKER APPLICATION
# ===========================

class WorkerApplication(db.Model):

    __tablename__ = "worker_applications"

    id = db.Column(db.Integer, primary_key=True)

    worker_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    applied_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ===========================
# OFFICER APPLICATION
# ===========================

class OfficerApplication(db.Model):

    __tablename__ = "officer_applications"

    id = db.Column(db.Integer, primary_key=True)

    officer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    applied_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )