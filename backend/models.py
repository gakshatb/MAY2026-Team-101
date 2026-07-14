from datetime import datetime
from flask_sqlalchemy import SQLAlchemy # type: ignore
from werkzeug.security import generate_password_hash # type: ignore

db = SQLAlchemy()

# ─────────────────────────────────────────────────────────────────────────────
# User
# Stores all three roles in one table: citizen | officer | worker
# Role-based access is enforced at the API layer using Flask-JWT-Extended.
# ─────────────────────────────────────────────────────────────────────────────
class User(db.Model):
    __tablename__ = 'users'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name       = db.Column(db.String(255), nullable=False)
    email      = db.Column(db.String(255), unique=True, nullable=False)
    password   = db.Column(db.String(255), nullable=False)          # bcrypt hash
    phone      = db.Column(db.String(20),  nullable=True)
    role       = db.Column(db.String(20),  nullable=False)          # citizen | officer | worker
    status     = db.Column(db.String(20),  nullable=False, default='active')
    created_at = db.Column(db.DateTime,    nullable=False, default=datetime.now)

    # ── relationships ────────────────────────────────────────────────────────

    # Department this user heads (only relevant when role = officer)
    department = db.relationship(
        'Department',
        backref='head_officer',
        uselist=False,          # one officer heads at most one department (0..1)
        lazy=True
    )

    # Complaints this user submitted (only relevant when role = citizen)
    submitted_complaints = db.relationship(
        'Complaint',
        foreign_keys='Complaint.created_by',
        backref='citizen',
        lazy=True
    )

    # Complaints this user is assigned to manage (only relevant when role = officer)
    managed_complaints = db.relationship(
        'Complaint',
        foreign_keys='Complaint.assigned_officer',
        backref='officer',
        lazy=True
    )

    # Assignments where this user is the worker
    worker_assignments = db.relationship(
        'Assignment',
        foreign_keys='Assignment.worker_id',
        backref='worker',
        lazy=True
    )

    # Assignments created by this user (officer who assigned)
    created_assignments = db.relationship(
        'Assignment',
        foreign_keys='Assignment.assigned_by',
        backref='assigner',
        lazy=True
    )

    def __repr__(self):
        return f'<User id={self.id} email={self.email} role={self.role}>'



# ─────────────────────────────────────────────────────────────────────────────
# Department
# Each department is headed by one officer (User with role='officer').
# Department_Name stores the type: Roads, Drainage, Sanitation, etc.
# ─────────────────────────────────────────────────────────────────────────────
class Department(db.Model):
    __tablename__ = 'departments'

    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)   # officer who heads it
    department_name = db.Column(db.String(100), nullable=False)
    created_at      = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Department id={self.id} name={self.department_name}>'


# ─────────────────────────────────────────────────────────────────────────────
# Complaint
# Core entity. Created by a citizen, routed to a department (stored as varchar),
# and optionally assigned to an officer.
# ─────────────────────────────────────────────────────────────────────────────
class Complaint(db.Model):
    __tablename__ = 'complaints'

    id               = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    title            = db.Column(db.String(255),  nullable=False)
    description      = db.Column(db.Text,         nullable=False)
    department       = db.Column(db.String(100),  nullable=False)
    location         = db.Column(db.String(255),  nullable=False)
    created_by       = db.Column(db.Integer,      db.ForeignKey('users.id'),  nullable=False)
    assigned_officer = db.Column(db.Integer,      db.ForeignKey('users.id'),  nullable=True)
    status           = db.Column(db.String(50),   nullable=False, default='Pending')
    is_escalated     = db.Column(db.Boolean,      nullable=False, default=False)
    updated_at       = db.Column(db.DateTime,     nullable=True,  onupdate=datetime.utcnow)
    created_at       = db.Column(db.DateTime,     nullable=False, default=datetime.utcnow)

    # ── relationships of complaint ────────────────────────────────────────────────────────
    status_logs      = db.relationship('StatusLog',       backref='complaint', lazy=True, cascade='all, delete-orphan')
    images           = db.relationship('ComplaintImages',  backref='complaint', lazy=True, cascade='all, delete-orphan')
    feedback         = db.relationship('Feedback',         backref='complaint', lazy=True, uselist=False)   # 1-to-1
    notifications    = db.relationship('Notification',     backref='complaint', lazy=True, cascade='all, delete-orphan')
    assignments      = db.relationship('Assignment',       backref='complaint', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Complaint id={self.id} title={self.title!r} status={self.status}>'


# ─────────────────────────────────────────────────────────────────────────────
# StatusLog
# Every status transition is recorded here, creating a full audit trail.
# Used by ComplaintTracking.vue to render the timeline.
# ─────────────────────────────────────────────────────────────────────────────
class StatusLog(db.Model):
    __tablename__ = 'status_logs'

    id           = db.Column(db.Integer,    primary_key=True, autoincrement=True)
    complaint_id = db.Column(db.Integer,    db.ForeignKey('complaints.id'), nullable=False)
    old_status   = db.Column(db.String(50), nullable=True)    # NULL for the first log entry
    new_status   = db.Column(db.String(50), nullable=False)
    remark       = db.Column(db.String(500), nullable=True)
    changed_at   = db.Column(db.DateTime,   nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<StatusLog id={self.id} complaint_id={self.complaint_id} {self.old_status}→{self.new_status}>'


# ─────────────────────────────────────────────────────────────────────────────
# ComplaintImages
# Stores image paths/URLs attached to a complaint at submission time.
# Matches Attachment model in existing code — renamed to match ER exactly.
# ─────────────────────────────────────────────────────────────────────────────
class ComplaintImages(db.Model):
    __tablename__ = 'complaint_images'

    id           = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    complaint_id = db.Column(db.Integer,     db.ForeignKey('complaints.id'), nullable=False)
    image_url    = db.Column(db.String(500), nullable=False)
    uploaded_at  = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<ComplaintImages id={self.id} complaint_id={self.complaint_id}>'


# ─────────────────────────────────────────────────────────────────────────────
# Feedback
# One-to-one with Complaint. Only available after status = 'Resolved'.
# uselist=False on Complaint.feedback enforces the 1:1 relationship.
# ─────────────────────────────────────────────────────────────────────────────
class Feedback(db.Model):
    __tablename__ = 'feedback'

    id           = db.Column(db.Integer,      primary_key=True, autoincrement=True)
    complaint_id = db.Column(db.Integer,      db.ForeignKey('complaints.id'), nullable=False, unique=True)  # unique = 1:1
    rating       = db.Column(db.Integer,      nullable=False)    # 1 to 5
    comments     = db.Column(db.String(1000), nullable=True)
    submitted_at = db.Column(db.DateTime,     nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Feedback id={self.id} complaint_id={self.complaint_id} rating={self.rating}>'


# ─────────────────────────────────────────────────────────────────────────────
# Notification
# Triggered on every status change. Linked to a complaint.
# citizen/officer/worker all receive notifications via their user_id
# NOTE: user_id not in ER but needed to deliver — added as nullable FK.
# ─────────────────────────────────────────────────────────────────────────────
class Notification(db.Model):
    __tablename__ = 'notifications'

    id           = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    complaint_id = db.Column(db.Integer,     db.ForeignKey('complaints.id'), nullable=True)
    message      = db.Column(db.String(500), nullable=False)
    created_at   = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Notification id={self.id} complaint_id={self.complaint_id}>'


# ─────────────────────────────────────────────────────────────────────────────
# Assignment
# Created by an officer (assigned_by) to assign a worker (worker_id)
# to a specific complaint. Multiple assignments per complaint are allowed
# (e.g. reassignment history), but only the latest is the active one.
# ─────────────────────────────────────────────────────────────────────────────
class Assignment(db.Model):
    __tablename__ = 'assignments'

    id           = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    complaint_id = db.Column(db.Integer,  db.ForeignKey('complaints.id'), nullable=False)
    worker_id    = db.Column(db.Integer,  db.ForeignKey('users.id'),      nullable=False)
    assigned_by  = db.Column(db.Integer,  db.ForeignKey('users.id'),      nullable=False)
    assigned_at  = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Assignment id={self.id} complaint_id={self.complaint_id} worker_id={self.worker_id}>'

def init_db(app):
    db.init_app(app)    
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(role='Admin').first():
            admin = User(
                name="Administrator",
                email="admin@gmail.com",
                phone="9999999999",
                role="Admin",
                password=generate_password_hash("Admin@123")
            )
            db.session.add(admin)
            db.session.commit()