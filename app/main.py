import logging
import os

import psycopg
from fastapi import FastAPI, HTTPException

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Developer Support Incident Lab",
    description="A support API for investigating technical incidents.",
    version="1.0.0",
)

DATABASE_URL = os.getenv("DATABASE_URL")


@app.get("/")
def root():
    return {
        "service": "Developer Support Incident Lab",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/tickets")
def get_tickets():
    try:
        with psycopg.connect(DATABASE_URL, connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, customer_name, issue, status
                    FROM support_tickets
                    ORDER BY id
                """)
                rows = cur.fetchall()

        return [
            {
                "id": row[0],
                "customer_name": row[1],
                "issue": row[2],
                "status": row[3],
            }
            for row in rows
        ]

    except psycopg.Error:
        logger.exception("Database error in GET /tickets")

        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve support tickets",
        )
