CREATE TABLE IF NOT EXISTS departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    city VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    position VARCHAR(50),
    started_at DATE,
    salary INT,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE IF NOT EXISTS clients (
    client_id INT PRIMARY KEY,
    client_name VARCHAR(100) NOT NULL,
    contact_name VARCHAR(100) NOT NULL,
    assigned_employee_id INT,
    FOREIGN KEY (assigned_employee_id) REFERENCES employees(employee_id)
);

CREATE TABLE IF NOT EXISTS projects (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(50) NOT NULL,
    started_date DATE,
    end_date DATE,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE employee_projects (
    employee_id INT,
    project_id INT,
    title VARCHAR(50),
    PRIMARY KEY (employee_id, project_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);



---------DATA INSERT
INSERT INTO departments(department_id, department_name, city) VALUES 
(1, 'Product Department', 'Almaty'),
(2, 'HR Department', 'Almaty'),
(3, 'System Administration Department', 'Almaty'),
(4, 'Backend Department', 'Almaty'),
(5, 'Frontend Department', 'Almaty');

INSERT INTO employees(employee_id, first_name, last_name,
                        position, started_at, salary, department_id) VALUES
(1, 'Aidos', 'Bekbolat', 'Backend developer', '2024-05-24', 300000, 4),
(2, 'Yernar', 'Mauletkhan', 'Frontend developer', '2023-07-21', 500000, 5),
(3, 'David', 'Manyukyan', 'Manager', '2024-08-30', 60000, 1),
(4, 'David', 'Michelangelo', 'Designer', '2024-07-23', 110000, 1),
(5, 'Nickolay', 'Richter', 'HR-Manager', '2024-02-24', 500000, 2);

INSERT INTO clients(client_id, client_name, contact_name, assigned_employee_id) VALUES
(1, 'Nurdaulet', 'zander559@mail.ru', 1),
(2, 'Yelaman', 'toksik@mail.ru', 2),
(3, 'Bakhredin', 'babakhredin@mail.ru', 4),
(4, 'Aldiyar', 'alldik@mail.ru', 3),
(5, 'Salamat', 'sala@mail.ru', 1);

INSERT INTO projects(project_id, project_name, started_date, end_date, department_id) VALUES
(1, 'Nazvanie.net', '2022-05-24', '2025-05-24', 1),
(2, 'Onboarding 2024', '2024-05-24', '2024-12-01', 2),
(3, 'New design', '2023-08-20', '2024-12-01', 5),
(4, 'MoshniyServer', '2021-05-04', '2026-05-10', 4);

INSERT INTO employee_projects(employee_id, project_id, title) VALUES
(1, 4, 'Backend'),
(2, 3, 'Frontend'),
(3, 2, 'Manager');



---------------TASKS
---------------TASK 1: 1)	Сделать выборку всех работников с именем “Давид” из отдела “Снабжение”
---------------с полями ФИО, заработная плата, должность

SELECT emp.first_name, emp.last_name, emp.salary, emp.position
FROM employees as emp
JOIN departments d ON d.department_id = emp.department_id
WHERE emp.first_name = 'David' AND d.department_name = 'Product Department';


---------------TASK 2: Посчитать среднюю заработную плату работников по отделам

SELECT d.department_name, AVG(emp.salary) AS average_salary
FROM departments d
JOIN employees emp ON emp.department_id = d.department_id
GROUP BY d.department_name;


---------------TASK 3:3) Сделать выборку по должностям, в результате
-- которой отобразятся данные, больше ли средняя ЗП по должности,
-- чем средняя ЗП по всем работникам


SELECT position, AVG(salary) AS average_salary_position,
    (SELECT AVG(salary) FROM employees) AS total_avg_salary,
    CASE
        WHEN AVG(salary) > (SELECT AVG(salary) FROM employees) THEN 'Выше'
        ELSE 'Меньше'
        END AS salary_comparison
FROM employees
GROUP BY position;



--------TASK 4: 4)	Сделать представление, в котором собраны данные
-- по должностям (Должность, в каких отделах встречается эта должность
-- (в виде массива), список сотрудников, начавших работать в этом отделе
-- не раньше 2021 года (Сгруппировать по отделам) (в формате JSON),
-- средняя заработная плата по должности)


CREATE VIEW position_overview AS
SELECT
    emp.position,
    ARRAY_AGG(DISTINCT d.department_name) AS departments,
    JSON_AGG(
            JSON_BUILD_OBJECT(
                    'first_name', emp.first_name,
                    'last_name', emp.last_name
            )
    ) AS employees,
    AVG(emp.salary) AS average_salary
FROM employees emp
         JOIN departments d ON emp.department_id = d.department_id
WHERE emp.started_at >= '2021-01-01'
GROUP BY emp.position;
