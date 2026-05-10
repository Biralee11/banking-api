# Banking API

A REST API built with FastAPI that exposes core banking operations including account creation, deposits, withdrawals, transfers, and account management. Account data is persisted in a PostgreSQL database with JWT-based authentication and role-based access control.

This project is the API layer built on top of the [Banking CLI App](https://github.com/Biralee11/banking-app), reusing the same account logic and extending it with a proper HTTP interface.

## Tech Stack

- Python 3.14
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL
- Docker
- JWT Authentication

## Running with Docker (Recommended)

Make sure Docker Desktop is running, then:

```bash
docker-compose up --build -d
```

The API will be available at `http://127.0.0.1:8000`

Interactive API documentation is available at `http://127.0.0.1:8000/docs`

To stop the containers:

```bash
docker-compose down
```

## Running Locally (Without Docker)

Clone the repository and navigate into the project folder.

```bash
git clone https://github.com/Biralee11/banking-api.git
cd banking-api
```

Create and activate a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root with the following:

```
SECRET_KEY=your_secret_key_here
```

Generate a secret key with:

```bash
openssl rand -hex 32
```

Run database migrations.

```bash
alembic upgrade head
```

Start the server.

```bash
uvicorn main:app --reload
```

## Authentication

The API uses JWT bearer token authentication. To access protected endpoints:

1. Register a user via `POST /auth/register`
2. Log in via `POST /auth/login` to receive a token
3. Include the token in the `Authorization` header as `Bearer <token>`

## Roles

- **User** — can create accounts, manage their own accounts, and deposit into any account
- **Admin** — has full access to all accounts and operations

## Endpoints

### Auth
| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | /auth/register | Public | Register a new user |
| POST | /auth/login | Public | Login and receive a JWT token |

### User Profile
| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | /user/me | Owner | View your profile |
| PUT | /user/me | Owner | Update your email |
| PUT | /user/me/password | Owner | Change your password |

### Accounts
| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | / | Public | Health check |
| POST | /accounts/savings | Authenticated | Create a savings account |
| POST | /accounts/current | Authenticated | Create a current account |
| GET | /accounts | Admin only | View all accounts |
| GET | /accounts/{account_number} | Owner or Admin | View a single account |
| POST | /accounts/{account_number}/deposit | Public | Deposit funds |
| POST | /accounts/{account_number}/withdraw | Owner or Admin | Withdraw funds |
| POST | /transfer | Owner or Admin | Transfer between accounts |
| PUT | /accounts/{account_number} | Owner or Admin | Update account details |
| DELETE | /accounts/{account_number} | Owner or Admin | Close an account |

## Roadmap

- Deployment