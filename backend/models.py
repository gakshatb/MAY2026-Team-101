from datetime import datetime, timezone, timedelta
from flask_sqlalchemy import SQLAlchemy # type: ignore
from werkzeug.security import generate_password_hash # type: ignore

db = SQLAlchemy()

IST = timezone(timedelta(hours=5, minutes=30))

def now_ist():
    """Current time in IST, returned as a naive datetime."""
    return datetime.now(IST).replace(tzinfo=None)

class User(db.Model):
    __tablename__ = 'users'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name       = db.Column(db.String(255), nullable=False)
    email      = db.Column(db.String(255), unique=True, nullable=False)
    phone      = db.Column(db.String(20),  nullable=True)
    password   = db.Column(db.String(255), nullable=False)
    address    = db.Column(db.String(255), nullable=True)
    city       = db.Column(db.String(100), nullable=True)
    state      = db.Column(db.String(100), nullable=True)
    pincode    = db.Column(db.String(20),  nullable=True)
    gender     = db.Column(db.String(20),  nullable=True)
    profile_photo = db.Column(db.String(500), nullable=True)
    dob               = db.Column(db.Date,        nullable=True)
    nationality       = db.Column(db.String(50),  nullable=True)
    emergency_contact = db.Column(db.String(100), nullable=True)
    recovery_email    = db.Column(db.String(255), nullable=True)
    role       = db.Column(db.String(20),  nullable=False)          # citizen | officer | worker
    status     = db.Column(db.String(20),  nullable=False, default='active')  # active | pending | suspended
    designation = db.Column(db.String(100), nullable=True)
    department_id = db.Column(db.Integer,  db.ForeignKey('departments.id'), nullable=True)  # Officer/Worker's assigned department
    created_at = db.Column(db.DateTime,    nullable=False, default=now_ist)

    member_department = db.relationship(
        'Department',
        foreign_keys=[department_id],
        backref='members',
        lazy=True
    )
    department = db.relationship(
        'Department',
        foreign_keys='Department.user_id',
        backref='head_officer',
        uselist=False,
        lazy=True
    )
    submitted_complaints = db.relationship(
        'Complaint',
        foreign_keys='Complaint.created_by',
        backref='citizen',
        lazy=True
    )
    managed_complaints = db.relationship(
        'Complaint',
        foreign_keys='Complaint.assigned_officer',
        backref='officer',
        lazy=True
    )
    worker_assignments = db.relationship(
        'Assignment',
        foreign_keys='Assignment.worker_id',
        backref='worker',
        lazy=True
    )
    created_assignments = db.relationship(
        'Assignment',
        foreign_keys='Assignment.assigned_by',
        backref='assigner',
        lazy=True
    )

    def __repr__(self):
        return f'<User id={self.id} email={self.email} role={self.role}>'


class Department(db.Model):
    __tablename__ = 'departments'

    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)   # head officer
    department_name = db.Column(db.String(100), nullable=False, unique=True)
    code            = db.Column(db.String(20),  nullable=True, unique=True)  # e.g. 'DEPT-GM'
    description     = db.Column(db.String(500), nullable=True)
    status          = db.Column(db.String(20),  nullable=False, default='Active')   # Active | Inactive | Under Maintenance
    created_at      = db.Column(db.DateTime,    nullable=False, default=now_ist)

    def __repr__(self):
        return f'<Department id={self.id} name={self.department_name}>'


class Complaint(db.Model):
    __tablename__ = 'complaints'

    id               = db.Column(db.Integer,    primary_key=True, autoincrement=True)
    title            = db.Column(db.String(255), nullable=False)
    category         = db.Column(db.String(100), nullable=False)
    description      = db.Column(db.Text,        nullable=False)
    priority         = db.Column(db.String(20),  nullable=False, default='Medium')
    department       = db.Column(db.String(100), nullable=False)  # auto-derived from category, see CATEGORY_DEPARTMENT_MAP
    location         = db.Column(db.String(255), nullable=False)  # human-readable summary, auto-composed from the fields below
    city             = db.Column(db.String(100), nullable=True)
    ward             = db.Column(db.String(50),  nullable=True)
    area             = db.Column(db.String(150), nullable=True)
    street           = db.Column(db.String(150), nullable=True)
    landmark         = db.Column(db.String(200), nullable=True)
    incident_date    = db.Column(db.Date,        nullable=True)
    visit_time       = db.Column(db.String(20),  nullable=True)   # 'Morning' | 'Afternoon' | 'Evening' | ''
    urgency_note     = db.Column(db.String(500), nullable=True)
    created_by       = db.Column(db.Integer,     db.ForeignKey('users.id'), nullable=False)
    assigned_officer = db.Column(db.Integer,     db.ForeignKey('users.id'), nullable=True)
    status           = db.Column(db.String(50),  nullable=False, default='Pending')
    is_escalated     = db.Column(db.Boolean,     nullable=False, default=False)
    updated_at       = db.Column(db.DateTime,    nullable=True,  onupdate=now_ist)
    created_at       = db.Column(db.DateTime,    nullable=False, default=now_ist)

    status_logs   = db.relationship('StatusLog',      backref='complaint', lazy=True, cascade='all, delete-orphan')
    images        = db.relationship('ComplaintImages', backref='complaint', lazy=True, cascade='all, delete-orphan')
    feedback      = db.relationship('Feedback',        backref='complaint', lazy=True, uselist=False)
    notifications = db.relationship('Notification',    backref='complaint', lazy=True, cascade='all, delete-orphan')
    assignments   = db.relationship('Assignment',      backref='complaint', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Complaint id={self.id} title={self.title!r} status={self.status}>'


class StatusLog(db.Model):
    __tablename__ = 'status_logs'

    id           = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    complaint_id = db.Column(db.Integer,     db.ForeignKey('complaints.id'), nullable=False)
    old_status   = db.Column(db.String(50),  nullable=True)
    new_status   = db.Column(db.String(50),  nullable=False)
    remark       = db.Column(db.String(500), nullable=True)
    changed_at   = db.Column(db.DateTime,    nullable=False, default=now_ist)

    def __repr__(self):
        return f'<StatusLog id={self.id} {self.old_status}→{self.new_status}>'


class ComplaintImages(db.Model):
    __tablename__ = 'complaint_images'

    id           = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    complaint_id = db.Column(db.Integer,     db.ForeignKey('complaints.id'), nullable=False)
    image_url    = db.Column(db.String(500), nullable=False)
    uploaded_at  = db.Column(db.DateTime,    nullable=False, default=now_ist)

    def __repr__(self):
        return f'<ComplaintImages id={self.id} complaint_id={self.complaint_id}>'


class Feedback(db.Model):
    __tablename__ = 'feedback'

    id               = db.Column(db.Integer,      primary_key=True, autoincrement=True)
    complaint_id     = db.Column(db.Integer,      db.ForeignKey('complaints.id'), nullable=False, unique=True)
    rating           = db.Column(db.Integer,      nullable=False)               # overall rating, 1-5
    service_ratings  = db.Column(db.Text,          nullable=True)               # JSON: {"quality":5,"response":4,...}
    categories       = db.Column(db.Text,          nullable=True)               # JSON list: ["Quick response", ...]
    comments         = db.Column(db.String(1000),  nullable=True)
    improvement      = db.Column(db.Text,          nullable=True)
    would_recommend  = db.Column(db.String(10),    nullable=True)               # 'Yes' | 'No' | 'Maybe'
    is_anonymous     = db.Column(db.Boolean,       nullable=False, default=False)
    submitted_at     = db.Column(db.DateTime,      nullable=False, default=now_ist)

    def __repr__(self):
        return f'<Feedback id={self.id} complaint_id={self.complaint_id} rating={self.rating}>'


class Notification(db.Model):
    __tablename__ = 'notifications'

    id           = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    user_id      = db.Column(db.Integer,     db.ForeignKey('users.id'), nullable=False)
    complaint_id = db.Column(db.Integer,     db.ForeignKey('complaints.id'), nullable=True)
    title        = db.Column(db.String(150), nullable=False)
    message      = db.Column(db.String(500), nullable=False)
    type         = db.Column(db.String(30),  nullable=False, default='info')  # submitted|verified|assigned|resolved|system
    is_read      = db.Column(db.Boolean,     nullable=False, default=False)
    created_at   = db.Column(db.DateTime,    nullable=False, default=now_ist)

    user = db.relationship('User', backref='notifications', lazy=True)

    def __repr__(self):
        return f'<Notification id={self.id} user_id={self.user_id} complaint_id={self.complaint_id}>'


class Assignment(db.Model):
    __tablename__ = 'assignments'

    id           = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    complaint_id = db.Column(db.Integer,  db.ForeignKey('complaints.id'), nullable=False)
    worker_id    = db.Column(db.Integer,  db.ForeignKey('users.id'),      nullable=False)
    assigned_by  = db.Column(db.Integer,  db.ForeignKey('users.id'),      nullable=False)
    assigned_at  = db.Column(db.DateTime, nullable=False, default=now_ist)

    def __repr__(self):
        return f'<Assignment id={self.id} complaint_id={self.complaint_id} worker_id={self.worker_id}>'


# ─────────────────────────────────────────────────────────────────────────────
# ActivityLog
# ─────────────────────────────────────────────────────────────────────────────
class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'

    id            = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    user_id       = db.Column(db.Integer,     db.ForeignKey('users.id'), nullable=False)
    complaint_id  = db.Column(db.Integer,     db.ForeignKey('complaints.id'), nullable=True)
    activity_type = db.Column(db.String(50),  nullable=False)   # see ACTIVITY_TYPES in api_auth_utils.py
    description   = db.Column(db.String(255), nullable=False)   # human-readable, ready to show in UI
    ip_address    = db.Column(db.String(45),  nullable=True)    # supports IPv6
    created_at    = db.Column(db.DateTime,    nullable=False, default=now_ist)

    user      = db.relationship('User', backref=db.backref('activity_logs', lazy=True, cascade='all, delete-orphan'))
    complaint = db.relationship('Complaint', backref=db.backref('activity_logs', lazy=True))

    def __repr__(self):
        return f'<ActivityLog id={self.id} user_id={self.user_id} type={self.activity_type}>'


# ─────────────────────────────────────────────────────────────────────────────
# TokenBlocklist
# ─────────────────────────────────────────────────────────────────────────────
class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'

    id         = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    jti        = db.Column(db.String(36),  nullable=False, unique=True, index=True)
    user_id    = db.Column(db.Integer,     db.ForeignKey('users.id'), nullable=True)
    expires_at = db.Column(db.DateTime,    nullable=False)   # token's own exp, for cleanup
    created_at = db.Column(db.DateTime,    nullable=False, default=now_ist)

    def __repr__(self):
        return f'<TokenBlocklist jti={self.jti}>'


# ─────────────────────────────────────────────────────────────────────────────
# LoginSession
# ─────────────────────────────────────────────────────────────────────────────
class LoginSession(db.Model):
    __tablename__ = 'login_sessions'

    id             = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    user_id        = db.Column(db.Integer,     db.ForeignKey('users.id'), nullable=False)
    jti            = db.Column(db.String(36),  nullable=True, unique=True, index=True)
    device         = db.Column(db.String(50),  nullable=True)   # Desktop | Mobile | Tablet | Unknown
    os             = db.Column(db.String(50),  nullable=True)
    browser        = db.Column(db.String(50),  nullable=True)
    ip_address     = db.Column(db.String(45),  nullable=True)
    status         = db.Column(db.String(20),  nullable=False, default='Success')  # Success | Failed
    created_at     = db.Column(db.DateTime,    nullable=False, default=now_ist)
    last_active_at = db.Column(db.DateTime,    nullable=True)
    expires_at     = db.Column(db.DateTime,    nullable=True)   # copied from the refresh token's exp
    revoked_at     = db.Column(db.DateTime,    nullable=True)

    user = db.relationship('User', backref=db.backref('login_sessions', lazy=True, cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<LoginSession id={self.id} user_id={self.user_id} status={self.status}>'


# ─────────────────────────────────────────────────────────────────────────────
# NotificationPreference
# One row per user. Created lazily with defaults on first read.
# ─────────────────────────────────────────────────────────────────────────────
class NotificationPreference(db.Model):
    __tablename__ = 'notification_preferences'

    id             = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    user_id        = db.Column(db.Integer,  db.ForeignKey('users.id'), nullable=False, unique=True)
    email          = db.Column(db.Boolean,  nullable=False, default=True)
    push           = db.Column(db.Boolean,  nullable=False, default=True)
    alerts         = db.Column(db.Boolean,  nullable=False, default=True)
    security       = db.Column(db.Boolean,  nullable=False, default=True)
    dept_updates   = db.Column(db.Boolean,  nullable=False, default=False)
    weekly_reports = db.Column(db.Boolean,  nullable=False, default=True)
    updated_at     = db.Column(db.DateTime, nullable=True, onupdate=now_ist)

    def __repr__(self):
        return f'<NotificationPreference user_id={self.user_id}>'


# ─────────────────────────────────────────────────────────────────────────────
# PasswordResetOTP
# ─────────────────────────────────────────────────────────────────────────────
class PasswordResetOTP(db.Model):
    __tablename__ = 'password_reset_otps'

    id         = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    email      = db.Column(db.String(255), nullable=False, unique=True, index=True)
    otp_hash   = db.Column(db.String(255), nullable=False)   # hashed, never store the raw OTP
    attempts   = db.Column(db.Integer,     nullable=False, default=0)
    expires_at = db.Column(db.DateTime,    nullable=False)
    created_at = db.Column(db.DateTime,    nullable=False, default=now_ist)

    MAX_ATTEMPTS = 5

    def __repr__(self):
        return f'<PasswordResetOTP email={self.email}>'


# ─────────────────────────────────────────────────────────────────────────────
# ContactMessage
# Stores messages submitted via the public Contact Us form.
# No authentication required — anyone can submit.
# ─────────────────────────────────────────────────────────────────────────────
class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'

    id         = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    name       = db.Column(db.String(255), nullable=False)
    email      = db.Column(db.String(255), nullable=False)
    subject    = db.Column(db.String(255), nullable=False, default='General Inquiry')
    message    = db.Column(db.Text,        nullable=False)
    is_read    = db.Column(db.Boolean,     nullable=False, default=False)
    created_at = db.Column(db.DateTime,    nullable=False, default=now_ist)

    def __repr__(self):
        return f'<ContactMessage id={self.name} email={self.email} subject={self.subject!r} message={self.message!r}>'


# ─────────────────────────────────────────────────────────────────────────────
# Announcement
# ─────────────────────────────────────────────────────────────────────────────
class Announcement(db.Model):
    __tablename__ = 'announcements'

    id         = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    title      = db.Column(db.String(255), nullable=False)
    summary    = db.Column(db.String(500), nullable=True)
    content    = db.Column(db.Text,        nullable=False)
    category   = db.Column(db.String(50),  nullable=False, default='General')     # Maintenance | Policy | Alert | Holiday | General
    priority   = db.Column(db.String(20),  nullable=False, default='Normal')      # Emergency | Critical | Important | Normal
    audience   = db.Column(db.String(50),  nullable=False, default='All Users')   # All Users | Citizens | Officers | Workers
    status     = db.Column(db.String(20),  nullable=False, default='Draft')       # Draft | Scheduled | Published | Archived
    is_pinned  = db.Column(db.Boolean,     nullable=False, default=False)
    views      = db.Column(db.Integer,     nullable=False, default=0)
    publish_at = db.Column(db.DateTime,    nullable=True)
    expiry_at  = db.Column(db.DateTime,    nullable=True)
    author_id  = db.Column(db.Integer,     db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime,    nullable=False, default=now_ist)
    updated_at = db.Column(db.DateTime,    nullable=True,  onupdate=now_ist)

    def __repr__(self):
        return f'<Announcement id={self.id} title={self.title!r} status={self.status}>'


def init_db(app, admin_config):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(role="Admin").first():
            admin = User(
                name=admin_config.get("name") or "Administrator",
                email=admin_config.get("email") or "admin@gmail.com",
                phone=admin_config.get("phone") or "9999999999",
                role="Admin",
                password=generate_password_hash(admin_config.get("password") or "Admin@123"),
            )
            db.session.add(admin)
            db.session.commit()

        if not Department.query.first():
            for name in [
                'Sanitation Department', 'Roads & Infrastructure',
                'Electrical Department', 'Water & Drainage Department',
                'General Administration'
            ]:
                db.session.add(Department(department_name=name, status='Active'))
            db.session.commit()