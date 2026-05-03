# Banking API

A REST API built with FastAPI that exposes core banking operations including account creation, deposits, withdrawals, transfers, and account management.

This project is the API layer built on top of the [Banking CLI App](https://github.com/Biralee11/banking-app), reusing the same account logic and extending it with a proper HTTP interface.

## Tech Stack

- Python 3.14
- FastAPI
- Uvicorn
- Pydantic
- Docker

## Getting Started

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

Start the server.

```bash
uvicorn main:app --reload
```

The API will be running at `http://127.0.0.1:8000`

Interactive API documentation is available at `http://127.0.0.1:8000/docs`

## Docker

Build the image.

```bash
docker build -t banking-api .
```

Run the container.

```bash
docker run -p 8000:8000 banking-api
```

The API will be available at `http://127.0.0.1:8000`

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

## Data Persistence

Account data is currently held in memory. Data does not persist between server restarts. A PostgreSQL database integration is planned for a future release.

## Roadmap

- PostgreSQL database integration
- Docker containerisation and deployment ✅
- Authentication and authorisation