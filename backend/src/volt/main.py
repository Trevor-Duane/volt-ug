from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from volt.db.session import engine

app = FastAPI(title="Volt API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to Volt API"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
def database_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"status": "ok", "database": "voltdb"}

    except SQLAlchemyError:
        return {
            "status": "error",
            "database": "voltdb",
            "message": "Database connection failed",
        }
