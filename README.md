# Natural Language HR Employee Records Query Application  

This project is a **Natural Language to SQL HR Query Application** that allows users to query employee records using plain English.  
The system converts natural language input into SQL queries, executes them against a PostgreSQL database, and displays results in both **text** and **table** formats.  

## 📸 Screenshots  

![Employee Hiredate](image/employee_hiredate.jpg)  
![Employee Leave](image/employee_leave.jpg)  
![Employee Manager](image/employee_manager.jpg)  
![Employee Salary](image/employee_salary.jpg) 

---

## 📂 Project Structure  

```
NATURAL_LANGUAGE_HR/
├── .env                   # Environment variables
├── backend/               # Backend application
│   ├── __pycache__/       
│   └── main.py            
├── frontend/              # Frontend application
│   └── app.py             
├── image/                 # (Placeholder for images or assets)
├── infra/                 # Infrastructure-related files
│   ├── docker-compose.yml 
│   └── init_db.sql        
├── HR_Query.ipynb         # Jupyter notebook for HR queries
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
└── run_all.py             # Script to run the whole project
```

---

## ⚙️ Backend (FastAPI)

**File:** `backend/main.py`  

Key components:
- Uses **OpenAI API** to convert natural language into SQL queries.  
- Executes queries on **PostgreSQL** via **SQLAlchemy**.  
- Returns results in JSON format for the frontend.  

---

## 🎨 Frontend (Streamlit)

**File:** `frontend/app.py`  

Key components:
- Simple **Streamlit UI** for entering employee-related questions.  
- Calls FastAPI backend for SQL generation and execution.  
- Displays SQL + results in **text** and **table** format.  

---

## 🐘 PostgreSQL in Docker  

The database runs inside a **Docker container**.  

### `docker-compose.yml` Example

```yaml
version: "3.9"
services:
  db:
    image: postgres:15
    container_name: hr_postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: hrdb
    volumes:
      - db-data:/var/lib/postgresql/data
      - ./init_db.sql:/docker-entrypoint-initdb.d/init_db.sql:ro
    ports:
      - "5432:5432"  

volumes:
  db-data:
```

Initialize database:
```bash
docker-compose up -d
```

---

## 📜 Example Queries  

1. **List employees hired in the last 11 months**  
   ```sql
   SELECT * 
   FROM employees 
   WHERE hire_date >= CURRENT_DATE - INTERVAL '11 months';
   ```

2. **List employees on parental leave**  
   ```sql
   SELECT * 
   FROM employees 
   WHERE leave_type = 'Parental Leave';
   ```

3. **Show employees managed by John Doe**  
   ```sql
   SELECT * 
   FROM employees 
   WHERE manager_name = 'John Doe';
   ```
4. **Show employees in Engineering with Salary greater than 120K**  
   ```sql
   SELECT *
   FROM employees
   WHERE department = 'Engineering'
   AND salary_usd > 120000;
   ```
---

## 🔑 Environment Variables  

Create a `.env` file in `backend/`:

```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/employees_db
```

---

## 📦 Requirements  

**requirements.txt**
```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
pandas
python-dotenv
openai
streamlit
sqlparse
requests
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🚀 Run the App  

1. Start PostgreSQL in Docker:  
   ```bash
   docker-compose up -d
   ```

2. Start backend and frontend:  
   ```bash
   python run_all.py
   ```

3. Open in browser: [http://localhost:8501](http://localhost:8501)  

---

✅ You now have a **working Natural Language HR Employee Records Query App** with FastAPI + Streamlit + PostgreSQL (Docker).  
