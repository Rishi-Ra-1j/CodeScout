import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect(
    host="127.0.0.1",
    port=5433,
    user="codescout",
    password=os.getenv("DB_PASSWORD"),
    dbname="codescout",
)
with conn.cursor() as cur:
    cur.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector'")
    print(cur.fetchone())
conn.close()