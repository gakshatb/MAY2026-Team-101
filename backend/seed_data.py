"""
Run:
    python seed_data.py            # append dummy data (safe to re-run; skips if complaints already exist)
    python seed_data.py --reset    # wipe all tables first, then reseed from scratch
"""

import argparse
import itertools
import random
from datetime import timedelta

from werkzeug.security import generate_password_hash

from models import (
    db, User, Department, Complaint, StatusLog, ComplaintImages,
    Feedback, Notification, Assignment, ActivityLog,
    TokenBlocklist, PasswordResetOTP, ContactMessage, now_ist,
)

try:
    from app import app
except ImportError as e:
    raise SystemExit(
        "Could not import `app` from app.py. If your Flask app instance is "
        "named differently or built via a factory function (e.g. create_app()), "
        "update the import at the top of seed_data.py accordingly.\n"
        f"Original error: {e}"
    )

random.seed(42)  # reproducible bulk data across runs

DEFAULT_PASSWORD = "Password@123"  # same for every dummy account, for easy testing
PWD_HASH = generate_password_hash(DEFAULT_PASSWORD)

USER_STATUSES = ['active', 'pending', 'suspended']

FIRST_NAMES = [
    'Prasad', 'Sneha', 'Sakshi', 'Pooja', 'Vikram', 'Gayatri', 'Ravi', 'Anita',
    'Suresh', 'Priya', 'Manoj', 'Deepak', 'Gopal', 'Akshat', 'Kiran', 'Sunita',
    'Amit', 'Ritesh', 'Rohit', 'Divya', 'Sanjay', 'Rekha', 'Vivek', 'Himanshu',
    'Nikhil', 'Anjali', 'Gaurav', 'Shravan', 'Karan', 'Rituka',
]
LAST_NAMES = [
    'Gupta', 'Verma', 'Iyer', 'Nair', 'Sharma', 'Kumar', 'Das', 'Singh',
    'Patil', 'Rao', 'Mehta', 'Kapoor', 'Reddy', 'Joshi', 'Malhotra',
    'Bansal', 'Chauhan', 'Agarwal', 'Menon', 'Pillai',
]
CITIES_UP = [
    ('Lucknow', 'Uttar Pradesh', '226001'), ('Lucknow', 'Uttar Pradesh', '226010'),
    ('Kanpur', 'Uttar Pradesh', '208001'), ('Kanpur', 'Uttar Pradesh', '208012'),
    ('Mumbai', 'Maharashtra', '400074'), ('Pune', 'Maharashtra', '411057'),
    ('Kolhapur', 'Maharashtra', '416012'), ('Karad', 'Maharashtra', '415110'),
    ('Satara', 'Maharashtra', '415001'), ('Sangli', 'Maharashtra', '416415'),
]

_name_counter = itertools.count()


def gen_name_and_email(domain, tag):
    """Deterministic, always-unique name + email pair."""
    idx = next(_name_counter)
    first = FIRST_NAMES[idx % len(FIRST_NAMES)]
    last = LAST_NAMES[(idx // len(FIRST_NAMES)) % len(LAST_NAMES)]
    email = f"{first.lower()}.{last.lower()}.{tag}{idx}@{domain}"
    phone = f"9{100000000 + idx * 137 % 900000000}"[:10]
    return f"{first} {last}", email, phone


def backdated(days_ago_min, days_ago_max):
    """A now_ist()-relative timestamp somewhere in the past, for realistic tenure/age."""
    days = random.randint(days_ago_min, days_ago_max)
    jitter = timedelta(seconds=random.randint(0, 86399))
    return now_ist() - timedelta(days=days) + jitter


def get_or_create_user(**kwargs):
    existing = User.query.filter_by(email=kwargs['email']).first()
    if existing:
        return existing
    u = User(**kwargs)
    db.session.add(u)
    return u


def reset_db():
    """Delete all rows, in reverse dependency order."""
    for model in [
        ActivityLog, Notification, Feedback, Assignment,
        ComplaintImages, StatusLog, Complaint,
        TokenBlocklist, PasswordResetOTP, ContactMessage,
        User, Department,
    ]:
        db.session.query(model).delete()
    db.session.commit()
    print("✔ Existing data wiped.")


def seed():
    # ── 1. Departments — one of each status, deliberately ───────────
    dept_specs = [
        ('Sanitation Department', 'DEPT-SAN', 'Active'),
        ('Roads & Infrastructure', 'DEPT-ROAD', 'Active'),
        ('Electrical Department', 'DEPT-ELEC', 'Under Maintenance'),
        ('Water & Drainage Department', 'DEPT-WATER', 'Inactive'),
        ('General Administration', 'DEPT-GEN', 'Active'),
    ]
    departments = {}
    for name, code, status in dept_specs:
        dept = Department.query.filter_by(department_name=name).first()
        if not dept:
            dept = Department(department_name=name, code=code,
                               description=f'Handles issues related to {name.lower()}',
                               status=status, created_at=backdated(500, 700))
            db.session.add(dept)
    db.session.commit()
    for name, _, _ in dept_specs:
        departments[name] = Department.query.filter_by(department_name=name).first()
    print(f"✔ Departments ready ({len(departments)}), statuses: "
          f"{', '.join(sorted({s for _, _, s in dept_specs}))}.")

    # ── 2. Users — admin, then officers/workers x every status x every dept,
    #      then a bulk batch of citizens (all active — see module docstring) ─
    admin = get_or_create_user(
        name='System Admin', email='admin@civicdesk.com', phone='9999900000',
        password=PWD_HASH, role='Admin', status='active', created_at=backdated(600, 650),
    )
    db.session.commit()

    officers = {status: {} for status in USER_STATUSES}   # status -> {dept_name: [User,...]}
    workers = {status: {} for status in USER_STATUSES}
    genders = ['male', 'female', 'other']
    staff_idx = 0

    for dept_name in departments:
        for status in USER_STATUSES:
            # pending accounts are brand-new (awaiting approval); active/suspended
            # accounts have real tenure behind them.
            tenure = backdated(1, 20) if status == 'pending' else backdated(30, 700)

            name, email, phone = gen_name_and_email('civicdesk.com', 'off')
            city, state, pincode = CITIES_UP[staff_idx % len(CITIES_UP)]
            u = get_or_create_user(
                name=name, email=email, phone=phone, password=PWD_HASH,
                address=f'{20 + staff_idx}, Civil Lines', city=city, state=state,
                pincode=pincode, gender=genders[staff_idx % len(genders)],
                role='Officer', status=status, designation=f'{dept_name.split()[0]} Officer',
                department_id=departments[dept_name].id, created_at=tenure,
            )
            officers[status].setdefault(dept_name, []).append(u)
            staff_idx += 1

            tenure = backdated(1, 20) if status == 'pending' else backdated(30, 700)
            name, email, phone = gen_name_and_email('civicdesk.com', 'wrk')
            city, state, pincode = CITIES_UP[staff_idx % len(CITIES_UP)]
            w = get_or_create_user(
                name=name, email=email, phone=phone, password=PWD_HASH,
                address=f'{20 + staff_idx}, Civil Lines', city=city, state=state,
                pincode=pincode, gender=genders[staff_idx % len(genders)],
                role='Worker', status=status, designation=f'{dept_name.split()[0]} Worker',
                department_id=departments[dept_name].id, created_at=tenure,
            )
            workers[status].setdefault(dept_name, []).append(w)
            staff_idx += 1
    db.session.commit()
    total_officers = sum(len(v) for d in officers.values() for v in d.values())
    total_workers = sum(len(v) for d in workers.values() for v in d.values())
    print(f"✔ Officers ready ({total_officers}: {len(departments)} depts x {len(USER_STATUSES)} statuses).")
    print(f"✔ Workers ready ({total_workers}: {len(departments)} depts x {len(USER_STATUSES)} statuses).")

    # Citizens: all 'active' — the real registration flow never produces a
    # pending or suspended citizen (see module docstring), so seeding one
    # would be testing a state the app can't actually reach.
    n_citizens = random.randint(25, 35)
    citizens = []
    genders = ['male', 'female', 'other']
    for i in range(n_citizens):
        name, email, phone = gen_name_and_email('example.com', 'cit')
        city, state, pincode = CITIES_UP[i % len(CITIES_UP)]
        c = get_or_create_user(
            name=name, email=email, phone=phone, password=PWD_HASH,
            address=f'{10 + i}, MG Road', city=city, state=state,
            pincode=pincode, gender=genders[i % len(genders)],
            role='Citizen', status='active', created_at=backdated(1, 500),
        )
        citizens.append(c)
    db.session.commit()
    print(f"✔ Citizens ready ({len(citizens)}, all active).")

    # ── 3. Department heads — only an ACTIVE officer can head a dept ─
    for dept_name, dept in departments.items():
        if not dept.user_id and officers['active'].get(dept_name):
            dept.user_id = officers['active'][dept_name][0].id
    db.session.commit()
    print("✔ Department heads assigned (from active officers only).")

    # ── 4. Complaints ─────────────────────────────────────────────────
    if Complaint.query.first():
        print("✔ Complaints already exist, skipping complaint/log/feedback/notification/activity seeding.")
        print(f"\nDone. Every dummy account's password is: {DEFAULT_PASSWORD}")
        return

    # Exact keys from CATEGORY_DEPARTMENT_MAP in api_citizen.py — the category
    # string decides auto-routing to a department, so it must match verbatim.
    category_dept_map = {
        'Garbage Collection':     'Sanitation Department',
        'Overflowing Dustbin':    'Sanitation Department',
        'Illegal Waste Dumping':  'Sanitation Department',
        'Potholes':               'Roads & Infrastructure',
        'Road Damage':            'Roads & Infrastructure',
        'Public Property Damage': 'Roads & Infrastructure',
        'Broken Streetlight':     'Electrical Department',
        'Water Leakage':          'Water & Drainage Department',
        'Blocked Drainage':       'Water & Drainage Department',
        'Other':                  'General Administration',
    }
    category_issues = {
        'Garbage Collection': [
            'Garbage not collected for over a week',
            'Segregated waste not being picked up on schedule',
            'Dead animal left uncollected on roadside',
        ],
        'Overflowing Dustbin': [
            'Overflowing dustbin attracting stray animals',
            'Community bin not emptied in days, foul smell spreading',
        ],
        'Illegal Waste Dumping': [
            'Illegal dumping near residential area',
            'Burning of garbage causing smoke nuisance',
        ],
        'Potholes': [
            'Large pothole causing traffic accidents',
            'Road surface caved in after heavy rain',
            'Deep crater blocking half the road width',
        ],
        'Road Damage': [
            'Broken road divider with exposed debris',
            'Uneven patchwork making the road unsafe',
        ],
        'Public Property Damage': [
            'Damaged park bench and playground equipment',
            'Vandalized public signage near the market',
        ],
        'Broken Streetlight': [
            'Street light not working for two weeks',
            'Flickering street light causing eye strain',
            'Entire street plunged in darkness at night',
        ],
        'Water Leakage': [
            'Water pipeline leakage flooding the road',
            'Broken water meter leaking continuously',
        ],
        'Blocked Drainage': [
            'Clogged drainage causing waterlogging after rain',
            'Sewage overflow mixing with drinking water line',
        ],
        'Other': [
            'Stray dog menace in the neighborhood',
            'Encroachment blocking public pathway',
            'Noise pollution from nearby construction',
            'Public toilet in unhygienic condition',
        ],
    }
    categories = list(category_dept_map.keys())

    # Weighted so most complaints look like a normal in-flight caseload,
    # with Emergency genuinely rare — matches how VALID_PRIORITIES is used.
    priority_choices = ['Low', 'Medium', 'High', 'Emergency']
    priority_weights = [0.25, 0.45, 0.25, 0.05]

    # This is the exact status vocabulary api_citizen.py / api_admin.py filter
    # and aggregate on (OPEN_STATUSES, Resolved/Closed groupings) — 'Rejected'
    # is intentionally not used since nothing in the backend recognizes it.
    status_choices = ['Pending', 'Under Review', 'Assigned', 'In Progress', 'Resolved', 'Closed']
    status_weights = [0.15, 0.10, 0.10, 0.20, 0.30, 0.15]

    areas = ['Indira Nagar', 'Alambagh', 'Gomti Nagar', 'Chowk', 'Hazratganj',
              'Aliganj', 'Mahanagar', 'Rajajipuram', 'Aminabad', 'Vikas Nagar']
    streets = ['12th Cross Street', 'Station Road', 'Vipin Khand', 'Nakhas Road',
               'MG Marg', 'Kanpur Road', 'Faizabad Road', 'Ashok Marg', 'Sector B Road']
    landmarks = ['near the community park', 'opposite the bus stop', 'next to the water tank',
                 'near the market entrance', 'behind the government school', 'near the temple',
                 'close to the railway crossing', 'near the flyover']
    visit_times = ['Morning', 'Afternoon', 'Evening', '']
    urgency_notes = [
        'Immediate attention required, elderly residents affected.',
        'Safety hazard — needs urgent inspection.',
        'Multiple residents have complained about this.',
        'Getting worse every day, please prioritize.',
    ]

    today = now_ist().date()

    MIN_COMPLAINTS_PER_CITIZEN = 6
    MAX_COMPLAINTS_PER_CITIZEN = 12

    OPEN_STATUSES = {'Pending', 'Under Review', 'Assigned', 'In Progress'}
    DONE_STATUSES = {'Resolved', 'Closed'}

    complaint_rows = []  # (Complaint, category, dept_name, status, officer_or_None, citizen)
    for citizen in citizens:
        n_complaints = random.randint(MIN_COMPLAINTS_PER_CITIZEN, MAX_COMPLAINTS_PER_CITIZEN)
        for _ in range(n_complaints):
            category = random.choice(categories)
            dept_name = category_dept_map[category]
            priority = random.choices(priority_choices, weights=priority_weights, k=1)[0]
            status = random.choices(status_choices, weights=status_weights, k=1)[0]
            area = random.choice(areas)
            street = random.choice(streets)
            landmark = random.choice(landmarks)
            ward = f'Ward {random.randint(1, 15)}'
            issue = random.choice(category_issues[category])

            active_officers_here = officers['active'].get(dept_name) or []
            officer = None
            if status != 'Pending':
                officer = random.choice(active_officers_here) if active_officers_here else None
            elif active_officers_here and random.random() < 0.15:
                officer = random.choice(active_officers_here)  # edge case: assigned but still Pending

            is_escalated = (priority in ('High', 'Emergency') and status in OPEN_STATUSES
                             and random.random() < 0.5)

            created_at = backdated(1, 90)
            updated_at = None
            if status in DONE_STATUSES:
                # resolved after a realistic 1-14 day handling window
                updated_at = created_at + timedelta(days=random.randint(1, 14),
                                                      hours=random.randint(0, 23))
                if updated_at > now_ist():
                    updated_at = now_ist()
            elif status != 'Pending':
                updated_at = created_at + timedelta(hours=random.randint(1, 72))

            c = Complaint(
                title=issue,
                category=category,
                description=f'{issue}, reported on {street}, {area}, {landmark}. '
                             f'Citizen requests prompt resolution.',
                priority=priority,
                department=dept_name,
                location=f'{street}, {area}, {ward}, {citizen.city}',
                city=citizen.city, ward=ward, area=area, street=street,
                landmark=landmark.capitalize(),
                incident_date=today - timedelta(days=random.randint(0, 60)),
                visit_time=random.choice(visit_times),
                urgency_note=random.choice(urgency_notes) if priority in ('High', 'Emergency') else None,
                created_by=citizen.id,
                assigned_officer=officer.id if officer else None,
                status=status,
                is_escalated=is_escalated,
                created_at=created_at,
                updated_at=updated_at,
            )
            db.session.add(c)
            complaint_rows.append((c, category, dept_name, status, officer, citizen))
    db.session.commit()
    print(f"✔ Complaints created ({len(complaint_rows)}: from {len(citizens)} "
          f"active citizens, {MIN_COMPLAINTS_PER_CITIZEN}-{MAX_COMPLAINTS_PER_CITIZEN} each, "
          f"weighted random category/priority/status/location per complaint).")

    # ── 5. StatusLog + 6. ComplaintImages ────────────────────────────
    # Logical transition chain matching the real status vocabulary, truncated
    # to wherever this particular complaint actually landed.
    FULL_CHAIN = ['Pending', 'Under Review', 'Assigned', 'In Progress', 'Resolved']
    sample_image = 'https://picsum.photos/seed/{}/600/400'
    for c, category, dept_name, status, officer, citizen in complaint_rows:
        if status == 'Closed':
            steps = FULL_CHAIN + ['Closed']
        else:
            steps = FULL_CHAIN[:FULL_CHAIN.index(status) + 1] if status in FULL_CHAIN else [status]

        prev = None
        step_time = c.created_at
        for i, step in enumerate(steps):
            remark = {
                'Pending': 'Complaint submitted by citizen.',
                'Under Review': 'Complaint under review by department staff.',
                'Assigned': f'Assigned to {officer.name if officer else "an officer"} for action.',
                'In Progress': 'Work has started on this complaint.',
                'Resolved': 'Issue resolved and verified on-site.',
                'Closed': 'Complaint closed after citizen confirmation.',
            }[step]
            db.session.add(StatusLog(complaint_id=c.id, old_status=prev, new_status=step,
                                      remark=remark, changed_at=step_time))
            prev = step
            if len(steps) > 1:
                step_time = step_time + (c.updated_at - c.created_at) / max(len(steps) - 1, 1) \
                    if c.updated_at else step_time

        db.session.add(ComplaintImages(complaint_id=c.id, image_url=sample_image.format(c.id),
                                        uploaded_at=c.created_at))
        if random.random() < 0.3:  # some complaints get a second photo
            db.session.add(ComplaintImages(complaint_id=c.id, image_url=sample_image.format(f'{c.id}-b'),
                                            uploaded_at=c.created_at))
    db.session.commit()
    print("✔ Status logs and complaint images added.")

    # ── 7. Assignment — worker assigned by officer once work has started ─
    # Only ACTIVE workers get real assignments — an admin wouldn't hand work
    # to a pending or suspended account.
    assignment_count = 0
    for c, category, dept_name, status, officer, citizen in complaint_rows:
        if status in ('Assigned', 'In Progress', 'Resolved', 'Closed') and officer:
            pool = workers['active'].get(dept_name)
            if pool:
                worker = pool[c.id % len(pool)]
                db.session.add(Assignment(complaint_id=c.id, worker_id=worker.id,
                                           assigned_by=officer.id, assigned_at=c.created_at))
                assignment_count += 1
    db.session.commit()
    print(f"✔ Assignments created ({assignment_count}).")

    # ── 8. Feedback — only Resolved/Closed complaints (unique per complaint) ─
    feedback_count = 0
    for c, category, dept_name, status, officer, citizen in complaint_rows:
        if status in ('Resolved', 'Closed'):
            rating = [3, 4, 4, 5, 5][c.id % 5]
            db.session.add(Feedback(
                complaint_id=c.id, rating=rating,
                service_ratings=f'{{"quality":{rating},"response":{max(rating - 1, 1)}}}',
                categories='["Quick response", "Problem solved"]' if rating >= 4 else '["Delayed response"]',
                comments='Issue was fixed, thank you.' if rating >= 4 else 'Took longer than expected but resolved.',
                improvement=None if rating >= 4 else 'Faster turnaround would help.',
                would_recommend='Yes' if rating >= 4 else 'Maybe',
                is_anonymous=(c.id % 4 == 0),
                submitted_at=c.updated_at or c.created_at,
            ))
            feedback_count += 1
    db.session.commit()
    print(f"✔ Feedback added ({feedback_count}, for resolved/closed complaints).")

    # ── 9. Notifications — documented type set: submitted|verified|assigned|resolved|system ─
    notif_count = 0
    for c, category, dept_name, status, officer, citizen in complaint_rows:
        db.session.add(Notification(
            user_id=citizen.id, complaint_id=c.id, title=f'Complaint CMP-{c.id:05d} submitted',
            message=f"Your complaint '{c.title}' has been received.", type='submitted',
            created_at=c.created_at,
        ))
        notif_count += 1
        if status != 'Pending':
            db.session.add(Notification(
                user_id=citizen.id, complaint_id=c.id, title=f'Complaint CMP-{c.id:05d} verified',
                message=f"Your complaint '{c.title}' has been verified by our team.", type='verified',
                created_at=c.created_at,
            ))
            notif_count += 1
        if status in ('Assigned', 'In Progress', 'Resolved', 'Closed') and officer:
            db.session.add(Notification(
                user_id=citizen.id, complaint_id=c.id, title=f'Complaint CMP-{c.id:05d} assigned',
                message=f"Your complaint '{c.title}' has been assigned to {officer.name}.", type='assigned',
                created_at=c.updated_at or c.created_at,
            ))
            notif_count += 1
        if status in ('Resolved', 'Closed'):
            db.session.add(Notification(
                user_id=citizen.id, complaint_id=c.id, title=f'Complaint CMP-{c.id:05d} resolved',
                message=f"Your complaint '{c.title}' has been marked {status.lower()}.", type='resolved',
                created_at=c.updated_at or c.created_at,
            ))
            notif_count += 1
    db.session.commit()
    print(f"✔ Notifications added ({notif_count}), types: submitted, verified, assigned, resolved.")

    # ── 10. ActivityLog — only values from ACTIVITY_TYPES in api_auth_utils.py ─
    activity_count = 0
    for c, category, dept_name, status, officer, citizen in complaint_rows:
        db.session.add(ActivityLog(
            user_id=citizen.id, complaint_id=c.id, activity_type='complaint_submitted',
            description=f"Submitted complaint '{c.title}'.", ip_address='127.0.0.1',
            created_at=c.created_at,
        ))
        activity_count += 1

    for c, category, dept_name, status, officer, citizen in complaint_rows:
        if status in ('Resolved', 'Closed'):
            db.session.add(ActivityLog(
                user_id=citizen.id, complaint_id=c.id, activity_type='feedback_submitted',
                description=f"Submitted feedback for complaint CMP-{c.id:05d}.", ip_address='127.0.0.1',
                created_at=c.updated_at or c.created_at,
            ))
            activity_count += 1

    # Department creation activity (admin-attributed)
    for name, dept in departments.items():
        db.session.add(ActivityLog(
            user_id=admin.id, activity_type='department_created',
            description=f"Created department '{name}'.", ip_address='127.0.0.1',
            created_at=dept.created_at,
        ))
        activity_count += 1

    # Officer lifecycle activity: one sample per dept/status, admin-attributed
    for dept_name, dept_officers in officers['active'].items():
        for off in dept_officers[:1]:
            db.session.add(ActivityLog(
                user_id=admin.id, activity_type='officer_approved',
                description=f"Approved officer account for {off.name} ({off.email}).",
                ip_address='127.0.0.1', created_at=off.created_at,
            ))
            activity_count += 1
    for dept_name, dept_officers in officers['suspended'].items():
        for off in dept_officers[:1]:
            db.session.add(ActivityLog(
                user_id=admin.id, activity_type='officer_suspended',
                description=f"Suspended officer account for {off.name} ({off.email}).",
                ip_address='127.0.0.1', created_at=off.created_at + timedelta(days=5),
            ))
            activity_count += 1

    # A recent login for every active officer/worker, so "Last Login" has something to show.
    sample_ips = ['192.168.1.4', '192.168.1.12', '10.0.0.23', '172.16.4.9']
    for dept_officers in officers['active'].values():
        for off in dept_officers:
            db.session.add(ActivityLog(
                user_id=off.id, activity_type='login', description='Logged in.',
                ip_address=sample_ips[off.id % len(sample_ips)], created_at=backdated(0, 3),
            ))
            activity_count += 1
    for dept_workers in workers['active'].values():
        for w in dept_workers:
            db.session.add(ActivityLog(
                user_id=w.id, activity_type='login', description='Logged in.',
                ip_address=sample_ips[w.id % len(sample_ips)], created_at=backdated(0, 3),
            ))
            activity_count += 1
    db.session.commit()
    print(f"✔ Activity logs added ({activity_count}).")

    print(f"\nAll done. Every dummy account's password is: {DEFAULT_PASSWORD}")
    print(f"Admin login: {admin.email} / {DEFAULT_PASSWORD}")
    print("Coverage check:")
    print(f"  User.role:          Admin, Citizen, Officer, Worker (Title Case)")
    print(f"  User.status:        {USER_STATUSES} (citizens always 'active')")
    print(f"  Department.status:  {sorted({s for _, _, s in dept_specs})}")
    print(f"  Complaint.status:   {status_choices}")
    print(f"  Complaint.priority: {priority_choices}")
    print("  Complaint.is_escalated: [True, False]")
    print("  Notification.type: [submitted, verified, assigned, resolved]")
    print("  ActivityLog.activity_type: [complaint_submitted, feedback_submitted, "
          "department_created, officer_approved, officer_suspended]")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Seed CivicDesk with bulk dummy data.')
    parser.add_argument('--reset', action='store_true', help='Wipe all tables before seeding.')
    args = parser.parse_args()

    with app.app_context():
        db.create_all()
        if args.reset:
            reset_db()
        seed()