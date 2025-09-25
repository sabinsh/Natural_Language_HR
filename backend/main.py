import re
import sqlparse
from sqlalchemy import create_engine, text
import pandas as pd
from dotenv import load_dotenv
import os
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel

# === Load environment variables ===
load_dotenv(override=True)

# === Initialize OpenAI client ===
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === PostgreSQL connection setup ===
#DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/hrdb")
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# === FastAPI app ===
app = FastAPI(title="Natural Language HR Employee Records Query Application")

# === Request model ===
class QueryRequest(BaseModel):
    question: str

# === Extract SQL helper ===
def extract_sql(text: str) -> str:
    match = re.search(r"```sql(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip()

@app.post("/query")
def run_query(request: QueryRequest):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that converts natural-language questions into SQL queries. "
                "The user is querying a PostgreSQL table called `employees` with columns: "
                "employee_id, first_name, last_name, department, role, employment_status, "
                "hire_date, leave_type, salary_local, salary_usd, manager_name. "
                "Respond ONLY with SQL that runs directly on PostgreSQL, wrapped in ```sql ... ``` if possible."
            )
        },
        {"role": "user", "content": request.question}
    ]

    try:
        # === OpenAI call ===
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=0
        )
        raw_response = response.choices[0].message.content

        # === Extract SQL ===
        stripped_sql = extract_sql(raw_response)
        unescaped_sql = stripped_sql.replace("\\n", "\n")
        cleaned_sql = unescaped_sql.rstrip(";")
        final_sql = sqlparse.format(cleaned_sql, reindent=True, keyword_case="upper")

        # === Execute SQL safely ===
        df = pd.read_sql(text(final_sql), engine)

        # === Prepare response ===
        if df.empty:
            results_text = "No employees found for your query."
        else:
            results_text = df.to_string(index=False)

        return {
            "query": final_sql,
            "results_table": df.to_dict(orient="records"),
            "results_text": results_text,
            "error": None,
        }

    except Exception as e:
        return {
            "query": None,
            "results_table": None,
            "results_text": None,
            "error": str(e),
        }

@app.get("/query")
def test_query():
    return {"message": "Use POST with JSON body to query the database."}
