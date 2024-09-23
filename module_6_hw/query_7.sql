SELECT 
    s.id AS student_id,
    s.name,
    g.grade,
    g.date
FROM 
    students s
JOIN 
    groups  ON s.group_id = groups.id
JOIN 
    grades g ON s.id = g.student_id
JOIN 
    subjects sub ON g.subject_id = sub.id
WHERE 
    groups.group_name = 'Alpha' 
    AND sub.subject_name = 'Microbiologist';
