# Expense Tracker API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

A secure REST API for expense tracking with JWT authentication, built with FastAPI and PostgreSQL.
```bash
.
├── alembic/       # Database migrations
├── models.py         # Database models
├── schema.py         # Pydantic schemas
├── main.py           # FastAPI application
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── alembic.ini
```

## Features

- User registration and authentication
- JWT token-based security
- Expense creation, tracking, and management
- Automatic database migrations with Alembic
- Docker containerization
- PostgreSQL database
- Pydantic data validation

## Technologies

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT
- **Containerization**: Docker
- **Migrations**: Alembic

## Prerequisites

- Python 3.12+
- Docker and Docker Compose
- PostgreSQL client (optional)

## Setup & Installation

### 1. Clone Repository
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker


Local Development Setup
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file (modify values as needed)
cp .env.example .env

# Initialize database
alembic upgrade head

# Run application
uvicorn main:app --reload

# Build and start containers
docker-compose up --build

# Apply database migrations
docker-compose exec app alembic upgrade head

Create .env file with these variables:

- DATABASE_URL=postgresql://postgres:password@db:5432/expense_tracker
- SECRET_KEY=your-secret-key-here
- DB_USER=postgres
- DB_PASSWORD=password
- DB_NAME=expense_tracker
- PGADMIN_EMAIL=admin@admin.com
- PGADMIN_PASSWORD=admin

Alembic Commands

Create new migration in bash:
alembic revision --autogenerate -m "description"

Apply migrations:
alembic upgrade head

In Docker:
docker-compose exec app alembic upgrade head

## API Endpoints

### Authentication
| Method | Endpoint    | Description          |
|--------|-------------|----------------------|
| POST   | `/register/` | User registration    |
| POST   | `/login/`    | Get JWT access token |

### Users
| Method | Endpoint       | Description          |
|--------|----------------|----------------------|
| GET    | `/users/me/`   | Get current user     |

### Expenses
| Method | Endpoint       | Description          |
|--------|----------------|----------------------|
| POST   | `/expenses/`   | Create new expense   |
| GET    | `/expenses/`   | List all expenses    |

---

## Running Tests

Example using curl:
```bash
# Register user
curl -X POST -H "Content-Type: application/json" -d '{"username":"test","email":"test@example.com","password":"testpass"}' http://localhost:8000/register/

# Login
curl -X POST -H "Content-Type: application/json" -d '{"username":"test","password":"testpass"}' http://localhost:8000/login/

# Create expense (replace TOKEN with JWT)
curl -X POST -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" -d '{"description":"Groceries","amount":75.50,"category":"food","expense_date":"2023-08-15T12:00:00"}' http://localhost:8000/expenses/

Database Access

   - PGAdmin: http://localhost:5050

   - PostgreSQL Direct:
-in bash
    - psql -h localhost -U postgres -d expense_tracker

