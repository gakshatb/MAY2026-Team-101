import os
import smtplib
import ssl
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv  # type: ignore

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").strip().lower() not in ("false", "0", "no")

SMTP_USERNAME = os.getenv("SMTP_USERNAME") or os.getenv("ADMIN_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD") or os.getenv("ADMIN_MAIL_PASSWORD")

MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "CivicDesk")
MAIL_FROM_ADDRESS = os.getenv("MAIL_FROM_ADDRESS") or SMTP_USERNAME

MAIL_ENABLED = os.getenv("MAIL_ENABLED", "true").strip().lower() not in ("false", "0", "no")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")

BRAND_COLOR = "#2563EB"
BRAND_COLOR_DARK = "#1E40AF"


def _log_error(message):
    print(f"[mail.py] {message}", file=sys.stderr)


# ─────────────────────────────────────────────────────────────────────────
# Core send — everything else in this file funnels through here.
# ─────────────────────────────────────────────────────────────────────────
def send_email(to_email, subject, html_body, text_body=None):
    """
    Send a single email. Returns True on success, False on any failure
    (including being unconfigured) — never raises.
    """
    if not to_email:
        _log_error("send_email called with no recipient — skipped.")
        return False

    if not MAIL_ENABLED:
        _log_error(f"MAIL_ENABLED is false — skipped email to {to_email}: {subject!r}")
        return False

    if not SMTP_USERNAME or not SMTP_PASSWORD:
        _log_error("SMTP_USERNAME/SMTP_PASSWORD (or ADMIN_EMAIL/ADMIN_MAIL_PASSWORD) not set — cannot send mail.")
        return False

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = f"{MAIL_FROM_NAME} <{MAIL_FROM_ADDRESS}>"
    message["To"] = to_email

    message.attach(MIMEText(text_body or _strip_html(html_body), "plain"))
    message.attach(MIMEText(html_body, "html"))

    try:
        if SMTP_USE_TLS:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
                server.ehlo()
                server.starttls(context=ssl.create_default_context())
                server.ehlo()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.sendmail(MAIL_FROM_ADDRESS, [to_email], message.as_string())
        else:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=10, context=ssl.create_default_context()) as server:
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.sendmail(MAIL_FROM_ADDRESS, [to_email], message.as_string())
        return True
    except Exception as exc:  # noqa: BLE001 — a mail failure must never crash the caller
        _log_error(f"Failed to send {subject!r} to {to_email}: {exc}")
        return False


def _strip_html(html):
    """Crude HTML->text fallback for email clients that reject HTML."""
    import re
    text = re.sub(r"<br\s*/?>", "\n", html)
    text = re.sub(r"</p>", "\n\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


# ─────────────────────────────────────────────────────────────────────────
# Shared HTML shell — every template below renders its body through this,
# so all outgoing mail looks consistent without repeating boilerplate.
# ─────────────────────────────────────────────────────────────────────────
def _render(preheader, heading, body_html, cta_text=None, cta_url=None, footnote=None):
    cta_html = ""
    if cta_text and cta_url:
        cta_html = f"""
        <tr>
          <td align="center" style="padding: 8px 0 28px 0;">
            <a href="{cta_url}"
               style="background:{BRAND_COLOR}; color:#ffffff; text-decoration:none;
                      padding:12px 28px; border-radius:8px; font-weight:700;
                      font-size:14px; display:inline-block;">
              {cta_text}
            </a>
          </td>
        </tr>
        """

    footnote_html = f'<p style="color:#94a3b8; font-size:12px; margin-top:24px;">{footnote}</p>' if footnote else ""

    return f"""\
<!DOCTYPE html>
<html>
  <body style="margin:0; padding:0; background:#f1f5f9; font-family:'Segoe UI', Arial, sans-serif;">
    <span style="display:none; max-height:0; overflow:hidden;">{preheader}</span>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f1f5f9; padding:32px 16px;">
      <tr>
        <td align="center">
          <table role="presentation" width="100%" style="max-width:520px; background:#ffffff; border-radius:14px; overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,0.08);">
            <tr>
              <td style="background:linear-gradient(135deg, {BRAND_COLOR_DARK}, {BRAND_COLOR}); padding:24px 32px;">
                <span style="color:#ffffff; font-size:20px; font-weight:800; letter-spacing:-0.02em;">CivicDesk</span>
              </td>
            </tr>
            <tr>
              <td style="padding:32px;">
                <h1 style="margin:0 0 16px 0; font-size:20px; color:#0f172a;">{heading}</h1>
                <div style="font-size:14px; line-height:1.7; color:#334155;">
                  {body_html}
                </div>
              </td>
            </tr>
            {cta_html}
            <tr>
              <td style="padding:0 32px 28px 32px;">
                {footnote_html}
              </td>
            </tr>
            <tr>
              <td style="background:#f8fafc; padding:18px 32px; border-top:1px solid #e2e8f0;">
                <p style="margin:0; font-size:12px; color:#94a3b8;">
                  This is an automated message from CivicDesk. Please do not reply directly to this email.
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""


# ─────────────────────────────────────────────────────────────────────────
# Auth & account lifecycle
# ─────────────────────────────────────────────────────────────────────────
def send_welcome_email(to_email, name):
    """Citizen (or any role) just registered."""
    html = _render(
        preheader="Welcome to CivicDesk",
        heading=f"Welcome, {name} 👋",
        body_html=f"""
            <p>Your CivicDesk account has been created successfully.</p>
            <p>You can now log in to submit complaints, track their progress, and stay updated
               on civic issues in your area.</p>
        """,
        cta_text="Log In to CivicDesk",
        cta_url=f"{FRONTEND_URL}/login",
    )
    return send_email(to_email, "Welcome to CivicDesk", html)


def send_registration_pending_email(to_email, name, role):
    """Officer/Worker registered and is awaiting approval."""
    html = _render(
        preheader="Your account is pending approval",
        heading="Registration Received",
        body_html=f"""
            <p>Hi {name},</p>
            <p>Thanks for registering as a{'n' if role[0].lower() in 'aeiou' else ''} <strong>{role}</strong>
               on CivicDesk. Your account is currently <strong>pending approval</strong>.</p>
            <p>We'll email you as soon as a decision is made — you don't need to do anything else for now.</p>
        """,
    )
    return send_email(to_email, "CivicDesk Registration Received", html)


def send_worker_approved_email(to_email, name, department_name=None):
    dept_line = f" and assigned to the <strong>{department_name}</strong> department" if department_name else ""
    html = _render(
        preheader="Your worker account has been approved",
        heading="Account Approved ✅",
        body_html=f"""
            <p>Hi {name},</p>
            <p>Good news — your CivicDesk worker account has been approved{dept_line}.</p>
            <p>You can now log in to view your assigned tasks.</p>
        """,
        cta_text="Log In",
        cta_url=f"{FRONTEND_URL}/login",
    )
    return send_email(to_email, "Your CivicDesk Account Has Been Approved", html)


def send_officer_approved_email(to_email, name, department_name=None):
    dept_line = f" and assigned to the <strong>{department_name}</strong> department" if department_name else ""
    html = _render(
        preheader="Your officer account has been approved",
        heading="Account Approved ✅",
        body_html=f"""
            <p>Hi {name},</p>
            <p>Your CivicDesk officer account has been approved{dept_line}.</p>
            <p>You can now log in to manage complaints and workers.</p>
        """,
        cta_text="Log In",
        cta_url=f"{FRONTEND_URL}/login",
    )
    return send_email(to_email, "Your CivicDesk Account Has Been Approved", html)


def send_account_rejected_email(to_email, name, role, reason=None):
    reason_html = f'<p><strong>Reason:</strong> {reason}</p>' if reason else ""
    html = _render(
        preheader="Update on your CivicDesk registration",
        heading="Registration Not Approved",
        body_html=f"""
            <p>Hi {name},</p>
            <p>Your CivicDesk {role.lower()} registration was not approved at this time.</p>
            {reason_html}
            <p>If you believe this is a mistake, you're welcome to register again or contact support.</p>
        """,
    )
    return send_email(to_email, "CivicDesk Registration Update", html)


def send_account_status_changed_email(to_email, name, new_status, reason=None):
    """Suspended / reactivated."""
    is_suspended = new_status == "suspended"
    reason_html = f'<p><strong>Reason:</strong> {reason}</p>' if (reason and is_suspended) else ""
    html = _render(
        preheader=f"Your account has been {new_status}",
        heading=f"Account {'Suspended' if is_suspended else 'Reactivated'}",
        body_html=f"""
            <p>Hi {name},</p>
            <p>Your CivicDesk account has been
               <strong>{'suspended' if is_suspended else 'reactivated'}</strong>.</p>
            {reason_html}
            <p>{"You won't be able to log in or receive new assignments until this is resolved." if is_suspended else "You can log in and resume normal activity right away."}</p>
        """,
    )
    return send_email(to_email, f"CivicDesk Account {'Suspended' if is_suspended else 'Reactivated'}", html)


def send_officer_transferred_email(to_email, name, old_department_name, new_department_name):
    html = _render(
        preheader="Your department assignment has changed",
        heading="Department Transfer",
        body_html=f"""
            <p>Hi {name},</p>
            <p>You've been transferred from <strong>{old_department_name}</strong> to
               <strong>{new_department_name}</strong>.</p>
        """,
        cta_text="View Dashboard",
        cta_url=f"{FRONTEND_URL}/officer/dashboard",
    )
    return send_email(to_email, f"You've Been Transferred to {new_department_name}", html)


def send_password_reset_email(to_email, name, reset_token):
    reset_url = f"{FRONTEND_URL}/reset-password?token={reset_token}"
    html = _render(
        preheader="Reset your CivicDesk password",
        heading="Reset Your Password",
        body_html=f"""
            <p>Hi {name},</p>
            <p>We received a request to reset your CivicDesk password. Click the button below to
               choose a new one. This link expires in 1 hour.</p>
        """,
        cta_text="Reset Password",
        cta_url=reset_url,
        footnote="If you didn't request this, you can safely ignore this email — your password won't change.",
    )
    return send_email(to_email, "Reset Your CivicDesk Password", html)


def send_password_reset_otp_email(to_email, name, otp):
    """CivicDesk's actual reset flow uses a 6-digit OTP, not a link."""
    html = _render(
        preheader="Your CivicDesk password reset code",
        heading="Password Reset Code",
        body_html=f"""
            <p>Hi {name},</p>
            <p>Use the code below to reset your CivicDesk password. It expires in
               <strong>10 minutes</strong>.</p>
            <p style="text-align:center; margin:24px 0;">
              <span style="display:inline-block; font-size:32px; font-weight:800; letter-spacing:8px;
                           color:#0f172a; background:#f1f5f9; padding:14px 24px; border-radius:10px;">
                {otp}
              </span>
            </p>
        """,
        footnote="If you didn't request this, you can safely ignore this email — your password won't change.",
    )
    return send_email(to_email, f"Your CivicDesk Password Reset Code: {otp}", html)


def send_password_changed_email(to_email, name):
    html = _render(
        preheader="Your password was changed",
        heading="Password Changed",
        body_html=f"""
            <p>Hi {name},</p>
            <p>This is a confirmation that your CivicDesk password was just changed.</p>
        """,
        footnote="If you didn't make this change, please contact support immediately.",
    )
    return send_email(to_email, "Your CivicDesk Password Was Changed", html)


# ─────────────────────────────────────────────────────────────────────────
# Complaint lifecycle
# ─────────────────────────────────────────────────────────────────────────
def send_complaint_submitted_email(to_email, name, complaint_id, title, category):
    html = _render(
        preheader=f"Complaint {complaint_id} received",
        heading="Complaint Submitted",
        body_html=f"""
            <p>Hi {name},</p>
            <p>Your complaint has been received and logged in our system.</p>
            <table style="width:100%; margin-top:12px; font-size:14px;">
              <tr><td style="color:#64748b; padding:4px 0;">Complaint ID</td><td style="font-weight:700;">{complaint_id}</td></tr>
              <tr><td style="color:#64748b; padding:4px 0;">Title</td><td>{title}</td></tr>
              <tr><td style="color:#64748b; padding:4px 0;">Category</td><td>{category}</td></tr>
            </table>
            <p style="margin-top:16px;">We'll notify you as it progresses.</p>
        """,
        cta_text="Track Complaint",
        cta_url=f"{FRONTEND_URL}/citizen/track/{complaint_id}",
    )
    return send_email(to_email, f"Complaint {complaint_id} Submitted", html)


def send_complaint_assigned_email(to_email, name, complaint_id, title, department_name):
    html = _render(
        preheader=f"Complaint {complaint_id} assigned",
        heading="Your Complaint Is Being Handled",
        body_html=f"""
            <p>Hi {name},</p>
            <p>Your complaint <strong>{title}</strong> ({complaint_id}) has been assigned to the
               <strong>{department_name}</strong> department for action.</p>
        """,
        cta_text="View Details",
        cta_url=f"{FRONTEND_URL}/citizen/track/{complaint_id}",
    )
    return send_email(to_email, f"Complaint {complaint_id} Assigned", html)


def send_complaint_status_updated_email(to_email, name, complaint_id, title, new_status, remark=None):
    remark_html = f'<p style="margin-top:12px; padding:12px; background:#f8fafc; border-radius:8px; font-style:italic;">"{remark}"</p>' if remark else ""
    html = _render(
        preheader=f"Complaint {complaint_id} status update",
        heading="Status Update",
        body_html=f"""
            <p>Hi {name},</p>
            <p>Your complaint <strong>{title}</strong> ({complaint_id}) is now
               <strong>{new_status}</strong>.</p>
            {remark_html}
        """,
        cta_text="View Details",
        cta_url=f"{FRONTEND_URL}/citizen/track/{complaint_id}",
    )
    return send_email(to_email, f"Complaint {complaint_id}: {new_status}", html)


def send_complaint_resolved_email(to_email, name, complaint_id, title):
    html = _render(
        preheader=f"Complaint {complaint_id} resolved",
        heading="Complaint Resolved ✅",
        body_html=f"""
            <p>Hi {name},</p>
            <p>Good news — your complaint <strong>{title}</strong> ({complaint_id}) has been marked
               as <strong>Resolved</strong>.</p>
            <p>We'd appreciate a moment of your time to share feedback on how it was handled.</p>
        """,
        cta_text="Leave Feedback",
        cta_url=f"{FRONTEND_URL}/citizen/feedback/{complaint_id}",
    )
    return send_email(to_email, f"Complaint {complaint_id} Resolved", html)


def send_worker_task_assigned_email(to_email, worker_name, complaint_id, title, priority, area):
    html = _render(
        preheader=f"New task assigned: {complaint_id}",
        heading="New Task Assigned",
        body_html=f"""
            <p>Hi {worker_name},</p>
            <p>You've been assigned a new task:</p>
            <table style="width:100%; margin-top:12px; font-size:14px;">
              <tr><td style="color:#64748b; padding:4px 0;">Complaint ID</td><td style="font-weight:700;">{complaint_id}</td></tr>
              <tr><td style="color:#64748b; padding:4px 0;">Title</td><td>{title}</td></tr>
              <tr><td style="color:#64748b; padding:4px 0;">Priority</td><td>{priority}</td></tr>
              <tr><td style="color:#64748b; padding:4px 0;">Area</td><td>{area}</td></tr>
            </table>
        """,
        cta_text="View Task",
        cta_url=f"{FRONTEND_URL}/worker/task/{complaint_id}",
    )
    return send_email(to_email, f"New Task Assigned: {complaint_id}", html)


# ─────────────────────────────────────────────────────────────────────────
# Department applications
# ─────────────────────────────────────────────────────────────────────────
def send_department_application_approved_email(to_email, worker_name, department_name):
    html = _render(
        preheader="Your department application was approved",
        heading="Department Transfer Approved",
        body_html=f"""
            <p>Hi {worker_name},</p>
            <p>Your application to join <strong>{department_name}</strong> has been approved.
               You're now part of this department.</p>
        """,
        cta_text="View Profile",
        cta_url=f"{FRONTEND_URL}/worker/profile",
    )
    return send_email(to_email, f"Approved: Transfer to {department_name}", html)


def send_department_application_rejected_email(to_email, worker_name, department_name, remark=None):
    remark_html = f'<p><strong>Reason:</strong> {remark}</p>' if remark else ""
    html = _render(
        preheader="Update on your department application",
        heading="Department Transfer Not Approved",
        body_html=f"""
            <p>Hi {worker_name},</p>
            <p>Your application to join <strong>{department_name}</strong> was not approved.</p>
            {remark_html}
        """,
        cta_text="View Departments",
        cta_url=f"{FRONTEND_URL}/worker/departmentapplications",
    )
    return send_email(to_email, f"Update: Transfer to {department_name}", html)


# ─────────────────────────────────────────────────────────────────────────
# Contact form & announcements
# ─────────────────────────────────────────────────────────────────────────
def send_contact_ack_email(to_email, name, subject):
    html = _render(
        preheader="We received your message",
        heading="We've Got Your Message",
        body_html=f"""
            <p>Hi {name},</p>
            <p>Thanks for reaching out — we've received your message
               "<strong>{subject}</strong>" and will get back to you shortly.</p>
        """,
    )
    return send_email(to_email, "We Received Your Message — CivicDesk", html)


def send_announcement_email(to_email, name, announcement_title, announcement_body):
    html = _render(
        preheader=announcement_title,
        heading=announcement_title,
        body_html=f"<p>Hi {name},</p><p>{announcement_body}</p>",
        cta_text="View Announcements",
        cta_url=f"{FRONTEND_URL}/announcements",
    )
    return send_email(to_email, f"CivicDesk Announcement: {announcement_title}", html)