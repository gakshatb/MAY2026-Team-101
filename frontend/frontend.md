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

## Public Pages

| Page | Route |
|------|-------|
| Home | `/` |
| About | `/about` |
| Services | `/services` |
| How It Works | `/how-it-works` |
| Contact Us | `/contact` |
| FAQs | `/faq` |

---

## Authentication

| Page | Route |
|------|-------|
| Login | `/login` |
| Register | `/register` |
| Forgot Password | `/forgot-password` |

---

## Citizen Portal

| Page | Route |
|------|-------|
| Dashboard | `/citizen/dashboard` |
| My Complaints | `/citizen/complaints` |
| Submit Complaint | `/citizen/submit` |
| Complaint Details | `/citizen/details/:id` |
| Track Complaint | `/citizen/track/:id` |
| Provide Feedback | `/citizen/feedback/:id` |
| Notifications | `/citizen/notifications` |
| Profile | `/citizen/profile` |

> **Note:** Replace `:id` with the appropriate complaint ID.

---

## Officer Portal

| Page | Route |
|------|-------|
| Dashboard | `/officer/dashboard` |
| Complaint Management | `/officer/complaints` |
| Complaint Details | `/officer/details/:id` |
| Manage Workers | `/officer/workers` |
| Assign Worker | `/officer/assign/:id` |
| Analytics & Reports | `/officer/analytics` |
| Notifications | `/officer/notifications` |
| Profile | `/officer/profile` |

> **Note:** Replace `:id` with the appropriate complaint or task ID.

---

## Field Worker Portal

| Page | Route |
|------|-------|
| Dashboard | `/worker/dashboard` |
| Assigned Tasks | `/worker/tasks` |
| Task Details | `/worker/task/:id` |
| Update Complaint | `/worker/update/:id` |
| Completed Tasks | `/worker/completed` |
| Notifications | `/worker/notifications` |
| Profile | `/worker/profile` |

> **Note:** Replace `:id` with the appropriate task ID.

---
