# CivicDesk Frontend Guide

This document explains how to run the CivicDesk Vue.js frontend locally and provides a complete list of all available application routes.

---

# Prerequisites

Before running the project, make sure you have the following installed:

- Node.js (Latest LTS version recommended)
- npm (Comes with Node.js)

---

# Running the Frontend

### 1. Clone the repository (if you haven't already)

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Install dependencies

```bash
npm install
```

### 3. Start the development server

```bash
npm run dev
```

### 4. Open the application

After the development server starts, open the URL shown in your terminal.

Typically:

```
http://localhost:5173
```

---

# Application Routes

Below is the complete list of routes available in the CivicDesk frontend.

---

## Pages and Routes

### Public (no login required)
| Route | Page |
|---|---|
| `/` | Landing Page |
| `/about` | About CivicDesk |
| `/services` | Services |
| `/how-it-works` | How It Works |
| `/contact` | Contact Us |
| `/faq` | FAQs |

### Auth
| Route | Page |
|---|---|
| `/login` | Login |
| `/register` | Register |
| `/forgot-password` | Reset Password |

### Citizen (requires login)
| Route | Page |
|---|---|
| `/citizen/dashboard` | Dashboard |
| `/citizen/complaints` | My Complaints |
| `/citizen/submit` | Submit Complaint |
| `/citizen/complaintdetails/:id` | Complaint Details |
| `/citizen/track/:id` | Track Complaint |
| `/citizen/feedback/:id` | Submit Feedback |
| `/citizen/notifications` | Notifications |
| `/citizen/profile` | Profile |

### Officer (requires login)
| Route | Page |
|---|---|
| `/officer/dashboard` | Officer Dashboard |
| `/officer/complaints` | Complaint Management |
| `/officer/complaintdetails/:id` | Complaint Details |
| `/officer/workers` | Manage Workers |
| `/officer/assign/:id` | Assign Worker |
| `/officer/analytics` | Analytics & Reports |
| `/officer/notifications` | Notifications |
| `/officer/profile` | Profile |

### Worker (requires login)
| Route | Page |
|---|---|
| `/worker/dashboard` | Worker Dashboard |
| `/worker/tasks` | Assigned Tasks |
| `/worker/task/:id` | Task Details |
| `/worker/update/:id` | Update Complaint |
| `/worker/completed` | Completed Tasks |
| `/worker/notifications` | Notifications |
| `/worker/profile` | Profile |
| `/worker/departmentapplications` | Department Applications |

### Admin (requires login)
| Route | Page |
|---|---|
| `/admin/dashboard` | Admin Dashboard |
| `/admin/departmentmanagement` | Department Management |
| `/admin/officerdetails` | Officer Details |
| `/admin/officermanagement` | Officer Management |
| `/admin/profile` | Profile |
| `/admin/systemanalytics` | System Analytics |
| `/admin/activitylogs` | Activity Logs |
| `/admin/announcements` | Announcements |
