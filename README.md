# Trekking Management Application

A full-stack role-based platform for managing trekking operations, bookings, staff assignments, and automated communication workflows.

## Overview

The Trekking Management Application is designed around three user roles: **Admin**, **Staff**, and **Trekker**. It provides separate workflows for trek management, user administration, booking operations, staff assignment, dashboards, and scheduled background tasks.

The project combines a Vue frontend with a Flask REST API backend and uses Redis and Celery for caching and asynchronous processing.

## Key Features

### Authentication & Access Control
- User registration and login
- JWT-based authentication
- Role-based authorization for Admin, Staff, and Trekker users
- Account blocking through active/inactive status
- Password hashing using Werkzeug

### Admin
- Create, view, update, and delete treks
- Manage trekkers and staff
- Assign staff members to treks
- View booking information
- Dashboard counts for treks, trekkers, staff, and bookings
- Block user accounts when required

### Trekker
- Register and maintain profile information
- Browse and book treks
- Track booking status
- Export booking history through an asynchronous background task

### Background Processing
- Daily reminder emails for trekkers whose trek starts the following day
- Automated monthly activity report for the administrator
- CSV booking-history export
- Celery worker and Celery Beat integration

### Performance
- Redis-backed application caching
- Cached dashboard and listing endpoints
- Cache invalidation after write operations

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vue 3, Vue Router, Axios, Bootstrap 5, Vite |
| Backend | Python, Flask, REST APIs |
| Authentication | Flask-JWT-Extended |
| Database | SQLite, SQLAlchemy |
| Caching | Redis, Flask-Caching |
| Background Jobs | Celery, Celery Beat |
| Email | Flask-Mail |

## Architecture

```text
                    ┌────────────────────┐
                    │     Vue 3 UI       │
                    │  Router + Axios    │
                    └─────────┬──────────┘
                              │ HTTP / JSON
                              ▼
                    ┌────────────────────┐
                    │    Flask REST API  │
                    │ JWT + Role Checks  │
                    └──────┬──────┬──────┘
                           │      │
                  ┌────────┘      └────────┐
                  ▼                        ▼
          ┌───────────────┐        ┌───────────────┐
          │ SQLite / ORM  │        │ Redis         │
          │ SQLAlchemy    │        │ Cache/Broker  │
          └───────────────┘        └───────┬───────┘
                                           │
                                           ▼
                                   ┌───────────────┐
                                   │ Celery Worker │
                                   │ + Celery Beat │
                                   └───────┬───────┘
                                           │
                                           ▼
                                   Email / CSV Tasks
```

## Data Model

The main entities are:

- **User** — authentication, role, account status
- **UserProfile** — personal profile information
- **Trek** — trek details, dates, difficulty, slots, and status
- **Booking** — connects trekkers with treks and stores booking status
- **StaffAssignment** — connects staff members with assigned treks

Database constraints prevent duplicate trek bookings for the same user and duplicate staff assignments for the same trek.

## Project Structure

```text
Trekking-Management-Application/
├── backend/
│   ├── application/
│   │   ├── __init__.py
│   │   ├── cache.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── email_utils.py
│   │   ├── models.py
│   │   └── tasks.py
│   ├── app.py
│   ├── celery_worker.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── router/
│   │   ├── services/
│   │   ├── views/
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

## Running Locally

### Prerequisites

Make sure you have:

- Python 3
- Node.js and npm
- Redis

### 1. Clone the repository

```bash
git clone https://github.com/harishgit0/Trekking-Management-Application.git
cd Trekking-Management-Application
```

### 2. Backend setup

```bash
python -m venv venv
```

Activate the environment and install dependencies:

```bash
pip install -r backend/requirements.txt
```

Create a `.env` file using `.env.example` as a reference and provide your own credentials/secrets.

Run Redis, then start the backend:

```bash
cd backend
python app.py
```

### 3. Celery worker

From the `backend` directory:

```bash
celery -A celery_worker.celery worker --loglevel=info
```

For scheduled tasks, run Celery Beat in another terminal:

```bash
celery -A celery_worker.celery beat --loglevel=info
```

### 4. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

## Security Notes

- Secrets and credentials are loaded through environment variables and should never be committed to source control.
- Passwords are stored as hashes rather than plaintext.
- Protected endpoints use JWT authentication and role checks.

## What This Project Demonstrates

This project demonstrates practical experience with:

- End-to-end full-stack application development
- REST API design
- Role-based access control
- Relational data modelling
- Asynchronous task processing
- Redis caching
- Automated email workflows
- Frontend/backend integration

## Author

**Harish Chauhan**  
BS Data Science & Applications, IIT Madras
