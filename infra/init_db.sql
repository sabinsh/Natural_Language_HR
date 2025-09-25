CREATE TABLE IF NOT EXISTS employees (
  employee_id SERIAL PRIMARY KEY,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  department VARCHAR(100),
  role VARCHAR(100),
  employment_status VARCHAR(50),
  hire_date DATE,
  leave_type VARCHAR(100),
  salary_local NUMERIC(12,2),
  salary_usd NUMERIC(12,2),
  manager_name VARCHAR(100)
);

INSERT INTO employees (first_name, last_name, department, role, employment_status, hire_date, leave_type, salary_local, salary_usd, manager_name) VALUES
('Alice','Smith','Engineering','Software Engineer','Active','2025-03-01',NULL,120000,120000,'John Doe'),
('Bob','Jones','Engineering','Senior Engineer','Active','2024-12-01',NULL,140000,140000,'John Doe'),
('Carol','Lee','HR','HR Manager','On Leave','2024-06-15','Parental Leave',90000,90000,'Sarah Connor');
