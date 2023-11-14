INSERT INTO taskify_task (name, description, status, dynamic_fields)
SELECT 'Task' || round(random() * 1000000),
       'A description.',
       'Created',
       '[{"name": "effort", "type": "int", "value": 1}, {"name": "category", "type": "string", "value": "epic"}]'
FROM generate_series(1, 250000);

INSERT INTO taskify_task (name, description, status, dynamic_fields)
SELECT 'Task' || round(random() * 1000000),
       'A description.',
       'Opened',
       '[{"name": "effort", "type": "int", "value": 2}, {"name": "category", "type": "string", "value": "feature"}]'
FROM generate_series(1, 250000);

INSERT INTO taskify_task (name, description, status, dynamic_fields)
SELECT 'Task' || round(random() * 1000000),
       'A description.',
       'In Progress',
       '[{"name": "effort", "type": "int", "value": 3}, {"name": "category", "type": "string", "value": "story"}]'
FROM generate_series(1, 250000);

INSERT INTO taskify_task (name, description, status, dynamic_fields)
SELECT 'Task' || round(random() * 1000000),
       'A description.',
       'Completed',
       '[{"name": "effort", "type": "int", "value": 4}, {"name": "category", "type": "string", "value": "task"}]'
FROM generate_series(1, 250000);
