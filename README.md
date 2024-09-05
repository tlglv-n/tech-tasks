# tech-tasks

If you want to clone this repo, then here is instruction:
```
cd existing_repo
git clone https://github.com/tlglv-n/tech-tasks.git
```

# Task 1

- 1.1
- We take the matches with the name 'David' and the department through WHERE
```
SELECT d.department_name, AVG(emp.salary) AS average_salary
FROM departments d
JOIN employees emp ON emp.department_id = d.department_id
GROUP BY d.department_name;
```

- 1.2
- Reading the average salary
```
SELECT emp.first_name, emp.last_name, emp.salary, emp.position
FROM employees as emp
JOIN departments d ON d.department_id = emp.department_id
WHERE emp.first_name = 'David' AND d.department_name = 'Product Department';
```

- 1.3
- Using a query for the average salary for each employee and a subquery for deducting the average salary for the total average salary
```
SELECT position, AVG(salary) AS average_salary_position,
    (SELECT AVG(salary) FROM employees) AS total_avg_salary,
    CASE
        WHEN AVG(salary) > (SELECT AVG(salary) FROM employees) THEN 'Выше'
        ELSE 'Меньше'
        END AS salary_comparison
FROM employees
GROUP BY position;
```

- 1.4
- We use View for further work with JSON
```
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
```


# Task 2-3

- Check the another branch "new"





