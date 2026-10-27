import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    return psycopg.connect(
        host="127.0.0.1",
        port=5433,
        user="codescout",
        password=os.getenv("DB_PASSWORD"),
        dbname="codescout",
    )

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS llm_calls (
                id SERIAL PRIMARY KEY,
                created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                endpoint TEXT NOT NULL,
                prompt_tokens INT NOT NULL,
                output_tokens INT NOT NULL,
                thinking_tokens INT NOT NULL,
                latency_ms INT NOT NULL
            )
        """)
        
def save_llm_call(endpoint: str, result: dict) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO llm_calls (endpoint, prompt_tokens, output_tokens, thinking_tokens, latency_ms) "
            "VALUES (%s, %s, %s, %s, %s)",
            (endpoint, result["prompt_tokens"], result["output_tokens"],
             result["thinking_tokens"], result["latency_ms"]),
        )

if __name__ == "__main__":
    init_db()
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO llm_calls (endpoint, prompt_tokens, output_tokens, thinking_tokens, latency_ms) "
            "VALUES (%s, %s, %s, %s, %s)",
            ("test", 9, 23, 0, 6800),
        )
        rows = conn.execute("SELECT id, endpoint, latency_ms, created_at FROM llm_calls").fetchall()
        print(rows)