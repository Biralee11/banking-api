# Banking API

A REST API built with FastAPI that exposes core banking operations including account creation, deposits, withdrawals, transfers, and account management. Account data is persisted in a PostgreSQL database.

This project is the API layer built on top of the [Banking CLI App](https://github.com/Biralee11/banking-app), reusing the same account logic and extending it with a proper HTTP interface.

## Tech Stack

- Python 3.14
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- PostgreSQL
- Alembic
- Docker

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

Run database migrations.

```bash
alembic upgrade head
```

Start the server.

```bash
uvicorn main:app --reload
```

The API will be running at `http://127.0.0.1:8000`

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Health check |
| POST | /accounts/savings | Create a savings account |
| POST | /accounts/current | Create a current account |
| GET | /accounts | View all accounts |
| GET | /accounts/{account_number} | View a single account |
| POST | /accounts/{account_number}/deposit | Deposit funds |
| POST | /accounts/{account_number}/withdraw | Withdraw funds |
| POST | /transfer | Transfer between accounts |
| PUT | /accounts/{account_number} | Update account details |
| DELETE | /accounts/{account_number} | Close an account |

## Roadmap

- Authentication and authorisation
- Deployment