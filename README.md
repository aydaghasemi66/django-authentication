# django-authentication
 
# Mentor — Online Course Platform (Django + DRF)

A full-stack online course platform built with Django, Django REST Framework, and PostgreSQL, fully containerized with Docker. The frontend is powered by the [Mentor Bootstrap template](https://bootstrapmade.com/mentor-free-education-bootstrap-theme/), served through Django templates and backed by real, dynamic data from the API.

Built as a portfolio project to demonstrate backend architecture, REST API design, authentication, and Docker-based deployment.

## Features

- **Custom user model** with email-based authentication (no username required)
- **Two-step registration flow**: create account → complete profile (choose Student or Trainer role)
- **Dual authentication**: JWT for the REST API, session-based auth for the server-rendered frontend
- **Role-based profiles**: `TrainerProfile` and `StudentProfile`, each with role-specific fields
- **Course management**: categories, courses, view/like counters, comments with nested replies
- **Shopping cart & checkout**: add courses to a cart, check out, and get automatically enrolled
- **Custom permissions**: e.g. only trainers can create courses, only the course owner can edit it, users must complete their profile before certain actions
- **Automated tests**: 27+ tests across all apps using `pytest-django`, including regression tests for real bugs found during development
- **Environment-based configuration**: all secrets (`SECRET_KEY`, database credentials) are read from environment variables, never hardcoded
- **Dockerized**: one command spins up the app and a PostgreSQL database together

## Tech Stack

| Layer          | Technology                                  |
|----------------|----------------------------------------------|
| Backend        | Django 5.2, Django REST Framework            |
| Auth           | `djangorestframework-simplejwt` (API), Django sessions (web) |
| Database       | PostgreSQL 16                                |
| Containerization | Docker, Docker Compose                     |
| Testing        | pytest, pytest-django                        |
| Frontend       | Django Templates + Bootstrap 5 (Mentor theme)|

## Project Structure

```
├── config/            # Project settings, root URLs
├── accounts/          # Custom User model, Trainer/Student profiles, auth (API + web)
├── courses/           # Categories, Courses, Comments, Replies
├── order/             # Cart, Orders, Enrollments
├── templates/         # Django templates (Mentor theme, adapted)
├── static/            # Static assets (CSS, JS, images)
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Data Model Overview

```
User (custom, email login)
 ├── TrainerProfile (1:1) ── Course (1:N) ── Comment (1:N) ── Reply (1:N)
 └── StudentProfile (1:1) ── Order (1:N) ── OrderItem (N:1 Course)
                          └── Enrollment (N:1 Course)
```

## Getting Started

### Prerequisites

- Docker & Docker Compose

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/aydaghasemi66/django-authentication.git
   cd django-authentication
   ```

2. Copy the example environment file and fill in your own values:
   ```bash
   cp .env.example .env
   ```

3. Build and start the containers:
   ```bash
   docker compose up --build
   ```

4. In a separate terminal, run migrations and create a superuser:
   ```bash
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py createsuperuser
   ```

5. Visit the app:
   - Website: [http://localhost:8000/](http://localhost:8000/)
   - Admin panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)
   - API root: [http://localhost:8000/api/](http://localhost:8000/api/)

### Running Tests

```bash
docker compose exec web pytest -v
```

## API Overview

| Endpoint                              | Method | Description                              |
|----------------------------------------|--------|-------------------------------------------|
| `/api/auth/register/`                  | POST   | Step 1: create account (email + password) |
| `/api/auth/login/`                     | POST   | Get JWT access & refresh tokens           |
| `/api/auth/complete-profile/`          | PATCH  | Step 2: name, photo, role                 |
| `/api/auth/me/`                        | GET    | Current user + profile completeness       |
| `/api/courses/`                        | GET/POST | List / create courses                   |
| `/api/courses/<slug>/`                 | GET/PATCH/DELETE | Course detail / edit / delete    |
| `/api/courses/<slug>/comments/`        | POST   | Leave a comment on a course               |
| `/api/orders/`                         | GET    | List my orders                            |
| `/api/orders/add-item/`                | POST   | Add a course to the cart                  |
| `/api/orders/<id>/checkout/`           | POST   | Complete an order                         |
| `/api/orders/my-enrollments/`          | GET    | List my enrolled courses                  |

## Notable Design Decisions

- **Email as the login identifier** instead of username — simpler for users, standard for modern SaaS apps.
- **`price_at_purchase` stored on `OrderItem`** rather than referencing `Course.price` directly, so historical orders aren't affected if a course's price changes later.
- **`on_delete=PROTECT`** on `OrderItem.course` to prevent deleting a course that has been purchased, preserving financial history.
- **JWT for the API, sessions for the website** — each authentication method is used where it fits best, rather than forcing one approach everywhere.

## Roadmap / Not Yet Implemented

- Real payment gateway integration (currently checkout is simulated)
- Email verification on signup
- Full test coverage for the `order` app's web views

## Credits

Frontend template: [Mentor by BootstrapMade](https://bootstrapmade.com/mentor-free-education-bootstrap-theme/) (used under its free license).