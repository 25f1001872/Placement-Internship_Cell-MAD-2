# 🎓 Placement Portal Application V2 (PPA-V2)

> A role-based, full-stack web application that modernizes the campus recruitment process — built as a Vue.js SPA frontend with a RESTful Flask backend, Redis caching, and Celery background jobs.

<br>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Caching-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-Background_Jobs-37814A?style=for-the-badge)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Core Features](#-core-features)
- [Database Design](#-database-design)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Setup & Installation](#-setup--installation)
- [Running the Application](#-running-the-application)
- [Default Admin Credentials](#-default-admin-credentials)
- [API Endpoints](#-api-endpoints)
- [Academic Note](#-academic-note)

---

## 🧠 Overview

**PPA-V2** is the upgraded version of the MAD-I Placement Portal, migrated from a Flask/Jinja2 monolithic app to a modern decoupled architecture. The backend exposes a RESTful API consumed by a Vue.js SPA frontend. Redis handles both caching and as a message broker for Celery async jobs.

The system supports three distinct user roles:

| Role | Description |
|------|-------------|
| 🏛️ **Admin** | Institute authority — manages users, approvals, blacklisting, and system oversight |
| 🏢 **Company** | Recruiter — posts drives, reviews applicants, manages application pipeline |
| 🎓 **Student** | Job seeker — browses drives, applies, and tracks application status |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, Flask (REST API) |
| **Frontend** | Vue.js 3 (SPA via Vite), Bootstrap 5 |
| **Database** | SQLite via Flask-SQLAlchemy |
| **Authentication** | Flask-JWT-Extended (JWT tokens) |
| **Caching** | Redis (Memurai on Windows) |
| **Background Jobs** | Celery + Redis |
| **Email** | Flask-Mail (Gmail SMTP) |
| **HTTP Client** | Axios |
| **Routing** | Vue Router |

---

## 🧩 Core Features

### 🔐 Authentication & Authorization
- JWT-based stateless authentication — no server-side sessions
- Role-based redirection after login (Admin / Company / Student)
- Admin pre-seeded on first run — no public registration for Admin
- Company registration requires Admin approval before access
- Route guards on Vue Router — unauthorized access redirected to login

### 👨‍💼 Admin Panel
- Dashboard with live stats: total students, companies, drives, applications
- Approve / Reject company registrations and placement drives
- Search companies by name or industry
- Search students by name, ID, or contact
- Blacklist / Unblacklist companies and students
- View detailed profiles with application history

### 🏢 Company Panel
- Register company profile (pending Admin approval)
- Create placement drives with title, description, skills, salary, benefits, deadline
- View applicants per drive with status management
- Full application pipeline: Applied → Shortlisted → Interview → Offer → Rejected → Placed
- Export application history as CSV

### 🎓 Student Panel
- Register, login, update profile (education, skills, experience, contact)
- Browse and search approved active drives (by company, position, skills)
- Apply to drives — duplicate applications strictly prevented
- Track real-time application status through full pipeline
- View complete application history
- Export application history as CSV

### ⚙️ Background Jobs (Celery + Redis)
- **Interview Reminder**: Daily job — emails students with Interview status
- **Monthly Report**: 1st of every month — emails HTML report to each company
- **CSV Export**: User-triggered async export of application history
- Celery Beat handles scheduled job execution

### 🚀 Caching (Redis)
- Job listings (`/api/student/drives`) cached with 5-minute TTL
- Company search (`/api/admin/companies`) cached
- Student search (`/api/admin/students`) cached
- Cache invalidated on mutations (new drive, company approval)

---

## 🗄 Database Design

### Models & Fields

```
User                          [users]
├── id (PK, autoincrement)
├── name
├── email (unique)
├── password_hash
├── role                      # "admin" | "company" | "student"
├── is_active
└── created_at

StudentProfile                [student_profiles]
├── id (PK)
├── user_id (FK → users.id, unique)
├── education
├── skills
├── experience
├── contact
├── resume_path
├── is_blacklisted
└── created_at

CompanyProfile                [company_profiles]
├── id (PK)
├── user_id (FK → users.id, unique)
├── company_description
├── industry
├── location
├── website
├── approval_status           # "Pending" | "Approved" | "Rejected"
├── is_blacklisted
└── created_at

PlacementDrive                [placement_drives]
├── id (PK)
├── company_id (FK → company_profiles.id)
├── job_title
├── job_description
├── skills_required
├── eligibility
├── salary
├── benefits
├── deadline
├── status                    # "Active" | "Closed"
├── approval_status           # "Pending" | "Approved" | "Rejected"
└── created_at

Application                   [applications]
├── id (PK)
├── student_id (FK → student_profiles.id)
├── drive_id (FK → placement_drives.id)
├── status                    # "Applied" | "Shortlisted" | "Interview" | "Offer" | "Rejected" | "Placed"
├── applied_at
└── UNIQUE CONSTRAINT on (student_id, drive_id)

Placement                     [placements]
├── id (PK)
├── student_id (FK → student_profiles.id)
├── company_id (FK → company_profiles.id)
├── drive_id (FK → placement_drives.id)
├── salary
├── joining_date
└── created_at
```

### Relationships

```
User            ──1  StudentProfile
User            ──1  CompanyProfile
CompanyProfile  ──<  PlacementDrive
StudentProfile  ──<  Application
PlacementDrive  ──<  Application
Application     ──1  Placement      (created when status = "Placed")
```

---

## 📁 Project Structure

```
Placement-Internship_Cell-MAD-2/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py              # App factory — Flask, db, jwt, mail, celery, blueprints
│   │   ├── config.py                # Configuration — DB, JWT, Redis, Mail
│   │   ├── extensions.py            # db, jwt, mail, celery instances
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── student.py
│   │   │   ├── company.py
│   │   │   ├── placement_drive.py
│   │   │   ├── application.py
│   │   │   └── placement.py
│   │   │
│   │   ├── routes/
│   │   │   ├── auth_routes.py       # Login, register student/company
│   │   │   ├── admin_routes.py      # Admin dashboard, approvals, blacklisting
│   │   │   ├── company_routes.py    # Company dashboard, drives, applicants
│   │   │   ├── student_routes.py    # Student dashboard, drives, applications
│   │   │   └── tasks_routes.py      # Celery task triggers, CSV export
│   │   │
│   │   ├── tasks/
│   │   │   ├── __init__.py
│   │   │   └── jobs.py              # Celery tasks — reminders, reports, CSV
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── cache.py             # Redis cache helpers
│   │
│   ├── instance/
│   │   └── placement.db             # Auto-generated SQLite database
│   │
│   ├── celery_worker.py             # Celery worker entry point
│   ├── run.py                       # Flask application entry point
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   │   └── logo.svg
│   ├── src/
│   │   ├── main.js                  # Vue app entry point
│   │   ├── App.vue                  # Root component with RouterView
│   │   ├── router/
│   │   │   └── index.js             # Vue Router with auth guards
│   │   ├── utils/
│   │   │   └── api.js               # Axios instance with JWT interceptor
│   │   └── views/
│   │       ├── HomePage.vue
│   │       ├── LoginPage.vue
│   │       ├── RegisterStudent.vue
│   │       ├── RegisterCompany.vue
│   │       ├── admin/
│   │       │   └── AdminDashboard.vue
│   │       ├── company/
│   │       │   ├── CompanyDashboard.vue
│   │       │   ├── CreateDrive.vue
│   │       │   └── DriveApplications.vue
│   │       └── student/
│   │           └── StudentDashboard.vue
│   ├── index.html
│   └── package.json
│
├── docs/
├── .gitignore
└── README.md
```

---

## ⚙️ Prerequisites

Make sure the following are installed before setup:

| Tool | Version | Notes |
|------|---------|-------|
| Python | 3.10+ | [python.org](https://python.org) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) |
| npm | 9+ | Comes with Node.js |
| Redis | Any | **Windows:** use [Memurai](https://www.memurai.com/get-memurai) |
| Git | Any | [git-scm.com](https://git-scm.com) |

---

## 🚀 Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/25f1001872/Placement-Internship_Cell-MAD-2.git
cd Placement-Internship_Cell-MAD-2
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate — Windows PowerShell
venv\Scripts\Activate.ps1

# Activate — macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Email (for background jobs)

Open `backend/app/config.py` and update:

```python
MAIL_USERNAME = "your_gmail@gmail.com"
MAIL_PASSWORD = "your_16_char_app_password"   # Gmail App Password — NOT your real password
MAIL_DEFAULT_SENDER = "your_gmail@gmail.com"
```

> To generate a Gmail App Password: Google Account → Security → 2-Step Verification → App Passwords → Generate

### 4. Frontend Setup

```bash
cd ../frontend
npm install
```

### 5. Start Redis

**Windows (Memurai):** Memurai runs as a Windows service and starts automatically after installation. Verify with:
```powershell
memurai-cli ping
# Expected output: PONG
```

**macOS/Linux:**
```bash
redis-server
```

---

## ▶️ Running the Application

You need **4 terminals** running simultaneously:

### Terminal 1 — Flask Backend

```bash
cd backend
# Activate venv first
python run.py
```

> Flask runs at `http://127.0.0.1:5000`
> On first run, `instance/placement.db` is created automatically and Admin is seeded.

### Terminal 2 — Vue Frontend

```bash
cd frontend
npm run dev
```

> Vue runs at `http://localhost:5173` — open this in your browser

### Terminal 3 — Celery Worker

```bash
cd backend
# Activate venv first
celery -A celery_worker.celery worker --loglevel=info --pool=solo
```

> `--pool=solo` is required on Windows

### Terminal 4 — Celery Beat (Scheduler)

```bash
cd backend
# Activate venv first
celery -A celery_worker.celery beat --loglevel=info
```

> Handles scheduled jobs — daily interview reminders and monthly placement reports

---

## 🔑 Default Admin Credentials

The Admin account is automatically seeded on first run:

| Field | Value |
|-------|-------|
| **Email** | `admin@gmail.com` |
| **Password** | `admin@2005` |

---

## 📡 API Endpoints

### Auth
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/login` | POST | Login for all roles, returns JWT token |
| `/api/auth/register/student` | POST | Student self-registration |
| `/api/auth/register/company` | POST | Company registration (pending approval) |

### Admin
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/admin/dashboard` | GET | System stats |
| `/api/admin/companies` | GET | List/search companies |
| `/api/admin/companies/:id/approve` | POST | Approve company |
| `/api/admin/companies/:id/reject` | POST | Reject company |
| `/api/admin/companies/:id/blacklist` | POST | Toggle blacklist |
| `/api/admin/students` | GET | List/search students |
| `/api/admin/students/:id/blacklist` | POST | Toggle blacklist |
| `/api/admin/drives` | GET | List all drives |
| `/api/admin/drives/:id/approve` | POST | Approve drive |
| `/api/admin/drives/:id/reject` | POST | Reject drive |
| `/api/admin/drives/:id/close` | POST | Close drive |
| `/api/admin/applications` | GET | List all applications |

### Company
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/company/dashboard` | GET | Company dashboard data |
| `/api/company/drives` | POST | Create placement drive |
| `/api/company/drives/:id/close` | POST | Close a drive |
| `/api/company/drives/:id/applications` | GET | View drive applicants |
| `/api/company/applications/:id` | GET | View single application |
| `/api/company/applications/:id/status` | POST | Update application status |
| `/api/company/students/:id` | GET | View student profile |

### Student
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/student/dashboard` | GET | Student dashboard data |
| `/api/student/drives` | GET | Browse approved drives (searchable) |
| `/api/student/drives/:id` | GET | Drive details |
| `/api/student/drives/:id/apply` | POST | Apply to drive |
| `/api/student/applications` | GET | Application history |
| `/api/student/profile` | GET | Get profile |
| `/api/student/profile` | PUT | Update profile |

### Tasks
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tasks/send-reminders` | POST | Trigger interview reminder emails (Admin) |
| `/api/tasks/monthly-report` | POST | Trigger monthly report emails (Admin) |
| `/api/tasks/export/student` | GET | Download applications CSV (Student) |
| `/api/tasks/export/company` | GET | Download applications CSV (Company) |
| `/api/tasks/status/:task_id` | GET | Check background task status |

---

## 🔄 Application Status Flow

```
Applied → Shortlisted → Interview → Offer → Placed
                    ↘              ↘
                     Rejected       Rejected
```

When status is set to `Placed`, a `Placement` record is automatically created in the database.

---

## 📜 Academic Note

This project was developed as part of the **Modern Application Development – II** course requirement at IIT Madras BS Degree program. It is a migration and upgrade of the MAD-I project into a modern decoupled full-stack architecture.

**Scope:** REST API Design · JWT Authentication · Vue.js SPA · Redis Caching · Celery Background Jobs · Email Notifications · Database Schema Design

---

## 👨‍💻 Developer

**Developed by:** Kshitiz Singh — Solo Developer, Full Stack
**GitHub:** [25f1001872](https://github.com/25f1001872)
**Course:** Modern Application Development II — IITM BS

---

<p align="center">
  <i>Built with ❤️ using Flask, Vue.js, Redis & Celery — Modern Application Development II</i>
</p>